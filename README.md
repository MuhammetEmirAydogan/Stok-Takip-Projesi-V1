#  Teker Stok ve Araç Kiralama Yönetim Sistemi (V1)

![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Django](https://img.shields.io/badge/Django-092E20?style=for-the-badge&logo=django&logoColor=white)
![Bootstrap](https://img.shields.io/badge/Bootstrap-563D7C?style=for-the-badge&logo=bootstrap&logoColor=white)

Bu proje, hem lastik satışı yapan hem de araç kiralama hizmeti sunan bir işletmenin tüm operasyonel ihtiyaçlarını karşılamak üzere Django framework'ü ile geliştirilmiş kapsamlı bir web uygulamasıdır. Uygulama, stok takibinden filo yönetimine, müşteri ilişkilerinden kiralama işlemlerine kadar tüm süreçleri tek bir modern ve kullanıcı dostu arayüzde birleştirmeyi hedefler.

## 🚀 Ana Özellikler

### 📦 Stok Yönetimi
* **Detaylı Ürün Tanımlama:** Ürün kodu, marka, model, ebat gibi lastiğe özel tüm detaylarla ürün kaydı.
* **Otomatik Stok Takibi:** Satış, mal alımı, fire veya servise parça çıkışı gibi her işlemde stok miktarlarının otomatik olarak güncellenmesi.
* **Kritik Stok Uyarıları:** Belirlenen minimum seviyenin altına düşen ürünlerin ana panelde anında görüntülenmesi.
* **İşlem Geçmişi:** Her bir ürün için yapılmış olan tüm stok hareketlerinin (alım, satım, servis) detaylı dökümü.

### 🚗 Kiralama ve Filo Yönetimi
* **Araç Filosu Yönetimi:** Şirkete ait araçların plaka, marka, model gibi bilgilerle sisteme kaydedilmesi ve yönetilmesi.
* **Kiralama İşlemleri:** Müşterilerin, filodaki araçları belirli tarihler arasında, günlük ücret üzerinden kiralaması ve bu işlemlerin kaydedilmesi.
* **Servis Kullanımı:** Stoktaki ürünlerin (örn: 4 adet lastik) filodaki bir araca bakım amaçlı atanması ve stoktan düşülmesi.

### 👥 CRM (Müşteri & Tedarikçi Yönetimi)
* Bireysel ve kurumsal müşteri kayıtları oluşturma, düzenleme ve listeleme.
* Tedarikçi firma bilgilerini kaydetme, düzenleme ve listeleme.
* Tüm listelerde akıllı arama fonksiyonu.

### 📊 Raporlama ve Analiz
* **Dinamik Gösterge Paneli (Dashboard):** Sisteme girildiğinde toplam ürün, müşteri, tedarikçi sayısı, kritik stoktaki ürünler, aktif kiralamalar ve son işlemler gibi özet bilgileri sunan ana sayfa.
* **Detaylı Hareket Raporu:** Tarih aralığı ve işlem tipine göre filtrelenebilen, tüm stok hareketlerini finansal özetlerle birlikte gösteren gelişmiş raporlama ekranı.

### 🔐 Kullanıcı Yönetimi ve Güvenlik
* **Rol Bazlı Yetkilendirme:** "Yönetici" ve "Personel" olmak üzere iki farklı kullanıcı grubu.
* **Yetki Kısıtlaması:** Ürün silme, toplu veri aktarımı gibi kritik işlemlerin sadece "Yonetici" rolündeki kullanıcılara özel olması.
* Tüm sayfaların giriş yapma zorunluluğu ile korunması.

### ⚙️ Veri Otomasyonu
* **Excel'den Toplu Aktarım:** Yüzlerce ürün, müşteri veya tedarikçinin tek bir Excel dosyası ile sisteme hızlı ve hatasız bir şekilde aktarılması. Sistem, tekrar eden kayıtları otomatik olarak atlar.

## 💻 Kullanılan Teknolojiler

* **Backend:** Python 3, Django 5+
* **Frontend:** HTML5, CSS3, JavaScript
* **Tasarım:** Bootstrap 5 (Bootswatch "Lux" Teması)
* **Veritabanı:** SQLite 3 (Geliştirme için)
* **Ek Kütüphaneler:**
    * `pandas` & `openpyxl`: Excel dosyalarını okumak ve işlemek için.
    * `Swup.js`: Sayfalar arası akıcı geçiş animasyonları için.

## 🛠️ Kurulum ve Çalıştırma

Projeyi yerel makinede çalıştırmak için aşağıdaki adımları izleyin:

1.  **Depoyu Klonlayın:**
    ```bash
    git clone [https://github.com/MuhammetEmirAydogan/Stok-Takip-Projesi-V1.git](https://github.com/MuhammetEmirAydogan/Stok-Takip-Projesi-V1.git)
    cd Stok-Takip-Projesi-V1
    ```

2.  **Sanal Ortamı Oluşturun ve Aktif Edin:**
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```

3.  **Gerekli Kütüphaneleri Yükleyin:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Veritabanını Oluşturun:**
    ```bash
    python manage.py migrate
    ```

5.  **Bir Yönetici (Superuser) Hesabı Oluşturun:**
    ```bash
    python manage.py createsuperuser
    ```

6.  **Geliştirme Sunucusunu Başlatın:**
    ```bash
    python manage.py runserver
    ```
    Uygulama artık `http://127.0.0.1:8000/` adresinde çalışıyor olacak.

## 🔮 Gelecek Planları (Versiyon 2.0)

* Barkod okuyucu entegrasyonu.
* Kiralama işlemleri için PDF formatında sözleşme/fatura taslağı oluşturma.
* Daha derinlemesine finansal raporlar (kâr/zarar analizi vb.).