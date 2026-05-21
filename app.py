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
