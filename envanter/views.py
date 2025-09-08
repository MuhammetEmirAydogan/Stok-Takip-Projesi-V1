from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required
from django.db import models
from django.core.exceptions import PermissionDenied
from .models import Urun, StokHareketi, Musteri, Tedarikci, Arac, Kiralama
from .forms import (
    SatisForm, MalAlimForm, UrunForm, MusteriForm, TedarikciForm, 
    AracForm, ServisCikisForm, RaporFiltreForm, KiralamaForm, ExcelImportForm,
    MusteriImportForm, TedarikciImportForm
)
from django.db.models import F, Q, Sum
import pandas as pd

@login_required
def urun_ice_aktar(request):
    if not request.user.groups.filter(name='Yonetici').exists(): raise PermissionDenied
    if request.method == 'POST':
        form = ExcelImportForm(request.POST, request.FILES)
        if form.is_valid():
            excel_dosyasi = request.FILES['excel_dosyasi']
            try:
                df = pd.read_excel(excel_dosyasi, engine='openpyxl')
                eklenen_sayisi = 0; atlanan_sayisi = 0
                gerekli_sutunlar = ['urun_kodu', 'urun_adi', 'marka']
                if not all(sutun in df.columns for sutun in gerekli_sutunlar):
                    messages.error(request, "Excel dosyasında 'urun_kodu', 'urun_adi', 'marka' sütunları bulunmalıdır.")
                    return redirect('urun-ice-aktar')
                for index, row in df.iterrows():
                    urun_kodu = row.get('urun_kodu')
                    if pd.isna(urun_kodu) or Urun.objects.filter(urun_kodu=urun_kodu).exists():
                        atlanan_sayisi += 1
                        continue
                    Urun.objects.create(urun_kodu=urun_kodu, urun_adi=row.get('urun_adi'), marka=row.get('marka'), model=row.get('model'), ebat=row.get('ebat'), mevsim=row.get('mevsim'), kritik_stok_seviyesi=row.get('kritik_stok_seviyesi', 5))
                    eklenen_sayisi += 1
                messages.success(request, f"{eklenen_sayisi} ürün başarıyla eklendi. {atlanan_sayisi} ürün zaten mevcut olduğu veya ürün kodu boş olduğu için atlandı.")
            except Exception as e:
                messages.error(request, f"Dosya işlenirken bir hata oluştu: {e}. Lütfen dosya formatının '.xlsx' olduğundan ve sütun başlıklarının doğru olduğundan emin olun.")
            return redirect('urun-listesi')
    else:
        form = ExcelImportForm()
    return render(request, 'envanter/urun_ice_aktar.html', {'form': form})

@login_required
def musteri_ice_aktar(request):
    if not request.user.groups.filter(name='Yonetici').exists(): raise PermissionDenied
    if request.method == 'POST':
        form = MusteriImportForm(request.POST, request.FILES)
        if form.is_valid():
            excel_dosyasi = request.FILES['excel_dosyasi']
            try:
                df = pd.read_excel(excel_dosyasi, engine='openpyxl')
                eklenen_sayisi = 0; atlanan_sayisi = 0
                gerekli_sutunlar = ['ad_soyad_veya_unvan']
                if not all(sutun in df.columns for sutun in gerekli_sutunlar):
                    messages.error(request, "Excel dosyasında 'ad_soyad_veya_unvan' sütunu bulunmalıdır.")
                    return redirect('musteri-ice-aktar')
                for index, row in df.iterrows():
                    isim = row.get('ad_soyad_veya_unvan')
                    if pd.isna(isim) or Musteri.objects.filter(ad_soyad_veya_unvan=isim).exists():
                        atlanan_sayisi += 1
                        continue
                    Musteri.objects.create(ad_soyad_veya_unvan=isim, telefon=row.get('telefon'), email=row.get('email'), adres=row.get('adres'), vergi_no=row.get('vergi_no'))
                    eklenen_sayisi += 1
                messages.success(request, f"{eklenen_sayisi} müşteri başarıyla eklendi. {atlanan_sayisi} müşteri zaten mevcut olduğu veya isim boş olduğu için atlandı.")
            except Exception as e:
                messages.error(request, f"Dosya işlenirken bir hata oluştu: {e}.")
            return redirect('musteri-listesi')
    else:
        form = MusteriImportForm()
    return render(request, 'envanter/musteri_ice_aktar.html', {'form': form})

