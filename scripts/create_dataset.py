
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment
from openpyxl.utils import get_column_letter
from pathlib import Path

# Projenin ana dizinini bul
PROJECT_DIR = Path(__file__).resolve().parent.parent

# Excel dosyasının kaydedileceği konum
OUTPUT_FILE = PROJECT_DIR / "data" / "dataset.xlsx"

# Veri seti
questions = [
    # Genel kültür (20)
    ("Genel Kültür", "Bir haftada kaç gün vardır?", "7"),
    ("Genel Kültür", "Bir yılda kaç ay vardır?", "12"),
    ("Genel Kültür", "Roma rakamlarında X hangi sayıyı ifade eder?", "10"),
    ("Genel Kültür", "Bir satranç tahtasında kaç kare bulunur?", "64"),
    ("Genel Kültür", "Bir üçgenin kaç kenarı vardır?", "3"),
    ("Genel Kültür", "Bir altıgenin kaç kenarı vardır?", "6"),
    ("Genel Kültür", "Bir artık yılda kaç gün vardır?", "366"),
    ("Genel Kültür", "Bir düzine kaç adettir?", "12"),
    ("Genel Kültür", "Bir yüzyıl kaç yıldır?", "100"),
    ("Genel Kültür", "Bir milenyum kaç yıldır?", "1000"),
    ("Genel Kültür", "Bir saatte kaç dakika vardır?", "60"),
    ("Genel Kültür", "Bir günde kaç saat vardır?", "24"),
    ("Genel Kültür", "Japonya'nın para biriminin adı nedir?", "Yen"),
    ("Genel Kültür", "Dünya üzerinde kaç temel ana yön vardır?", "4"),
    ("Genel Kültür", "Türk alfabesinde kaç harf vardır?", "29"),
    ("Genel Kültür", "Bir futbol maçının normal süresi kaç dakikadır?", "90"),
    ("Genel Kültür", "Bir kilogram kaç gramdır?", "1000"),
    ("Genel Kültür", "Bir metrede kaç santimetre vardır?", "100"),
    ("Genel Kültür", "İngiliz alfabesinde kaç harf vardır?", "26"),
    ("Genel Kültür", "Bir karenin kaç eşit kenarı vardır?", "4"),

    # Coğrafya (15)
    ("Coğrafya", "Türkiye'nin başkenti neresidir?", "Ankara"),
    ("Coğrafya", "Fransa'nın başkenti neresidir?", "Paris"),
    ("Coğrafya", "Japonya'nın başkenti neresidir?", "Tokyo"),
    ("Coğrafya", "İtalya'nın başkenti neresidir?", "Roma"),
    ("Coğrafya", "Almanya'nın başkenti neresidir?", "Berlin"),
    ("Coğrafya", "Dünyanın en büyük okyanusu hangisidir?", "Pasifik Okyanusu"),
    ("Coğrafya", "Dünyanın en yüksek dağı hangisidir?", "Everest Dağı"),
    ("Coğrafya", "Nil Nehri hangi kıtadadır?", "Afrika"),
    ("Coğrafya", "Mısır'ın başkenti neresidir?", "Kahire"),
    ("Coğrafya", "Brezilya'nın başkenti neresidir?", "Brasília"),
    ("Coğrafya", "Avustralya'nın başkenti neresidir?", "Canberra"),
    ("Coğrafya", "Kanada'nın başkenti neresidir?", "Ottawa"),
    ("Coğrafya", "İspanya'nın başkenti neresidir?", "Madrid"),
    ("Coğrafya", "Dünyanın en büyük sıcak çölü hangisidir?", "Sahra Çölü"),
    ("Coğrafya", "Türkiye'nin en uzun nehri hangisidir?", "Kızılırmak"),

    # Tarih (15)
    ("Tarih", "Türkiye Cumhuriyeti hangi tarihte ilan edilmiştir?", "29 Ekim 1923"),
    ("Tarih", "İstanbul hangi yıl fethedilmiştir?", "1453"),
    ("Tarih", "Türkiye Cumhuriyeti'nin ilk cumhurbaşkanı kimdir?", "Mustafa Kemal Atatürk"),
    ("Tarih", "Fransız İhtilali hangi yıl başlamıştır?", "1789"),
    ("Tarih", "Birinci Dünya Savaşı hangi yıl başlamıştır?", "1914"),
    ("Tarih", "Birinci Dünya Savaşı hangi yıl sona ermiştir?", "1918"),
    ("Tarih", "İkinci Dünya Savaşı hangi yıl sona ermiştir?", "1945"),
    ("Tarih", "Amerika Birleşik Devletleri Bağımsızlık Bildirgesi hangi yıl kabul edilmiştir?", "1776"),
    ("Tarih", "Magna Carta hangi yıl imzalanmıştır?", "1215"),
    ("Tarih", "Türkiye Büyük Millet Meclisi hangi tarihte açılmıştır?", "23 Nisan 1920"),
    ("Tarih", "Kurtuluş Savaşı'nın başlangıcı kabul edilen tarih nedir?", "19 Mayıs 1919"),
    ("Tarih", "Ankara hangi yıl Türkiye'nin başkenti olmuştur?", "1923"),
    ("Tarih", "Berlin Duvarı hangi yıl yıkılmıştır?", "1989"),
    ("Tarih", "Osmanlı Devleti'nin kurucusu kimdir?", "Osman Gazi"),
    ("Tarih", "Ay'a ilk insanlı iniş hangi yıl gerçekleşmiştir?", "1969"),

    # Bilim (15)
    ("Bilim", "Suyun kimyasal formülü nedir?", "H2O"),
    ("Bilim", "Oksijenin kimyasal sembolü nedir?", "O"),
    ("Bilim", "Altının kimyasal sembolü nedir?", "Au"),
    ("Bilim", "Güneş sisteminin en büyük gezegeni hangisidir?", "Jüpiter"),
    ("Bilim", "Dünya'nın doğal uydusunun adı nedir?", "Ay"),
    ("Bilim", "Işığın boşluktaki yaklaşık hızı saniyede kaç kilometredir?", "300000 km/s"),
    ("Bilim", "İnsan vücudunda kanı pompalayan organ hangisidir?", "Kalp"),
    ("Bilim", "Fotosentez yapan canlılarda temel pigmentin adı nedir?", "Klorofil"),
    ("Bilim", "Suyun deniz seviyesindeki kaynama sıcaklığı kaç santigrat derecedir?", "100 °C"),
    ("Bilim", "Normal atmosfer basıncında suyun donma sıcaklığı kaç santigrat derecedir?", "0 °C"),
    ("Bilim", "Atomun pozitif yüklü parçacığına ne ad verilir?", "Proton"),
    ("Bilim", "Atomun negatif yüklü parçacığına ne ad verilir?", "Elektron"),
    ("Bilim", "İnsanlarda solunumun temel organı hangisidir?", "Akciğer"),
    ("Bilim", "Dünya'nın Güneş etrafındaki bir tam dolanımı yaklaşık kaç gün sürer?", "365,25 gün"),
    ("Bilim", "Ses boşlukta yayılabilir mi?", "Hayır"),

    # Bilgisayar ve Teknoloji (20)
    ("Bilgisayar ve Teknoloji", "Python programlama dili ilk kez hangi yıl yayımlanmıştır?", "1991"),
    ("Bilgisayar ve Teknoloji", "HTML'nin açılımı nedir?", "HyperText Markup Language"),
    ("Bilgisayar ve Teknoloji", "CSS'nin açılımı nedir?", "Cascading Style Sheets"),
    ("Bilgisayar ve Teknoloji", "JavaScript hangi tür programlama dilidir?", "Programlama dili"),
    ("Bilgisayar ve Teknoloji", "SQL'nin açılımı nedir?", "Structured Query Language"),
    ("Bilgisayar ve Teknoloji", "İkili sayı sisteminde hangi iki rakam kullanılır?", "0 ve 1"),
    ("Bilgisayar ve Teknoloji", "Bir byte kaç bittir?", "8"),
    ("Bilgisayar ve Teknoloji", "CPU'nun açılımı nedir?", "Central Processing Unit"),
    ("Bilgisayar ve Teknoloji", "RAM'in açılımı nedir?", "Random Access Memory"),
    ("Bilgisayar ve Teknoloji", "ROM'un açılımı nedir?", "Read Only Memory"),
    ("Bilgisayar ve Teknoloji", "HTTP'nin açılımı nedir?", "Hypertext Transfer Protocol"),
    ("Bilgisayar ve Teknoloji", "HTTPS'deki S harfi neyi ifade eder?", "Secure"),
    ("Bilgisayar ve Teknoloji", "Git hangi amaçla kullanılan bir araçtır?", "Sürüm kontrolü"),
    ("Bilgisayar ve Teknoloji", "Linux çekirdeğinin ilk sürümü hangi yıl yayımlanmıştır?", "1991"),
    ("Bilgisayar ve Teknoloji", "Veritabanlarında SQL ile kayıt silmek için kullanılan komut nedir?", "DELETE"),
    ("Bilgisayar ve Teknoloji", "Python'da liste oluşturmak için kullanılan köşeli parantezler nelerdir?", "[]"),
    ("Bilgisayar ve Teknoloji", "IP adresinin temel amacı nedir?", "Ağdaki cihazları tanımlamak"),
    ("Bilgisayar ve Teknoloji", "DNS'nin temel görevi nedir?", "Alan adlarını IP adreslerine çözümlemek"),
    ("Bilgisayar ve Teknoloji", "Yapay sinir ağlarının temel esin kaynağı nedir?", "Biyolojik sinir ağları"),
    ("Bilgisayar ve Teknoloji", "JSON'un açılımı nedir?", "JavaScript Object Notation"),

    # Edebiyat ve Sanat (10)
    ("Edebiyat ve Sanat", "Romeo ve Juliet adlı eserin yazarı kimdir?", "William Shakespeare"),
    ("Edebiyat ve Sanat", "Don Kişot adlı romanın yazarı kimdir?", "Miguel de Cervantes"),
    ("Edebiyat ve Sanat", "Sefiller romanının yazarı kimdir?", "Victor Hugo"),
    ("Edebiyat ve Sanat", "Suç ve Ceza romanının yazarı kimdir?", "Fyodor Dostoyevski"),
    ("Edebiyat ve Sanat", "İlahi Komedya adlı eserin yazarı kimdir?", "Dante Alighieri"),
    ("Edebiyat ve Sanat", "Mona Lisa tablosunu kim yapmıştır?", "Leonardo da Vinci"),
    ("Edebiyat ve Sanat", "Guernica tablosunun ressamı kimdir?", "Pablo Picasso"),
    ("Edebiyat ve Sanat", "İstiklal Marşı'nın şairi kimdir?", "Mehmet Akif Ersoy"),
    ("Edebiyat ve Sanat", "Nutuk adlı eserin yazarı kimdir?", "Mustafa Kemal Atatürk"),
    ("Edebiyat ve Sanat", "Hamlet adlı tiyatro eserinin yazarı kimdir?", "William Shakespeare"),

    # Spor (5)
    ("Spor", "Bir basketbol takımından sahada aynı anda kaç oyuncu bulunur?", "5"),
    ("Spor", "Bir voleybol takımından sahada aynı anda kaç oyuncu bulunur?", "6"),
    ("Spor", "Modern Olimpiyat Oyunları ilk kez hangi yıl düzenlenmiştir?", "1896"),
    ("Spor", "FIFA Dünya Kupası ilk kez hangi yıl düzenlenmiştir?", "1930"),
    ("Spor", "Maraton koşusunun resmi mesafesi kaç kilometredir?", "42,195 km"),
]

