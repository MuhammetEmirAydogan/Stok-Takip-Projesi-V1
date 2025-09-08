from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.db.models import Sum, Case, When, IntegerField, F

from .models import StokHareketi, Urun

@receiver(post_save, sender=StokHareketi)
def stok_guncelle_kayit_sonrasi(sender, instance, **kwargs):
    urun = instance.urun

    stok_toplami = StokHareketi.objects.filter(urun=urun).aggregate(
        toplam=Sum(
            Case(
                When(islem_tipi__in=['Mal Alımı', 'İade (Giriş)'], then=F('adet')),
                # DEĞİŞİKLİK: 'Servis Kullanımı'nı bu listeye ekliyoruz.
                When(islem_tipi__in=['Satış', 'İade (Çıkış)', 'Fire', 'Servis Kullanımı'], then=-F('adet')),
                default=0,
                output_field=IntegerField(),
            )
        )
    )['toplam'] or 0

    urun.mevcut_stok = stok_toplami
    urun.save(update_fields=['mevcut_stok'])


@receiver(post_delete, sender=StokHareketi)
def stok_guncelle_silme_sonrasi(sender, instance, **kwargs):
    stok_guncelle_kayit_sonrasi(sender, instance, **kwargs)