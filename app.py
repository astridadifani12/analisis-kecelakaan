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
