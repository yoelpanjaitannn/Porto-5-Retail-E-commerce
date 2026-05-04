import pandas as pd

try:
    df = pd.read_excel("Consolidated_Marketplace_Ledger.xlsx")
    
    # Check 1: Apakah ada Order_ID yang duplikat antar platform?
    dup_orders = df[df.duplicated('Order_ID', keep=False)]
    
    # Check 2: Rekapitulasi per Platform
    recap = df.groupby('Platform').agg({
        'Order_ID': 'count',
        'Net_Settlement': 'sum'
    })
    
    print("--- HASIL AUDIT KONSOLIDASI ---")
    print(recap)
    
    if not dup_orders.empty:
        print("\nTEMUAN: Ada Order ID Duplikat!")
        print(dup_orders[['Platform', 'Order_ID']])
    else:
        print("\nIntegritas Order ID Aman (Unik).")

except Exception as e:
    print(f"Eror saat membaca file: {e}")