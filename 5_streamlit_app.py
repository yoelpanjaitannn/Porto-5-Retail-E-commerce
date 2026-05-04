import streamlit as st
import pandas as pd
import plotly.express as px

# ==========================================
# 1. SETUP HALAMAN (Otomatis Modern)
# ==========================================
st.set_page_config(page_title="Forensic Audit Dashboard", layout="wide", initial_sidebar_state="collapsed")

st.title("🚨 Forensic Audit Dashboard: Financial Leakage Detection")
st.markdown("Dashboard ini mendeteksi dan mengkategorikan anomali transaksi lintas platform secara otomatis.")
st.markdown("---")

# ==========================================
# 2. LOAD DATA
# ==========================================
@st.cache_data
def load_data():
    file_path = 'FINAL_PORTFOLIO_REPORT_AUTO.xlsx'
    df_summary = pd.read_excel(file_path, sheet_name='📊 Executive_Summary')
    df_full = pd.read_excel(file_path, sheet_name='Full_Database')
    
    missing_internal = pd.read_excel(file_path, sheet_name='⚠️ Missing_Internal')
    missing_mkt = pd.read_excel(file_path, sheet_name='❌ Missing_Marketplace')
    cross_plat = pd.read_excel(file_path, sheet_name='🔄 Cross_Platform_Error')
    price_gap = pd.read_excel(file_path, sheet_name='💰 Price_Discrepancies')

# === THE FIX: MENGHAPUS FOOTNOTE DARI PERHITUNGAN ===
    # Footnote tidak memiliki Order_ID, jadi kita buang semua baris yang Order_ID-nya kosong (NaN)
    missing_internal = missing_internal.dropna(subset=['Order_ID'])
    missing_mkt = missing_mkt.dropna(subset=['Order_ID'])

    return df_summary, df_full, missing_internal, missing_mkt, cross_plat, price_gap

df_summary, df_full, missing_internal, missing_mkt, cross_plat, price_gap = load_data()

# ==========================================
# 3. KPI METRICS (Elemen Eksekutif)
# ==========================================
total_risk = df_summary.iloc[6]['Value'] # Mengambil baris TOTAL
unrecorded = df_summary.iloc[2]['Value']
ghost_tx = df_summary.iloc[3]['Value']

col_kpi1, col_kpi2, col_kpi3 = st.columns(3)
col_kpi1.metric(label="🚨 TOTAL FINANCIAL RISK", value=f"Rp {total_risk:,.0f}")
col_kpi2.metric(label="⚠️ Unrecorded Sales", value=f"Rp {unrecorded:,.0f}")
col_kpi3.metric(label="❌ Ghost Transactions", value=f"Rp {ghost_tx:,.0f}")
st.markdown("<br>", unsafe_allow_html=True)

# ==========================================
# 4. VISUALISASI PLOTLY
# ==========================================
col1, col2 = st.columns([6, 4])

with col1:
    fig_bar = px.bar(
        df_summary.iloc[2:6], 
        x='Investigation Area', 
        y='Value', 
        title="Total Financial Risk (IDR) by Category",
        color='Investigation Area',
        color_discrete_sequence=['#ff4b4b', '#ffa424', '#00d4ff', '#1f77b4']
    )
    fig_bar.update_layout(showlegend=False, margin=dict(l=0, r=0, t=40, b=0))
    st.plotly_chart(fig_bar, use_container_width=True)

with col2:
    counts = {
        'Unrecorded': len(missing_internal), 
        'Ghost Tx': len(missing_mkt), 
        'Price Gap': len(price_gap), 
        'Cross Platform': len(cross_plat)
    }
    df_counts = pd.DataFrame(list(counts.items()), columns=['Type', 'Count'])
    fig_pie = px.pie(
        df_counts, values='Count', names='Type', 
        title="Distribution of Anomaly Frequency",
        hole=0.4,
        color_discrete_sequence=px.colors.qualitative.Pastel
    )
    fig_pie.update_layout(margin=dict(l=0, r=0, t=40, b=0))
    st.plotly_chart(fig_pie, use_container_width=True)

# ==========================================
# 5. DATA TABLE INTERAKTIF
# ==========================================
st.markdown("### 📋 Anomaly Transaction Log")
st.caption("Gunakan fitur *filter* pada kolom untuk mencari Order_ID spesifik atau jenis Record_Status (Requires Manual Override).")

anomalies_df = df_full[df_full['Record_Status'] != 'Matched']
cols_to_show = [c for c in ['Platform', 'Order_ID', 'Gross_Sales', 'Price_Gap', 'Record_Status'] if c in anomalies_df.columns]

# Tabel Streamlit otomatis modern
st.dataframe(anomalies_df[cols_to_show], use_container_width=True, hide_index=True)