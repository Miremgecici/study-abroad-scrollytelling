# Hayalin Faturası

Uluslararası üniversite maliyetleri ve yaşam endeksleri üzerine kaydırdıkça değişen, tek sayfalık interaktif bir veri hikâyesi.

- 71 ülke, 622 üniversite, 868 program kaydı
- Giriş, üç perde ve kullanıcının kendi kriterleriyle ülke bulduğu kapanış bölümü
- Dış kütüphane yok: HTML, CSS ve saf JavaScript (SVG)

## Dosyalar

| Dosya | Açıklama |
| --- | --- |
| `index.html` | Siteyi oluşturan tek dosya. Veri içinde gömülü. |
| `veri.json` | Temizlenmiş veri |
| `temizlik.py` | `veri_seti.xlsx` dosyasından `veri.json` üretir |
| `veri_seti.xlsx` | Ham veri seti |

## Veriyi yeniden üretmek

```
pip install pandas openpyxl
python3 temizlik.py veri_seti.xlsx veri.json
```

Temizlik adımları: 39 birebir tekrar satır silindi, Excel'in tarihe çevirdiği 8 yaşam endeksi hücresi (Mısır, Tunus) boş bırakıldı, boş `OGRENCİ_ORANI` sütunu atıldı, ülke adları Türkçeleştirildi.

## GitHub Pages ile yayınlamak

1. GitHub'da yeni bir depo aç (ör. `veri-hikayesi`).
2. `index.html`, `veri.json`, `temizlik.py`, `veri_seti.xlsx` ve bu dosyayı depoya yükle.
3. Depoda Settings > Pages bölümünden "Deploy from a branch", `main` dalı ve `/ (root)` klasörünü seç.
4. Birkaç dakika sonra site `https://KULLANICIADIN.github.io/veri-hikayesi/` adresinde açılır.

## Veri notları

- Maliyet = okul ücreti + 12 × aylık kira. Para birimi veride yazmıyor, USD varsayıldı.
- Popülerlik endeksi, veri setinde üniversite sayısıyla aynı değerdir.
- Veride akademik kalite sütunu yok; "uygun" ucuz demektir, daha iyi demek değildir.