@login_required
def tedarikci_ice_aktar(request):
    if not request.user.groups.filter(name='Yonetici').exists(): raise PermissionDenied
    if request.method == 'POST':
        form = TedarikciImportForm(request.POST, request.FILES)
        if form.is_valid():
            excel_dosyasi = request.FILES['excel_dosyasi']
            try:
                df = pd.read_excel(excel_dosyasi, engine='openpyxl')
                eklenen_sayisi = 0; atlanan_sayisi = 0
                gerekli_sutunlar = ['firma_adi']
                if not all(sutun in df.columns for sutun in gerekli_sutunlar):
                    messages.error(request, "Excel dosyasında 'firma_adi' sütunu bulunmalıdır.")
                    return redirect('tedarikci-ice-aktar')
                for index, row in df.iterrows():
                    isim = row.get('firma_adi')
                    if pd.isna(isim) or Tedarikci.objects.filter(firma_adi=isim).exists():
                        atlanan_sayisi += 1
                        continue
                    Tedarikci.objects.create(firma_adi=isim, yetkili_kisi=row.get('yetkili_kisi'), telefon=row.get('telefon'), email=row.get('email'), adres=row.get('adres'))
                    eklenen_sayisi += 1
                messages.success(request, f"{eklenen_sayisi} tedarikçi başarıyla eklendi. {atlanan_sayisi} tedarikçi zaten mevcut olduğu veya firma adı boş olduğu için atlandı.")
            except Exception as e:
                messages.error(request, f"Dosya işlenirken bir hata oluştu: {e}.")
            return redirect('tedarikci-listesi')
    else:
        form = TedarikciImportForm()
    return render(request, 'envanter/tedarikci_ice_aktar.html', {'form': form})

@login_required
def kiralama_listesi(request):
    kiralamalar = Kiralama.objects.select_related('arac', 'musteri').all().order_by('-baslangic_tarihi')
    return render(request, 'envanter/kiralama_listesi.html', {'kiralamalar': kiralamalar})

@login_required
def kiralama_ekle(request):
    if request.method == 'POST':
        form = KiralamaForm(request.POST)
        if form.is_valid():
            kiralama = form.save(commit=False)
            if kiralama.bitis_tarihi and kiralama.baslangic_tarihi:
                if kiralama.bitis_tarihi < kiralama.baslangic_tarihi:
                    messages.error(request, "Bitiş tarihi, başlangıç tarihinden önce olamaz.")
                    return render(request, 'envanter/kiralama_form.html', {'form': form, 'form_baslik': 'Yeni Kiralama Ekle'})
                else:
                    gun_sayisi = (kiralama.bitis_tarihi - kiralama.baslangic_tarihi).days + 1
                    kiralama.toplam_ucret = kiralama.gunluk_ucret * gun_sayisi
                    kiralama.durum = 'Kirada'
                    kiralama.save()
                    messages.success(request, "Yeni kiralama işlemi başarıyla kaydedildi.")
                    return redirect('kiralama-listesi')
            else:
                kiralama.durum = 'Kirada'
                kiralama.save()
                messages.success(request, "Yeni kiralama işlemi başarıyla kaydedildi.")
                return redirect('kiralama-listesi')
    else:
        form = KiralamaForm()
    return render(request, 'envanter/kiralama_form.html', {'form': form, 'form_baslik': 'Yeni Kiralama Ekle'})
    
@login_required
def raporlar(request):
    form = RaporFiltreForm(request.GET or None)
    hareketler = StokHareketi.objects.select_related('urun', 'musteri', 'tedarikci', 'arac', 'kullanici').all()
    if form.is_valid():
        baslangic = form.cleaned_data.get('baslangic_tarihi')
        bitis = form.cleaned_data.get('bitis_tarihi')
        islem_tipi = form.cleaned_data.get('islem_tipi')
        if baslangic:
            hareketler = hareketler.filter(tarih__gte=baslangic)
        if bitis:
            hareketler = hareketler.filter(tarih__date__lte=bitis)
        if islem_tipi:
            hareketler = hareketler.filter(islem_tipi=islem_tipi)
    toplamlar = hareketler.aggregate(
        toplam_satis_tutari=Sum(F('adet')*F('birim_satis_fiyati'), filter=Q(islem_tipi='Satış')),
        toplam_alim_tutari=Sum(F('adet')*F('birim_alis_fiyati'), filter=Q(islem_tipi='Mal Alımı'))
    )
    context = {'form': form, 'hareketler': hareketler.order_by('-tarih'), 'toplamlar': toplamlar}
    return render(request, 'envanter/raporlar.html', context)

@permission_required('envanter.delete_urun', raise_exception=True)
def urun_sil(request, pk):
    urun = get_object_or_404(Urun, pk=pk)
    if request.method == 'POST':
        try:
            urun.delete()
            messages.success(request, f"'{urun.urun_adi}' başarıyla silindi.")
            return redirect('urun-listesi')
        except models.ProtectedError:
            messages.error(request, f"'{urun.urun_adi}' silinemez çünkü işlem geçmişi bulunmaktadır.")
            return redirect('urun-detay', pk=urun.pk)
    return render(request, 'envanter/urun_sil_onay.html', {'urun': urun})

