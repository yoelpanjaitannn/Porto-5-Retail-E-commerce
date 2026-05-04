import pandas as pd
import random
from datetime import datetime, timedelta

def generate_clean_production():
    print("[1/3] Membangun Database Produksi (100% Clean Base)...")
    try:
        mkt = pd.read_excel("Consolidated_Marketplace_Ledger.xlsx").astype(object)
        internal = pd.read_excel("Dataset_4_Internal_Raw.xlsx").astype(object)
    except Exception as e:
        print(f"Error membaca seed file: {e}")
        return

    products = {
        "Glow Serum 30ml": {"min": 85000, "max": 145000, "fee": 0.08},
        "Oud Eau de Parfum 50ml": {"min": 250000, "max": 350000, "fee": 0.10},
        "Velvet Lip Tint": {"min": 45000, "max": 75000, "fee": 0.05},
        "Cleansing Oil 100ml": {"min": 110000, "max": 180000, "fee": 0.07}
    }
    product_names = list(products.keys())

    factor = 20
    mkt_large = pd.concat([mkt] * factor, ignore_index=True)
    int_large = pd.concat([internal] * factor, ignore_index=True)
    
    start_date = datetime(2025, 1, 1)

    for i in range(len(mkt_large)):
        orig_id = str(mkt_large.iloc[i]['Order_ID']).split('-')[0] + "-" + str(mkt_large.iloc[i]['Order_ID']).split('-')[1] + f"-{i:04d}"
        sku = random.choice(product_names)
        price = random.randint(products[sku]['min'], products[sku]['max'])
        new_date = (start_date + timedelta(days=random.randint(0, 90))).date()
        
        # Penyelarasan Platform ID agar tidak terjadi Cross-Platform "Gaib"
        platform = str(mkt_large.iloc[i]['Platform']).upper()
        if 'SHOPEE' in platform: prefix = 'INT-SHP'
        elif 'TOKOPEDIA' in platform: prefix = 'INT-TKP'
        elif 'TIKTOK' in platform: prefix = 'INT-TTS'
        else: prefix = 'INT-OTH'
        
        # Marketplace Update
        mkt_large.at[i, 'Order_ID'] = orig_id
        mkt_large.at[i, 'SKU_Name'] = sku
        mkt_large.at[i, 'Gross_Sales'] = price
        mkt_large.at[i, 'VAT'] = round((price / 1.12) * 0.12, 2)
        mkt_large.at[i, 'Platform_Fee'] = round(price * products[sku]['fee'], 2)
        mkt_large.at[i, 'Net_Settlement'] = price - mkt_large.at[i, 'Platform_Fee']
        mkt_large.at[i, 'Tx_Date'] = new_date
        
        # Internal Update (Sinkronisasi Penuh)
        int_large.at[i, 'Order_ID'] = orig_id
        int_large.at[i, 'Internal_ID'] = f"{prefix}-{i:04d}" # Mengunci kebenaran Platform
        int_large.at[i, 'SKU_Name'] = sku
        int_large.at[i, 'Price_Captured'] = price
        int_large.at[i, 'Tx_Date'] = new_date

    mkt_large.to_excel("MASTER_MARKETPLACE_PROD.xlsx", index=False)
    int_large.to_excel("MASTER_INTERNAL_PROD.xlsx", index=False)
    print("      ✓ 1.200 Transaksi Suci berhasil dibuat dengan ID selaras.\n")

if __name__ == "__main__":
    generate_clean_production()