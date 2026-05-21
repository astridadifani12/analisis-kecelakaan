# ============================================================
# DASHBOARD ANALISIS KECELAKAAN FATAL USA 2015
# Versi Lengkap & Dikembangkan
# ============================================================

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np

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

/* Background utama */
.main { background-color: #f0f2f6; }

/* Metric cards */
[data-testid="metric-container"] {
    background: linear-gradient(135deg, #ffffff 0%, #f8f9ff 100%);
    border: 1px solid #e0e4f0;
    padding: 18px 20px;
    border-radius: 16px;
    box-shadow: 0 4px 12px rgba(0,0,0,0.07);
    transition: transform 0.2s;
}
[data-testid="metric-container"]:hover {
    transform: translateY(-2px);
    box-shadow: 0 6px 18px rgba(0,0,0,0.10);
}

/* Label metric lebih besar */
[data-testid="metric-container"] label {
    font-size: 13px !important;
    font-weight: 600 !important;
    color: #6b7280 !important;
    text-transform: uppercase;
    letter-spacing: 0.5px;
}
[data-testid="metric-container"] [data-testid="metric-value"] {
    font-size: 28px !important;
    font-weight: 800 !important;
    color: #1e3a5f !important;
}

/* Judul utama */
h1 { color: #1e3a5f !important; font-weight: 800 !important; }
h2, h3 { color: #1e3a5f !important; font-weight: 700 !important; }

/* Sidebar */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #1e3a5f 0%, #2d5986 100%);
}
[data-testid="stSidebar"] * { color: white !important; }
[data-testid="stSidebar"] .stMultiSelect > label,
[data-testid="stSidebar"] .stSelectbox > label,
[data-testid="stSidebar"] .stSlider > label { color: #cce0ff !important; font-weight: 600 !important; }

/* Tab style */
.stTabs [data-baseweb="tab-list"] {
    gap: 8px;
    background-color: #e8edf5;
    padding: 6px;
    border-radius: 12px;
}
.stTabs [data-baseweb="tab"] {
    border-radius: 8px;
    padding: 8px 20px;
    font-weight: 600;
    color: #4a5568;
}
.stTabs [aria-selected="true"] {
    background-color: #1e3a5f !important;
    color: white !important;
}

/* Card wrapper */
.card-box {
    background: white;
    border-radius: 16px;
    padding: 20px;
    margin-bottom: 16px;
    box-shadow: 0 2px 10px rgba(0,0,0,0.06);
}

/* Insight box */
.insight-card {
    background: linear-gradient(135deg, #1e3a5f 0%, #2d5986 100%);
    border-radius: 14px;
    padding: 18px 22px;
    margin-bottom: 12px;
    color: white;
}
.insight-card .icon { font-size: 24px; }
.insight-card .title { font-size: 13px; opacity: 0.8; margin-bottom: 4px; }
.insight-card .value { font-size: 20px; font-weight: 700; }

/* Alert info custom */
.stInfo { border-radius: 12px !important; }

/* Divider style */
hr { border-color: #e0e4f0 !important; margin: 24px 0 !important; }

/* Expander */
.streamlit-expanderHeader {
    font-weight: 600 !important;
    color: #1e3a5f !important;
}

/* Footer */
.footer-text {
    text-align: center;
    color: #9ca3af;
    font-size: 12px;
    padding: 20px 0 10px 0;
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

df_raw = load_data()

# ============================================================
# PREPROCESSING
# ============================================================

hari_mapping = {
    1: 'Minggu', 2: 'Senin', 3: 'Selasa',
    4: 'Rabu', 5: 'Kamis', 6: 'Jumat', 7: 'Sabtu'
}
hari_order = ['Senin', 'Selasa', 'Rabu', 'Kamis', 'Jumat', 'Sabtu', 'Minggu']

bulan_mapping = {
    1:'Januari', 2:'Februari', 3:'Maret', 4:'April',
    5:'Mei', 6:'Juni', 7:'Juli', 8:'Agustus',
    9:'September', 10:'Oktober', 11:'November', 12:'Desember'
}

def kategori_waktu(jam):
    if 0 <= jam < 6:   return 'Dini Hari (00-05)'
    elif 6 <= jam < 12: return 'Pagi (06-11)'
    elif 12 <= jam < 18: return 'Siang (12-17)'
    else:               return 'Malam (18-23)'

def kategori_waktu_short(jam):
    if 0 <= jam < 6:    return 'Dini Hari'
    elif 6 <= jam < 12: return 'Pagi'
    elif 12 <= jam < 18: return 'Siang'
    else:               return 'Malam'

# Terapkan mapping
df_raw['DAY_NAME']      = df_raw['day_of_week'].map(hari_mapping)
df_raw['BULAN_NAMA']    = df_raw['month_of_crash'].map(bulan_mapping)
df_raw['TIME_CATEGORY'] = df_raw['hour_of_crash'].apply(kategori_waktu)
df_raw['TIME_SHORT']    = df_raw['hour_of_crash'].apply(kategori_waktu_short)

# Drunk driver flag
df_raw['IS_DRUNK'] = df_raw['number_of_drunk_drivers'] > 0

# ============================================================
# HEADER
# ============================================================

col_logo, col_title = st.columns([1, 11])
with col_title:
    st.markdown("## 🚗 Analisis Pola Kecelakaan Fatal di Amerika Serikat Tahun 2015")
    st.markdown(
        "<span style='color:#6b7280; font-size:15px;'>"
        "Dashboard interaktif untuk mengeksplorasi pola kecelakaan fatal berdasarkan "
        "faktor waktu, geografis, dan perilaku pengemudi."
        "</span>",
        unsafe_allow_html=True
    )

st.markdown("---")

# ============================================================
# SIDEBAR – FILTER
# ============================================================

st.sidebar.markdown("## 🔍 Filter Dashboard")
st.sidebar.markdown("---")

# Filter Bulan
bulan_opts = sorted(df_raw['month_of_crash'].unique())
bulan_sel = st.sidebar.multiselect(
    "📅 Pilih Bulan",
    options=bulan_opts,
    default=bulan_opts,
    format_func=lambda x: bulan_mapping[x]
)

# Filter State
state_opts = sorted(df_raw['state_name'].unique())
state_sel = st.sidebar.multiselect(
    "🗺️ Pilih State",
    options=state_opts,
    default=state_opts
)

# Filter Kategori Waktu
waktu_opts = ['Dini Hari', 'Pagi', 'Siang', 'Malam']
waktu_sel = st.sidebar.multiselect(
    "⏰ Kategori Waktu",
    options=waktu_opts,
    default=waktu_opts
)

# Filter Hari
hari_opts = hari_order
hari_sel = st.sidebar.multiselect(
    "📆 Pilih Hari",
    options=hari_opts,
    default=hari_opts
)

# Filter Drunk Driver
st.sidebar.markdown("---")
drunk_filter = st.sidebar.radio(
    "🍺 Status Pengemudi Mabuk",
    options=["Semua", "Melibatkan Drunk Driver", "Tidak Melibatkan"],
    index=0
)

st.sidebar.markdown("---")
st.sidebar.markdown(
    "<div style='font-size:11px; opacity:0.7;'>"
    "📊 Data: NHTSA FARS 2015<br>"
    "🛠️ Dashboard v2.0"
    "</div>",
    unsafe_allow_html=True
)

# ============================================================
# TERAPKAN FILTER
# ============================================================

df = df_raw.copy()
df = df[df['month_of_crash'].isin(bulan_sel)]
df = df[df['state_name'].isin(state_sel)]
df = df[df['TIME_SHORT'].isin(waktu_sel)]
df = df[df['DAY_NAME'].isin(hari_sel)]

if drunk_filter == "Melibatkan Drunk Driver":
    df = df[df['IS_DRUNK'] == True]
elif drunk_filter == "Tidak Melibatkan":
    df = df[df['IS_DRUNK'] == False]

# ============================================================
# PREVIEW DATA
# ============================================================

with st.expander("📄 Preview Dataset (5 Baris Pertama)"):
    st.dataframe(
        df.head(),
        use_container_width=True,
        hide_index=True
    )
    st.caption(f"Total baris setelah filter: **{len(df):,}** dari **{len(df_raw):,}** data")

# ============================================================
# KPI METRICS – BARIS 1
# ============================================================

st.markdown("### 📌 Ringkasan Data")

c1, c2, c3, c4, c5, c6 = st.columns(6)

total_acc      = len(df)
total_fatal    = int(df['number_of_fatalities'].sum())
total_drunk    = int(df['number_of_drunk_drivers'].sum())
total_states   = df['state_name'].nunique()
pct_drunk      = (df['IS_DRUNK'].sum() / len(df) * 100) if len(df) > 0 else 0
avg_fatal_acc  = round(df['number_of_fatalities'].mean(), 2) if len(df) > 0 else 0

with c1:
    st.metric("🚗 Total Kecelakaan",  f"{total_acc:,}")
with c2:
    st.metric("💀 Total Fatalitas",   f"{total_fatal:,}")
with c3:
    st.metric("🍺 Drunk Driver",      f"{total_drunk:,}")
with c4:
    st.metric("🗺️ Jumlah State",      f"{total_states}")
with c5:
    st.metric("🔴 % Kasus Mabuk",     f"{pct_drunk:.1f}%")
with c6:
    st.metric("📊 Rata-rata Fatalitas/Kasus", f"{avg_fatal_acc}")

st.markdown("---")

# ============================================================
# TABS UTAMA
# ============================================================

tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "📊 Analisis Waktu",
    "🗺️ Analisis Geografis",
    "🍺 Analisis Drunk Driver",
    "📈 Analisis Lanjutan",
    "📌 Insight & Kesimpulan"
])

# ============================================================
# TAB 1 – ANALISIS WAKTU
# ============================================================

with tab1:

    st.markdown("### 📅 Distribusi Waktu Kecelakaan")

    # Baris 1: Bulan & Jam
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
            plot_bgcolor='white',
            paper_bgcolor='white',
            showlegend=False,
            coloraxis_showscale=False,
            margin=dict(t=20, b=10),
            xaxis_title="",
            yaxis_title="Jumlah Kecelakaan"
        )
        st.plotly_chart(fig_month, use_container_width=True)

    with colB:
        st.markdown("#### Distribusi per Jam (24 jam)")
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
        fig_hour.update_layout(
            plot_bgcolor='white',
            paper_bgcolor='white',
            margin=dict(t=20, b=10),
            xaxis=dict(tickmode='linear', dtick=2, title="Jam (00-23)"),
            yaxis_title="Jumlah Kecelakaan",
            showlegend=False
        )
        # Tambah highlight zona malam
        fig_hour.add_vrect(x0=18, x1=23, fillcolor='rgba(220,38,38,0.08)',
                            layer='below', line_width=0,
                            annotation_text="Malam", annotation_position="top left",
                            annotation_font_color='#dc2626')
        fig_hour.add_vrect(x0=0, x1=6, fillcolor='rgba(220,38,38,0.08)',
                            layer='below', line_width=0)
        st.plotly_chart(fig_hour, use_container_width=True)

    # Baris 2: Hari & Kategori Waktu
    colC, colD = st.columns(2)

    with colC:
        st.markdown("#### Distribusi per Hari")
        hari_count = df.groupby('DAY_NAME').size().reset_index(name='Jumlah')
        hari_count['DAY_NAME'] = pd.Categorical(hari_count['DAY_NAME'], categories=hari_order, ordered=True)
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
        color_map = {
            'Dini Hari': '#1e3a5f', 'Pagi': '#f59e0b',
            'Siang': '#10b981', 'Malam': '#ef4444'
        }

        fig_waktu = px.pie(
            waktu_count,
            values='Jumlah',
            names='TIME_SHORT',
            color='TIME_SHORT',
            color_discrete_map=color_map,
            hole=0.45
        )
        fig_waktu.update_traces(textinfo='label+percent', pull=[0.05]*4)
        fig_waktu.update_layout(
            paper_bgcolor='white',
            margin=dict(t=20, b=10),
            showlegend=True,
            legend=dict(orientation='h', yanchor='bottom', y=-0.2)
        )
        st.plotly_chart(fig_waktu, use_container_width=True)

    # Heatmap Hari vs Jam
    st.markdown("#### 🔥 Heatmap Kecelakaan: Hari vs Jam")

    heatmap_data = pd.pivot_table(
        df,
        values='number_of_fatalities',
        index='DAY_NAME',
        columns='hour_of_crash',
        aggfunc='sum',
        fill_value=0
    )
    # Urutkan baris sesuai hari
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
    st.caption("💡 Sel lebih gelap = lebih banyak fatalitas. Malam hari Jumat–Sabtu cenderung paling rawan.")

    # Tren Bulanan per Kategori Waktu
    st.markdown("#### 📈 Tren Bulanan per Kategori Waktu")
    tren = df.groupby(['month_of_crash', 'TIME_SHORT']).size().reset_index(name='Jumlah')
    tren['Bulan'] = tren['month_of_crash'].map(bulan_mapping)
    tren['Bulan'] = pd.Categorical(tren['Bulan'], categories=list(bulan_mapping.values()), ordered=True)
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


# ============================================================
# TAB 2 – ANALISIS GEOGRAFIS
# ============================================================

with tab2:

    st.markdown("### 🗺️ Distribusi Geografis Kecelakaan")

    # Peta Choropleth
    st.markdown("#### 🇺🇸 Peta Interaktif Fatalitas per State")

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

    col_map_toggle = st.radio(
        "Tampilkan berdasarkan:",
        ["Total Fatalitas", "Total Kecelakaan", "Rata-rata Fatalitas/Kasus"],
        horizontal=True
    )
    map_col = {
        "Total Fatalitas": "Total_Fatalitas",
        "Total Kecelakaan": "Total_Kecelakaan",
        "Rata-rata Fatalitas/Kasus": "Rata_Fatalitas"
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
            'Total_Fatalitas': True,
            'Rata_Fatalitas': True,
            'Total_Drunk': True
        },
        labels={
            'Total_Kecelakaan': 'Kecelakaan',
            'Total_Fatalitas': 'Fatalitas',
            'Rata_Fatalitas': 'Rata-rata',
            'Total_Drunk': 'Drunk Driver'
        }
    )
    fig_map.update_layout(
        paper_bgcolor='white',
        margin=dict(t=10, b=10, l=0, r=0),
        coloraxis_colorbar=dict(title=col_map_toggle)
    )
    st.plotly_chart(fig_map, use_container_width=True)

    # Bar & Scatter
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
                'Total_Fatalitas': 'Total Fatalitas',
                'Total_Drunk': 'Drunk Driver',
                'Rata_Fatalitas': 'Rata-rata Fatalitas'
            }
        )
        fig_scatter.update_traces(textposition='top center', textfont_size=9)
        fig_scatter.update_layout(
            plot_bgcolor='white', paper_bgcolor='white',
            margin=dict(t=20, b=10)
        )
        st.plotly_chart(fig_scatter, use_container_width=True)
        st.caption("💡 Ukuran titik = jumlah drunk driver. Warna = rata-rata fatalitas per kasus.")

    # Tabel Ringkasan per State
    st.markdown("#### 📋 Tabel Ringkasan per State")

    tabel_state = map_data.copy()
    tabel_state.columns = ['State', 'Total Kecelakaan', 'Total Fatalitas',
                            'Rata-rata Fatalitas', 'Total Drunk Driver']
    tabel_state = tabel_state.sort_values('Total Kecelakaan', ascending=False).reset_index(drop=True)
    tabel_state.index += 1

    def color_kecelakaan(val):
        """Warna biru proporsional untuk kolom Total Kecelakaan."""
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
        """Warna merah proporsional untuk kolom Total Fatalitas."""
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
        """Warna oranye proporsional untuk kolom Total Drunk Driver."""
        col = tabel_state['Total Drunk Driver']
        if col.max() == col.min():
            intensity = 0
        else:
            intensity = (val - col.min()) / (col.max() - col.min())
        r = int(255)
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
            'Total Kecelakaan':   '{:,}',
            'Total Fatalitas':    '{:,}',
            'Rata-rata Fatalitas':'{:.2f}',
            'Total Drunk Driver': '{:,}'
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


# ============================================================
# TAB 3 – ANALISIS DRUNK DRIVER
# ============================================================

with tab3:

    st.markdown("### 🍺 Analisis Kecelakaan Melibatkan Pengemudi Mabuk")

    # Metrik Drunk
    d1, d2, d3, d4 = st.columns(4)
    drunk_cases = df[df['IS_DRUNK']].shape[0]
    sober_cases = df[~df['IS_DRUNK']].shape[0]
    drunk_fatal = int(df[df['IS_DRUNK']]['number_of_fatalities'].sum())
    sober_fatal = int(df[~df['IS_DRUNK']]['number_of_fatalities'].sum())

    with d1:
        st.metric("🍺 Kasus Drunk Driver", f"{drunk_cases:,}")
    with d2:
        st.metric("✅ Kasus Non-Drunk", f"{sober_cases:,}")
    with d3:
        st.metric("💀 Fatalitas (Drunk)", f"{drunk_fatal:,}")
    with d4:
        ratio = round(drunk_fatal / drunk_cases, 2) if drunk_cases > 0 else 0
        st.metric("⚠️ Rasio Fatal/Kasus Mabuk", str(ratio))

    colG, colH = st.columns(2)

    with colG:
        st.markdown("#### Perbandingan Drunk vs Non-Drunk")
        compare_df = pd.DataFrame({
            'Status': ['Drunk Driver', 'Non-Drunk Driver'],
            'Kecelakaan': [drunk_cases, sober_cases],
            'Fatalitas': [drunk_fatal, sober_fatal]
        })

        fig_compare = go.Figure()
        fig_compare.add_trace(go.Bar(
            name='Kecelakaan', x=compare_df['Status'], y=compare_df['Kecelakaan'],
            marker_color=['#ef4444', '#3b82f6'], text=compare_df['Kecelakaan'],
            texttemplate='%{text:,}', textposition='outside'
        ))
        fig_compare.add_trace(go.Bar(
            name='Fatalitas', x=compare_df['Status'], y=compare_df['Fatalitas'],
            marker_color=['#dc2626', '#1d4ed8'], text=compare_df['Fatalitas'],
            texttemplate='%{text:,}', textposition='outside'
        ))
        fig_compare.update_layout(
            barmode='group', plot_bgcolor='white', paper_bgcolor='white',
            margin=dict(t=20, b=10), legend=dict(orientation='h', y=1.1)
        )
        st.plotly_chart(fig_compare, use_container_width=True)

    with colH:
        st.markdown("#### Drunk Driver per Kategori Waktu")
        drunk_time = df.groupby('TIME_SHORT').agg(
            Total_Drunk=('IS_DRUNK', 'sum'),
            Total_Kasus=('IS_DRUNK', 'count')
        ).reset_index()
        drunk_time['Pct_Drunk'] = (drunk_time['Total_Drunk'] / drunk_time['Total_Kasus'] * 100).round(1)

        fig_drunk_time = px.bar(
            drunk_time,
            x='TIME_SHORT',
            y='Pct_Drunk',
            color='Pct_Drunk',
            color_continuous_scale='Reds',
            text='Pct_Drunk',
            labels={'TIME_SHORT': 'Kategori Waktu', 'Pct_Drunk': '% Kasus Drunk Driver'}
        )
        fig_drunk_time.update_traces(texttemplate='%{text}%', textposition='outside')
        fig_drunk_time.update_layout(
            plot_bgcolor='white', paper_bgcolor='white',
            coloraxis_showscale=False,
            margin=dict(t=20, b=10), xaxis_title=""
        )
        st.plotly_chart(fig_drunk_time, use_container_width=True)
        st.caption("💡 Dini hari cenderung memiliki persentase kasus mabuk tertinggi.")

    # Scatter Drunk vs Fatalitas
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
            'number_of_fatalities': 'Jumlah Fatalitas',
            'TIME_SHORT': 'Kategori Waktu'
        }
    )
    # Tambah garis tren
    fig_scatter_drunk.update_layout(
        plot_bgcolor='white', paper_bgcolor='white',
        margin=dict(t=20, b=10)
    )
    st.plotly_chart(fig_scatter_drunk, use_container_width=True)

    # Drunk per Hari
    st.markdown("#### Distribusi Drunk Driver per Hari")
    drunk_hari = df.groupby('DAY_NAME')['IS_DRUNK'].mean().reset_index()
    drunk_hari['Pct'] = (drunk_hari['IS_DRUNK'] * 100).round(1)
    drunk_hari['DAY_NAME'] = pd.Categorical(drunk_hari['DAY_NAME'], categories=hari_order, ordered=True)
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


