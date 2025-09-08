from django.contrib import admin
from .models import Tedarikci, Musteri, Urun, StokHareketi, Arac, Kiralama # Arac ve Kiralama'yı ekle

admin.site.register(Tedarikci)
admin.site.register(Musteri)
admin.site.register(Urun)
admin.site.register(StokHareketi)
admin.site.register(Arac)
admin.site.register(Kiralama) # YENİ