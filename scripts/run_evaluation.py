
import os
import re
import time
import requests
import pandas as pd
from dotenv import load_dotenv

# ==========================================
# 1. API AYARLARI
# ==========================================

load_dotenv()

API_KEY = os.getenv("OPENROUTER_API_KEY")

URL = "https://openrouter.ai/api/v1/chat/completions"

MODELS = {
    "Qwen3.7-Flash": "qwen/qwen3.7-flash",
    "Qwen3-32B": "qwen/qwen3-32b",
    "Qwen3.8-27B": "qwen/qwen3.8-27b"
}

# İlk testte kullanılacak soru sayısı
MAX_QUESTIONS = 100

# Maliyet hesaplaması için fiyatlar
# Birim: 1 milyon token başına USD

MODEL_PRICES = {
    "Qwen3.7-Flash": {
        "input": 0.03,
        "output": 0.13
    },
    "Qwen3-32B": {
        "input": 0.08,
        "output": 0.28
    },
    "Qwen3.8-27B": {
        "input": 0.06,
        "output": 1.96
    }
}

if not API_KEY:
    raise ValueError("API anahtarı bulunamadı!")

print("LLM Evaluation sistemi başlatıldı.")

# ==========================================
# 2. VERİ SETİNİ YÜKLE
# ==========================================

DATASET_PATH = "data/dataset.xlsx"

df = pd.read_excel(DATASET_PATH)

required_columns = ["id", "question", "ground_truth"]

for column in required_columns:
    if column not in df.columns:
        raise ValueError(f"Eksik sütun: {column}")

df = df.dropna(subset=["question", "ground_truth"])

# İlk 10 soruyu al
test_df = df.head(MAX_QUESTIONS).copy()

print("\n--- TEST BİLGİLERİ ---")
print("Toplam veri seti:", len(df))
print("Test edilecek soru:", len(test_df))
print("Model sayısı:", len(MODELS))
print("Toplam API isteği:", len(test_df) * len(MODELS))


# ==========================================
# 3. CEVAP NORMALİZASYONU
# ==========================================

def normalize_text(text):

    text = str(text).casefold().strip()

    # Noktalama işaretlerini kaldır
    text = re.sub(r"[^\w\s]", " ", text)

    # Fazla boşlukları kaldır
    text = re.sub(r"\s+", " ", text)

    return text.strip()


# ==========================================
# 4. DOĞRULUK KONTROLÜ
# ==========================================

def check_answer(model_answer, ground_truth):

    answer = normalize_text(model_answer)
    truth = normalize_text(ground_truth)

    if not answer or not truth:
        return False

    # Tam eşleşme
    if answer == truth:
        return True

    # Doğru cevap model cevabında bağımsız
    # bir kelime veya ifade olarak geçiyor mu?
    pattern = r"(?<!\w)" + re.escape(truth) + r"(?!\w)"

    return re.search(pattern, answer) is not None


# ==========================================
# 5. MODEL İSTEK FONKSİYONU
# ==========================================

def ask_model(model_id, model_name, question):

    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }

    data = {
        "model": model_id,
        "messages": [
            {
                "role": "system",
                "content": "Türkçe cevap ver. Soruları kısa ve doğru cevapla."
            },
            {
                "role": "user",
                "content": str(question)
            }
        ],
        "temperature": 0,
        "max_tokens": 600
    }

    start_time = time.time()

    response = requests.post(
        URL,
        headers=headers,
        json=data,
        timeout=120
    )

    elapsed_time = time.time() - start_time

    if not response.ok:
        raise Exception(
            f"HTTP {response.status_code}: {response.text}"
        )

    result = response.json()

    choice = result["choices"][0]
    message = choice["message"]

    answer = message.get("content")

    usage = result.get("usage", {})
    details = usage.get("completion_tokens_details", {})

    reasoning_tokens = details.get("reasoning_tokens", 0)
    finish_reason = choice.get("finish_reason")

    # Boş cevap durumunda teşhis bilgisi
    if not answer or not str(answer).strip():

        print("BOŞ CEVAP TEŞHİSİ")
        print("Finish reason:", finish_reason)
        print("Reasoning tokens:", reasoning_tokens)
        print("Completion tokens:", usage.get("completion_tokens"))
        print("Model:", result.get("model"))

        raise Exception(
            f"Boş cevap. Finish reason: {finish_reason}"
        )

    input_tokens = usage.get("prompt_tokens", 0)
    output_tokens = usage.get("completion_tokens", 0)
    total_tokens = usage.get("total_tokens", 0)

    cost = usage.get("cost")

    if cost is None:
        prices = MODEL_PRICES[model_name]

        cost = (
            input_tokens * prices["input"]
            + output_tokens * prices["output"]
        ) / 1_000_000

        cost_source = "Tahmini"
    else:
        cost = float(cost)
        cost_source = "API"

    return {
        "answer": str(answer).strip(),
        "elapsed_time": elapsed_time,
        "input_tokens": input_tokens,
        "output_tokens": output_tokens,
        "total_tokens": total_tokens,
        "cost": cost,
        "cost_source": cost_source
    }



