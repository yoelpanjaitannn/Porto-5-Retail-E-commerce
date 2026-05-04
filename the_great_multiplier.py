import pandas as pd
import numpy as np
import random
from datetime import datetime, timedelta

def multiply_and_sync():
    # 1. Load & Force Object Type (Mencegah TypeError PyArrow String)
    try:
        mkt = pd.read_excel("Consolidated_Marketplace_Ledger.xlsx").astype(object)
        internal = pd.read_excel("Dataset_4_Internal_Raw.xlsx").astype(object)
    except Exception as e:
        print(f"Eror Loading File: {e}")
        return

    # 2. Master SKU & Price Range
    products = {
        "Glow Serum 30ml": {"min": 85000, "max": 145000, "fee": 0.08},
        "Oud Eau de Parfum 50ml": {"min": 250000, "max": 350000, "fee": 0.10},
        "Velvet Lip Tint": {"min": 45000, "max": 75000, "fee": 0.05},
        "Cleansing Oil 100ml": {"min": 110000, "max": 180000, "fee": 0.07}
    }
    product_names = list(products.keys())

    # 3. Multiplier Factor (60 baris -> 1.200 baris)
    factor = 20
    mkt_large = pd.concat([mkt] * factor, ignore_index=True)
    int_large = pd.concat([internal] * factor, ignore_index=True)

    # 4. Injeksi Data Riil & Acak
    total_rows = len(mkt_large)
    start_date = datetime(2025, 1, 1)

    for i in range(total_rows):
        # Generate Unique ID (String Casting untuk keamanan)
        orig_id = str(mkt_large.iloc[i]['Order_ID'])
        new_id = f"{orig_id}-V{i}"
        
        # Acak Produk & Harga
        sku = random.choice(product_names)
        price = random.randint(products[sku]['min'], products[sku]['max'])
        new_date = (start_date + timedelta(days=random.randint(0, 90))).date()
        
        # Update Marketplace Side
        mkt_large.at[i, 'Order_ID'] = new_id
        mkt_large.at[i, 'SKU_Name'] = sku
        mkt_large.at[i, 'Gross_Sales'] = price
        mkt_large.at[i, 'VAT'] = round((price / 1.12) * 0.12, 2)
        mkt_large.at[i, 'Platform_Fee'] = round(price * products[sku]['fee'], 2)
        mkt_large.at[i, 'Net_Settlement'] = price - mkt_large.at[i, 'Platform_Fee']
        mkt_large.at[i, 'Tx_Date'] = new_date
        
        # Update Internal Side (Syncing)
        int_large.at[i, 'Order_ID'] = new_id
        int_large.at[i, 'SKU_Name'] = sku
        int_large.at[i, 'Price_Captured'] = price
        int_large.at[i, 'Tx_Date'] = new_date

    # 5. Save Production Files
    mkt_large.to_excel("MASTER_MARKETPLACE_PROD.xlsx", index=False)
    int_large.to_excel("MASTER_INTERNAL_PROD.xlsx", index=False)
    
    print(f"SUKSES: {len(mkt_large)} data produksi telah dibuat dan disinkronkan.")

if __name__ == "__main__":
    multiply_and_sync()