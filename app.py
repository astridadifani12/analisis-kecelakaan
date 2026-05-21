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
