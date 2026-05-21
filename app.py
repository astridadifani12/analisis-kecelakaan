






























image(92).png
CARA UP FILE ANALISIS IPYNB DI GITHUB GIMANA

Cara upload file .ipynb (Jupyter Notebook) ke GitHub dari tampilan yang kamu buka itu gampang 👇

Langkah Upload File .ipynb ke GitHub
1. Buat Repository Dulu
Sekarang kamu masih di bagian Projects, bukan repository.

Klik:

Foto profil kanan atas → Your repositories

Klik tombol New

Isi:

Repository name → misal: analisis-kecelakaan

Pilih Public / Private

Centang:

✅ Add README

Klik Create repository

2. Upload File .ipynb
Setelah repository jadi:

Klik:

Add file → Upload files

Lalu:

Drag file .ipynb kamu ke halaman
ATAU

Klik choose your files

Contoh file:

analisis.ipynb
3. Commit File
Di bawah nanti ada:

Commit changes
Isi misal:

Upload notebook analisis data
Lalu klik:

Commit changes
Kalau Dari VS Code / Git Bash (Lebih Profesional)
Kalau mau pakai terminal:

git init
git add .
git commit -m "upload ipynb"
git branch -M main
git remote add origin https://github.com/USERNAME/NAMA-REPO.git
git push -u origin main
Supaya Notebook Bisa Dibuka di GitHub
Pastikan:

file ekstensi .ipynb

ukuran tidak terlalu besar

sudah di-save di Jupyter/Colab sebelum upload

Kalau Dari Google Colab
Langsung:

File

Save a copy in GitHub

Nanti tinggal pilih repository.

Yang kamu buka sekarang itu GitHub Projects, jadi memang belum bisa upload file notebook langsung di situ.
Upload .ipynb harus lewat Repository dulu.


buatkan file untuk tampilan (main)

Mau dibuatkan file main untuk apa dulu?

Contohnya:

Streamlit → main.py

Flask

React

HTML CSS

Dashboard analisis data

Portofolio GitHub

Machine Learning app

Kalau bisa kirim juga:

Tema/projectnya apa

Mau tampilannya seperti apa

Pakai bahasa/framework apa (Python Streamlit, React, HTML, dll)

Nanti saya buatin langsung file lengkap siap upload ke GitHub 🚀


Analisis Pola Kecelakaan Fatal di Amerika Serikat Tahun 2015 Berdasarkan Faktor Waktu dan Geografis

image(93).png

image(94).png

df clean


INI MASUKIN KE GITHUB NYA GIMANA

Masukinnya ke GitHub itu lewat edit file app.py di repository kamu 👇

1. Buka app.py
Di GitHub:

klik file app.py

klik ikon ✏️ Edit

2. Hapus kode lama
Hapus semua isi file lama.

3. Paste kode ini FULL
import streamlit as st
import pandas as pd
import plotly.express as px

from google.cloud import bigquery
from google.oauth2 import service_account

# ==================================
# KONFIGURASI HALAMAN
# ==================================

st.set_page_config(
    page_title="Analisis Kecelakaan Fatal AS 2015",
    page_icon="🚗",
    layout="wide"
)

# ==================================
# TITLE
# ==================================

st.title("🚗 Analisis Pola Kecelakaan Fatal di Amerika Serikat Tahun 2015")

st.markdown("""
Dashboard ini menampilkan analisis pola kecelakaan fatal di Amerika Serikat tahun 2015 berdasarkan faktor waktu dan geografis.
""")

# ==================================
# CONNECT BIGQUERY
# ==================================

credentials = service_account.Credentials.from_service_account_info(
    st.secrets["gcp_service_account"]
)

client = bigquery.Client(
    credentials=credentials,
    project=credentials.project_id,
)

# ==================================
# LOAD DATA
# ==================================

@st.cache_data
def load_data():

    query = """
    SELECT
        state_name,
        hour_of_crash,
        month_of_crash,
        day_of_week,
        number_of_fatalities,
        number_of_drunk_drivers

    FROM `bigquery-public-data.nhtsa_traffic_fatalities.accident_2015`
    LIMIT 1000
    """

    df = client.query(query).to_dataframe()

    return df

df = load_data()

# ==================================
# SIDEBAR
# ==================================

st.sidebar.header("🔍 Filter Data")

# FILTER BULAN
bulan = st.sidebar.multiselect(
    "Pilih Bulan",
    options=sorted(df['month_of_crash'].unique()),
    default=sorted(df['month_of_crash'].unique())
)

df = df[df['month_of_crash'].isin(bulan)]

# FILTER STATE
state = st.sidebar.multiselect(
    "Pilih State",
    options=sorted(df['state_name'].unique()),
    default=sorted(df['state_name'].unique())
)

df = df[df['state_name'].isin(state)]

# ==================================
# METRIC
# ==================================

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Total Kecelakaan", len(df))

with col2:
    st.metric("Jumlah State", df['state_name'].nunique())

with col3:
    st.metric("Total Fatalitas", int(df['number_of_fatalities'].sum()))

# ==================================
# VISUALISASI BULAN
# ==================================

st.subheader("📊 Distribusi Kecelakaan Berdasarkan Bulan")

fig_month = px.histogram(
    df,
    x='month_of_crash',
    color='month_of_crash'
)

st.plotly_chart(fig_month, use_container_width=True)

# ==================================
# VISUALISASI STATE
# ==================================

st.subheader("🗺️ Distribusi Kecelakaan Berdasarkan State")

state_count = df['state_name'].value_counts().reset_index()
state_count.columns = ['State', 'Jumlah']

fig_state = px.bar(
    state_count,
    x='State',
    y='Jumlah'
)

st.plotly_chart(fig_state, use_container_width=True)

# ==================================
# VISUALISASI JAM
# ==================================

st.subheader("⏰ Distribusi Kecelakaan Berdasarkan Jam")

fig_hour = px.histogram(
    df,
    x='hour_of_crash',
    nbins=24
)

st.plotly_chart(fig_hour, use_container_width=True)

# ==================================
# VISUALISASI DRUNK DRIVER
# ==================================

st.subheader("🍺 Pengaruh Pengemudi Mabuk")

fig_drunk = px.scatter(
    df,
    x='number_of_drunk_drivers',
    y='number_of_fatalities',
    size='number_of_fatalities'
)

st.plotly_chart(fig_drunk, use_container_width=True)

# ==================================
# FOOTER
# ==================================

st.markdown("---")
st.caption("Dashboard dibuat menggunakan Streamlit dan BigQuery 🚀")
4. Commit Changes
Scroll paling bawah:

Isi:

update streamlit bigquery dashboard
Klik:

Commit changes
5. Edit requirements.txt
Isi jadi:

streamlit
pandas
plotly
google-cloud-bigquery
google-auth
db-dtypes
Commit lagi.

6. Tambahkan Secrets BigQuery
Di Streamlit Cloud:

Manage app → Settings → Secrets
Paste JSON credential Google Cloud service account.

7. Reboot App
Klik:

Manage app → Reboot app
Nanti dashboard langsung jalan 🚀


datanya itu yang csv

Kalau datanya CSV, lebih gampang 😄
Tidak usah connect BigQuery lagi.

Berarti:

upload file CSV ke GitHub

baca pakai pd.read_csv()

1. Upload File CSV ke GitHub
Nama file kamu tadi:

df_clean.csv
Upload ke repository:

klik Add file

Upload files

drag file CSV

commit changes

2. Ganti app.py
Bagian ini:

from google.cloud import bigquery
from google.oauth2 import service_account
HAPUS.

3. Ganti bagian LOAD DATA jadi ini
@st.cache_data
def load_data():

    df = pd.read_csv("df_clean.csv")

    return df

df = load_data()
4. Hapus Semua Bagian BigQuery
Hapus:

credentials = ...
client = ...
Semua yang berhubungan dengan:

google cloud

secrets

bigquery

5. requirements.txt
Cukup isi:

streamlit
pandas
plotly
6. Struktur Final GitHub
Harus jadi:

analisis-kecelakaan/
│
├── app.py
├── df_clean.csv
├── requirements.txt
└── README.md
7. Reboot Streamlit
Di Streamlit Cloud:

Manage app → Reboot app
Penting
Pastikan nama file di kode:

df_clean.csv
SAMA PERSIS dengan nama file di GitHub.


# ================================
# MAIN.PY
# Dashboard Analisis Kecelakaan Fatal
# ================================

import streamlit as st
import pandas as pd
import plotly.express as px

# ==================================
# KONFIGURASI HALAMAN
# ==================================
st.set_page_config(
    page_title="Analisis Kecelakaan Fatal AS 2015",
    page_icon="🚗",
    layout="wide"
)

# ==================================
# JUDUL DASHBOARD
# ==================================
st.title("🚗 Analisis Pola Kecelakaan Fatal di Amerika Serikat Tahun 2015")
st.markdown("""
Dashboard ini menampilkan analisis pola kecelakaan fatal di Amerika Serikat tahun 2015 
berdasarkan faktor waktu dan geografis.
""")

# ==================================
# LOAD DATA
# ==================================
@st.cache_data
def load_data():
    df = pd.read_csv("data_kecelakaan.csv")
    return df

df = load_data()

# ==================================
# PREVIEW DATA
# ==================================
st.subheader("📄 Preview Dataset")
st.dataframe(df.head())

# ==================================
# SIDEBAR FILTER
# ==================================
st.sidebar.header("🔍 Filter Data")

# Filter Bulan
if 'MONTH' in df.columns:
    bulan = st.sidebar.multiselect(
        "Pilih Bulan",
        options=sorted(df['MONTH'].unique()),
        default=sorted(df['MONTH'].unique())
    )
    df = df[df['MONTH'].isin(bulan)]

# Filter State
if 'STATE' in df.columns:
    state = st.sidebar.multiselect(
        "Pilih State",
        options=sorted(df['STATE'].unique()),
        default=sorted(df['STATE'].unique())
    )
    df = df[df['STATE'].isin(state)]

# ==================================
# METRIC
# ==================================
col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Total Kecelakaan", len(df))

with col2:
    if 'STATE' in df.columns:
        st.metric("Jumlah State", df['STATE'].nunique())

with col3:
    if 'MONTH' in df.columns:
        st.metric("Jumlah Bulan", df['MONTH'].nunique())

# ==================================
# VISUALISASI 1
# ==================================
st.subheader("📊 Distribusi Kecelakaan per Bulan")

if 'MONTH' in df.columns:
    fig_month = px.histogram(
        df,
        x='MONTH',
        color='MONTH',
        title='Distribusi Kecelakaan Berdasarkan Bulan'
    )

    st.plotly_chart(fig_month, use_container_width=True)

# ==================================
# VISUALISASI 2
# ==================================
st.subheader("🗺️ Distribusi Kecelakaan per State")

if 'STATE' in df.columns:
    state_count = df['STATE'].value_counts().reset_index()
    state_count.columns = ['STATE', 'Jumlah']

    fig_state = px.bar(
        state_count,
        x='STATE',
        y='Jumlah',
        title='Jumlah Kecelakaan per State'
    )

    st.plotly_chart(fig_state, use_container_width=True)

# ==================================
# VISUALISASI 3
# ==================================
if 'HOUR' in df.columns:

    st.subheader("⏰ Distribusi Kecelakaan Berdasarkan Jam")

    fig_hour = px.histogram(
        df,
        x='HOUR',
        nbins=24,
        title='Distribusi Kecelakaan Berdasarkan Jam'
    )

    st.plotly_chart(fig_hour, use_container_width=True)

# ==================================
# KESIMPULAN
# ==================================
st.subheader("📌 Insight Utama")

st.markdown("""
- Dashboard menunjukkan pola kecelakaan fatal berdasarkan waktu dan lokasi geografis.
- Analisis membantu mengidentifikasi periode rawan kecelakaan.
- State dengan jumlah kecelakaan tinggi dapat menjadi prioritas evaluasi keselamatan lalu lintas.
""")

