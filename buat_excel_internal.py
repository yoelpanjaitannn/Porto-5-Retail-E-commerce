import pandas as pd

def generate_internal_ledger():
    data = []
    
    # 1. Data Shopee (SHP-2025-001 s/d 020)
    for i in range(1, 21):
        order_id = f"SHP-2025-{i:03d}"
        if order_id == "SHP-2025-005": continue # Anomali: Ada di marketplace, hilang di internal
        data.append({"Internal_ID": f"INT-SHP-{i:03d}", "Order_ID": order_id, "Tx_Date": f"2025-01-{i:02d}", "SKU_Name": "Beauty Item", "Price_Captured": 150000, "Status": "Completed"})

    # 2. Data Tokopedia (TKP-2025-001 s/d 020)
    for i in range(1, 21):
        data.append({"Internal_ID": f"INT-TKP-{i:03d}", "Order_ID": f"TKP-2025-{i:03d}", "Tx_Date": f"2025-01-{i:02d}", "SKU_Name": "Beauty Item", "Price_Captured": 150000, "Status": "Completed"})

    # 3. Data TikTok (TTS-2025-01-001 s/d 020)
    for i in range(1, 21):
        order_id = f"TTS-2025-01-{i:03d}"
        status = "Returned" if order_id == "TTS-2025-01-009" else "Completed"
        data.append({"Internal_ID": f"INT-TTS-{i:03d}", "Order_ID": order_id, "Tx_Date": f"2025-01-{i:02d}", "SKU_Name": "Beauty Item", "Price_Captured": 150000, "Status": status})

    # 4. Anomali Tambahan (Fiktif & Duplikat)
    data.append({"Internal_ID": "INT-ERR-999", "Order_ID": "OFFLINE-001", "Tx_Date": "2025-01-15", "SKU_Name": "Fragrance", "Price_Captured": 150000, "Status": "Completed"})
    data.append({"Internal_ID": "INT-DUP-001", "Order_ID": "SHP-2025-001", "Tx_Date": "2025-01-01", "SKU_Name": "Glow Serum", "Price_Captured": 150000, "Status": "Completed"})

    df = pd.DataFrame(data)
    df.to_excel("Dataset_4_Internal_Raw.xlsx", index=False)
    print(f"Dataset_4_Internal_Raw.xlsx BERHASIL dibuat ({len(df)} baris).")

if __name__ == "__main__":
    generate_internal_ledger()