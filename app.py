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