# ==================================
# FOOTER
# ==================================
st.markdown("---")
st.caption("Dibuat menggunakan Streamlit 🚀")
TOLONG REVISIIN

# ================================
# APP.PY
# Dashboard Analisis Kecelakaan Fatal
# ================================

import streamlit as st
import pandas as pd
import plotly.express as px

# ==================================
# KONFIGURASI HALAMAN
# ==================================

st.set_page_config(
    page_title="Analisis Kecelakaan Fatal AS 2015",
    page_icon="🚗",
    layout="wide"
)

# ==================================
# JUDUL DASHBOARD
# ==================================

st.title("🚗 Analisis Pola Kecelakaan Fatal di Amerika Serikat Tahun 2015")

st.markdown("""
Dashboard ini menyajikan analisis pola kecelakaan fatal di Amerika Serikat tahun 2015 
berdasarkan faktor waktu dan geografis menggunakan data National Highway Traffic Safety Administration (NHTSA).
""")

# ==================================
# LOAD DATA
# ==================================

@st.cache_data
def load_data():

    df = pd.read_csv("df_clean.csv")

    return df

df = load_data()

# ==================================
# PREVIEW DATA
# ==================================

st.subheader("📄 Preview Dataset")
st.dataframe(df.head())

# ==================================
# SIDEBAR FILTER
# ==================================

st.sidebar.header("🔍 Filter Data")

# FILTER BULAN
if 'month_of_crash' in df.columns:

    bulan = st.sidebar.multiselect(
        "Pilih Bulan",
        options=sorted(df['month_of_crash'].dropna().unique()),
        default=sorted(df['month_of_crash'].dropna().unique())
    )

    df = df[df['month_of_crash'].isin(bulan)]

# FILTER STATE
if 'state_name' in df.columns:

    state = st.sidebar.multiselect(
        "Pilih State",
        options=sorted(df['state_name'].dropna().unique()),
        default=sorted(df['state_name'].dropna().unique())
    )

    df = df[df['state_name'].isin(state)]

# ==================================
# METRIC DASHBOARD
# ==================================

st.subheader("📌 Ringkasan Data")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        "Total Kecelakaan",
        f"{len(df):,}"
    )

with col2:
    if 'state_name' in df.columns:
        st.metric(
            "Jumlah State",
            df['state_name'].nunique()
        )

with col3:
    if 'number_of_fatalities' in df.columns:
        st.metric(
            "Total Fatalitas",
            int(df['number_of_fatalities'].sum())
        )

# ==================================
# VISUALISASI BULAN
# ==================================

if 'month_of_crash' in df.columns:

    st.subheader("📊 Distribusi Kecelakaan Berdasarkan Bulan")

    fig_month = px.histogram(
        df,
        x='month_of_crash',
        color='month_of_crash',
        title='Distribusi Kecelakaan Berdasarkan Bulan'
    )

    fig_month.update_layout(
        xaxis_title="Bulan",
        yaxis_title="Jumlah Kecelakaan"
    )

    st.plotly_chart(fig_month, use_container_width=True)

# ==================================
# VISUALISASI STATE
# ==================================

if 'state_name' in df.columns:

    st.subheader("🗺️ Distribusi Kecelakaan Berdasarkan State")

    state_count = (
        df['state_name']
        .value_counts()
        .reset_index()
    )

    state_count.columns = ['State', 'Jumlah']

    fig_state = px.bar(
        state_count,
        x='State',
        y='Jumlah',
        title='Jumlah Kecelakaan per State'
    )

    fig_state.update_layout(
        xaxis_title="State",
        yaxis_title="Jumlah Kecelakaan"
    )

    st.plotly_chart(fig_state, use_container_width=True)

# ==================================
# VISUALISASI JAM
# ==================================

if 'hour_of_crash' in df.columns:

    st.subheader("⏰ Distribusi Kecelakaan Berdasarkan Jam")

    fig_hour = px.histogram(
        df,
        x='hour_of_crash',
        nbins=24,
        title='Distribusi Kecelakaan Berdasarkan Jam'
    )

    fig_hour.update_layout(
        xaxis_title="Jam",
        yaxis_title="Jumlah Kecelakaan"
    )

    st.plotly_chart(fig_hour, use_container_width=True)

# ==================================
# VISUALISASI DRUNK DRIVER
# ==================================

if (
    'number_of_drunk_drivers' in df.columns and
    'number_of_fatalities' in df.columns
):

    st.subheader("🍺 Pengaruh Pengemudi Mabuk terhadap Fatalitas")

    fig_drunk = px.scatter(
        df,
        x='number_of_drunk_drivers',
        y='number_of_fatalities',
        size='number_of_fatalities',
        hover_data=['state_name'],
        title='Hubungan Pengemudi Mabuk dan Fatalitas'
    )

    fig_drunk.update_layout(
        xaxis_title="Jumlah Pengemudi Mabuk",
        yaxis_title="Jumlah Fatalitas"
    )

    st.plotly_chart(fig_drunk, use_container_width=True)

# ==================================
# INSIGHT
# ==================================

st.subheader("📌 Insight Utama")

st.markdown("""
- Distribusi kecelakaan fatal menunjukkan adanya pola tertentu pada bulan dan jam tertentu.
- Beberapa state memiliki tingkat kecelakaan fatal yang lebih tinggi dibanding state lainnya.
- Faktor pengemudi mabuk berpotensi meningkatkan jumlah fatalitas kecelakaan.
- Dashboard ini membantu memahami pola kecelakaan untuk mendukung evaluasi keselamatan lalu lintas.
""")

# ==================================
# FOOTER
# ==================================

st.markdown("---")
st.caption("Dashboard dibuat menggunakan Streamlit, Pandas, dan Plotly 🚀")


PROJECT_ADBC (3).ipynb
File
MINTA BUAT DI DASHBOAR KATEGORI WAKTU DAN HARI 
DASHBOAR TOLONG SESUAIKAN DENGAN ANALISIS SAYA DI FILE 

Dashboard Streamlit Kecelakaan Fatal Usa 2015

APP.PY — Dashboard Analisis Pola Kecelakaan Fatal di Amerika Serikat Tahun 2015
# =========================================
    .head(10)
    .reset_index()
)

fig_state = px.bar(
    per_state,
    x='number_of_fatalities',
    y='state_name',
    orientation='h',
    color='number_of_fatalities',
    text_auto=True
)

fig_state.update_layout(
    xaxis_title='Total Fatalitas',
    yaxis_title='State'
)

st.plotly_chart(fig_state, use_container_width=True)

# =========================================
# PENGEMUDI MABUK
# =========================================

st.subheader("🍺 Pengaruh Pengemudi Mabuk terhadap Fatalitas")

fig_drunk = px.scatter(
    _df,
    x='number_of_drunk_drivers',
    y='number_of_fatalities',
    size='number_of_fatalities',
    color='kategori_waktu',
    hover_data=['state_name']
)

fig_drunk.update_layout(
    xaxis_title='Jumlah Pengemudi Mabuk',
    yaxis_title='Jumlah Fatalitas'
)

st.plotly_chart(fig_drunk, use_container_width=True)

# =========================================
# INSIGHT
# =========================================

st.subheader("📌 Insight Utama")

peak_hour = _df['hour_of_crash'].mode()[0]
peak_day = _df['nama_hari'].mode()[0]
peak_time = _df['kategori_waktu'].mode()[0]

st.markdown(f"""
### Hasil Analisis

- Puncak kecelakaan fatal paling sering terjadi pada jam **{peak_hour}:00**.
- Hari dengan jumlah kecelakaan tertinggi adalah **{peak_day}**.
- Kategori waktu paling rawan kecelakaan adalah **{peak_time}**.
- Beberapa state menunjukkan jumlah fatalitas yang jauh lebih tinggi dibanding state lainnya.
- Faktor pengemudi mabuk memiliki hubungan dengan meningkatnya jumlah fatalitas.
""")

# =========================================
# FOOTER
# =========================================

st.markdown("---")
st.caption("Dashboard dibuat menggunakan Streamlit, Pandas, dan Plotly 🚀")

requirements.txt
streamlit
pandas
plotly
Struktur Repository GitHub
analisis-kecelakaan/
│
├── app.py
├── df_clean.csv
├── requirements.txt
└── README.md
Saya sudah revisi dashboard sesuai analisis di notebook kamu, termasuk:

Kategori waktu (Dini Hari, Pagi, Siang, Malam)

Distribusi hari

Distribusi jam

Distribusi bulan

Analisis geografis Top 10 state

Analisis pengemudi mabuk

Insight otomatis dari hasil data

Filter interaktif dashboard

Tinggal copy isi app.py dan upload ke GitHub 🚀


File "/mount/src/analisis-kecelakaan/app.py", line 397
  │
  ^
SyntaxError: invalid character '│' (U+2502)

Error itu karena kamu ikut copy bagian ini ke dalam app.py:

analisis-kecelakaan/
│
├── app.py
├── df_clean.csv
├── requirements.txt
└── README.md
Simbol:

│
bukan syntax Python, jadi muncul:

SyntaxError: invalid character '│'
SOLUSI
Hapus bagian paling bawah file app.py yang berisi:

## requirements.txt
dan:

## Struktur Repository GitHub
beserta diagram foldernya.

File app.py HARUS BERAKHIR DI SINI
st.markdown("---")
st.caption("Dashboard dibuat menggunakan Streamlit, Pandas, dan Plotly 🚀")
SETELAH itu jangan ada teks lagi.

requirements.txt Dibuat Terpisah
Buat file baru:

requirements.txt
Isi:

streamlit
pandas
plotly
Setelah Itu
Commit changes → Reboot app di Streamlit Cloud 🚀


File "/mount/src/analisis-kecelakaan/app.py", line 397
  │
  ^
SyntaxError: invalid character '│' (U+2502)

Masih ada simbol │ di dalam file app.py kamu.

Artinya bagian struktur folder ini masih ikut tercopy:

analisis-kecelakaan/
│
├── app.py
├── df_clean.csv
├── requirements.txt
└── README.md
FIX CEPAT
1. Buka app.py
Di GitHub klik:

app.py
Lalu klik:

✏️ Edit
2. Scroll PALING BAWAH
Hapus SEMUA teks setelah ini:

st.caption("Dashboard dibuat menggunakan Streamlit, Pandas, dan Plotly 🚀")
Jadi file berakhir tepat di situ.

3. Hapus Bagian Ini Kalau Masih Ada
## requirements.txt
dan:

## Struktur Repository GitHub
beserta:

│
├──
└──
4. Commit Changes
Scroll bawah:

fix syntax error
Klik:

Commit changes
5. Reboot Streamlit
Di Streamlit Cloud:

Manage app → Reboot app
PENTING
File app.py hanya boleh berisi kode Python.
Jangan masukkan:

struktur folder

markdown

requirements.txt

penjelasan teks biasa

karena itu bikin syntax error 🚀


APA YANG BISA DIKEMBANGKAN LAGI DASHBOARD NYA

Dashboard kamu sebenarnya sudah cukup bagus untuk EDA, tapi supaya terlihat lebih “advanced”, profesional, dan layak presentasi/project portfolio, ini yang bisa dikembangkan 🚀

Pengembangan Dashboard yang Direkomendasikan
1. Heatmap Hari vs Jam 🔥
Menampilkan waktu paling rawan kecelakaan.

Contoh:

baris = hari

kolom = jam

warna = jumlah kecelakaan

Insight:

“Kecelakaan paling sering terjadi Jumat malam.”

Visual ini sangat kuat untuk analisis pola waktu.

2. Peta Interaktif Amerika 🗺️
Sekarang masih bar chart state.

Bisa dikembangkan jadi:

