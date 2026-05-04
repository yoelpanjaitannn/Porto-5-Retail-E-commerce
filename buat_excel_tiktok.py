import pandas as pd
import io

# Data yang diekstrak langsung dari terminal Anda
raw_data_tiktok = """
| Order_ID | Tx_Date | SKU_Name | Item_Price | VAT_12% | TikTok_Platform_Fee | Net_Settlement |
|---|---|---|---|---|---|---|
| TTS-2025-01-001 | 2025-01-01 | Glow Serum | 150000 | 16071.43 | 15000 | 118928.57 |
| TTS-2025-01-002 | 2025-01-02 | Oud Eau de Parfum | 150000 | 16071.43 | 15000 | 118928.57 |
| TTS-2025-01-003 | 2025-01-03 | Velvet Lip Tint | 150000 | 16071.43 | 15000 | 118928.57 |
| TTS-2025-01-004 | 2025-01-04 | Cleansing Oil | 150000 | 16071.43 | 15000 | 118928.57 |
| TTS-2025-01-005 | 2025-01-05 | Glow Serum | 150000 | 16071.43 | 15000 | 118928.57 |
| TTS-2025-01-006 | 2025-01-06 | Oud Eau de Parfum | 150000 | 16071.43 | 15000 | 118928.57 |
| TTS-2025-01-007 | 2025-01-07 | Velvet Lip Tint | 150000 | 16071.43 | 15000 | 118928.57 |
| TTS-2025-01-008 | 2025-01-08 | Cleansing Oil | 150000 | 16071.43 | 15000 | 118928.57 |
| TTS-2025-01-009 | 2025-01-09 | Oud Eau de Parfum | -150000 | -16071.43 | 0 | -133928.57 |
| TTS-2025-01-010 | 2025-01-10 | Glow Serum | 150000 | 16071.43 | 15000 | 118928.57 |
| TTS-2025-01-011 | 2025-01-11 | Velvet Lip Tint | 150000 | 16071.43 | 15000 | 118928.57 |
| TTS-2025-01-012 | 2025-01-12 | Cleansing Oil | 150000 | 16071.43 | 15000 | 118928.57 |
| TTS-2025-01-013 | 2025-01-13 | Glow Serum | 150000 | 16071.43 | 15000 | 118928.57 |
| TTS-2025-01-014 | 2025-01-14 | Oud Eau de Parfum | 150000 | 16071.43 | 15000 | 118928.57 |
| TTS-2025-01-015 | 2025-01-15 | Velvet Lip Tint | 150000 | 16071.43 | 15000 | 118928.57 |
| TTS-2025-01-016 | 2025-01-16 | Cleansing Oil | 150000 | 16071.43 | 15000 | 118928.57 |
| TTS-2025-01-017 | 2025-01-17 | Glow Serum | 150000 | 16071.43 | 15000 | 118928.57 |
| TTS-2025-01-018 | 2025-01-18 | Glow Serum | 150000 | 16071.43 | 0 | 133928.57 |
| TTS-2025-01-019 | 2025-01-19 | Velvet Lip Tint | 150000 | 16071.43 | 15000 | 118928.57 |
| TTS-2025-01-020 | 2025-01-20 | Cleansing Oil | 150000 | 16071.43 | 15000 | 118928.57 |
"""

# Proses pembersihan data
df = pd.read_csv(io.StringIO(raw_data_tiktok.strip()), sep="|", skipinitialspace=True).dropna(axis=1, how='all')
df.columns = df.columns.str.strip()

# Konversi kolom numerik
cols = ['Item_Price', 'VAT_12%', 'TikTok_Platform_Fee', 'Net_Settlement']
for col in cols:
    df[col] = pd.to_numeric(df[col], errors='coerce')

# Simpan ke Excel
df.to_excel("Dataset_3_TikTok_Raw.xlsx", index=False)
print("Dataset_3_TikTok_Raw.xlsx berhasil dibuat.")