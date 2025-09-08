from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('raporlar/', views.raporlar, name='raporlar'),
    path('kiralamalar/', views.kiralama_listesi, name='kiralama-listesi'),
    path('kiralamalar/yeni/', views.kiralama_ekle, name='kiralama-ekle'),
    path('araclar/', views.arac_listesi, name='arac-listesi'),
    path('araclar/yeni/', views.arac_ekle, name='arac-ekle'),
    path('araclar/<int:pk>/duzenle/', views.arac_duzenle, name='arac-duzenle'),
    path('musteriler/', views.musteri_listesi, name='musteri-listesi'),
    path('musteriler/yeni/', views.musteri_ekle, name='musteri-ekle'),
    path('musteriler/<int:pk>/duzenle/', views.musteri_duzenle, name='musteri-duzenle'),
    path('musteriler/ice-aktar/', views.musteri_ice_aktar, name='musteri-ice-aktar'),
    path('tedarikciler/', views.tedarikci_listesi, name='tedarikci-listesi'),
    path('tedarikciler/yeni/', views.tedarikci_ekle, name='tedarikci-ekle'),
    path('tedarikciler/<int:pk>/duzenle/', views.tedarikci_duzenle, name='tedarikci-duzenle'),
    path('tedarikciler/ice-aktar/', views.tedarikci_ice_aktar, name='tedarikci-ice-aktar'),
    path('urunler/', views.urun_listesi, name='urun-listesi'),
    path('urunler/ice-aktar/', views.urun_ice_aktar, name='urun-ice-aktar'),
    path('urun/yeni/', views.urun_ekle, name='urun-ekle'),
    path('urun/<int:pk>/', views.urun_detay, name='urun-detay'),
    path('urun/<int:pk>/duzenle/', views.urun_duzenle, name='urun-duzenle'),
    path('urun/<int:pk>/sil/', views.urun_sil, name='urun-sil'),
    path('urun/<int:pk>/alim/', views.mal_alimi_yap, name='mal-alimi'),
    path('urun/<int:pk>/servis/', views.servis_cikisi_yap, name='servis-cikisi'),
]