from django.db import models
from django.contrib.auth.models import User

class Kiralama(models.Model):
    DURUM_SECENEKLERI = [('Rezerve', 'Rezerve'), ('Kirada', 'Kirada'), ('Tamamlandı', 'Tamamlandı'), ('İptal', 'İptal'),]
    arac = models.ForeignKey('Arac', on_delete=models.PROTECT, verbose_name="Kiralanan Araç")
    musteri = models.ForeignKey('Musteri', on_delete=models.PROTECT, verbose_name="Kiralayan Müşteri")
    baslangic_tarihi = models.DateField(verbose_name="Kiralama Başlangıç Tarihi")
    bitis_tarihi = models.DateField(verbose_name="Kiralama Bitiş Tarihi", blank=True, null=True)
    gunluk_ucret = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Günlük Ücret (₺)")
    toplam_ucret = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Toplam Ücret (₺)", blank=True, null=True)
    durum = models.CharField(max_length=20, choices=DURUM_SECENEKLERI, default='Rezerve')
    kayit_tarihi = models.DateTimeField(auto_now_add=True)
    def __str__(self): return f"{self.arac.plaka} - {self.musteri.ad_soyad_veya_unvan} ({self.baslangic_tarihi})"
    class Meta: verbose_name = "Kiralama İşlemi"; verbose_name_plural = "Kiralama İşlemleri"

class Arac(models.Model):
    plaka = models.CharField(max_length=20, unique=True, verbose_name="Plaka")
    marka = models.CharField(max_length=100, verbose_name="Marka")
    model = models.CharField(max_length=100, verbose_name="Model")
    yil = models.IntegerField(verbose_name="Yıl", blank=True, null=True)
    aktif_mi = models.BooleanField(default=True, verbose_name="Filoda Aktif Mi?")
    def __str__(self): return f"{self.plaka} - {self.marka} {self.model}"
    class Meta: verbose_name = "Araç"; verbose_name_plural = "Araçlar"

class Tedarikci(models.Model):
    firma_adi = models.CharField(max_length=255, verbose_name="Firma Adı")
    yetkili_kisi = models.CharField(max_length=150, blank=True, null=True, verbose_name="Yetkili Kişi")
    telefon = models.CharField(max_length=20, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    adres = models.TextField(blank=True, null=True)
    kayit_tarihi = models.DateTimeField(auto_now_add=True, verbose_name="Kayıt Tarihi")
    aktif_mi = models.BooleanField(default=True, verbose_name="Aktif Mi?")
    def __str__(self): return self.firma_adi
    class Meta: verbose_name = "Tedarikçi"; verbose_name_plural = "Tedarikçiler"

class Musteri(models.Model):
    ad_soyad_veya_unvan = models.CharField(max_length=255, verbose_name="Ad Soyad / Ünvan")
    telefon = models.CharField(max_length=20, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    adres = models.TextField(blank=True, null=True)
    vergi_no = models.CharField(max_length=50, blank=True, null=True, verbose_name="Vergi Numarası")
    kayit_tarihi = models.DateTimeField(auto_now_add=True, verbose_name="Kayıt Tarihi")
    def __str__(self): return self.ad_soyad_veya_unvan
    class Meta: verbose_name = "Müşteri"; verbose_name_plural = "Müşteriler"

class Urun(models.Model):
    MEVSIM_SECENEKLERI = [('Yaz', 'Yaz'), ('Kış', 'Kış'), ('4 Mevsim', '4 Mevsim'),]
    urun_kodu = models.CharField(max_length=100, unique=True, verbose_name="Ürün Kodu/Barkod")
    urun_adi = models.CharField(max_length=255, verbose_name="Ürün Adı")
    marka = models.CharField(max_length=100, blank=True, null=True)
    model = models.CharField(max_length=100, blank=True, null=True)
    ebat = models.CharField(max_length=50, blank=True, null=True)
    mevsim = models.CharField(max_length=20, choices=MEVSIM_SECENEKLERI, blank=True, null=True)
    uretim_tarihi_dot = models.CharField(max_length=10, blank=True, null=True, verbose_name="Üretim Tarihi (DOT)")
    yuk_endeksi = models.IntegerField(blank=True, null=True, verbose_name="Yük Endeksi")
    hiz_endeksi = models.CharField(max_length=5, blank=True, null=True, verbose_name="Hız Endeksi")
    mevcut_stok = models.IntegerField(default=0, verbose_name="Mevcut Stok")
    kritik_stok_seviyesi = models.IntegerField(default=5, verbose_name="Kritik Stok Seviyesi")
    aktif_mi = models.BooleanField(default=True, verbose_name="Aktif Mi?")
    def __str__(self): return f"{self.urun_adi} ({self.ebat})"
    class Meta: verbose_name = "Ürün"; verbose_name_plural = "Ürünler"

class StokHareketi(models.Model):
    ISLEM_TİPLERİ = [
        ('Mal Alımı', 'Mal Alımı'),
        ('Satış', 'Satış'),
        ('Servis Kullanımı (Filo)', 'Servis Kullanımı (Filo)'),
        ('İade (Giriş)', 'İade (Giriş)'),
        ('İade (Çıkış)', 'İade (Çıkış)'),
        ('Fire', 'Fire'),
    ]
    urun = models.ForeignKey(Urun, on_delete=models.PROTECT, verbose_name="Ürün")
    islem_tipi = models.CharField(max_length=30, choices=ISLEM_TİPLERİ, verbose_name="İşlem Tipi")
    adet = models.IntegerField()
    birim_alis_fiyati = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name="Birim Alış Fiyatı (₺)")
    birim_satis_fiyati = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name="Birim Satış Fiyatı (₺)")
    tarih = models.DateTimeField(auto_now_add=True)
    tedarikci = models.ForeignKey(Tedarikci, on_delete=models.SET_NULL, blank=True, null=True)
    musteri = models.ForeignKey(Musteri, on_delete=models.SET_NULL, blank=True, null=True)
    arac = models.ForeignKey(Arac, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="Araç")
    aciklama = models.TextField(blank=True, null=True, verbose_name="Açıklama (Fatura No vb.)")
    kullanici = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, verbose_name="İşlemi Yapan")
    def __str__(self): return f"{self.urun.urun_adi} - {self.islem_tipi} ({self.adet} adet)"
    class Meta: verbose_name = "Stok Hareketi"; verbose_name_plural = "Stok Hareketleri"