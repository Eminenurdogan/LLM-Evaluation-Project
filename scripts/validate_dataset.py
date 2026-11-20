
from pathlib import Path
from openpyxl import load_workbook

# 1. Excel dosyasının konumunu belirle
BASE_DIR = Path(__file__).resolve().parent.parent
DATASET_FILE = BASE_DIR / "data" / "dataset.xlsx"

# 2. Excel dosyasını aç
workbook = load_workbook(DATASET_FILE, data_only=True)
sheet = workbook.active

# 3. Başlıkları oku
headers = [
    cell.value
    for cell in sheet[1]
    if cell.value is not None
]

expected_headers = [
    "id",
    "category",
    "question",
    "ground_truth"
]

print("\n--- VERI SETI KALITE KONTROLU ---\n")

# 4. Sütun kontrolü
if headers == expected_headers:
    print("[OK] Sutun isimleri dogru.")
else:
    print("[HATA] Sutun isimleri hatali!")
    print("Bulunan:", headers)

# 5. Verileri oku
rows = list(sheet.iter_rows(min_row=2, values_only=True))

print(f"\nToplam soru sayisi: {len(rows)}")

# 6. Boş alan kontrolü
empty_rows = []

for row_number, row in enumerate(rows, start=2):
    if any(value is None or str(value).strip() == "" for value in row):
        empty_rows.append(row_number)

if not empty_rows:
    print("[OK] Bos alan bulunmadi.")
else:
    print("[HATA] Bos alan bulunan satirlar:", empty_rows)

# 7. ID kontrolü
ids = [row[0] for row in rows]

if len(ids) == len(set(ids)) and ids == list(range(1, len(rows) + 1)):
    print("[OK] ID numaralari benzersiz ve sirali.")
else:
    print("[HATA] ID numaralarinda eksiklik veya tekrar var.")

# 8. Tekrarlanan soru kontrolü
questions = [
    str(row[2]).strip().casefold()
    for row in rows
    if row[2] is not None
]

duplicates = {
    question
    for question in questions
    if questions.count(question) > 1
}

if not duplicates:
    print("[OK] Tekrarlanan soru bulunmadi.")
else:
    print("[HATA] Tekrarlanan sorular:", duplicates)

# 9. Kategori dagilimi
print("\n--- KATEGORI DAGILIMI ---")

categories = {}

for row in rows:
    category = row[1]
    categories[category] = categories.get(category, 0) + 1

for category, count in categories.items():
    print(f"{category}: {count} soru")

# 10. Genel sonuc
print("\n--- KONTROL TAMAMLANDI ---")
