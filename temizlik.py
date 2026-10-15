"""Hayalin Faturası - veri temizliği.

Kullanım:  python3 temizlik.py veri_seti.xlsx veri.json

Yapılanlar
1. 'International_Education_Costs' sayfası okunur ('unı names' sayfasındaki yaşam
   endeksleri 10 ile çarpılmış ve Mısır değerleri bozuk olduğu için kullanılmaz).
2. Boş 'OGRENCİ_ORANI' sütunu atılır.
3. Yaşam endeksi sayıya çevrilir; Excel'in tarihe çevirdiği 8 hücre (Mısır 5, Tunus 3)
   boş (null) bırakılır.
4. Birebir aynı 39 satır silinir.
5. Ülke adları Türkçeleştirilir; ülke bazlı özet (ortanca ve ortalama) hesaplanır.
"""
import json
import statistics as st
import sys

import pandas as pd

TR = {
    "Algeria": "Cezayir", "Argentina": "Arjantin", "Australia": "Avustralya",
    "Austria": "Avusturya", "Bahrain": "Bahreyn", "Bangladesh": "Bangladeş",
    "Belgium": "Belçika", "Brazil": "Brezilya", "Bulgaria": "Bulgaristan",
    "Canada": "Kanada", "China": "Çin", "Colombia": "Kolombiya",
    "Croatia": "Hırvatistan", "Cyprus": "Kıbrıs", "Czech Republic": "Çekya",
    "Denmark": "Danimarka", "Dominican Republic": "Dominik Cumhuriyeti",
    "Ecuador": "Ekvador", "Egypt": "Mısır", "El Salvador": "El Salvador",
    "Finland": "Finlandiya", "France": "Fransa", "Germany": "Almanya",
    "Ghana": "Gana", "Greece": "Yunanistan", "Hong Kong": "Hong Kong",
    "Hungary": "Macaristan", "Iceland": "İzlanda", "India": "Hindistan",
    "Indonesia": "Endonezya", "Iran": "İran", "Ireland": "İrlanda",
    "Israel": "İsrail", "Italy": "İtalya", "Japan": "Japonya", "Kuwait": "Kuveyt",
    "Lebanon": "Lübnan", "Luxembourg": "Lüksemburg", "Malaysia": "Malezya",
    "Mexico": "Meksika", "Morocco": "Fas", "Netherlands": "Hollanda",
    "New Zealand": "Yeni Zelanda", "Nigeria": "Nijerya", "Norway": "Norveç",
    "Panama": "Panama", "Peru": "Peru", "Poland": "Polonya", "Portugal": "Portekiz",
    "Romania": "Romanya", "Russia": "Rusya", "Saudi Arabia": "Suudi Arabistan",
    "Serbia": "Sırbistan", "Singapore": "Singapur", "Slovenia": "Slovenya",
    "South Africa": "Güney Afrika", "South Korea": "Güney Kore", "Spain": "İspanya",
    "Sweden": "İsveç", "Switzerland": "İsviçre", "Taiwan": "Tayvan",
    "Thailand": "Tayland", "Tunisia": "Tunus", "Turkey": "Türkiye", "UAE": "BAE",
    "UK": "İngiltere", "USA": "ABD", "Ukraine": "Ukrayna", "Uruguay": "Uruguay",
    "Uzbekistan": "Özbekistan", "Vietnam": "Vietnam",
}


def main(src, dst):
    df = pd.read_excel(src, sheet_name="International_Education_Costs")
    df.columns = [c.strip() for c in df.columns]
    df = df.rename(columns={
        "ÜLKE": "ulke_en", "ÜNİVEERSİTE": "uni", "OKUL ÜCRETİ": "ucret",
        "YAŞAM İNDEKSİ": "yasam", "KİRA": "kira", "ÜNİVERSİTE SAYISI": "unisay",
        "TOPLAM YILLIK MALİYET": "toplam", "ÜLKE POPÜLERLİK ENDEKSİ": "pop",
    }).drop(columns=["OGRENCİ_ORANI"])

    ham = len(df)
    df["yasam"] = pd.to_numeric(df["yasam"], errors="coerce")  # tarihe dönenler NaN olur
    bozuk = int(df["yasam"].isna().sum())
    df = df.drop_duplicates().reset_index(drop=True)
    tekrar = ham - len(df)

    # Doğrulamalar
    assert (df["toplam"] == df["ucret"] + 12 * df["kira"]).all(), "toplam = ücret + 12*kira değil"
    assert (df["pop"] == df["unisay"]).all(), "popülerlik ile üniversite sayısı farklı"
    assert set(df["ulke_en"]) <= set(TR), set(df["ulke_en"]) - set(TR)

    programlar = []
    for r in df.itertuples():
        programlar.append({
            "ulke": TR[r.ulke_en], "uni": r.uni, "ucret": int(r.ucret),
            "kira": int(r.kira), "yasam": None if pd.isna(r.yasam) else round(float(r.yasam), 1),
            "toplam": int(r.toplam), "pop": int(r.pop),
        })

    ulkeler = []
    for ad, g in df.groupby("ulke_en"):
        y = g["yasam"].dropna()
        ulkeler.append({
            "ulke": TR[ad], "n": int(len(g)), "nuni": int(g["uni"].nunique()),
            "pop": int(g["pop"].iloc[0]),
            "ucret_med": float(g["ucret"].median()), "kira_med": float(g["kira"].median()),
            "toplam_med": float(g["toplam"].median()),
            "yasam_med": None if y.empty else round(float(y.median()), 1),
            "ucret_ort": round(float(g["ucret"].mean())), "kira_ort": round(float(g["kira"].mean())),
            "toplam_ort": round(float(g["toplam"].mean())),
            "ucretsiz": int((g["ucret"] == 0).sum()),
        })
    ulkeler.sort(key=lambda u: -u["toplam_med"])

    out = {
        "meta": {
            "ham_satir": ham, "tekrar_silinen": tekrar, "satir": len(df),
            "ulke": int(df["ulke_en"].nunique()), "universite": int(df["uni"].nunique()),
            "yasam_bos": bozuk, "medyan_toplam": float(df["toplam"].median()),
        },
        "programlar": programlar,
        "ulkeler": ulkeler,
    }
    with open(dst, "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, separators=(",", ":"))
    print(out["meta"])


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "veri_seti.xlsx",
         sys.argv[2] if len(sys.argv) > 2 else "veri.json")