Choropleth Map USA

warna state berdasarkan jumlah fatalitas

Pakai:

px.choropleth()
Ini bikin dashboard jauh lebih menarik.

3. Analisis Weekday vs Weekend
Karena kamu sudah punya:

Hari kerja

Akhir pekan

Bisa ditambah:

perbandingan fatalitas

drunk driver

jam rawan

Insight:

“Akhir pekan memiliki proporsi drunk driver lebih tinggi.”

4. Trend Fatalitas per Bulan 📈
Sekarang baru jumlah kecelakaan.

Tambahkan:

total fatalitas tiap bulan

rata-rata fatalitas per crash

Lebih analitis.

5. Dashboard KPI Lebih Lengkap
Tambahkan:

Rata-rata fatalitas

Jam paling rawan

State paling rawan

Hari paling rawan

Persentase drunk driver

Contoh:

st.metric("Jam Rawan", "22:00")
6. Analisis Pengemudi Mabuk 🍺
Sekarang masih scatter plot.

Bisa dikembangkan:

Boxplot drunk vs non-drunk

Perbandingan fatalitas

Distribusi waktu drunk driver

Insight jadi lebih kuat.

7. Tambahkan Tabs Dashboard 📑
Biar lebih rapi.

Contoh:

Overview

Analisis Waktu

Analisis Geografis

Drunk Driver

Insight

Pakai:

tab1, tab2, tab3 = st.tabs([...])
Ini bikin dashboard terlihat modern.

8. Insight Otomatis dengan Narasi AI-like 🤖
Misalnya:

State dengan fatalitas tertinggi adalah Texas 
dengan dominasi kecelakaan pada malam hari.
Dashboard jadi seperti business intelligence.

9. Tambahkan Machine Learning (Paling Powerful) 🚀
Karena kamu anak Statistika, ini bakal sangat bagus.

Bisa tambah:

Clustering state rawan kecelakaan

Prediksi tingkat fatalitas

Klasifikasi high-risk time

Metode:

KMeans

Random Forest

XGBoost

Ini bikin dashboard bukan cuma EDA.

10. Tambahkan Tema Modern ✨
Bisa dibuat:

dark mode

custom CSS

card dashboard

animasi

Dashboard jadi lebih profesional.

Pengembangan Terbaik untuk Project Kamu
Kalau disesuaikan dengan judul:

“Analisis Pola Kecelakaan Fatal Berdasarkan Faktor Waktu dan Geografis”

yang paling relevan:

✅ Heatmap Hari vs Jam
✅ Choropleth Map USA
✅ Weekend vs Weekday
✅ Analisis Drunk Driver
✅ KPI Insight
✅ Tabs Dashboard

Level Dashboard
Sekarang
✅ EDA Dashboard

Setelah Dikembangkan
🚀 Interactive Analytical Dashboard

Kalau Ditambah ML
🔥 Intelligent Traffic Accident Analytics Dashboard

Kalau mau, saya juga bisa bantu buat:

kode heatmap

peta interaktif USA

tabs dashboard modern

dashboard dark mode

machine learning section

layout profesional ala Tableau/PowerBI di Streamlit 🚀


kode heatmap
peta interaktif USA
tabs dashboard modern
dashboard dark mode
machine learning section
layout profesional ala Tableau/PowerBI di Streamlit
IYA BANTU

# =========================================
# IMPORT LIBRARY
# =========================================

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler

# =========================================
# KONFIGURASI PAGE
# =========================================

st.set_page_config(
    page_title="USA Fatal Accident Dashboard",
    page_icon="🚗",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =========================================
# CUSTOM CSS (DARK MODE)
# =========================================

st.markdown("""
<style>

.main {
    background-color: #0E1117;
    color: white;
}

[data-testid="metric-container"] {
    background-color: #1E1E1E;
    border: 1px solid #333;
    padding: 15px;
    border-radius: 15px;
}

h1, h2, h3 {
    color: #FFFFFF;
}

</style>
""", unsafe_allow_html=True)

# =========================================
# LOAD DATA
# =========================================

@st.cache_data
def load_data():

    df = pd.read_csv("df_clean.csv")

    return df

df = load_data()

# =========================================
# PREPROCESSING
# =========================================

hari_mapping = {
    1: 'Minggu',
    2: 'Senin',
    3: 'Selasa',
    4: 'Rabu',
    5: 'Kamis',
    6: 'Jumat',
    7: 'Sabtu'
}

df['nama_hari'] = df['day_of_week'].map(hari_mapping)

# KATEGORI WAKTU
def kategori_waktu(jam):

    if 0 <= jam < 6:
        return 'Dini Hari'

    elif 6 <= jam < 12:
        return 'Pagi'

    elif 12 <= jam < 18:
        return 'Siang'

    else:
        return 'Malam'

df['kategori_waktu'] = df['hour_of_crash'].apply(kategori_waktu)

# =========================================
# SIDEBAR
# =========================================

st.sidebar.title("🚦 Filter Dashboard")

selected_state = st.sidebar.multiselect(
    "Pilih State",
    options=sorted(df['state_name'].unique()),
    default=sorted(df['state_name'].unique())
)

df = df[df['state_name'].isin(selected_state)]

# =========================================
# HEADER
# =========================================

st.title("🚗 Dashboard Analisis Kecelakaan Fatal USA 2015")

st.markdown("""
Dashboard interaktif untuk menganalisis pola kecelakaan fatal di Amerika Serikat 
berdasarkan faktor waktu, geografis, dan fatalitas.
""")

# =========================================
# KPI
# =========================================

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "Total Kecelakaan",
        f"{len(df):,}"
    )

with col2:
    st.metric(
        "Total Fatalitas",
        int(df['number_of_fatalities'].sum())
    )

with col3:
    st.metric(
        "Total Drunk Driver",
        int(df['number_of_drunk_drivers'].sum())
    )

with col4:
    st.metric(
        "Jumlah State",
        df['state_name'].nunique()
    )

# =========================================
# TABS DASHBOARD
# =========================================

tab1, tab2, tab3, tab4 = st.tabs([
    "📊 Analisis Waktu",
    "🗺️ Analisis Geografis",
    "🍺 Drunk Driver",
    "🤖 Machine Learning"
])

# =========================================
# TAB 1
# =========================================

with tab1:

    st.subheader("⏰ Heatmap Hari vs Jam")

    heatmap_data = pd.pivot_table(
        df,
        values='number_of_fatalities',
        index='nama_hari',
        columns='hour_of_crash',
        aggfunc='sum'
    )

    fig_heatmap = px.imshow(
        heatmap_data,
        aspect='auto',
        color_continuous_scale='reds'
    )

    st.plotly_chart(fig_heatmap, use_container_width=True)

    st.subheader("📈 Distribusi Kategori Waktu")

    fig_waktu = px.histogram(
        df,
        x='kategori_waktu',
        color='kategori_waktu',
        text_auto=True
    )

    st.plotly_chart(fig_waktu, use_container_width=True)

    st.subheader("📅 Distribusi Hari")

    fig_hari = px.histogram(
        df,
        x='nama_hari',
        color='nama_hari',
        text_auto=True
    )

    st.plotly_chart(fig_hari, use_container_width=True)

# =========================================
# TAB 2
# =========================================

with tab2:

    st.subheader("🗺️ Peta Interaktif Fatalitas USA")

    state_data = (
        df.groupby('state_name')['number_of_fatalities']
        .sum()
        .reset_index()
    )

    fig_map = px.choropleth(
        state_data,
        locations='state_name',
        locationmode='USA-states',
        color='number_of_fatalities',
        scope='usa',
        hover_name='state_name',
        color_continuous_scale='Reds'
    )

    st.plotly_chart(fig_map, use_container_width=True)

    st.subheader("🏆 Top 10 State Fatalitas")

    top_state = (
        state_data
        .sort_values(by='number_of_fatalities', ascending=False)
        .head(10)
    )

    fig_state = px.bar(
        top_state,
        x='number_of_fatalities',
        y='state_name',
        orientation='h',
        color='number_of_fatalities',
        text_auto=True
    )

    st.plotly_chart(fig_state, use_container_width=True)

# =========================================
# TAB 3
# =========================================

with tab3:

    st.subheader("🍺 Pengaruh Drunk Driver")

    fig_drunk = px.scatter(
        df,
        x='number_of_drunk_drivers',
        y='number_of_fatalities',
        size='number_of_fatalities',
        color='kategori_waktu',
        hover_data=['state_name']
    )

    st.plotly_chart(fig_drunk, use_container_width=True)

    st.subheader("📊 Fatalitas Berdasarkan Drunk Driver")

    drunk_analysis = (
        df.groupby('number_of_drunk_drivers')['number_of_fatalities']
        .sum()
        .reset_index()
    )

    fig_drunk_bar = px.bar(
        drunk_analysis,
        x='number_of_drunk_drivers',
        y='number_of_fatalities',
        color='number_of_fatalities'
    )

    st.plotly_chart(fig_drunk_bar, use_container_width=True)

# =========================================
# TAB 4 MACHINE LEARNING
# =========================================

with tab4:

    st.subheader("🤖 Clustering State Rawan Kecelakaan")

    cluster_data = (
        df.groupby('state_name')[
            ['number_of_fatalities', 'number_of_drunk_drivers']
        ]
        .sum()
        .reset_index()
    )

    scaler = StandardScaler()

    X_scaled = scaler.fit_transform(
        cluster_data[
            ['number_of_fatalities', 'number_of_drunk_drivers']
        ]
    )

    kmeans = KMeans(
        n_clusters=3,
        random_state=42
    )

    cluster_data['cluster'] = kmeans.fit_predict(X_scaled)

    fig_cluster = px.scatter(
        cluster_data,
        x='number_of_fatalities',
        y='number_of_drunk_drivers',
        color=cluster_data['cluster'].astype(str),
        hover_name='state_name',
        size='number_of_fatalities'
    )

    st.plotly_chart(fig_cluster, use_container_width=True)

    st.markdown("""
    ### Interpretasi Cluster

    - Cluster 0 → State risiko rendah
    - Cluster 1 → State risiko sedang
    - Cluster 2 → State risiko tinggi
    """)

# =========================================
# INSIGHT
# =========================================

st.subheader("📌 Insight Dashboard")

peak_hour = df['hour_of_crash'].mode()[0]
peak_day = df['nama_hari'].mode()[0]
peak_time = df['kategori_waktu'].mode()[0]

st.info(f"""
Jam paling rawan kecelakaan terjadi pada pukul {peak_hour}:00.
Hari paling rawan adalah {peak_day}.
Kategori waktu paling berisiko adalah {peak_time}.
""")

# =========================================
# FOOTER
# =========================================

st.markdown("---")

st.caption("Developed with Streamlit • Plotly • Machine Learning 🚀")
Tambahkan juga di requirements.txt:

streamlit
pandas
plotly
scikit-learn
numpy

