# LLM Evaluation Project

Türkçe soru-cevap veri seti kullanılarak farklı Qwen büyük dil modellerinin (LLM) doğruluk, yanıt süresi, token kullanımı ve API maliyeti açısından karşılaştırılması.

## Proje Hakkında

Bu projenin amacı, farklı büyük dil modellerinin aynı sorulara verdiği cevapları değerlendirerek performanslarını karşılaştırmaktır.

Değerlendirme kapsamında 100 sorudan oluşan Türkçe bir veri seti kullanılmış ve üç farklı Qwen modeli test edilmiştir.

Her model için aşağıdaki metrikler ölçülmüştür:

- Doğruluk oranı (Accuracy)
- Başarılı ve başarısız yanıt sayısı
- Ortalama yanıt süresi
- Kullanılan token miktarı
- API kullanım maliyeti

## Kullanılan Modeller

| Model         | OpenRouter Model ID  |
| ------------- | -------------------- |
| Qwen3.7-Flash | `qwen/qwen3.7-flash` |
| Qwen3-32B     | `qwen/qwen3-32b`     |
| Qwen3.8-27B   | `qwen/qwen3.8-27b`   |

Modeller OpenRouter API üzerinden kullanılmıştır.

## Veri Seti

Toplam 100 sorudan oluşan veri seti yedi kategoriden oluşmaktadır.

| Kategori                | Soru Sayısı |
| ----------------------- | ----------: |
| Genel Kültür            |          20 |
| Coğrafya                |          15 |
| Tarih                   |          15 |
| Bilim                   |          15 |
| Bilgisayar ve Teknoloji |          20 |
| Edebiyat ve Sanat       |          10 |
| Spor                    |           5 |
| **Toplam**              |     **100** |

Veri setindeki temel sütunlar:

- `id`: Soru numarası
- `category`: Soru kategorisi
- `question`: Soru metni
- `ground_truth`: Beklenen doğru cevap

## Değerlendirme Sonuçları

100 soruluk test sonucunda elde edilen model karşılaştırması:

| Metrik          | Qwen3.7-Flash | Qwen3-32B | Qwen3.8-27B |
| --------------- | ------------: | --------: | ----------: |
| Toplam Soru     |           100 |       100 |         100 |
| Başarılı Yanıt  |            97 |        99 |         100 |
| Başarısız Yanıt |             3 |         1 |           0 |
| Doğru Cevap     |            84 |        78 |          90 |
| Yanlış Cevap    |            16 |        22 |          10 |
| Doğruluk        |           %84 |       %78 |     **%90** |
| Ortalama Süre   |      4.650 sn |  7.009 sn |    1.732 sn |
| Toplam Token    |        34.267 |    26.348 |      17.410 |
| Toplam Maliyet  |     $0.004058 | $0.009186 |   $0.024844 |

### Sonuçların Yorumu

- Qwen3.8-27B, %90 doğruluk oranıyla en yüksek performansı göstermiştir.
- Qwen3.8-27B, 1.732 saniyelik ortalama yanıt süresiyle en hızlı model olmuştur.
- Qwen3.7-Flash, üç model arasında en düşük toplam API maliyetine sahiptir.
- Qwen3-32B, bu testte %78 doğruluk oranı elde etmiştir.

Bu sonuçlar kullanılan 100 soruluk veri setine ve mevcut değerlendirme yöntemine aittir.

**Not:** Doğruluk kontrolü, normalize edilmiş tam eşleşme ve beklenen cevabın model cevabında ifade olarak bulunması yöntemlerine dayanır. Anlamsal olarak doğru fakat farklı biçimde ifade edilmiş cevaplar yanlış sınıflandırılabilir.

## Kullanılan Teknolojiler

- Python 3.13
- Pandas
- Requests
- Python-dotenv
- OpenPyXL
- OpenRouter API
- Qwen LLM
- Docker

## Proje Klasör Yapısı

```text
LLM-Evaluation-Project/
│
├── data/
│   └── dataset.xlsx
│
├── results/
│   ├── evaluation_10_questions.xlsx
│   ├── evaluation_100_questions.xlsx
│   └── first_test_results.xlsx
│
├── scripts/
│   ├── create_dataset.py
│   ├── validate_dataset.py
│   ├── test_api.py
│   └── run_evaluation.py
│
├── .dockerignore
├── .gitignore
├── Dockerfile
└── requirements.txt
```

## Kurulum

### 1. Repository'yi klonlayın

```bash
git clone https://github.com/Eminenurdogan/LLM-Evaluation-Project.git
```

```bash
cd LLM-Evaluation-Project
```

### 2. Sanal ortam oluşturun

Windows:

```bash
python -m venv venv
venv\Scripts\activate
```

### 3. Gerekli kütüphaneleri yükleyin

```bash
pip install -r requirements.txt
```

### 4. API anahtarını tanımlayın

Proje ana dizininde `.env` dosyası oluşturun:

```env
OPENROUTER_API_KEY=your_api_key
```

OpenRouter API anahtarı gereklidir. Gerçek API anahtarınızı GitHub'a yüklemeyin.

### 5. Veri setini doğrulayın

```bash
python scripts/validate_dataset.py
```

### 6. Model değerlendirmesini başlatın

```bash
python scripts/run_evaluation.py
```

Değerlendirme tamamlandığında sonuçlar `results/evaluation_100_questions.xlsx` dosyasına kaydedilir.

## Docker ile Çalıştırma

Proje Docker kullanılarak konteyner ortamında çalıştırılabilecek şekilde hazırlanmıştır.

### 1. Docker imajını oluşturun

```bash
docker build -t llm-evaluation-project .
```

### 2. API anahtarını tanımlayın

PowerShell:

```powershell
$env:OPENROUTER_API_KEY="your_api_key"
```

### 3. Konteyneri çalıştırın

PowerShell:

```powershell
docker run --rm -e OPENROUTER_API_KEY -v "${PWD}/results:/app/results" llm-evaluation-project
```

Bu komut değerlendirme sonuçlarının bilgisayarınızdaki `results` klasörüne kaydedilmesini sağlar.

### 4. Veri setini Docker üzerinden doğrulayın

```bash
docker run --rm llm-evaluation-project python scripts/validate_dataset.py
```

## Güvenlik

- API anahtarı `.env` dosyasında tutulur.
- `.env` dosyası `.gitignore` ve `.dockerignore` içerisinde hariç tutulmuştur.
- Sanal ortam dosyaları GitHub'a yüklenmez.

## Geliştirici

**Emine Nur Doğan**

GitHub: https://github.com/Eminenurdogan

## Lisans

Bu proje eğitim ve araştırma amacıyla geliştirilmiştir.
