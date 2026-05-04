import pandas as pd
import io

# 1. Tempelkan data Tokopedia dari CMD ke dalam triple quotes ini
raw_data_tkp = """
| ID Pesanan | Tanggal | Nama Produk | Harga Jual | PPN_12% | Biaya Layanan | Dana Diteruskan |
|------------|---------|-------------|------------|---------|---------------|-----------------|
| TKP-2025-001 | 2025-01-01 | Produk A | 150000 | 16071.43 | 12000 | 121928.57 |
| TKP-2025-002 | 2025-01-02 | Produk B | 150000 | 16071.43 | 12000 | 121928.57 |
| TKP-2025-003 | 2025-01-03 | Produk C | 150000 | 16071.43 | 12000 | 121928.57 |
| TKP-2025-004 | 2025-01-04 | Produk D | 150000 | 16071.43 | 12000 | 121928.57 |
| TKP-2025-005 | 2025-01-05 | Produk E | 150000 | 16071.43 | 12000 | 121928.57 |
| TKP-2025-006 | 2025-01-06 | Produk F | 150000 | 16071.43 | 12000 | 121928.57 |
| TKP-2025-007 | 2025-01-07 | Produk G | 150000 | 16071.43 | 24000 | 109928.57 |
| TKP-2025-008 | 2025-01-08 | Produk H | 150000 | 16071.43 | 12000 | 121928.57 |
| TKP-2025-009 | 2025-01-09 | Produk I | 150000 | 16071.43 | 12000 | 121928.57 |
| TKP-2025-010 | 2025-01-10 | Produk J | 150000 | 16071.43 | 12000 | 121928.57 |
| TKP-2025-011 | 2025-01-11 | Produk K | 150000 | 16071.43 | 12000 | 121928.57 |
| TKP-2025-012 | 2025-01-12 | Produk L | 150000 | 16071.43 | 12000 | 121928.57 |
| TKP-2025-013 | 2025-01-13 | Produk M | 150000 | 16071.43 | 12000 | 121928.57 |
| TKP-2025-014 | 2025-01-14 | Produk N | 150000 | 16071.43 | 12000 | 121928.57 |
| TKP-2025-LOST | 2025-01-15 | Produk O | 150000 | 16071.43 | 12000 | 121928.57 |
| TKP-2025-016 | 2025-01-16 | Produk P | 150000 | 16071.43 | 12000 | 121928.57 |
| TKP-2025-017 | 2025-01-17 | Produk Q | 150000 | 16071.43 | 12000 | 121928.57 |
| TKP-2025-018 | 2025-01-18 | Produk R | 150000 | 16071.43 | 12000 | 121928.57 |
| TKP-2025-019 | 2025-01-19 | Produk S | 150000 | 16071.43 | 12000 | 121928.57 |
| TKP-2025-020 | 2025-01-20 | Produk T | 150000 | 16071.43 | 12000 | 121928.57 |
"""

# 2. Pembersihan Data Menggunakan Pipe (|)
lines = [line.strip() for line in raw_data_tkp.strip().split('\n') if '---' not in line]
clean_lines = ['|'.join([cell.strip() for cell in line.split('|') if cell.strip()]) for line in lines]
clean_csv = '\n'.join(clean_lines)

# 3. Load ke DataFrame
df = pd.read_csv(io.StringIO(clean_csv), sep='|')

# 4. Normalisasi Angka dan Tanggal
numeric_cols = ['Harga Jual', 'PPN_12%', 'Biaya Layanan', 'Dana Diteruskan']
for col in numeric_cols:
    df[col] = df[col].astype(str).str.replace('.', '', regex=False).str.replace(',', '.', regex=False).astype(float)

# Standarisasi Tanggal ke tipe datetime agar tidak rusak di Excel
df['Tanggal'] = pd.to_datetime(df['Tanggal'], format='%Y-%m-%d').dt.date

# 5. Simpan ke Excel
output_name = "Dataset_2_Tokopedia_Raw.xlsx"
df.to_excel(output_name, index=False)
print(f"File '{output_name}' berhasil disimpan dan distandarisasi.")