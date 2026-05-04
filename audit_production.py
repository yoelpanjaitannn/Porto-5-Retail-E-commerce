import pandas as pd

def audit_production_files():
    # 1. Load Data Produksi
    mkt = pd.read_excel("MASTER_MARKETPLACE_PROD.xlsx")
    internal = pd.read_excel("MASTER_INTERNAL_PROD.xlsx")
    
    print("--- RINGKASAN DATA PRODUKSI ---")
    print(f"Total Baris Marketplace : {len(mkt)}")
    print(f"Total Baris Internal    : {len(internal)}")
    
    # 2. Cek Variasi Produk (Beauty & Fragrance)
    print("\n[Variasi Produk di Marketplace]")
    print(mkt['SKU_Name'].value_counts())
    
    # 3. Cek Rentang Harga (Apakah sudah acak?)
    print("\n[Statistik Harga Marketplace]")
    print(mkt['Gross_Sales'].describe())
    
    # 4. Cek Konsistensi Order_ID (Rekonsiliasi Cepat)
    mkt_ids = set(mkt['Order_ID'])
    int_ids = set(internal['Order_ID'])
    
    only_mkt = mkt_ids - int_ids
    only_int = int_ids - mkt_ids
    
    print("\n--- CEK KONSISTENSI ID ---")
    print(f"ID yang HANYA ada di Marketplace: {len(only_mkt)}")
    print(f"ID yang HANYA ada di Internal   : {len(only_int)}")
    
    # 5. Cek Selisih Nominal (Price Match)
    # Kita adu harga di marketplace vs internal untuk order yang sama
    merged = pd.merge(mkt, internal, on="Order_ID")
    merged['Diff'] = merged['Gross_Sales'] - merged['Price_Captured']
    
    price_mismatch = merged[merged['Diff'] != 0]
    print(f"Jumlah Transaksi dengan Selisih Harga: {len(price_mismatch)}")
    
    if not price_mismatch.empty:
        print("\n[Sampel Selisih Harga]")
        print(price_mismatch[['Order_ID', 'Gross_Sales', 'Price_Captured', 'Diff']].head())

if __name__ == "__main__":
    audit_production_files()