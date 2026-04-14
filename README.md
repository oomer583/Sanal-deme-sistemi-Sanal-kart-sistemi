# Kesintiye Dayanıklı Ödeme + Sanal Kart Sistemi (MVP)

Bu depo, **kesintiye dayanıklı** bir ödeme orkestrasyonu ve **sanal kart** yönetimi için temel bir Python MVP içerir.

## Özellikler

- Çoklu sağlayıcı ile ödeme denemesi (failover)
- Idempotency key ile çift çekim engeli
- Basit çift kayıt (double-entry) ledger
- Sanal kart oluşturma, dondurma/açma, limit güncelleme
- Birim testler

## Çalıştırma

```bash
python -m unittest discover -s tests -v
```

## Not

Bu proje eğitim amaçlıdır. Gerçek üretim kullanımı için PCI DSS, KYC/AML, HSM/KMS, audit log, şifreleme, izleme ve regülasyon gereksinimleri eklenmelidir.