# Veri seti sayısını kontrol et
if len(questions) != 100:
    raise ValueError(f"100 soru bekleniyordu, {len(questions)} soru bulundu.")

# Excel çalışma kitabı oluştur
workbook = Workbook()
sheet = workbook.active
sheet.title = "Dataset"

# Başlıklar
headers = ["id", "category", "question", "ground_truth"]
sheet.append(headers)

# Soruları Excel'e ekle
for question_id, (category, question, answer) in enumerate(questions, start=1):
    sheet.append([question_id, category, question, answer])

# Başlık biçimlendirme
header_fill = PatternFill(
    fill_type="solid",
    fgColor="1F4E78"
)

for cell in sheet[1]:
    cell.font = Font(bold=True, color="FFFFFF")
    cell.fill = header_fill
    cell.alignment = Alignment(horizontal="center")

# Sütun genişlikleri
column_widths = {
    "A": 10,
    "B": 28,
    "C": 75,
    "D": 40
}

for column, width in column_widths.items():
    sheet.column_dimensions[column].width = width

# Satırları düzenle
for row in sheet.iter_rows(min_row=2):
    for cell in row:
        cell.alignment = Alignment(vertical="center", wrap_text=True)

# Başlık satırını sabitle
sheet.freeze_panes = "A2"

# Filtre ekle
sheet.auto_filter.ref = sheet.dimensions

# Dosyayı kaydet
workbook.save(OUTPUT_FILE)

print("Veri seti başarıyla oluşturuldu!")
print(f"Toplam soru sayısı: {len(questions)}")
print(f"Dosya konumu: {OUTPUT_FILE}")
