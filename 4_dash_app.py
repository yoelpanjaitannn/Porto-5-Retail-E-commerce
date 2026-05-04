import dash
from dash import dcc, html, dash_table
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd

# ==========================================
# 1. LOAD DATA DIAGNOSIS (Dinamis dari Patch 1.2)
# ==========================================
# Pastikan nama file ini sesuai dengan yang ada di folder lokal laptop Anda.
file_path = 'FINAL_PORTFOLIO_REPORT_AUTO.xlsx' 

df_summary = pd.read_excel(file_path, sheet_name='📊 Executive_Summary')
df_full = pd.read_excel(file_path, sheet_name='Full_Database')

# Untuk Pie Chart yang akurat, kita hitung langsung dari sheet masing-masing
missing_internal = pd.read_excel(file_path, sheet_name='⚠️ Missing_Internal')
missing_mkt = pd.read_excel(file_path, sheet_name='❌ Missing_Marketplace')
cross_plat = pd.read_excel(file_path, sheet_name='🔄 Cross_Platform_Error')
price_gap = pd.read_excel(file_path, sheet_name='💰 Price_Discrepancies')

# ==========================================
# 2. APP SETUP & UI LAYOUT
# ==========================================
app = dash.Dash(__name__)

# Filter hanya data yang bermasalah untuk ditampilkan di tabel UI
anomalies_df = df_full[df_full['Record_Status'] != 'Matched']

app.layout = html.Div(style={'backgroundColor': '#111111', 'color': '#ffffff', 'padding': '30px', 'fontFamily': 'Arial'}, children=[
    html.H1("Forensic Audit Dashboard: Financial Leakage Detection", 
            style={'textAlign': 'center', 'borderBottom': '2px solid #00d4ff', 'paddingBottom': '15px'}),
    
    html.Div([
        # Sisi Kiri: Bar Chart Risiko Finansial
        html.Div([
            dcc.Graph(id='leakage-bar')
        ], style={'width': '58%', 'display': 'inline-block', 'verticalAlign': 'top'}),
        
        # Sisi Kanan: Pie Chart Distribusi Error
        html.Div([
            dcc.Graph(id='anomaly-pie')
        ], style={'width': '40%', 'display': 'inline-block', 'verticalAlign': 'top', 'marginLeft': '2%'}),
    ]),

    html.H3("🚨 Anomaly Transaction Log (Requires Manual Override)", style={'marginTop': '40px', 'color': '#ff4b4b'}),
    
    # Tabel Data Interaktif
    dash_table.DataTable(
        id='table-anomali',
        columns=[{"name": i, "id": i} for i in anomalies_df.columns if i in ['Order_ID', 'Platform', 'Gross_Sales', 'Price_Gap', 'Record_Status']],
        data=anomalies_df.to_dict('records'),
        style_header={'backgroundColor': '#113249', 'fontWeight': 'bold', 'color': 'white', 'border': '1px solid #444'},
        style_cell={'backgroundColor': '#222222', 'color': 'white', 'textAlign': 'left', 'border': '1px solid #444'},
        page_size=10,
        sort_action="native",
        filter_action="native" 
    )
])

# ==========================================
# 3. CALLBACKS (Logika Visualisasi Plotly)
# ==========================================
@app.callback(
    [Output('leakage-bar', 'figure'),
     Output('anomaly-pie', 'figure')],
    [Input('table-anomali', 'data')] 
)
def update_graphs(data):
    # --- BAR CHART LOGIC ---
    fig_bar = px.bar(
        df_summary.iloc[2:6], 
        x='Investigation Area', 
        y='Value', 
        title="Total Financial Risk (IDR) by Category", 
        template='plotly_dark',
        color='Investigation Area',
        color_discrete_sequence=['#ff4b4b', '#ffa424', '#00d4ff', '#1f77b4']
    )
    fig_bar.update_layout(showlegend=False, margin=dict(l=20, r=20, t=50, b=20))
    
    # --- PIE CHART LOGIC ---
    counts = {
        'Unrecorded Sales': len(missing_internal), 
        'Ghost Transactions': len(missing_mkt), 
        'Price Gap': len(price_gap), 
        'Cross Platform': len(cross_plat)
    }
    df_counts = pd.DataFrame(list(counts.items()), columns=['Type', 'Count'])
    
    fig_pie = px.pie(
        df_counts, values='Count', names='Type', 
        title="Distribution of Anomaly Frequency",
        template='plotly_dark', hole=0.4,
        color_discrete_sequence=px.colors.qualitative.Pastel
    )
    fig_pie.update_layout(margin=dict(l=20, r=20, t=50, b=20))
    
    return fig_bar, fig_pie

if __name__ == '__main__':
    # FIX: app.run_server diubah menjadi app.run untuk kompatibilitas versi Dash terbaru
    app.run(debug=True)