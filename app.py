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