# ============================================================
# TAB 4 – ANALISIS LANJUTAN
# ============================================================

with tab4:

    st.markdown("### 📈 Analisis Lanjutan")

    # Distribusi Fatalitas
    colI, colJ = st.columns(2)

    with colI:
        st.markdown("#### Distribusi Jumlah Fatalitas per Kecelakaan")
        fig_hist_fatal = px.histogram(
            df,
            x='number_of_fatalities',
            nbins=20,
            color_discrete_sequence=['#1e3a5f'],
            labels={'number_of_fatalities': 'Jumlah Fatalitas', 'count': 'Frekuensi'}
        )
        fig_hist_fatal.update_layout(
            plot_bgcolor='white', paper_bgcolor='white',
            margin=dict(t=20, b=10),
            bargap=0.1
        )
        st.plotly_chart(fig_hist_fatal, use_container_width=True)
        st.caption("💡 Mayoritas kecelakaan menghasilkan 1 fatalitas per kejadian.")

    with colJ:
        st.markdown("#### Box Plot Fatalitas per Kategori Waktu")
        fig_box = px.box(
            df,
            x='TIME_SHORT',
            y='number_of_fatalities',
            color='TIME_SHORT',
            color_discrete_map=color_map,
            points='outliers',
            labels={'TIME_SHORT': 'Kategori Waktu', 'number_of_fatalities': 'Jumlah Fatalitas'}
        )
        fig_box.update_layout(
            plot_bgcolor='white', paper_bgcolor='white',
            showlegend=False,
            margin=dict(t=20, b=10), xaxis_title=""
        )
        st.plotly_chart(fig_box, use_container_width=True)

    # Ranking State dengan Metrik Ganda
    st.markdown("#### 🏆 Ranking State — Multi Metrik")

    n_top = st.slider("Tampilkan top N State:", min_value=5, max_value=20, value=10, step=1)

    rank_data = df.groupby('state_name').agg(
        Kecelakaan=('number_of_fatalities', 'count'),
        Fatalitas=('number_of_fatalities', 'sum'),
        Drunk=('number_of_drunk_drivers', 'sum')
    ).nlargest(n_top, 'Kecelakaan').reset_index()

    fig_multi = go.Figure()
    fig_multi.add_trace(go.Bar(
        name='Kecelakaan', x=rank_data['state_name'], y=rank_data['Kecelakaan'],
        marker_color='#1e3a5f', yaxis='y'
    ))
    fig_multi.add_trace(go.Bar(
        name='Fatalitas', x=rank_data['state_name'], y=rank_data['Fatalitas'],
        marker_color='#ef4444', yaxis='y'
    ))
    fig_multi.add_trace(go.Scatter(
        name='Drunk Driver', x=rank_data['state_name'], y=rank_data['Drunk'],
        mode='lines+markers', marker=dict(color='#f59e0b', size=9),
        line=dict(width=2.5), yaxis='y2'
    ))
    fig_multi.update_layout(
        barmode='group',
        plot_bgcolor='white', paper_bgcolor='white',
        margin=dict(t=20, b=10),
        yaxis=dict(title='Jumlah'),
        yaxis2=dict(title='Drunk Driver', overlaying='y', side='right', showgrid=False),
        legend=dict(orientation='h', y=1.1)
    )
    st.plotly_chart(fig_multi, use_container_width=True)

    # Korelasi
    st.markdown("#### 🔗 Korelasi Antar Variabel Numerik")

    num_cols = ['hour_of_crash', 'month_of_crash', 'day_of_week',
                'number_of_fatalities', 'number_of_drunk_drivers']
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
    st.caption("💡 Nilai mendekati 1 = korelasi positif kuat. Nilai mendekati -1 = korelasi negatif kuat.")