@login_required
def servis_cikisi_yap(request, pk):
    urun = get_object_or_404(Urun, pk=pk)
    if request.method == 'POST':
        form = ServisCikisForm(request.POST)
        if form.is_valid():
            adet = form.cleaned_data['adet']
            arac = form.cleaned_data['arac']
            if adet > urun.mevcut_stok:
                messages.error(request, f"Stokta yeterli ürün yok! Mevcut stok: {urun.mevcut_stok}")
            else:
                StokHareketi.objects.create(urun=urun, islem_tipi='Servis Kullanımı (Filo)', adet=adet, arac=arac, kullanici=request.user)
                messages.success(request, f"{adet} adet {urun.urun_adi}, {arac.plaka} plakalı araca atandı.")
                return redirect('urun-detay', pk=urun.pk)
    else:
        form = ServisCikisForm()
    context = {'urun': urun, 'form': form}
    return render(request, 'envanter/servis_cikisi.html', context)

@login_required
def arac_listesi(request):
    araclar = Arac.objects.all().order_by('plaka')
    return render(request, 'envanter/arac_listesi.html', {'araclar': araclar})

@login_required
def arac_ekle(request):
    if request.method == 'POST':
        form = AracForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Yeni araç filoya başarıyla eklendi.")
            return redirect('arac-listesi')
    else:
        form = AracForm()
    return render(request, 'envanter/arac_form.html', {'form': form, 'form_baslik': 'Yeni Araç Ekle'})

@login_required
def arac_duzenle(request, pk):
    arac = get_object_or_404(Arac, pk=pk)
    if request.method == 'POST':
        form = AracForm(request.POST, instance=arac)
        if form.is_valid():
            form.save()
            messages.success(request, f"{arac.plaka} plakalı araç güncellendi.")
            return redirect('arac-listesi')
    else:
        form = AracForm(instance=arac)
    return render(request, 'envanter/arac_form.html', {'form': form, 'form_baslik': 'Aracı Düzenle'})

@login_required
def dashboard(request):
    toplam_urun_cesidi = Urun.objects.count()
    toplam_musteri = Musteri.objects.count()
    toplam_tedarikci = Tedarikci.objects.count()
    aktif_kiralamalar = Kiralama.objects.filter(durum='Kirada').select_related('arac', 'musteri')
    kritik_stoktaki_urunler = Urun.objects.filter(mevcut_stok__lte=F('kritik_stok_seviyesi'))
    son_hareketler = StokHareketi.objects.all().order_by('-tarih')[:5]
    context = {'toplam_urun_cesidi': toplam_urun_cesidi, 'toplam_musteri': toplam_musteri,'toplam_tedarikci': toplam_tedarikci, 'kritik_stoktaki_urunler': kritik_stoktaki_urunler,'son_hareketler': son_hareketler, 'aktif_kiralamalar': aktif_kiralamalar,}
    return render(request, 'envanter/dashboard.html', context)

@login_required
def urun_listesi(request):
    sorgu = request.GET.get('q')
    urunler = Urun.objects.all().order_by('urun_adi')
    if sorgu:
        urunler = urunler.filter(Q(urun_adi__icontains=sorgu) | Q(urun_kodu__icontains=sorgu) | Q(marka__icontains=sorgu))
    context = {'urunler': urunler, 'sorgu': sorgu}
    return render(request, 'envanter/urun_listesi.html', context)

@login_required
def musteri_duzenle(request, pk):
    musteri = get_object_or_404(Musteri, pk=pk)
    if request.method == 'POST':
        form = MusteriForm(request.POST, instance=musteri)
        if form.is_valid():
            form.save()
            messages.success(request, "Müşteri bilgileri başarıyla güncellendi.")
            return redirect('musteri-listesi')
    else:
        form = MusteriForm(instance=musteri)
    context = {'form': form, 'musteri': musteri}
    return render(request, 'envanter/musteri_duzenle.html', context)

@login_required
def tedarikci_duzenle(request, pk):
    tedarikci = get_object_or_404(Tedarikci, pk=pk)
    if request.method == 'POST':
        form = TedarikciForm(request.POST, instance=tedarikci)
        if form.is_valid():
            form.save()
            messages.success(request, "Tedarikçi bilgileri başarıyla güncellendi.")
            return redirect('tedarikci-listesi')
    else:
        form = TedarikciForm(instance=tedarikci)
    context = {'form': form, 'tedarikci': tedarikci}
    return render(request, 'envanter/tedarikci_duzenle.html', context)

