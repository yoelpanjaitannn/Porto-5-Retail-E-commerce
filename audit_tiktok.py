import pandas as pd

# 1. Load Data
file_path = 'Dataset_3_TikTok_Raw.xlsx'
try:
    df = pd.read_excel(file_path)
    print(f"--- Memulai Audit: {file_path} ---")
except FileNotFoundError:
    print(f"EROR: File {file_path} tidak ditemukan. Jalankan 'buat_excel_tiktok.py' dulu!")
    exit()

# 2. Logika Audit: Deteksi Anomali
# Anomali 1: Refund (Nilai Negatif)
df['Is_Refund'] = df['Item_Price'] < 0

# Anomali 2: Zero Fee (Kesalahan Sistem/Platform)
# Platform fee 0 pada barang yang harganya positif (Bukan refund)
df['Is_Fee_Error'] = (df['TikTok_Platform_Fee'] == 0) & (df['Item_Price'] > 0)

# 3. Filter Temuan
anomalies = df[df['Is_Refund'] | df['Is_Fee_Error']]

# 4. Tampilkan Hasil
print(f"Total Transaksi: {len(df)}")
print(f"Temuan Anomali: {len(anomalies)}")
print("\n[DETAIL TEMUAN]")
if not anomalies.empty:
    print(anomalies[['Order_ID', 'SKU_Name', 'Item_Price', 'TikTok_Platform_Fee', 'Is_Refund', 'Is_Fee_Error']])
else:
    print("Tidak ada anomali terdeteksi.")

# 5. Export Hasil Audit untuk Kertas Kerja
anomalies.to_excel("Audit_Result_TikTok.xlsx", index=False)
print("\nHasil audit detail disimpan di: Audit_Result_TikTok.xlsx")