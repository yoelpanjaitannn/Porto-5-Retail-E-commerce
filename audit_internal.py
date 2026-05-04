import pandas as pd

df = pd.read_excel("Dataset_4_Internal_Raw.xlsx")

# 1. Cek Duplikat Order ID
duplicates = df[df.duplicated('Order_ID', keep=False)]

# 2. Cek Status Returned
returned = df[df['Status'] == 'Returned']

print("--- Hasil Audit Internal ---")
print(f"Total Baris: {len(df)}")
print(f"Temuan Duplikat: {len(duplicates)}")
if not duplicates.empty:
    print(duplicates[['Internal_ID', 'Order_ID']])
print(f"\nTemuan Retur: {len(returned)}")
print(returned[['Order_ID', 'Status']])

df[df.duplicated('Order_ID', keep=False)].to_excel("Audit_Result_Internal.xlsx", index=False)