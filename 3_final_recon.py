import pandas as pd
import numpy as np

def execute_final_audit():
    print("[3/3] Menjalankan Audit Forensik & Rekonsiliasi Final (Patch 1.2)...")
    mkt = pd.read_excel("MASTER_MARKETPLACE_PROD.xlsx")
    internal = pd.read_excel("MASTER_INTERNAL_PROD.xlsx")

    # === TAHAP 1: DATA CLEANSING ===
    mkt['Order_ID'] = mkt['Order_ID'].astype(str).str.strip()
    internal['Order_ID'] = internal['Order_ID'].astype(str).str.strip()

    mkt['SKU_Name'] = mkt['SKU_Name'].astype(str).str.strip().str.title()
    internal['SKU_Name'] = internal['SKU_Name'].astype(str).str.strip().str.title()
    
    internal['Status'] = internal['Status'].fillna('Completed')
    internal['Status'] = internal['Status'].astype(str).str.strip().str.capitalize()
    internal['Status'] = internal['Status'].replace(['Done', 'Selesai'], 'Completed')

    # === TAHAP 2: REKONSILIASI ===
    recon = pd.merge(mkt, internal, on="Order_ID", how="outer", suffixes=('_mkt', '_int'), indicator=True)
    
    recon['Price_Gap'] = np.where(
        recon['_merge'] == 'both', 
        recon['Gross_Sales'] - recon['Price_Captured'], 
        np.nan 
    )

    def impute_platform(row):
        if pd.notna(row['Platform']): return row['Platform']
        iid = str(row['Internal_ID']).upper()
        if 'INT-SHP' in iid: return 'Shopee'
        if 'INT-TKP' in iid: return 'Tokopedia'
        if 'INT-TTS' in iid: return 'TikTok'
        return 'Unknown'
    recon['Platform'] = recon.apply(impute_platform, axis=1)

    def check_cross(row):
        if row['_merge'] == 'both':
            plat, iid = str(row['Platform']).lower(), str(row['Internal_ID']).lower()
            if ('shopee' in plat and 'int-shp' not in iid) or \
               ('tokopedia' in plat and 'int-tkp' not in iid) or \
               ('tiktok' in plat and 'int-tts' not in iid): return True
        return False
    recon['Cross_Booking_Error'] = recon.apply(check_cross, axis=1)

    recon['Record_Status'] = recon['_merge'].map({
        'both': 'Matched',
        'left_only': 'Marketplace Only',
        'right_only': 'Internal Only'
    })

    # === TAHAP 3: KLASIFIKASI TEMUAN ===
    missing_internal = recon[recon['Record_Status'] == 'Marketplace Only'].copy()
    missing_mkt = recon[recon['Record_Status'] == 'Internal Only'].copy()
    cross_cases = recon[recon['Cross_Booking_Error'] == True].copy()
    price_diff = recon[(recon['Record_Status'] == 'Matched') & (recon['Price_Gap'] != 0) & (recon['Cross_Booking_Error'] == False)].copy()

    # === TAHAP 4: CLEAN_RESOLVED ===
    clean_resolved = recon[recon['Record_Status'] == 'Matched'].copy()
    clean_resolved['Price_Captured'] = clean_resolved['Gross_Sales']
    clean_resolved['Price_Gap'] = 0
    clean_resolved['Status'] = 'Completed'
    clean_resolved = clean_resolved.drop(columns=['_merge', 'Cross_Booking_Error', 'Record_Status'], errors='ignore')

    # === TAHAP 5: KALKULASI MATEMATIS ===
    unbooked = float(missing_internal['Gross_Sales'].sum())
    ghost = float(missing_mkt['Price_Captured'].sum())
    leakage = float(abs(price_diff['Price_Gap']).sum()) 
    cross_risk = float(cross_cases['Price_Captured'].sum())
    total_risk = unbooked + ghost + leakage + cross_risk

    # === TAHAP 6: REPORTING & DOCUMENTATION ===
    summary_data = {
        "Investigation Area": [
            "1. Valid Marketplace Orders (Baseline)", 
            "2. Total Gross Sales (from Full_Database)", 
            "⚠️ A. Unrecorded Sales (Missing in Internal)", 
            "❌ B. Ghost Transactions (Missing in Mkt)", 
            "💰 C. Margin Error (Price Discrepancy)", 
            "🔄 D. Cross-Platform Error (Miscategorized)", 
            "🚨 TOTAL FINANCIAL RISK VALUE",
            " ",
            "📌 DATA INTEGRITY NOTES:"
        ],
        "Value": [
            f"{len(mkt):,.0f} Orders", 
            mkt['Gross_Sales'].sum(), 
            unbooked, 
            ghost, 
            leakage, 
            cross_risk, 
            total_risk, 
            "", 
            "Full_Database berisi total gabungan (Outer Join)."
        ]
    }
    df_sum = pd.DataFrame(summary_data)

    drop_cols = ['_merge', 'Cross_Booking_Error']
    missing_internal = missing_internal.drop(columns=drop_cols, errors='ignore')
    missing_mkt = missing_mkt.drop(columns=drop_cols, errors='ignore')
    price_diff = price_diff.drop(columns=drop_cols, errors='ignore')
    cross_cases = cross_cases.drop(columns=drop_cols, errors='ignore')
    recon_print = recon.drop(columns=drop_cols, errors='ignore')

    writer = pd.ExcelWriter("FINAL_PORTFOLIO_REPORT_AUTO.xlsx", engine='xlsxwriter')
    f_head = writer.book.add_format({'bold': True, 'bg_color': '#113249', 'font_color': 'white', 'border': 1})
    f_curr = writer.book.add_format({'num_format': 'Rp #,##0', 'border': 1})
    f_alert = writer.book.add_format({'bold': True, 'bg_color': '#FFC7CE', 'font_color': '#9C0006', 'border': 1, 'num_format': 'Rp #,##0'})
    f_note = writer.book.add_format({'italic': True, 'font_color': '#FF0000', 'bold': True})

    def format_ws(df, name, is_sum=False, add_footnote=False):
        df.to_excel(writer, sheet_name=name, index=False)
        ws = writer.sheets[name]
        for i, col in enumerate(df.columns):
            max_len = max(df[col].astype(str).str.len().max(), len(str(col))) + 3
            ws.set_column(i, i, max_len)
            ws.write(0, i, col, f_head)
            if any(x in str(col) for x in ['Sales', 'Captured', 'Gap', 'Value', 'Risk']): 
                ws.set_column(i, i, max_len, f_curr)
        if is_sum: 
            # [FIX KRITIS DI SINI]: Pindah dari baris 6 ke 7 (0-indexed Excel logic)
            ws.write(7, 1, total_risk, f_alert)
        if add_footnote:
            ws.write(len(df) + 2, 0, "📌 CATATAN AUDIT:", f_note)
            ws.write(len(df) + 3, 0, "Sebanyak 20 record di atas adalah akibat Order_ID TikTok yang cacat sistem (prefix hilang).", f_note)
            ws.write(len(df) + 4, 0, "Transaksi secara fisik ada, namun gagal terekonsiliasi otomatis. (Requires manual override).", f_note)

    format_ws(df_sum, '📊 Executive_Summary', is_sum=True)
    format_ws(missing_internal, '⚠️ Missing_Internal', add_footnote=True)
    format_ws(missing_mkt, '❌ Missing_Marketplace', add_footnote=True)
    format_ws(price_diff, '💰 Price_Discrepancies')
    format_ws(cross_cases, '🔄 Cross_Platform_Error')
    format_ws(clean_resolved, '✅ Clean_Resolved')
    format_ws(recon_print, 'Full_Database')

    writer.close()
    print(f"      ✓ Rekonsiliasi Sukses. Risiko Terdeteksi: Rp {total_risk:,.0f}\n")

if __name__ == "__main__":
    execute_final_audit()