@login_required
def tedarikci_listesi(request):
    sorgu = request.GET.get('q')
    tedarikciler = Tedarikci.objects.all().order_by('firma_adi')
    if sorgu:
        tedarikciler = tedarikciler.filter(Q(firma_adi__icontains=sorgu) | Q(yetkili_kisi__icontains=sorgu))
    context = {'tedarikciler': tedarikciler, 'sorgu': sorgu}
    return render(request, 'envanter/tedarikci_listesi.html', context)

@login_required
def tedarikci_ekle(request):
    if request.method == 'POST':
        form = TedarikciForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Yeni tedarikçi başarıyla eklendi.")
            return redirect('tedarikci-listesi')
    else:
        form = TedarikciForm()
    context = {'form': form}
    return render(request, 'envanter/tedarikci_ekle.html', context)

@login_required
def musteri_listesi(request):
    sorgu = request.GET.get('q')
    musteriler = Musteri.objects.all().order_by('ad_soyad_veya_unvan')
    if sorgu:
        musteriler = musteriler.filter(Q(ad_soyad_veya_unvan__icontains=sorgu) | Q(telefon__icontains=sorgu) | Q(email__icontains=sorgu))
    context = {'musteriler': musteriler, 'sorgu': sorgu}
    return render(request, 'envanter/musteri_listesi.html', context)

@login_required
def musteri_ekle(request):
    if request.method == 'POST':
        form = MusteriForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Yeni müşteri başarıyla eklendi.")
            return redirect('musteri-listesi')
    else:
        form = MusteriForm()
    context = {'form': form}
    return render(request, 'envanter/musteri_ekle.html', context)

@login_required
def urun_duzenle(request, pk):
    urun = get_object_or_404(Urun, pk=pk)
    if request.method == 'POST':
        form = UrunForm(request.POST, instance=urun)
        if form.is_valid():
            form.save()
            messages.success(request, f"'{urun.urun_adi}' başarıyla güncellendi.")
            return redirect('urun-detay', pk=urun.pk)
    else:
        form = UrunForm(instance=urun)
    context = {'form': form, 'urun': urun}
    return render(request, 'envanter/urun_duzenle.html', context)

@login_required
def urun_ekle(request):
    if request.method == 'POST':
        form = UrunForm(request.POST)
        if form.is_valid():
            yeni_urun = form.save()
            messages.success(request, f"'{yeni_urun.urun_adi}' başarıyla eklendi.")
            return redirect('urun-detay', pk=yeni_urun.pk)
    else:
        form = UrunForm()
    context = {'form': form}
    return render(request, 'envanter/urun_ekle.html', context)

@login_required
def urun_detay(request, pk):
    urun = get_object_or_404(Urun, pk=pk)
    hareketler = StokHareketi.objects.filter(urun=urun).order_by('-tarih')
    if request.method == 'POST':
        form = SatisForm(request.POST)
        if form.is_valid():
            adet = form.cleaned_data['adet']
            musteri = form.cleaned_data['musteri']
            birim_satis_fiyati = form.cleaned_data['birim_satis_fiyati']
            if adet > urun.mevcut_stok:
                messages.error(request, f"Stokta yeterli ürün yok! Mevcut stok: {urun.mevcut_stok}")
            else:
                StokHareketi.objects.create(urun=urun, islem_tipi='Satış', adet=adet, musteri=musteri, birim_satis_fiyati=birim_satis_fiyati, kullanici=request.user)
                messages.success(request, "Satış başarıyla kaydedildi!")
                return redirect('urun-detay', pk=urun.pk)
    else:
        form = SatisForm()
    context = {'urun': urun, 'form': form, 'hareketler': hareketler}
    return render(request, 'envanter/urun_detay.html', context)

@login_required
def mal_alimi_yap(request, pk):
    urun = get_object_or_404(Urun, pk=pk)
    if request.method == 'POST':
        form = MalAlimForm(request.POST)
        if form.is_valid():
            adet = form.cleaned_data['adet']
            tedarikci = form.cleaned_data['tedarikci']
            birim_alis_fiyati = form.cleaned_data['birim_alis_fiyati']
            StokHareketi.objects.create(urun=urun, islem_tipi='Mal Alımı', adet=adet, tedarikci=tedarikci, birim_alis_fiyati=birim_alis_fiyati, kullanici=request.user)
            messages.success(request, f"{adet} adet {urun.urun_adi} stoğa eklendi.")
            return redirect('urun-detay', pk=urun.pk)
    else:
        form = MalAlimForm()
    context = {'urun': urun, 'form': form}
    return render(request, 'envanter/mal_alimi.html', context)