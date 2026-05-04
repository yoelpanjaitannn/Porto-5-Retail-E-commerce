import pandas as pd
import numpy as np

def inject_realistic_anomalies():
    print("[2/3] Menyuntikkan Anomali Riil & Kekacauan Struktural...")
    
    try:
        mkt = pd.read_excel("MASTER_MARKETPLACE_PROD.xlsx")
        internal = pd.read_excel("MASTER_INTERNAL_PROD.xlsx")
    except Exception as e:
        print(f"Error membaca file: {e}")
        return

    # === A. KERUSAKAN LOGIS (Financial Risks) ===
    # 1. Unrecorded Sales (Hapus 15 baris di Internal)
    drop_indices = np.random.choice(internal.index, size=15, replace=False)
    internal = internal.drop(drop_indices).reset_index(drop=True)

    # 2. Price Discrepancies (Ubah harga 20 baris di Internal)
    mismatch_indices = np.random.choice(internal.index, size=20, replace=False)
    for idx in mismatch_indices:
        internal.at[idx, 'Price_Captured'] += float(np.random.choice([-15000, 5000, 12000]))

    # 3. Cross-Platform Booking Error (Kesalahan Input ID Platform)
    cross_indices = np.random.choice(internal.index, size=10, replace=False)
    for idx in cross_indices:
        old_internal_id = str(internal.at[idx, 'Internal_ID'])
        if "INT-SHP" in old_internal_id:
            internal.at[idx, 'Internal_ID'] = old_internal_id.replace("INT-SHP", "INT-TKP")
        elif "INT-TKP" in old_internal_id:
            internal.at[idx, 'Internal_ID'] = old_internal_id.replace("INT-TKP", "INT-TTS")
            
    # 4. Ghost Transactions (Hapus 5 baris di Marketplace)
    drop_mkt = np.random.choice(mkt.index, size=5, replace=False)
    mkt = mkt.drop(drop_mkt).reset_index(drop=True)

    # === B. KERUSAKAN STRUKTURAL (Data Cleaning Tests) ===
    print("      -> Mengotori sintaksis (Typos, Spasi Siluman, Case Inconsistency)...")
    
    # 5. Spasi Siluman di Order ID Internal (Mematikan fungsi VLOOKUP/Merge)
    space_indices = np.random.choice(internal.index, size=15, replace=False)
    for idx in space_indices:
        internal.at[idx, 'Order_ID'] = str(internal.at[idx, 'Order_ID']) + " "
        
    # 6. Inkonsistensi Huruf di SKU_Name (Menyulitkan Pivot/Group By)
    sku_indices = np.random.choice(internal.index, size=25, replace=False)
    for idx in sku_indices:
        current_sku = str(internal.at[idx, 'SKU_Name'])
        internal.at[idx, 'SKU_Name'] = np.random.choice([current_sku.upper(), current_sku.lower()])

    # 7. Typo di Kolom Status
    status_indices = np.random.choice(internal.index, size=10, replace=False)
    for idx in status_indices:
        internal.at[idx, 'Status'] = np.random.choice(["completed", "COMPLETED", "Done", " Selesai "])

    # Ekspor Data Kotor
    mkt.to_excel("MASTER_MARKETPLACE_PROD.xlsx", index=False)
    internal.to_excel("MASTER_INTERNAL_PROD.xlsx", index=False)
    print("      ✓ Database sukses dirusak secara logis dan struktural.\n")

if __name__ == "__main__":
    inject_realistic_anomalies()