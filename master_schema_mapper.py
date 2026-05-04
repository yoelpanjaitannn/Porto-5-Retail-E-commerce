import pandas as pd

def consolidate_data():
    # 1. Load Datasets
    shp = pd.read_excel("Dataset_1_Shopee_Raw.xlsx")
    tkp = pd.read_excel("Dataset_2_Tokopedia_Raw.xlsx")
    tt = pd.read_excel("Dataset_3_TikTok_Raw.xlsx")
    
    # 2. STANDARISASI SHOPEE
    shp_mapped = shp.rename(columns={
        'Order ID': 'Order_ID', 'Date': 'Tx_Date', 'SKU': 'SKU_Name',
        'Price': 'Gross_Sales', 'VAT_12%': 'VAT', 'Admin_Fee': 'Platform_Fee',
        'Settlement_Amount': 'Net_Settlement'
    })
    shp_mapped['Platform'] = 'Shopee'

    # 3. STANDARISASI TOKOPEDIA (With Decimal Fix)
    tkp_mapped = tkp.rename(columns={
        'ID Pesanan': 'Order_ID', 'Tanggal': 'Tx_Date', 'Nama Produk': 'SKU_Name',
        'Harga Jual': 'Gross_Sales', 'PPN_12%': 'VAT', 'Biaya Layanan': 'Platform_Fee',
        'Dana Diteruskan': 'Net_Settlement'
    })
    # FIX: Koreksi desimal jika nilai Net_Settlement > Gross_Sales (Eror Tokopedia sebelumnya)
    tkp_mapped['Net_Settlement'] = tkp_mapped.apply(
        lambda x: x['Net_Settlement'] / 100 if x['Net_Settlement'] > x['Gross_Sales'] else x['Net_Settlement'], axis=1
    )
    tkp_mapped['Platform'] = 'Tokopedia'

    # 4. STANDARISASI TIKTOK
    tt_mapped = tt.rename(columns={
        'Item_Price': 'Gross_Sales', 'VAT_12%': 'VAT', 
        'TikTok_Platform_Fee': 'Platform_Fee'
    })
    tt_mapped['Platform'] = 'TikTok'

    # 5. PENGGABUNGAN (CONSOLIDATION)
    common_cols = ['Platform', 'Order_ID', 'Tx_Date', 'SKU_Name', 'Gross_Sales', 'VAT', 'Platform_Fee', 'Net_Settlement']
    master_df = pd.concat([shp_mapped[common_cols], tkp_mapped[common_cols], tt_mapped[common_cols]], ignore_index=True)

    # 6. EXPORT
    master_df.to_excel("Consolidated_Marketplace_Ledger.xlsx", index=False)
    print(f"Master Ledger BERHASIL dibuat: {len(master_df)} baris terkonsolidasi.")

if __name__ == "__main__":
    consolidate_data()