# ============================================================
# TAB 5 – INSIGHT & KESIMPULAN
# ============================================================

with tab5:

    st.markdown("### 📌 Insight Utama dari Data")

    # Hitung insight otomatis dari data yang sudah difilter
    if len(df) > 0:
        peak_hour  = int(df['hour_of_crash'].mode()[0])
        peak_month = bulan_mapping[int(df['month_of_crash'].mode()[0])]
        peak_time  = df['TIME_SHORT'].mode()[0]
        peak_day   = df['DAY_NAME'].mode()[0]
        top_state  = df['state_name'].value_counts().idxmax()
        pct_mabuk  = round(df['IS_DRUNK'].mean() * 100, 1)
        avg_fat    = round(df['number_of_fatalities'].mean(), 2)
        peak_drunk_time = (
            df.groupby('TIME_SHORT')['IS_DRUNK'].mean()
            .idxmax()
        )

        # Grid insight cards
        r1c1, r1c2, r1c3 = st.columns(3)
        r2c1, r2c2, r2c3 = st.columns(3)
        r3c1, r3c2, r3c3 = st.columns(3)

        def insight_card(icon, label, value, note=""):
            st.markdown(
                f"""
                <div style="background: linear-gradient(135deg,#1e3a5f,#2d5986);
                            border-radius:14px; padding:18px 20px; height:130px;
                            color:white; margin-bottom:10px;">
                    <div style="font-size:26px">{icon}</div>
                    <div style="font-size:12px; opacity:0.75; margin-top:4px">{label}</div>
                    <div style="font-size:20px; font-weight:800; margin-top:4px">{value}</div>
                    <div style="font-size:11px; opacity:0.65; margin-top:3px">{note}</div>
                </div>
                """,
                unsafe_allow_html=True
            )

        with r1c1: insight_card("⏰", "Jam Paling Rawan", f"{peak_hour:02d}:00",
                                 "Puncak kecelakaan harian")
        with r1c2: insight_card("📅", "Bulan Paling Rawan", peak_month,
                                 "Bulan dengan kasus terbanyak")
        with r1c3: insight_card("🌙", "Kategori Waktu Rawan", peak_time,
                                 "Berdasarkan frekuensi kasus")
        with r2c1: insight_card("📆", "Hari Paling Rawan", peak_day,
                                 "Hari dengan kasus terbanyak")
        with r2c2: insight_card("🗺️", "State Teratas", top_state,
                                 "Jumlah kecelakaan tertinggi")
        with r2c3: insight_card("🍺", "% Kasus Drunk Driver", f"{pct_mabuk}%",
                                 "Dari total kecelakaan terfilter")
        with r3c1: insight_card("💀", "Rata-rata Fatalitas", str(avg_fat),
                                 "Per kejadian kecelakaan")
        with r3c2: insight_card("🚨", "Waktu Rawan Drunk", peak_drunk_time,
                                 "% kasus mabuk tertinggi")
        with r3c3: insight_card("📊", "Total Data Dianalisis", f"{len(df):,}",
                                 "Setelah filter diterapkan")

    st.markdown("---")

    # Analisis Naratif
    st.markdown("### 📝 Ringkasan Analisis")

    st.markdown("""
    <div style="background:white; border-radius:16px; padding:24px; box-shadow:0 2px 10px rgba(0,0,0,0.06);">

    <h4 style="color:#1e3a5f;">⏱️ Pola Waktu</h4>
    <p style="color:#374151;">
    Kecelakaan fatal di AS pada tahun 2015 memperlihatkan pola waktu yang konsisten.
    Kecelakaan paling sering terjadi pada malam hari dan dini hari, terutama antara pukul 18.00–02.00.
    Kondisi ini diduga berkaitan dengan menurunnya visibilitas, kelelahan pengemudi, serta
    meningkatnya aktivitas hiburan malam yang berpotensi mendorong perilaku mengemudi di bawah
    pengaruh alkohol.
    </p>

    <h4 style="color:#1e3a5f;">🗺️ Pola Geografis</h4>
    <p style="color:#374151;">
    Beberapa state dengan populasi dan lalu lintas tinggi seperti Texas, California, dan Florida
    secara konsisten berada di peringkat atas dalam jumlah kecelakaan fatal. Namun bila dilihat
    dari rata-rata fatalitas per kasus, beberapa state yang lebih kecil justru menunjukkan angka
    yang lebih tinggi, mengindikasikan kondisi infrastruktur jalan atau kecepatan berkendara
    yang lebih berbahaya.
    </p>

    <h4 style="color:#1e3a5f;">🍺 Pengaruh Drunk Driver</h4>
    <p style="color:#374151;">
    Kecelakaan yang melibatkan pengemudi mabuk memiliki rasio fatalitas yang lebih tinggi
    dibandingkan kecelakaan biasa. Pola ini paling terlihat pada hari Sabtu–Minggu dini hari,
    yang bertepatan dengan aktivitas akhir pekan. Penanganan serius terhadap perilaku mengemudi
    di bawah pengaruh alkohol menjadi salah satu kunci penting untuk menurunkan angka
    kecelakaan fatal.
    </p>

    <h4 style="color:#1e3a5f;">📌 Rekomendasi</h4>
    <ul style="color:#374151;">
        <li>Tingkatkan patroli dan razia pada jam-jam puncak kecelakaan (18.00–02.00)</li>
        <li>Fokuskan program edukasi anti-drunk-driving pada hari Jumat–Minggu</li>
        <li>Prioritaskan perbaikan infrastruktur di state dengan rata-rata fatalitas tinggi</li>
        <li>Kampanye keselamatan berkendara lebih intensif pada bulan-bulan rawan</li>
    </ul>

    </div>
    """, unsafe_allow_html=True)

# ============================================================
# FOOTER
# ============================================================

st.markdown("---")
st.markdown(
    "<div class='footer-text'>"
    "🚗 Dashboard Analisis Kecelakaan Fatal USA 2015 &nbsp;|&nbsp; "
    "📊 Data: NHTSA FARS 2015 &nbsp;|&nbsp; "
    "🛠️ Dibangun dengan Streamlit · Plotly · Pandas &nbsp;|&nbsp; "
    "v2.0"
    "</div>",
    unsafe_allow_html=True
)
