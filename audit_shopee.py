import pandas as pd
import numpy as np

def run_audit_shopee(file_path):
    print(f"--- Memulai Audit: {file_path} ---")
    
    # 1. Load Data
    try:
        df = pd.read_excel(file_path)
    except Exception as e:
        print(f"Error: Gagal membaca file. Pastikan library 'openpyxl' terinstal. {e}")
        return

    # 2. Pembersihan Data (Handling format ribuan titik dan desimal koma jika ada)
    for col in ['Price', 'VAT_12%', 'Admin_Fee', 'Settlement_Amount']:
        if df[col].dtype == 'object':
            df[col] = df[col].str.replace('.', '', regex=False).str.replace(',', '.', regex=False).astype(float)

    # 3. Parameter Audit Pro (Standar Januari 2025)
    # Rumus: DPP = Price / 1.12 | PPN = DPP * 0.12
    df['DPP_Calculated'] = df['Price'] / 1.12
    df['VAT_Expected'] = (df['DPP_Calculated'] * 0.12).round(2)
    df['Settlement_Expected'] = (df['Price'] - df['VAT_Expected'] - df['Admin_Fee']).round(2)

    # 4. Deteksi Anomali
    # Selisih PPN (Mencari tarif 11% yang terselip)
    df['VAT_Gap'] = (df['VAT_12%'] - df['VAT_Expected']).abs()
    # Selisih Settlement (Mencari kebocoran kas)
    df['Settlement_Gap'] = (df['Settlement_Amount'] - df['Settlement_Expected']).abs()
    
    # Flagging
    df['Is_VAT_Anomaly'] = df['VAT_Gap'] > 1.0
    df['Is_Missing_ID'] = df['Order ID'].str.contains('MISSING', na=False)

    # 5. Output Laporan ke Terminal
    vat_anomalies = df[df['Is_VAT_Anomaly']]
    missing_ids = df[df['Is_Missing_ID']]
    
    print(f"Total Transaksi: {len(df)}")
    print(f"Anomali PPN Ditemukan: {len(vat_anomalies)}")
    print(f"Order ID Tidak Terdaftar: {len(missing_ids)}")
    
    if not vat_anomalies.empty:
        print("\n[DETAIL ANOMALI PPN]")
        print(vat_anomalies[['Order ID', 'VAT_12%', 'VAT_Expected', 'VAT_Gap']])
        
    if not missing_ids.empty:
        print("\n[DETAIL ORDER ID MISSING]")
        print(missing_ids[['Order ID', 'Date', 'Settlement_Amount']])

    # 6. Simpan Hasil Audit ke Excel Baru
    output_file = "Audit_Result_Shopee.xlsx"
    df.to_excel(output_file, index=False)
    print(f"\nAudit selesai. Hasil detail disimpan di: {output_file}")

if __name__ == "__main__":
    run_audit_shopee('Dataset_1_Shopee_Raw.xlsx')