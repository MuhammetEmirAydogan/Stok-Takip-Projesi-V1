from django import forms
from .models import Musteri, Tedarikci, Urun, Arac, Kiralama, StokHareketi
from django.core.validators import MinValueValidator
from django.core.exceptions import ValidationError
from django import forms
from .models import Musteri, Tedarikci, Urun, Arac, Kiralama, StokHareketi
from django.core.validators import MinValueValidator
from django.core.exceptions import ValidationError

class KiralamaForm(forms.ModelForm):
    class Meta:
        model = Kiralama
        fields = ['arac', 'musteri', 'baslangic_tarihi', 'bitis_tarihi', 'gunluk_ucret']
        widgets = {
            'arac': forms.Select(attrs={'class': 'form-select'}),
            'musteri': forms.Select(attrs={'class': 'form-select'}),
            'baslangic_tarihi': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'bitis_tarihi': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'gunluk_ucret': forms.NumberInput(attrs={'class': 'form-control'}),
        }
    def clean(self):
        cleaned_data = super().clean()
        baslangic = cleaned_data.get("baslangic_tarihi")
        bitis = cleaned_data.get("bitis_tarihi")
        if baslangic and bitis:
            if bitis < baslangic:
                raise ValidationError("Hata: Bitiş tarihi, başlangıç tarihinden önce olamaz!")
        return cleaned_data
# ... (Diğer tüm formlar)
class ExcelImportForm(forms.Form):
    excel_dosyasi = forms.FileField(label="Ürünleri İçeren Excel Dosyasını Seçin")

class MusteriImportForm(forms.Form):
    excel_dosyasi = forms.FileField(label="Müşterileri İçeren Excel Dosyasını Seçin")

class TedarikciImportForm(forms.Form):
    excel_dosyasi = forms.FileField(label="Tedarikçileri İçeren Excel Dosyasını Seçin")

class KiralamaForm(forms.ModelForm):
    class Meta:
        model = Kiralama
        fields = ['arac', 'musteri', 'baslangic_tarihi', 'bitis_tarihi', 'gunluk_ucret']
        widgets = {
            'arac': forms.Select(attrs={'class': 'form-select'}),
            'musteri': forms.Select(attrs={'class': 'form-select'}),
            'baslangic_tarihi': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'bitis_tarihi': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'gunluk_ucret': forms.NumberInput(attrs={'class': 'form-control'}),
        }
    def clean(self):
        cleaned_data = super().clean()
        baslangic = cleaned_data.get("baslangic_tarihi")
        bitis = cleaned_data.get("bitis_tarihi")
        if baslangic and bitis:
            if bitis < baslangic:
                raise ValidationError("Hata: Bitiş tarihi, başlangıç tarihinden önce olamaz!")
        return cleaned_data

class RaporFiltreForm(forms.Form):
    baslangic_tarihi = forms.DateField(label="Başlangıç Tarihi", required=False, widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}))
    bitis_tarihi = forms.DateField(label="Bitiş Tarihi", required=False, widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}))
    ISLEM_TİPİ_SECENEKLERI = [('', 'Tümü')] + StokHareketi.ISLEM_TİPLERİ
    islem_tipi = forms.ChoiceField(label="İşlem Tipi", required=False, choices=ISLEM_TİPİ_SECENEKLERI, widget=forms.Select(attrs={'class': 'form-select'}))

class ServisCikisForm(forms.Form):
    arac = forms.ModelChoiceField(queryset=Arac.objects.filter(aktif_mi=True), label="Araç")
    adet = forms.IntegerField(label="Kullanılan Adet", validators=[MinValueValidator(1)])

class AracForm(forms.ModelForm):
    class Meta:
        model = Arac
        fields = ['plaka', 'marka', 'model', 'yil', 'aktif_mi']
        widgets = {'plaka': forms.TextInput(attrs={'class': 'form-control'}), 'marka': forms.TextInput(attrs={'class': 'form-control'}), 'model': forms.TextInput(attrs={'class': 'form-control'}), 'yil': forms.NumberInput(attrs={'class': 'form-control'}), 'aktif_mi': forms.CheckboxInput(attrs={'class': 'form-check-input'}),}

class TedarikciForm(forms.ModelForm):
    class Meta:
        model = Tedarikci
        fields = ['firma_adi', 'yetkili_kisi', 'telefon', 'email', 'adres', 'aktif_mi']
        widgets = {'firma_adi': forms.TextInput(attrs={'class': 'form-control'}), 'yetkili_kisi': forms.TextInput(attrs={'class': 'form-control'}), 'telefon': forms.TextInput(attrs={'class': 'form-control'}), 'email': forms.EmailInput(attrs={'class': 'form-control'}), 'adres': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}), 'aktif_mi': forms.CheckboxInput(attrs={'class': 'form-check-input'}),}

class MusteriForm(forms.ModelForm):
    class Meta:
        model = Musteri
        fields = ['ad_soyad_veya_unvan', 'telefon', 'email', 'adres', 'vergi_no']
        widgets = {'ad_soyad_veya_unvan': forms.TextInput(attrs={'class': 'form-control'}), 'telefon': forms.TextInput(attrs={'class': 'form-control'}), 'email': forms.EmailInput(attrs={'class': 'form-control'}), 'adres': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}), 'vergi_no': forms.TextInput(attrs={'class': 'form-control'}),}

class UrunForm(forms.ModelForm):
    class Meta:
        model = Urun
        fields = ['urun_kodu', 'urun_adi', 'marka', 'model', 'ebat', 'mevsim', 'uretim_tarihi_dot', 'yuk_endeksi', 'hiz_endeksi', 'kritik_stok_seviyesi']
        widgets = {'urun_kodu': forms.TextInput(attrs={'class': 'form-control'}), 'urun_adi': forms.TextInput(attrs={'class': 'form-control'}), 'marka': forms.TextInput(attrs={'class': 'form-control'}), 'model': forms.TextInput(attrs={'class': 'form-control'}), 'ebat': forms.TextInput(attrs={'class': 'form-control'}), 'mevsim': forms.Select(attrs={'class': 'form-select'}), 'uretim_tarihi_dot': forms.TextInput(attrs={'class': 'form-control'}), 'yuk_endeksi': forms.NumberInput(attrs={'class': 'form-control'}), 'hiz_endeksi': forms.TextInput(attrs={'class': 'form-control'}), 'kritik_stok_seviyesi': forms.NumberInput(attrs={'class': 'form-control'}),}

class SatisForm(forms.Form):
    musteri = forms.ModelChoiceField(queryset=Musteri.objects.all(), label="Müşteri", widget=forms.Select(attrs={'class': 'form-control'}))
    adet = forms.IntegerField(label="Satış Adedi", validators=[MinValueValidator(1)], widget=forms.NumberInput(attrs={'class': 'form-control'}))
    birim_satis_fiyati = forms.DecimalField(label="Birim Satış Fiyatı (₺)", min_value=0.01, decimal_places=2, widget=forms.NumberInput(attrs={'class': 'form-control'}))

class MalAlimForm(forms.Form):
    tedarikci = forms.ModelChoiceField(queryset=Tedarikci.objects.filter(aktif_mi=True), label="Tedarikçi", widget=forms.Select(attrs={'class': 'form-select'}))
    adet = forms.IntegerField(label="Alınan Adet", validators=[MinValueValidator(1)], widget=forms.NumberInput(attrs={'class': 'form-control'}))
    birim_alis_fiyati = forms.DecimalField(label="Birim Alış Fiyatı (₺)", min_value=0.01, decimal_places=2, widget=forms.NumberInput(attrs={'class': 'form-control'}))