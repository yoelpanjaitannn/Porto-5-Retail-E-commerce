import pandas as pd

def run_audit_tokopedia(file_path):
    print(f"--- Memulai Audit: {file_path} ---")
    
    try:
        df = pd.read_excel(file_path)
    except Exception as e:
        print(f"Error: Gagal membaca file. {e}")
        return

    # 1. Parameter Audit (Standar Pajak & Fee Tokopedia Simulasi)
    df['DPP_Calculated'] = df['Harga Jual'] / 1.12
    df['PPN_Expected'] = (df['DPP_Calculated'] * 0.12).round(2)
    df['Dana_Expected'] = (df['Harga Jual'] - df['PPN_Expected'] - df['Biaya Layanan']).round(2)

    # 2. Deteksi Anomali
    df['Fee_Gap'] = (df['Biaya Layanan'] - 12000).abs() # Baseline fee normal = 12000
    df['Settlement_Gap'] = (df['Dana Diteruskan'] - df['Dana_Expected']).abs()
    
    # Flagging
    df['Is_Fee_Anomaly'] = df['Fee_Gap'] > 0
    df['Is_Missing_ID'] = df['ID Pesanan'].str.contains('LOST', na=False)

    # 3. Ekstraksi Temuan
    fee_anomalies = df[df['Is_Fee_Anomaly']]
    missing_ids = df[df['Is_Missing_ID']]
    
    print(f"Total Transaksi Diperiksa: {len(df)}")
    print(f"Anomali Biaya Layanan Ditemukan: {len(fee_anomalies)}")
    print(f"Order ID Tidak Valid/Lost: {len(missing_ids)}")
    
    if not fee_anomalies.empty:
        print("\n[DETAIL ANOMALI BIAYA LAYANAN - POTENSI DOUBLE CHARGE]")
        print(fee_anomalies[['ID Pesanan', 'Biaya Layanan', 'Dana Diteruskan', 'Fee_Gap']])
        
    if not missing_ids.empty:
        print("\n[DETAIL ORDER ID LOST]")
        print(missing_ids[['ID Pesanan', 'Tanggal', 'Dana Diteruskan']])

    # 4. Export Hasil
    output_file = "Audit_Result_Tokopedia.xlsx"
    df.to_excel(output_file, index=False)
    print(f"\nAudit selesai. Hasil detail disimpan di: {output_file}")

if __name__ == "__main__":
    run_audit_tokopedia('Dataset_2_Tokopedia_Raw.xlsx')