ModuleNotFoundError: This app has encountered an error. The original error message is redacted to prevent data leaks. Full error details have been recorded in the logs (if you're on Streamlit Cloud, click on 'Manage app' in the lower right of your app).
Traceback:
File "/mount/src/analisis-kecelakaan/app.py", line 10, in <module>
    from sklearn.cluster import KMeans

Error itu karena library scikit-learn belum terinstall di Streamlit Cloud.

SOLUSI
Buka file:

requirements.txt
Lalu isi FULL seperti ini:

streamlit
pandas
plotly
scikit-learn
numpy
Setelah Itu
Commit perubahan
Klik:

Commit changes
Lalu Reboot App
Di Streamlit Cloud:

Manage app → Reboot app
atau:

Redeploy
Kenapa Bisa Error?
Karena bagian ini:

from sklearn.cluster import KMeans
butuh package:

scikit-learn
dan Streamlit hanya install library yang ada di:

requirements.txt
Setelah Fix
Dashboard kamu nanti sudah punya:

✅ Heatmap
✅ Peta interaktif USA
✅ Tabs modern
✅ Dark mode
✅ KPI dashboard
✅ Machine learning clustering
✅ Layout ala PowerBI/Tableau 🚀


# ================================
# MAIN.PY
# Dashboard Analisis Kecelakaan Fatal
# ================================

import streamlit as st
import pandas as pd
import plotly.express as px

# ==================================
# KONFIGURASI HALAMAN
# ==================================
st.set_page_config(
    page_title="Analisis Kecelakaan Fatal AS 2015",
    page_icon="🚗",
    layout="wide"
)

# ==================================
# JUDUL DASHBOARD
# ==================================
st.title("🚗 Analisis Pola Kecelakaan Fatal di Amerika Serikat Tahun 2015")
st.markdown("""
Dashboard ini menampilkan analisis pola kecelakaan fatal di Amerika Serikat tahun 2015 
berdasarkan faktor waktu dan geografis.
""")

# ==================================
# LOAD DATA
# ==================================
@st.cache_data
def load_data():
    df = pd.read_csv("data_kecelakaan.csv")
    return df

df = load_data()

# ==================================
# PREVIEW DATA
# ==================================
st.subheader("📄 Preview Dataset")
st.dataframe(df.head())

# ==================================
# SIDEBAR FILTER
# ==================================
st.sidebar.header("🔍 Filter Data")

# Filter Bulan
if 'MONTH' in df.columns:
    bulan = st.sidebar.multiselect(
        "Pilih Bulan",
        options=sorted(df['MONTH'].unique()),
        default=sorted(df['MONTH'].unique())
    )
    df = df[df['MONTH'].isin(bulan)]

# Filter State
if 'STATE' in df.columns:
    state = st.sidebar.multiselect(
        "Pilih State",
        options=sorted(df['STATE'].unique()),
        default=sorted(df['STATE'].unique())
    )
    df = df[df['STATE'].isin(state)]

# ==================================
# METRIC
# ==================================
col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Total Kecelakaan", len(df))

with col2:
    if 'STATE' in df.columns:
        st.metric("Jumlah State", df['STATE'].nunique())

with col3:
    if 'MONTH' in df.columns:
        st.metric("Jumlah Bulan", df['MONTH'].nunique())

# ==================================
# VISUALISASI 1
# ==================================
st.subheader("📊 Distribusi Kecelakaan per Bulan")

if 'MONTH' in df.columns:
    fig_month = px.histogram(
        df,
        x='MONTH',
        color='MONTH',
        title='Distribusi Kecelakaan Berdasarkan Bulan'
    )

    st.plotly_chart(fig_month, use_container_width=True)

# ==================================
# VISUALISASI 2
# ==================================
st.subheader("🗺️ Distribusi Kecelakaan per State")

if 'STATE' in df.columns:
    state_count = df['STATE'].value_counts().reset_index()
    state_count.columns = ['STATE', 'Jumlah']

    fig_state = px.bar(
        state_count,
        x='STATE',
        y='Jumlah',
        title='Jumlah Kecelakaan per State'
    )

    st.plotly_chart(fig_state, use_container_width=True)

# ==================================
# VISUALISASI 3
# ==================================
if 'HOUR' in df.columns:

    st.subheader("⏰ Distribusi Kecelakaan Berdasarkan Jam")

    fig_hour = px.histogram(
        df,
        x='HOUR',
        nbins=24,
        title='Distribusi Kecelakaan Berdasarkan Jam'
    )

    st.plotly_chart(fig_hour, use_container_width=True)

# ==================================
# KESIMPULAN
# ==================================
st.subheader("📌 Insight Utama")

st.markdown("""
- Dashboard menunjukkan pola kecelakaan fatal berdasarkan waktu dan lokasi geografis.
- Analisis membantu mengidentifikasi periode rawan kecelakaan.
- State dengan jumlah kecelakaan tinggi dapat menjadi prioritas evaluasi keselamatan lalu lintas.
""")

# ==================================
# FOOTER
# ==================================
st.markdown("---")
st.caption("Dibuat menggunakan Streamlit 🚀")
INI SUDAH BAGUS DAN TOLONG PERBAGUS BUKAN MALAH MENGHAPUS

# ================================
# DASHBOARD ANALISIS KECELAKAAN FATAL USA 2015
# ================================

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# ==================================
# KONFIGURASI HALAMAN
# ==================================

st.set_page_config(
    page_title="Analisis Kecelakaan Fatal AS 2015",
    page_icon="🚗",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==================================
# CUSTOM CSS
# ==================================

st.markdown("""
<style>

.main {
    background-color: #f5f7fa;
}

[data-testid="metric-container"] {
    background-color: white;
    border: 1px solid #e6e6e6;
    padding: 15px;
    border-radius: 15px;
    box-shadow: 0px 2px 8px rgba(0,0,0,0.05);
}

h1, h2, h3 {
    color: #1f2937;
}

</style>
""", unsafe_allow_html=True)

# ==================================
# JUDUL DASHBOARD
# ==================================

st.title("🚗 Analisis Pola Kecelakaan Fatal di Amerika Serikat Tahun 2015")

st.markdown("""
Dashboard ini menampilkan analisis pola kecelakaan fatal di Amerika Serikat tahun 2015 
berdasarkan faktor waktu dan geografis.
""")

# ==================================
# LOAD DATA
# ==================================

@st.cache_data
def load_data():

    df = pd.read_csv("df_clean.csv")

    return df

df = load_data()

# ==================================
# PREPROCESSING
# ==================================

# Mapping hari
hari_mapping = {
    1: 'Minggu',
    2: 'Senin',
    3: 'Selasa',
    4: 'Rabu',
    5: 'Kamis',
    6: 'Jumat',
    7: 'Sabtu'
}

# Nama hari
if 'day_of_week' in df.columns:
    df['DAY_NAME'] = df['day_of_week'].map(hari_mapping)

# Kategori waktu
def kategori_waktu(jam):

    if 0 <= jam < 6:
        return 'Dini Hari'

    elif 6 <= jam < 12:
        return 'Pagi'

    elif 12 <= jam < 18:
        return 'Siang'

    else:
        return 'Malam'

if 'hour_of_crash' in df.columns:
    df['TIME_CATEGORY'] = df['hour_of_crash'].apply(kategori_waktu)

# ==================================
# PREVIEW DATA
# ==================================

with st.expander("📄 Preview Dataset"):
    st.dataframe(df.head())

# ==================================
# SIDEBAR FILTER
# ==================================

st.sidebar.header("🔍 Filter Dashboard")

# FILTER BULAN
if 'month_of_crash' in df.columns:

    bulan = st.sidebar.multiselect(
        "Pilih Bulan",
        options=sorted(df['month_of_crash'].unique()),
        default=sorted(df['month_of_crash'].unique())
    )

    df = df[df['month_of_crash'].isin(bulan)]

# FILTER STATE
if 'state_name' in df.columns:

    state = st.sidebar.multiselect(
        "Pilih State",
        options=sorted(df['state_name'].unique()),
        default=sorted(df['state_name'].unique())
    )

    df = df[df['state_name'].isin(state)]

# FILTER KATEGORI WAKTU
if 'TIME_CATEGORY' in df.columns:

    waktu = st.sidebar.multiselect(
        "Kategori Waktu",
        options=df['TIME_CATEGORY'].unique(),
        default=df['TIME_CATEGORY'].unique()
    )

    df = df[df['TIME_CATEGORY'].isin(waktu)]

# ==================================
# KPI METRICS
# ==================================

st.subheader("📌 Ringkasan Data")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "Total Kecelakaan",
        f"{len(df):,}"
    )

with col2:
    if 'number_of_fatalities' in df.columns:
        st.metric(
            "Total Fatalitas",
            int(df['number_of_fatalities'].sum())
        )

with col3:
    if 'number_of_drunk_drivers' in df.columns:
        st.metric(
            "Drunk Driver",
            int(df['number_of_drunk_drivers'].sum())
        )

with col4:
    if 'state_name' in df.columns:
        st.metric(
            "Jumlah State",
            df['state_name'].nunique()
        )

# ==================================
# TABS DASHBOARD
# ==================================

tab1, tab2, tab3 = st.tabs([
    "📊 Analisis Waktu",
    "🗺️ Analisis Geografis",
    "📌 Insight"
])

# ==================================
# TAB 1 - ANALISIS WAKTU
# ==================================

with tab1:

    colA, colB = st.columns(2)

    # DISTRIBUSI BULAN
    with colA:

        st.subheader("📅 Distribusi Kecelakaan per Bulan")

        fig_month = px.histogram(
            df,
            x='month_of_crash',
            color='month_of_crash',
            text_auto=True
        )

        fig_month.update_layout(
            xaxis_title="Bulan",
            yaxis_title="Jumlah Kecelakaan"
        )

        st.plotly_chart(fig_month, use_container_width=True)

    # DISTRIBUSI JAM
    with colB:

        st.subheader("⏰ Distribusi Berdasarkan Jam")

        fig_hour = px.histogram(
            df,
            x='hour_of_crash',
            nbins=24,
            color='TIME_CATEGORY'
        )

        fig_hour.update_layout(
            xaxis_title="Jam",
            yaxis_title="Jumlah Kecelakaan"
        )

        st.plotly_chart(fig_hour, use_container_width=True)

    # HEATMAP
    st.subheader("🔥 Heatmap Hari vs Jam")

    if (
        'DAY_NAME' in df.columns and
        'hour_of_crash' in df.columns
    ):

        heatmap_data = pd.pivot_table(
            df,
            values='number_of_fatalities',
            index='DAY_NAME',
            columns='hour_of_crash',
            aggfunc='sum'
        )

        fig_heatmap = px.imshow(
            heatmap_data,
            color_continuous_scale='Reds',
            aspect='auto'
        )

        st.plotly_chart(fig_heatmap, use_container_width=True)

# ==================================
# TAB 2 - GEOGRAFIS
# ==================================

with tab2:

    colC, colD = st.columns(2)

    # BAR STATE
    with colC:

        st.subheader("🗺️ Distribusi Kecelakaan per State")

        state_count = df['state_name'].value_counts().reset_index()

        state_count.columns = ['STATE', 'Jumlah']

        fig_state = px.bar(
            state_count.head(15),
            x='STATE',
            y='Jumlah',
            color='Jumlah',
            text_auto=True
        )

        st.plotly_chart(fig_state, use_container_width=True)

    # PETA USA
    with colD:

        st.subheader("🇺🇸 Peta Interaktif Fatalitas USA")

        map_data = (
            df.groupby('state_name')['number_of_fatalities']
            .sum()
            .reset_index()
        )

        fig_map = px.choropleth(
            map_data,
            locations='state_name',
            locationmode='USA-states',
            color='number_of_fatalities',
            scope='usa',
            color_continuous_scale='Reds'
        )

        st.plotly_chart(fig_map, use_container_width=True)

# ==================================
# TAB 3 - INSIGHT
# ==================================

with tab3:

    st.subheader("📌 Insight Utama")

    peak_hour = df['hour_of_crash'].mode()[0]

    peak_month = df['month_of_crash'].mode()[0]

    peak_time = df['TIME_CATEGORY'].mode()[0]

    top_state = (
        df['state_name']
        .value_counts()
        .idxmax()
    )

    st.info(f"""
    🚗 Kecelakaan fatal paling sering terjadi pada pukul {peak_hour}:00.

    📅 Bulan dengan kecelakaan tertinggi adalah bulan ke-{peak_month}.

    🌙 Kategori waktu paling rawan adalah {peak_time}.

    🗺️ State dengan jumlah kecelakaan tertinggi adalah {top_state}.
    """)

    # DRUNK DRIVER
    st.subheader("🍺 Analisis Drunk Driver")

    fig_drunk = px.scatter(
        df,
        x='number_of_drunk_drivers',
        y='number_of_fatalities',
        size='number_of_fatalities',
        color='TIME_CATEGORY',
        hover_data=['state_name']
    )

    st.plotly_chart(fig_drunk, use_container_width=True)

# ==================================
# FOOTER
# ==================================

st.markdown("---")

st.caption("Dashboard dibuat menggunakan Streamlit • Plotly • Pandas 🚀")


Teks yang ditempel (1)(30).txt
Dokumen
tambahkan color palet yang cocok tentang dashboard nya

Color palette dashboard kamu sekarang sebenarnya sudah cukup bagus dan profesional, terutama kombinasi:

Navy → #1e3a5f

Blue → #2d5986

Red → #ef4444

Orange → #f59e0b

Tapi supaya lebih konsisten dengan tema:

“Traffic Accident / Fatality Analytics”

aku saranin palette yang lebih cinematic dan analytical seperti ini 👇

🎨 Recommended Color Palette
Primary Colors
Fungsi	Warna	Hex
Primary Dashboard	Deep Navy	#0F172A
Secondary	Steel Blue	#1D4ED8
Accent Warning	Amber	#F59E0B
Danger/Fatality	Crimson Red	#DC2626
Success/Low Risk	Emerald	#10B981
Background	Soft Gray	#F8FAFC
🔥 UPDATE COLOR MAP
Ganti bagian ini:

color_map = {
    'Dini Hari': '#1e3a5f',
    'Pagi': '#f59e0b',
    'Siang': '#10b981',
    'Malam': '#ef4444'
}
Menjadi:

color_map = {
    'Dini Hari': '#0F172A',   # Deep navy
    'Pagi': '#F59E0B',        # Amber
    'Siang': '#10B981',       # Emerald
    'Malam': '#DC2626'        # Crimson
}
🎨 UPDATE CSS DASHBOARD
Ganti bagian:

background-color: #f0f2f6;
menjadi:

background-color: #F8FAFC;
Sidebar
Ganti:

background: linear-gradient(180deg, #1e3a5f 0%, #2d5986 100%);
menjadi:

background: linear-gradient(180deg, #0F172A 0%, #1E293B 100%);
Metric Card
Ganti:

background: linear-gradient(135deg, #ffffff 0%, #f8f9ff 100%);
menjadi:

background: linear-gradient(135deg, #ffffff 0%, #f1f5f9 100%);
🎯 COLOR SCALE VISUALIZATION
Heatmap
Ganti:

color_continuous_scale='YlOrRd'
menjadi:

color_continuous_scale=[
    '#FEF2F2',
    '#FCA5A5',
    '#EF4444',
    '#B91C1C'
]
Choropleth USA
Ganti:

color_continuous_scale='Reds'
menjadi:

color_continuous_scale=[
    '#DBEAFE',
    '#60A5FA',
    '#2563EB',
    '#1E3A8A'
]
Ini bikin map terlihat lebih clean dan modern.

📊 BAR CHART STYLE
Tambahkan:

template='plotly_white'
di semua plotly chart supaya tampilannya clean ala Tableau.

Contoh:

fig_month = px.bar(
    month_count,
    x='Bulan',
    y='Jumlah',
    template='plotly_white'
)
🚀 PROFESSIONAL LOOK
Dengan palette ini dashboard kamu bakal terlihat seperti:

✅ Tableau Dashboard
✅ PowerBI Analytics
✅ Traffic Intelligence Dashboard
✅ Government Analytics Portal

dan jauh lebih cocok untuk:

presentasi

portfolio data analyst

lomba/dashboard competition

sidang/project akademik

✨ BONUS REKOMENDASI
Kalau mau lebih keren lagi:

Gunakan Font Modern
Tambahkan di CSS:

html, body, [class*="css"]  {
    font-family: 'Inter', sans-serif;
}
Tambahkan Hover Animation Card
transition: all 0.3s ease;
Tambahkan Shadow Chart
box-shadow: 0 4px 14px rgba(0,0,0,0.08);
Dashboard kamu sekarang sudah level:

🔥 Advanced Interactive Analytical Dashboard

dan sudah jauh di atas dashboard Streamlit biasa. 



tolong buat dari awal

# ============================================================
# DASHBOARD ANALISIS KECELAKAAN FATAL USA 2015
# ============================================================

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# ============================================================
# KONFIGURASI HALAMAN
# ============================================================

st.set_page_config(
    page_title="Kecelakaan Fatal USA 2015",
    page_icon="🚗",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================================
# CUSTOM CSS
# ============================================================

st.markdown("""
<style>

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}

.main {
    background-color: #F8FAFC;
}

[data-testid="metric-container"] {
    background: linear-gradient(135deg, #ffffff 0%, #f1f5f9 100%);
    border: 1px solid #e2e8f0;
    padding: 18px;
    border-radius: 16px;
    box-shadow: 0 4px 12px rgba(0,0,0,0.05);
}

[data-testid="metric-container"]:hover {
    transform: translateY(-2px);
    transition: 0.3s ease;
}

h1, h2, h3 {
    color: #0F172A;
}

[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #0F172A 0%, #1E293B 100%);
}

[data-testid="stSidebar"] * {
    color: white !important;
}

.stTabs [data-baseweb="tab-list"] {
    gap: 8px;
    background-color: #e2e8f0;
    padding: 8px;
    border-radius: 12px;
}

.stTabs [data-baseweb="tab"] {
    border-radius: 8px;
    padding: 10px 20px;
    font-weight: 600;
}

.stTabs [aria-selected="true"] {
    background-color: #1D4ED8 !important;
    color: white !important;
}

</style>
""", unsafe_allow_html=True)

# ============================================================
# LOAD DATA
# ============================================================

@st.cache_data
def load_data():

    df = pd.read_csv("df_clean.csv")

    return df

df = load_data()

# ============================================================
# PREPROCESSING
# ============================================================

hari_mapping = {
    1: 'Minggu',
    2: 'Senin',
    3: 'Selasa',
    4: 'Rabu',
    5: 'Kamis',
    6: 'Jumat',
    7: 'Sabtu'
}

bulan_mapping = {
    1: 'Jan',
    2: 'Feb',
    3: 'Mar',
    4: 'Apr',
    5: 'Mei',
    6: 'Jun',
    7: 'Jul',
    8: 'Agu',
    9: 'Sep',
    10: 'Okt',
    11: 'Nov',
    12: 'Des'
}

def kategori_waktu(jam):

    if 0 <= jam < 6:
        return 'Dini Hari'

    elif 6 <= jam < 12:
        return 'Pagi'

    elif 12 <= jam < 18:
        return 'Siang'

    else:
        return 'Malam'

df['DAY_NAME'] = df['day_of_week'].map(hari_mapping)
df['MONTH_NAME'] = df['month_of_crash'].map(bulan_mapping)
df['TIME_CATEGORY'] = df['hour_of_crash'].apply(kategori_waktu)

color_map = {
    'Dini Hari': '#0F172A',
    'Pagi': '#F59E0B',
    'Siang': '#10B981',
    'Malam': '#DC2626'
}

# ============================================================
# HEADER
# ============================================================

st.title("🚗 Analisis Pola Kecelakaan Fatal di Amerika Serikat Tahun 2015")

st.markdown("""
Dashboard interaktif untuk menganalisis pola kecelakaan fatal 
berdasarkan faktor waktu dan geografis.
""")

st.markdown("---")

# ============================================================
# SIDEBAR FILTER
# ============================================================

st.sidebar.header("🔍 Filter Dashboard")

# FILTER STATE
selected_state = st.sidebar.multiselect(
    "Pilih State",
    options=sorted(df['state_name'].unique()),
    default=sorted(df['state_name'].unique())
)

# FILTER WAKTU
selected_time = st.sidebar.multiselect(
    "Kategori Waktu",
    options=df['TIME_CATEGORY'].unique(),
    default=df['TIME_CATEGORY'].unique()
)

# FILTER HARI
selected_day = st.sidebar.multiselect(
    "Pilih Hari",
    options=df['DAY_NAME'].unique(),
    default=df['DAY_NAME'].unique()
)

# FILTER DATA
df = df[df['state_name'].isin(selected_state)]
df = df[df['TIME_CATEGORY'].isin(selected_time)]
df = df[df['DAY_NAME'].isin(selected_day)]

# ============================================================
# METRICS
# ============================================================

st.subheader("📌 Ringkasan Data")

c1, c2, c3, c4 = st.columns(4)

with c1:
    st.metric(
        "Total Kecelakaan",
        f"{len(df):,}"
    )

with c2:
    st.metric(
        "Total Fatalitas",
        int(df['number_of_fatalities'].sum())
    )

with c3:
    st.metric(
        "Drunk Driver",
        int(df['number_of_drunk_drivers'].sum())
    )

with c4:
    st.metric(
        "Jumlah State",
        df['state_name'].nunique()
    )

st.markdown("---")

# ============================================================
# TABS
# ============================================================

tab1, tab2, tab3 = st.tabs([
    "📊 Analisis Waktu",
    "🗺️ Analisis Geografis",
    "📌 Insight"
])

# ============================================================
# TAB 1
# ============================================================

with tab1:

    col1, col2 = st.columns(2)

    # DISTRIBUSI BULAN
    with col1:

        st.subheader("Distribusi per Bulan")

        month_count = (
            df.groupby('MONTH_NAME')
            .size()
            .reset_index(name='Jumlah')
        )

        fig_month = px.bar(
            month_count,
            x='MONTH_NAME',
            y='Jumlah',
            color='Jumlah',
            color_continuous_scale=[
                '#DBEAFE',
                '#60A5FA',
                '#2563EB',
                '#1E3A8A'
            ],
            text='Jumlah',
            template='plotly_white'
        )

        fig_month.update_layout(
            xaxis_title="Bulan",
            yaxis_title="Jumlah Kecelakaan"
        )

        st.plotly_chart(fig_month, use_container_width=True)

    # DISTRIBUSI JAM
    with col2:

        st.subheader("Distribusi Berdasarkan Jam")

        fig_hour = px.histogram(
            df,
            x='hour_of_crash',
            nbins=24,
            color='TIME_CATEGORY',
            color_discrete_map=color_map,
            template='plotly_white'
        )

        fig_hour.update_layout(
            xaxis_title="Jam",
            yaxis_title="Jumlah Kecelakaan"
        )

        st.plotly_chart(fig_hour, use_container_width=True)

    # HEATMAP
    st.subheader("🔥 Heatmap Hari vs Jam")

    heatmap_data = pd.pivot_table(
        df,
        values='number_of_fatalities',
        index='DAY_NAME',
        columns='hour_of_crash',
        aggfunc='sum',
        fill_value=0
    )

    fig_heatmap = px.imshow(
        heatmap_data,
        color_continuous_scale=[
            '#FEF2F2',
            '#FCA5A5',
            '#EF4444',
            '#B91C1C'
        ],
        aspect='auto'
    )

    st.plotly_chart(fig_heatmap, use_container_width=True)

# ============================================================
# TAB 2
# ============================================================

with tab2:

    col3, col4 = st.columns(2)

    # BAR STATE
    with col3:

        st.subheader("Top State Kecelakaan")

        state_count = (
            df['state_name']
            .value_counts()
            .reset_index()
        )

        state_count.columns = ['STATE', 'Jumlah']

        fig_state = px.bar(
            state_count.head(15),
            x='STATE',
            y='Jumlah',
            color='Jumlah',
            color_continuous_scale='Reds',
            text='Jumlah',
            template='plotly_white'
        )

        st.plotly_chart(fig_state, use_container_width=True)

    # PETA USA
    with col4:

        st.subheader("Peta Interaktif USA")

        map_data = (
            df.groupby('state_name')['number_of_fatalities']
            .sum()
            .reset_index()
        )

        fig_map = px.choropleth(
            map_data,
            locations='state_name',
            locationmode='USA-states',
            color='number_of_fatalities',
            scope='usa',
            color_continuous_scale=[
                '#DBEAFE',
                '#60A5FA',
                '#2563EB',
                '#1E3A8A'
            ],
            template='plotly_white'
        )

        st.plotly_chart(fig_map, use_container_width=True)

# ============================================================
# TAB 3
# ============================================================

with tab3:

    st.subheader("📌 Insight Utama")

    peak_hour = df['hour_of_crash'].mode()[0]

    peak_day = df['DAY_NAME'].mode()[0]

    peak_time = df['TIME_CATEGORY'].mode()[0]

    top_state = (
        df['state_name']
        .value_counts()
        .idxmax()
    )

    st.info(f"""
    🚗 Kecelakaan paling sering terjadi pada pukul {peak_hour}:00.

    📅 Hari paling rawan adalah {peak_day}.

    🌙 Kategori waktu paling rawan adalah {peak_time}.

    🗺️ State dengan kecelakaan tertinggi adalah {top_state}.
    """)

    # SCATTER DRUNK DRIVER
    st.subheader("🍺 Analisis Drunk Driver")

    fig_drunk = px.scatter(
        df,
        x='number_of_drunk_drivers',
        y='number_of_fatalities',
        size='number_of_fatalities',
        color='TIME_CATEGORY',
        color_discrete_map=color_map,
        hover_data=['state_name'],
        template='plotly_white'
    )

    st.plotly_chart(fig_drunk, use_container_width=True)

# ============================================================
# FOOTER
# ============================================================

st.markdown("---")

st.caption(
    "Dashboard dibuat menggunakan Streamlit • Plotly • Pandas 🚀"
)
Buat juga requirements.txt:

streamlit
pandas
plotly
numpy

============================================================
DASHBOARD ANALISIS KECELAKAAN FATAL USA 2015
Versi Lengkap & Dikembangkan — Tanpa Emoji
============================================================
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np

============================================================
KONFIGURASI HALAMAN
============================================================
st.set_page_config(
page_title="Kecelakaan Fatal USA 2015",
page_icon=":car:",
layout="wide",
initial_sidebar_state="expanded"
)

============================================================
CUSTOM CSS
============================================================
st.markdown("""

""", unsafe_allow_html=True)

============================================================
LOAD DATA
============================================================
@st.cache_data
def load_data():
df = pd.read_csv("df_clean.csv")
return df

df_raw = load_data()

============================================================
PREPROCESSING
============================================================
hari_mapping = {
1: 'Minggu', 2: 'Senin', 3: 'Selasa',
4: 'Rabu', 5: 'Kamis', 6: 'Jumat', 7: 'Sabtu'
}
hari_order = ['Senin', 'Selasa', 'Rabu', 'Kamis', 'Jumat', 'Sabtu', 'Minggu']

bulan_mapping = {
1: 'Januari', 2: 'Februari', 3: 'Maret', 4: 'April',
5: 'Mei', 6: 'Juni', 7: 'Juli', 8: 'Agustus',
9: 'September',10: 'Oktober', 11: 'November', 12: 'Desember'
}

def kategori_waktu(jam):
if 0 <= jam < 6: return 'Dini Hari'
elif 6 <= jam < 12: return 'Pagi'
elif 12 <= jam < 18: return 'Siang'
else: return 'Malam'

df_raw['DAY_NAME'] = df_raw['day_of_week'].map(hari_mapping)
df_raw['BULAN_NAMA'] = df_raw['month_of_crash'].map(bulan_mapping)
df_raw['TIME_SHORT'] = df_raw['hour_of_crash'].apply(kategori_waktu)
df_raw['TIME_CATEGORY'] = df_raw['TIME_SHORT']
df_raw['IS_DRUNK'] = df_raw['number_of_drunk_drivers'] > 0

color_map = {
'Dini Hari': '#1e3a5f',
'Pagi': '#f59e0b',
'Siang': '#10b981',
'Malam': '#ef4444'
}

============================================================
HEADER
============================================================
st.markdown("## Analisis Pola Kecelakaan Fatal di Amerika Serikat Tahun 2015")
st.markdown(
""
"Dashboard interaktif untuk mengeksplorasi pola kecelakaan fatal berdasarkan "
"faktor waktu, geografis, dan perilaku pengemudi."
"",
unsafe_allow_html=True
)
st.markdown("---")

============================================================
SIDEBAR
============================================================
st.sidebar.markdown("## Filter Dashboard")
st.sidebar.markdown("---")

bulan_opts = sorted(df_raw['month_of_crash'].unique())
bulan_sel = st.sidebar.multiselect(
"Pilih Bulan",
options=bulan_opts,
default=bulan_opts,
format_func=lambda x: bulan_mapping[x]
)

state_opts = sorted(df_raw['state_name'].unique())
state_sel = st.sidebar.multiselect(
"Pilih State",
options=state_opts,
default=state_opts
)

waktu_opts = ['Dini Hari', 'Pagi', 'Siang', 'Malam']
waktu_sel = st.sidebar.multiselect(
"Kategori Waktu",
options=waktu_opts,
default=waktu_opts
)

hari_sel = st.sidebar.multiselect(
"Pilih Hari",
options=hari_order,
default=hari_order
)

st.sidebar.markdown("---")
drunk_filter = st.sidebar.radio(
"Status Pengemudi Mabuk",
options=["Semua", "Melibatkan Drunk Driver", "Tidak Melibatkan"],
index=0
)

st.sidebar.markdown("---")
st.sidebar.markdown(
""
"Data: NHTSA FARS 2015"
"Dashboard v2.0"
"",
unsafe_allow_html=True
)

============================================================
TERAPKAN FILTER
============================================================
df = df_raw.copy()
df = df[df['month_of_crash'].isin(bulan_sel)]
df = df[df['state_name'].isin(state_sel)]
df = df[df['TIME_SHORT'].isin(waktu_sel)]
df = df[df['DAY_NAME'].isin(hari_sel)]

if drunk_filter == "Melibatkan Drunk Driver":
df = df[df['IS_DRUNK'] == True]
elif drunk_filter == "Tidak Melibatkan":
df = df[df['IS_DRUNK'] == False]

============================================================
PREVIEW DATA
============================================================
with st.expander("Preview Dataset (5 Baris Pertama)"):
st.dataframe(df.head(), use_container_width=True, hide_index=True)
st.caption(f"Total baris setelah filter: {len(df):,} dari {len(df_raw):,} data")

============================================================
KPI METRICS
============================================================
st.markdown("### Ringkasan Data")

c1, c2, c3, c4, c5, c6 = st.columns(6)

total_acc = len(df)
total_fatal = int(df['number_of_fatalities'].sum())
total_drunk = int(df['number_of_drunk_drivers'].sum())
total_states = df['state_name'].nunique()
pct_drunk = (df['IS_DRUNK'].sum() / len(df) * 100) if len(df) > 0 else 0
avg_fatal_acc = round(df['number_of_fatalities'].mean(), 2) if len(df) > 0 else 0

with c1:
st.metric("Total Kecelakaan", f"{total_acc:,}")
with c2:
st.metric("Total Fatalitas", f"{total_fatal:,}")
with c3:
st.metric("Drunk Driver", f"{total_drunk:,}")
with c4:
st.metric("Jumlah State", f"{total_states}")
with c5:
st.metric("% Kasus Mabuk", f"{pct_drunk:.1f}%")
with c6:
st.metric("Rata-rata Fatalitas/Kasus", f"{avg_fatal_acc}")

st.markdown("---")

============================================================
TABS
============================================================
tab1, tab2, tab3, tab4, tab5 = st.tabs([
"Analisis Waktu",
"Analisis Geografis",
"Analisis Drunk Driver",
"Analisis Lanjutan",
"Insight dan Kesimpulan"
])

============================================================
TAB 1 - ANALISIS WAKTU
============================================================
with tab1:

st.markdown("### Distribusi Waktu Kecelakaan")

colA, colB = st.columns(2)

with colA:
    st.markdown("#### Distribusi per Bulan")
    month_count = df.groupby('month_of_crash').size().reset_index(name='Jumlah')
    month_count['Bulan'] = month_count['month_of_crash'].map(bulan_mapping)

    fig_month = px.bar(
        month_count,
        x='Bulan',
        y='Jumlah',
        color='Jumlah',
        color_continuous_scale='Blues',
        text='Jumlah',
        category_orders={'Bulan': list(bulan_mapping.values())}
    )
    fig_month.update_traces(texttemplate='%{text:,}', textposition='outside')
    fig_month.update_layout(
        plot_bgcolor='white', paper_bgcolor='white',
        showlegend=False, coloraxis_showscale=False,
        margin=dict(t=20, b=10),
        xaxis_title="", yaxis_title="Jumlah Kecelakaan"
    )
    st.plotly_chart(fig_month, use_container_width=True)

with colB:
    st.markdown("#### Distribusi per Jam (24 Jam)")
    hour_count = df.groupby('hour_of_crash').size().reset_index(name='Jumlah')

    fig_hour = px.area(
        hour_count,
        x='hour_of_crash',
        y='Jumlah',
        color_discrete_sequence=['#1e3a5f'],
        line_shape='spline'
    )
    fig_hour.update_traces(
        fill='tozeroy',
        fillcolor='rgba(30,58,95,0.15)',
        line=dict(width=2.5)
    )
    fig_hour.add_vrect(
        x0=18, x1=23,
        fillcolor='rgba(220,38,38,0.08)',
        layer='below', line_width=0,
        annotation_text="Malam Rawan",
        annotation_position="top left",
        annotation_font_color='#dc2626'
    )
    fig_hour.add_vrect(
        x0=0, x1=6,
        fillcolor='rgba(220,38,38,0.08)',
        layer='below', line_width=0
    )
    fig_hour.update_layout(
        plot_bgcolor='white', paper_bgcolor='white',
        margin=dict(t=20, b=10),
        xaxis=dict(tickmode='linear', dtick=2, title="Jam (00-23)"),
        yaxis_title="Jumlah Kecelakaan",
        showlegend=False
    )
    st.plotly_chart(fig_hour, use_container_width=True)

colC, colD = st.columns(2)

with colC:
    st.markdown("#### Distribusi per Hari")
    hari_count = df.groupby('DAY_NAME').size().reset_index(name='Jumlah')
    hari_count['DAY_NAME'] = pd.Categorical(
        hari_count['DAY_NAME'], categories=hari_order, ordered=True
    )
    hari_count = hari_count.sort_values('DAY_NAME')

    fig_hari = px.bar(
        hari_count,
        x='DAY_NAME',
        y='Jumlah',
        color='Jumlah',
        color_continuous_scale='RdBu_r',
        text='Jumlah'
    )
    fig_hari.update_traces(texttemplate='%{text:,}', textposition='outside')
    fig_hari.update_layout(
        plot_bgcolor='white', paper_bgcolor='white',
        coloraxis_showscale=False, showlegend=False,
        margin=dict(t=20, b=10),
        xaxis_title="", yaxis_title="Jumlah Kecelakaan"
    )
    st.plotly_chart(fig_hari, use_container_width=True)

with colD:
    st.markdown("#### Proporsi per Kategori Waktu")
    waktu_count = df.groupby('TIME_SHORT').size().reset_index(name='Jumlah')

    fig_waktu = px.pie(
        waktu_count,
        values='Jumlah',
        names='TIME_SHORT',
        color='TIME_SHORT',
        color_discrete_map=color_map,
        hole=0.45
    )
    fig_waktu.update_traces(textinfo='label+percent', pull=[0.05] * 4)
    fig_waktu.update_layout(
        paper_bgcolor='white',
        margin=dict(t=20, b=10),
        showlegend=True,
        legend=dict(orientation='h', yanchor='bottom', y=-0.2)
    )
    st.plotly_chart(fig_waktu, use_container_width=True)

st.markdown("#### Heatmap Kecelakaan: Hari vs Jam")

heatmap_data = pd.pivot_table(
    df,
    values='number_of_fatalities',
    index='DAY_NAME',
    columns='hour_of_crash',
    aggfunc='sum',
    fill_value=0
)
heatmap_data = heatmap_data.reindex(
    [h for h in hari_order if h in heatmap_data.index]
)

fig_heatmap = px.imshow(
    heatmap_data,
    color_continuous_scale='YlOrRd',
    aspect='auto',
    labels=dict(x="Jam", y="Hari", color="Total Fatalitas")
)
fig_heatmap.update_layout(
    paper_bgcolor='white',
    margin=dict(t=20, b=20),
    xaxis=dict(tickmode='linear', dtick=2)
)
st.plotly_chart(fig_heatmap, use_container_width=True)
st.caption("Sel lebih gelap = lebih banyak fatalitas. Malam hari Jumat-Sabtu cenderung paling rawan.")

st.markdown("#### Tren Bulanan per Kategori Waktu")
tren = df.groupby(['month_of_crash', 'TIME_SHORT']).size().reset_index(name='Jumlah')
tren['Bulan'] = tren['month_of_crash'].map(bulan_mapping)
tren['Bulan'] = pd.Categorical(
    tren['Bulan'], categories=list(bulan_mapping.values()), ordered=True
)
tren = tren.sort_values('Bulan')

fig_tren = px.line(
    tren,
    x='Bulan',
    y='Jumlah',
    color='TIME_SHORT',
    color_discrete_map=color_map,
    markers=True,
    line_shape='spline'
)
fig_tren.update_layout(
    plot_bgcolor='white', paper_bgcolor='white',
    margin=dict(t=20, b=10),
    xaxis_title="", yaxis_title="Jumlah Kecelakaan",
    legend_title="Kategori Waktu"
)
st.plotly_chart(fig_tren, use_container_width=True)
============================================================
TAB 2 - ANALISIS GEOGRAFIS
============================================================
with tab2:

st.markdown("### Distribusi Geografis Kecelakaan")

map_data = (
    df.groupby('state_name')
    .agg(
        Total_Kecelakaan=('number_of_fatalities', 'count'),
        Total_Fatalitas=('number_of_fatalities', 'sum'),
        Rata_Fatalitas=('number_of_fatalities', 'mean'),
        Total_Drunk=('number_of_drunk_drivers', 'sum')
    )
    .reset_index()
)
map_data['Rata_Fatalitas'] = map_data['Rata_Fatalitas'].round(2)

st.markdown("#### Peta Interaktif Fatalitas per State")

col_map_toggle = st.radio(
    "Tampilkan berdasarkan:",
    ["Total Fatalitas", "Total Kecelakaan", "Rata-rata Fatalitas/Kasus"],
    horizontal=True
)
map_col = {
    "Total Fatalitas":            "Total_Fatalitas",
    "Total Kecelakaan":           "Total_Kecelakaan",
    "Rata-rata Fatalitas/Kasus":  "Rata_Fatalitas"
}[col_map_toggle]

fig_map = px.choropleth(
    map_data,
    locations='state_name',
    locationmode='USA-states',
    color=map_col,
    scope='usa',
    color_continuous_scale='Reds',
    hover_data={
        'Total_Kecelakaan': True,
        'Total_Fatalitas':  True,
        'Rata_Fatalitas':   True,
        'Total_Drunk':      True
    },
    labels={
        'Total_Kecelakaan': 'Kecelakaan',
        'Total_Fatalitas':  'Fatalitas',
        'Rata_Fatalitas':   'Rata-rata',
        'Total_Drunk':      'Drunk Driver'
    }
)
fig_map.update_layout(
    paper_bgcolor='white',
    margin=dict(t=10, b=10, l=0, r=0),
    coloraxis_colorbar=dict(title=col_map_toggle)
)
st.plotly_chart(fig_map, use_container_width=True)

colE, colF = st.columns(2)

with colE:
    st.markdown("#### Top 15 State — Jumlah Kecelakaan")
    top15 = map_data.nlargest(15, 'Total_Kecelakaan')

    fig_bar_state = px.bar(
        top15.sort_values('Total_Kecelakaan'),
        x='Total_Kecelakaan',
        y='state_name',
        orientation='h',
        color='Total_Kecelakaan',
        color_continuous_scale='Blues',
        text='Total_Kecelakaan'
    )
    fig_bar_state.update_traces(texttemplate='%{text:,}', textposition='outside')
    fig_bar_state.update_layout(
        plot_bgcolor='white', paper_bgcolor='white',
        coloraxis_showscale=False, showlegend=False,
        margin=dict(t=20, b=10, l=10),
        xaxis_title="Jumlah Kecelakaan", yaxis_title=""
    )
    st.plotly_chart(fig_bar_state, use_container_width=True)

with colF:
    st.markdown("#### Kecelakaan vs Fatalitas per State")

    fig_scatter = px.scatter(
        map_data,
        x='Total_Kecelakaan',
        y='Total_Fatalitas',
        size='Total_Drunk',
        color='Rata_Fatalitas',
        color_continuous_scale='RdYlGn_r',
        hover_name='state_name',
        text='state_name',
        labels={
            'Total_Kecelakaan': 'Total Kecelakaan',
            'Total_Fatalitas':  'Total Fatalitas',
            'Total_Drunk':      'Drunk Driver',
            'Rata_Fatalitas':   'Rata-rata Fatalitas'
        }
    )
    fig_scatter.update_traces(textposition='top center', textfont_size=9)
    fig_scatter.update_layout(
        plot_bgcolor='white', paper_bgcolor='white',
        margin=dict(t=20, b=10)
    )
    st.plotly_chart(fig_scatter, use_container_width=True)
    st.caption("Ukuran titik = jumlah drunk driver. Warna = rata-rata fatalitas per kasus.")

st.markdown("#### Tabel Ringkasan per State")

tabel_state = map_data.copy()
tabel_state.columns = [
    'State', 'Total Kecelakaan', 'Total Fatalitas',
    'Rata-rata Fatalitas', 'Total Drunk Driver'
]
tabel_state = tabel_state.sort_values(
    'Total Kecelakaan', ascending=False
).reset_index(drop=True)
tabel_state.index += 1

def color_kecelakaan(val):
    col = tabel_state['Total Kecelakaan']
    if col.max() == col.min():
        intensity = 0
    else:
        intensity = (val - col.min()) / (col.max() - col.min())
    r = int(219 - intensity * 150)
    g = int(234 - intensity * 150)
    b = int(254 - intensity * 50)
    font = 'white' if intensity > 0.6 else '#1e3a5f'
    return f'background-color: rgb({r},{g},{b}); color: {font}; font-weight: 600'

def color_fatalitas(val):
    col = tabel_state['Total Fatalitas']
    if col.max() == col.min():
        intensity = 0
    else:
        intensity = (val - col.min()) / (col.max() - col.min())
    r = int(254 - intensity * 50)
    g = int(226 - intensity * 180)
    b = int(226 - intensity * 180)
    font = 'white' if intensity > 0.6 else '#7f1d1d'
    return f'background-color: rgb({r},{g},{b}); color: {font}; font-weight: 600'

def color_drunk(val):
    col = tabel_state['Total Drunk Driver']
    if col.max() == col.min():
        intensity = 0
    else:
        intensity = (val - col.min()) / (col.max() - col.min())
    r = 255
    g = int(237 - intensity * 130)
    b = int(213 - intensity * 180)
    font = 'white' if intensity > 0.7 else '#7c2d12'
    return f'background-color: rgb({r},{g},{b}); color: {font}'

styled = (
    tabel_state.style
    .applymap(color_kecelakaan, subset=['Total Kecelakaan'])
    .applymap(color_fatalitas,  subset=['Total Fatalitas'])
    .applymap(color_drunk,      subset=['Total Drunk Driver'])
    .format({
        'Total Kecelakaan':    '{:,}',
        'Total Fatalitas':     '{:,}',
        'Rata-rata Fatalitas': '{:.2f}',
        'Total Drunk Driver':  '{:,}'
    })
    .set_properties(**{
        'font-size': '13px',
        'border': '1px solid #e5e7eb',
        'padding': '6px 12px'
    })
    .set_table_styles([{
        'selector': 'thead tr th',
        'props': [
            ('background-color', '#1e3a5f'),
            ('color', 'white'),
            ('font-weight', '700'),
            ('font-size', '13px'),
            ('padding', '8px 12px'),
            ('text-align', 'center')
        ]
    }])
)

st.dataframe(styled, use_container_width=True, height=400)
============================================================
TAB 3 - ANALISIS DRUNK DRIVER
============================================================
with tab3:

st.markdown("### Analisis Kecelakaan Melibatkan Pengemudi Mabuk")

drunk_cases = df[df['IS_DRUNK']].shape[0]
sober_cases = df[~df['IS_DRUNK']].shape[0]
drunk_fatal = int(df[df['IS_DRUNK']]['number_of_fatalities'].sum())
sober_fatal = int(df[~df['IS_DRUNK']]['number_of_fatalities'].sum())
ratio = round(drunk_fatal / drunk_cases, 2) if drunk_cases > 0 else 0

d1, d2, d3, d4 = st.columns(4)
with d1:
    st.metric("Kasus Drunk Driver",        f"{drunk_cases:,}")
with d2:
    st.metric("Kasus Non-Drunk",           f"{sober_cases:,}")
with d3:
    st.metric("Fatalitas (Drunk)",         f"{drunk_fatal:,}")
with d4:
    st.metric("Rasio Fatal/Kasus Mabuk",   str(ratio))

colG, colH = st.columns(2)

with colG:
    st.markdown("#### Perbandingan Drunk vs Non-Drunk")
    compare_df = pd.DataFrame({
        'Status':     ['Drunk Driver', 'Non-Drunk Driver'],
        'Kecelakaan': [drunk_cases, sober_cases],
        'Fatalitas':  [drunk_fatal, sober_fatal]
    })

    fig_compare = go.Figure()
    fig_compare.add_trace(go.Bar(
        name='Kecelakaan',
        x=compare_df['Status'],
        y=compare_df['Kecelakaan'],
        marker_color=['#ef4444', '#3b82f6'],
        text=compare_df['Kecelakaan'],
        texttemplate='%{text:,}',
        textposition='outside'
    ))
    fig_compare.add_trace(go.Bar(
        name='Fatalitas',
        x=compare_df['Status'],
        y=compare_df['Fatalitas'],
        marker_color=['#dc2626', '#1d4ed8'],
        text=compare_df['Fatalitas'],
        texttemplate='%{text:,}',
        textposition='outside'
    ))
    fig_compare.update_layout(
        barmode='group',
        plot_bgcolor='white', paper_bgcolor='white',
        margin=dict(t=20, b=10),
        legend=dict(orientation='h', y=1.1)
    )
    st.plotly_chart(fig_compare, use_container_width=True)

with colH:
    st.markdown("#### Persentase Kasus Mabuk per Kategori Waktu")
    drunk_time = df.groupby('TIME_SHORT').agg(
        Total_Drunk=('IS_DRUNK', 'sum'),
        Total_Kasus=('IS_DRUNK', 'count')
    ).reset_index()
    drunk_time['Pct_Drunk'] = (
        drunk_time['Total_Drunk'] / drunk_time['Total_Kasus'] * 100
    ).round(1)

    fig_drunk_time = px.bar(
        drunk_time,
        x='TIME_SHORT',
        y='Pct_Drunk',
        color='Pct_Drunk',
        color_continuous_scale='Reds',
        text='Pct_Drunk',
        labels={
            'TIME_SHORT': 'Kategori Waktu',
            'Pct_Drunk': '% Kasus Drunk Driver'
        }
    )
    fig_drunk_time.update_traces(texttemplate='%{text}%', textposition='outside')
    fig_drunk_time.update_layout(
        plot_bgcolor='white', paper_bgcolor='white',
        coloraxis_showscale=False,
        margin=dict(t=20, b=10), xaxis_title=""
    )
    st.plotly_chart(fig_drunk_time, use_container_width=True)
    st.caption("Dini hari cenderung memiliki persentase kasus mabuk tertinggi.")

st.markdown("#### Hubungan Jumlah Drunk Driver dengan Fatalitas")

fig_scatter_drunk = px.scatter(
    df,
    x='number_of_drunk_drivers',
    y='number_of_fatalities',
    color='TIME_SHORT',
    size='number_of_fatalities',
    color_discrete_map=color_map,
    hover_data=['state_name'],
    opacity=0.6,
    labels={
        'number_of_drunk_drivers': 'Jumlah Pengemudi Mabuk',
        'number_of_fatalities':    'Jumlah Fatalitas',
        'TIME_SHORT':              'Kategori Waktu'
    }
)
fig_scatter_drunk.update_layout(
    plot_bgcolor='white', paper_bgcolor='white',
    margin=dict(t=20, b=10)
)
st.plotly_chart(fig_scatter_drunk, use_container_width=True)

st.markdown("#### Distribusi Drunk Driver per Hari")
drunk_hari = df.groupby('DAY_NAME')['IS_DRUNK'].mean().reset_index()
drunk_hari['Pct'] = (drunk_hari['IS_DRUNK'] * 100).round(1)
drunk_hari['DAY_NAME'] = pd.Categorical(
    drunk_hari['DAY_NAME'], categories=hari_order, ordered=True
)
drunk_hari = drunk_hari.sort_values('DAY_NAME')

fig_drunk_hari = px.bar(
    drunk_hari, x='DAY_NAME', y='Pct',
    color='Pct', color_continuous_scale='RdYlGn_r',
    text='Pct',
    labels={'DAY_NAME': 'Hari', 'Pct': '% Kasus Mabuk'}
)
fig_drunk_hari.update_traces(texttemplate='%{text}%', textposition='outside')
fig_drunk_hari.update_layout(
    plot_bgcolor='white', paper_bgcolor='white',
    coloraxis_showscale=False,
    margin=dict(t=20, b=10), xaxis_title=""
)
st.plotly_chart(fig_drunk_hari, use_container_width=True)
============================================================
TAB 4 - ANALISIS LANJUTAN
============================================================
with tab4:

st.markdown("### Analisis Lanjutan")

colI, colJ = st.columns(2)

with colI:
    st.markdown("#### Distribusi Jumlah Fatalitas per Kecelakaan")
    fig_hist_fatal = px.histogram(
        df,
        x='number_of_fatalities',
        nbins=20,
        color_discrete_sequence=['#1e3a5f'],
        labels={
            'number_of_fatalities': 'Jumlah Fatalitas',
            'count': 'Frekuensi'
        }
    )
    fig_hist_fatal.update_layout(
        plot_bgcolor='white', paper_bgcolor='white',
        margin=dict(t=20, b=10), bargap=0.1
    )
    st.plotly_chart(fig_hist_fatal, use_container_width=True)
    st.caption("Mayoritas kecelakaan menghasilkan 1 fatalitas per kejadian.")

with colJ:
    st.markdown("#### Box Plot Fatalitas per Kategori Waktu")
    fig_box = px.box(
        df,
        x='TIME_SHORT',
        y='number_of_fatalities',
        color='TIME_SHORT',
        color_discrete_map=color_map,
        points='outliers',
        labels={
            'TIME_SHORT': 'Kategori Waktu',
            'number_of_fatalities': 'Jumlah Fatalitas'
        }
    )
    fig_box.update_layout(
        plot_bgcolor='white', paper_bgcolor='white',
        showlegend=False,
        margin=dict(t=20, b=10), xaxis_title=""
    )
    st.plotly_chart(fig_box, use_container_width=True)

st.markdown("#### Ranking State — Multi Metrik")

n_top = st.slider("Tampilkan top N State:", min_value=5, max_value=20, value=10, step=1)

rank_data = df.groupby('state_name').agg(
    Kecelakaan=('number_of_fatalities', 'count'),
    Fatalitas=('number_of_fatalities', 'sum'),
    Drunk=('number_of_drunk_drivers', 'sum')
).nlargest(n_top, 'Kecelakaan').reset_index()

fig_multi = go.Figure()
fig_multi.add_trace(go.Bar(
    name='Kecelakaan',
    x=rank_data['state_name'],
    y=rank_data['Kecelakaan'],
    marker_color='#1e3a5f',
    yaxis='y'
))
fig_multi.add_trace(go.Bar(
    name='Fatalitas',
    x=rank_data['state_name'],
    y=rank_data['Fatalitas'],
    marker_color='#ef4444',
    yaxis='y'
))
fig_multi.add_trace(go.Scatter(
    name='Drunk Driver',
    x=rank_data['state_name'],
    y=rank_data['Drunk'],
    mode='lines+markers',
    marker=dict(color='#f59e0b', size=9),
    line=dict(width=2.5),
    yaxis='y2'
))
fig_multi.update_layout(
    barmode='group',
    plot_bgcolor='white', paper_bgcolor='white',
    margin=dict(t=20, b=10),
    yaxis=dict(title='Jumlah'),
    yaxis2=dict(
        title='Drunk Driver',
        overlaying='y', side='right',
        showgrid=False
    ),
    legend=dict(orientation='h', y=1.1)
)
st.plotly_chart(fig_multi, use_container_width=True)

st.markdown("#### Korelasi Antar Variabel Numerik")

num_cols = [
    'hour_of_crash', 'month_of_crash', 'day_of_week',
    'number_of_fatalities', 'number_of_drunk_drivers'
]
corr_df = df[num_cols].corr().round(3)

fig_corr = px.imshow(
    corr_df,
    text_auto=True,
    color_continuous_scale='RdBu_r',
    zmin=-1, zmax=1,
    labels=dict(color="Korelasi")
)
fig_corr.update_layout(
    paper_bgcolor='white',
    margin=dict(t=20, b=20)
)
st.plotly_chart(fig_corr, use_container_width=True)
st.caption("Nilai mendekati 1 = korelasi positif kuat. Nilai mendekati -1 = korelasi negatif kuat.")
============================================================
TAB 5 - INSIGHT DAN KESIMPULAN
============================================================
with tab5:

st.markdown("### Insight Utama dari Data")

if len(df) > 0:
    peak_hour       = int(df['hour_of_crash'].mode()[0])
    peak_month      = bulan_mapping[int(df['month_of_crash'].mode()[0])]
    peak_time       = df['TIME_SHORT'].mode()[0]
    peak_day        = df['DAY_NAME'].mode()[0]
    top_state       = df['state_name'].value_counts().idxmax()
    pct_mabuk       = round(df['IS_DRUNK'].mean() * 100, 1)
    avg_fat         = round(df['number_of_fatalities'].mean(), 2)
    peak_drunk_time = df.groupby('TIME_SHORT')['IS_DRUNK'].mean().idxmax()

    r1c1, r1c2, r1c3 = st.columns(3)
    r2c1, r2c2, r2c3 = st.columns(3)
    r3c1, r3c2, r3c3 = st.columns(3)

    def insight_card(label, value, note=""):
        st.markdown(
            f"""
            <div style="background: linear-gradient(135deg,#1e3a5f,#2d5986);
                        border-radius:14px; padding:18px 20px; height:110px;
                        color:white; margin-bottom:10px;">
                <div style="font-size:12px; opacity:0.75; margin-top:4px">{label}</div>
                <div style="font-size:20px; font-weight:800; margin-top:6px">{value}</div>
                <div style="font-size:11px; opacity:0.65; margin-top:4px">{note}</div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with r1c1: insight_card("Jam Paling Rawan",       f"{peak_hour:02d}:00",     "Puncak kecelakaan harian")
    with r1c2: insight_card("Bulan Paling Rawan",     peak_month,                "Kasus terbanyak")
    with r1c3: insight_card("Kategori Waktu Rawan",   peak_time,                 "Berdasarkan frekuensi kasus")
    with r2c1: insight_card("Hari Paling Rawan",      peak_day,                  "Kasus terbanyak")
    with r2c2: insight_card("State Teratas",          top_state,                 "Jumlah kecelakaan tertinggi")
    with r2c3: insight_card("Persentase Kasus Mabuk", f"{pct_mabuk}%",           "Dari total kasus terfilter")
    with r3c1: insight_card("Rata-rata Fatalitas",    str(avg_fat),              "Per kejadian kecelakaan")
    with r3c2: insight_card("Waktu Rawan Drunk",      peak_drunk_time,           "Persentase kasus mabuk tertinggi")
    with r3c3: insight_card("Total Data Dianalisis",  f"{len(df):,}",            "Setelah filter diterapkan")

st.markdown("---")
st.markdown("### Ringkasan Analisis")

st.markdown("""
<div style="background:white; border-radius:16px; padding:24px;
            box-shadow:0 2px 10px rgba(0,0,0,0.06);">

<h4 style="color:#1e3a5f;">Pola Waktu</h4>
<p style="color:#374151;">
Kecelakaan fatal di AS pada tahun 2015 memperlihatkan pola waktu yang konsisten.
Kecelakaan paling sering terjadi pada malam hari dan dini hari, terutama antara pukul 18.00-02.00.
Kondisi ini berkaitan dengan menurunnya visibilitas, kelelahan pengemudi, serta meningkatnya
aktivitas hiburan malam yang berpotensi mendorong perilaku mengemudi di bawah pengaruh alkohol.
</p>

<h4 style="color:#1e3a5f;">Pola Geografis</h4>
<p style="color:#374151;">
Beberapa state dengan populasi dan lalu lintas tinggi seperti Texas, California, dan Florida
secara konsisten berada di peringkat atas dalam jumlah kecelakaan fatal. Namun bila dilihat
dari rata-rata fatalitas per kasus, beberapa state yang lebih kecil justru menunjukkan angka
yang lebih tinggi, mengindikasikan kondisi infrastruktur jalan atau kecepatan berkendara
yang lebih berbahaya.
</p>

<h4 style="color:#1e3a5f;">Pengaruh Drunk Driver</h4>
<p style="color:#374151;">
Kecelakaan yang melibatkan pengemudi mabuk memiliki rasio fatalitas yang lebih tinggi
dibandingkan kecelakaan biasa. Pola ini paling terlihat pada hari Sabtu-Minggu dini hari.
Penanganan serius terhadap perilaku mengemudi di bawah pengaruh alkohol menjadi salah satu
kunci penting untuk menurunkan angka kecelakaan fatal.
</p>

<h4 style="color:#1e3a5f;">Rekomendasi</h4>
<ul style="color:#374151;">
    <li>Tingkatkan patroli dan razia pada jam-jam puncak kecelakaan (18.00-02.00)</li>
    <li>Fokuskan program edukasi anti-drunk-driving pada hari Jumat-Minggu</li>
    <li>Prioritaskan perbaikan infrastruktur di state dengan rata-rata fatalitas tinggi</li>
    <li>Kampanye keselamatan berkendara lebih intensif pada bulan-bulan rawan</li>
</ul>

</div>
""", unsafe_allow_html=True)
============================================================
FOOTER
============================================================
st.markdown("---")
st.markdown(
""
"Dashboard Analisis Kecelakaan Fatal USA 2015  |  "
"Data: NHTSA FARS 2015  |  "
"Dibangun dengan Streamlit, Plotly, Pandas  |  "
"v2.0"
"",
unsafe_allow_html=True
)


Tutup