# ==========================================
# 6. TÜM MODELLERİ TEST ET
# ==========================================

all_results = []

total_requests = len(test_df) * len(MODELS)
completed_requests = 0

for name, model_id in MODELS.items():

    print("\n" + "=" * 55)
    print("MODEL:", name)
    print("=" * 55)

    for _, row in test_df.iterrows():

        question_id = row["id"]
        question = str(row["question"])
        ground_truth = str(row["ground_truth"])

        completed_requests += 1

        print(
            f"\n[{completed_requests}/{total_requests}] "
            f"Soru ID: {question_id}"
        )

        print("Soru:", question)

        try:
            result = ask_model(
                model_id,
                name,
                question
            )

            answer = result["answer"]

            is_correct = check_answer(
                answer,
                ground_truth
            )

            print("Model cevabı:", answer)
            print("Doğru cevap:", ground_truth)
            print("Sonuç:", "DOĞRU" if is_correct else "YANLIŞ")
            print(
                f"Süre: {result['elapsed_time']:.2f} saniye"
            )
            print(
                f"Maliyet: ${result['cost']:.8f}"
            )

            all_results.append({
                "Question_ID": question_id,
                "Model": name,
                "Question": question,
                "Ground_Truth": ground_truth,
                "Model_Answer": answer,
                "Is_Correct": is_correct,
                "Response_Time": result["elapsed_time"],
                "Input_Tokens": result["input_tokens"],
                "Output_Tokens": result["output_tokens"],
                "Total_Tokens": result["total_tokens"],
                "Cost_USD": result["cost"],
                "Cost_Source": result["cost_source"],
                "Status": "Success",
                "Error": ""
            })

        except Exception as e:

            print("HATA:", str(e))

            all_results.append({
                "Question_ID": question_id,
                "Model": name,
                "Question": question,
                "Ground_Truth": ground_truth,
                "Model_Answer": "",
                "Is_Correct": False,
                "Response_Time": None,
                "Input_Tokens": 0,
                "Output_Tokens": 0,
                "Total_Tokens": 0,
                "Cost_USD": 0,
                "Cost_Source": "",
                "Status": "Error",
                "Error": str(e)
            })

        # İstekler arasında kısa bekleme
        time.sleep(1)


# ==========================================
# 7. PERFORMANS RAPORU
# ==========================================

results_df = pd.DataFrame(all_results)

summary_results = []

for name in MODELS.keys():

    model_data = results_df[
        results_df["Model"] == name
    ]

    successful = model_data[
        model_data["Status"] == "Success"
    ]

    correct_count = int(
        successful["Is_Correct"].sum()
    )

    total_questions = len(test_df)

    accuracy = (
        correct_count / total_questions
    ) * 100

    average_time = (
        successful["Response_Time"].mean()
        if len(successful) > 0 else 0
    )

    total_tokens = model_data["Total_Tokens"].sum()

    total_cost = model_data["Cost_USD"].sum()

    summary_results.append({
        "Model": name,
        "Total_Questions": total_questions,
        "Successful_Responses": len(successful),
        "Failed_Responses": total_questions - len(successful),
        "Correct_Answers": correct_count,
        "Wrong_Answers": total_questions - correct_count,
        "Accuracy_Percent": round(accuracy, 2),
        "Average_Response_Time": round(average_time, 3),
        "Total_Tokens": int(total_tokens),
        "Total_Cost_USD": round(total_cost, 8)
    })


summary_df = pd.DataFrame(summary_results)


# ==========================================
# 8. EXCEL RAPORU OLUŞTUR
# ==========================================

os.makedirs("results", exist_ok=True)

OUTPUT_PATH = "results/evaluation_100_questions.xlsx"

with pd.ExcelWriter(OUTPUT_PATH) as writer:

    results_df.to_excel(
        writer,
        sheet_name="Detailed Results",
        index=False
    )

    summary_df.to_excel(
        writer,
        sheet_name="Model Comparison",
        index=False
    )


# ==========================================
# 9. SONUÇLARI EKRANA YAZDIR
# ==========================================

print("\n")
print("=" * 65)
print("MODEL PERFORMANS KARŞILAŞTIRMASI")
print("=" * 65)

print(
    summary_df.to_string(index=False)
)

print("\nRAPOR KAYDEDİLDİ:")
print(OUTPUT_PATH)

print("\n--- DEĞERLENDİRME TAMAMLANDI ---")
