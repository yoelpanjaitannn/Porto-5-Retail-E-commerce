# 🚨 End-to-End E-Commerce Financial Reconciliation & Forensic Audit Pipeline

## 📌 Executive Summary
Dalam ekosistem e-commerce *multichannel* (Shopee, Tokopedia, TikTok), pencocokan data pesanan dari platform ke sistem ERP internal secara manual adalah proses yang rentan *error* dan memakan waktu. Proyek ini adalah simulasi **Forensic Audit & Automation Pipeline** yang dirancang untuk mendeteksi anomali finansial (kebocoran dana, transaksi fiktif, selisih harga) dan menghasilkan *Clean Master Data* secara otomatis dalam hitungan detik.

## 🛠️ Tech Stack
*   **Core Engine:** Python 3
*   **Data Manipulation:** Pandas, NumPy
*   **Reporting:** XlsxWriter (Automated Excel Formatting)
*   **Interactive Dashboard:** Streamlit, Plotly Express (Dash is also available)

## 🏗️ System Architecture & Pipeline
Sistem ini dibangun melalui 4 tahapan eksekusi yang mereplikasi skenario dunia nyata:

1.  **`1_the_multiplier.py` (Data Generator)**: Menciptakan *baseline* database bersih yang mensimulasikan ribuan transaksi dari berbagai *marketplace*.
2.  **`2_the_injector.py` (Chaos Simulation)**: Menyuntikkan anomali finansial dunia nyata ke dalam data, termasuk:
    *   *Missing Internal:* Penjualan valid namun tidak tercatat di buku besar internal.
    *   *Ghost Transactions:* Data tercatat di internal namun fiktif/tidak ada di *marketplace*.
    *   *Margin Errors:* Selisih nilai harga yang ditangkap (*Price Discrepancy*).
    *   *Cross-Platform Mismatch:* Kesalahan kategorisasi (misal: pesanan Tokopedia dicatat sebagai Shopee).
    *   *System Glitches:* Kerusakan *prefix Order ID* (contoh: kegagalan sistem TikTok Shop).
3.  **`3_final_recon.py` (The Forensic Engine)**: Melakukan proses ETL (*Extract, Transform, Load*), standarisasi teks, penanganan nilai *null*, rekonsiliasi data (*Outer Join*), dan ekstraksi perhitungan "Total Financial Risk". Menghasilkan laporan Excel multishcet otomatis yang berisi pemisahan anomali dan *sheet* `Clean_Resolved` untuk diinjeksi kembali ke ERP.
4.  **`5_streamlit_app.py` (Executive Dashboard)**: Membaca hasil audit dan menampilkannya dalam visualisasi web modern yang dinamis untuk konsumsi level C-Suite.

## 📊 Key Business Value
*   **Risk Mitigation:** Berhasil mengidentifikasi dan mengkategorikan kebocoran finansial (*Financial Leakage*) secara presisi.
*   **Data Integrity:** Mengubah data kotor yang tidak bisa diproses menjadi *clean master ledger* yang siap digunakan oleh sistem Akuntansi.
*   **Time Efficiency:** Menggantikan proses VLOOKUP manual berjam-jam menjadi eksekusi *script* yang berjalan kurang dari 5 detik.

## 🚀 How to Run Locally

1. **Clone the repository:**
   ```bash
   git clone [https://github.com/yoelpanjaitannn/Porto-5-Retail-E-commerce.git](https://github.com/yoelpanjaitannn/Porto-5-Retail-E-commerce.git)
   cd Porto-5-Retail-E-commerce

python -m pip install pandas numpy xlsxwriter streamlit plotly dash


**Run the pipeline sequentially:**
   ```bash
   # 1. Bangun fondasi data
   python 1_the_multiplier.py
   
   # 2. Injeksi anomali (Simulasi human error/system glitch)
   python 2_the_injector.py
   
   # 3. Jalankan audit & keluarkan laporan Excel
   python 3_final_recon.py
   
   # 4. Nyalakan dashboard visualisasi eksekutif
   python -m streamlit run 5_streamlit_app.py



   View the Dashboard:
Buka browser pada tautan http://localhost:8501/
