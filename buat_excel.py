import pandas as pd
import io

# 1. Tempelkan data mentah dari CMD Anda di sini
raw_data = """
| Order ID | Date | SKU | Price | VAT_12% | Admin_Fee | Settlement_Amount |
|----------|------|-----|-------|---------|-----------|-------------------|
| SHP-2025-001 | 2025-01-01 | ABC123 | 150.000 | 16.071,43 | 10.000 | 123.928,57 |
| SHP-2025-002 | 2025-01-02 | ABC123 | 150.000 | 16.071,43 | 10.000 | 123.928,57 |
| SHP-2025-003 | 2025-01-03 | ABC123 | 150.000 | 16.071,43 | 10.000 | 123.928,57 |
| SHP-2025-004 | 2025-01-04 | ABC123 | 150.000 | 16.071,43 | 10.000 | 123.928,57 |
| SHP-2025-005 | 2025-01-05 | ABC123 | 150.000 | 14.732,14 | 10.000 | 125.267,86 |
| SHP-2025-006 | 2025-01-06 | ABC123 | 150.000 | 16.071,43 | 10.000 | 123.928,57 |
| SHP-2025-007 | 2025-01-07 | ABC123 | 150.000 | 16.071,43 | 10.000 | 123.928,57 |
| SHP-2025-008 | 2025-01-08 | ABC123 | 150.000 | 16.071,43 | 10.000 | 123.928,57 |
| SHP-2025-009 | 2025-01-09 | ABC123 | 150.000 | 16.071,43 | 10.000 | 123.928,57 |
| SHP-2025-MISSING | 2025-01-10 | ABC123 | 150.000 | 16.071,43 | 10.000 | 123.928,57 |
| SHP-2025-010 | 2025-01-11 | ABC123 | 150.000 | 16.071,43 | 10.000 | 123.928,57 |
| SHP-2025-011 | 2025-01-12 | ABC123 | 150.000 | 16.071,43 | 10.000 | 123.928,57 |
| SHP-2025-012 | 2025-01-13 | ABC123 | 150.000 | 16.071,43 | 10.000 | 123.928,57 |
| SHP-2025-013 | 2025-01-14 | ABC123 | 150.000 | 16.071,43 | 10.000 | 123.928,57 |
| SHP-2025-014 | 2025-01-15 | ABC123 | 150.000 | 16.071,43 | 10.000 | 123.928,57 |
| SHP-2025-015 | 2025-01-16 | ABC123 | 150.000 | 16.071,43 | 10.000 | 123.928,57 |
| SHP-2025-016 | 2025-01-17 | ABC123 | 150.000 | 16.071,43 | 10.000 | 123.928,57 |
| SHP-2025-017 | 2025-01-18 | ABC123 | 150.000 | 16.071,43 | 10.000 | 123.928,57 |
| SHP-2025-018 | 2025-01-19 | ABC123 | 150.000 | 16.071,43 | 10.000 | 123.928,57 |
| SHP-2025-019 | 2025-01-20 | ABC123 | 150.000 | 16.071,43 | 10.000 | 123.928,57 |
| SHP-2025-020 | 2025-01-21 | ABC123 | 150.000 | 16.071,43 | 10.000 | 123.928,57 |
"""

# 2. Pembersihan Data Menggunakan Pipe (|) sebagai Separator
lines = [line.strip() for line in raw_data.strip().split('\n') if '---' not in line]
# Pastikan setiap baris dibersihkan dari spasi berlebih namun tetap dipisah tanda |
clean_lines = ['|'.join([cell.strip() for cell in line.split('|') if cell.strip()]) for line in lines]
clean_csv = '\n'.join(clean_lines)

# 3. Load ke DataFrame dengan separator |
df = pd.read_csv(io.StringIO(clean_csv), sep='|')

# 4. Normalisasi Angka (Titik ribuan dihilangkan, koma desimal jadi titik)
numeric_cols = ['Price', 'VAT_12%', 'Admin_Fee', 'Settlement_Amount']
for col in numeric_cols:
    df[col] = df[col].astype(str).str.replace('.', '', regex=False).str.replace(',', '.', regex=False).astype(float)

# 5. Simpan ulang
df.to_excel("Dataset_1_Shopee_Raw.xlsx", index=False)
print("File 'Dataset_1_Shopee_Raw.xlsx' berhasil diperbaiki dan disimpan.")