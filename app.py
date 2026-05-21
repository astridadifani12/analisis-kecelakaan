# APP.PY — Dashboard Analisis Pola Kecelakaan Fatal di Amerika Serikat Tahun 2015

```python
# =========================================
# DASHBOARD ANALISIS KECELAKAAN FATAL USA 2015
# =========================================

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# =========================================
# KONFIGURASI HALAMAN
# =========================================

st.set_page_config(
    page_title="Analisis Kecelakaan Fatal USA 2015",
    page_icon="🚗",
    layout="wide"
)

# =========================================
# LOAD DATA
# =========================================

@st.cache_data
def load_data():

    df = pd.read_csv("df_clean.csv")

    return df


# LOAD DATA
_df = load_data()

# COPY DATA
_df = _df.copy()

# =========================================
# PREPROCESSING TAMBAHAN
# =========================================

# Mapping nama hari
hari_mapping = {
    1: 'Minggu',
    2: 'Senin',
    3: 'Selasa',
    4: 'Rabu',
    5: 'Kamis',
    6: 'Jumat',
    7: 'Sabtu'
}

# Mapping nama bulan
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

# Nama hari
if 'day_of_week' in _df.columns:
    _df['nama_hari'] = _df['day_of_week'].map(hari_mapping)

# Nama bulan
if 'month_of_crash' in _df.columns:
    _df['nama_bulan'] = _df['month_of_crash'].map(bulan_mapping)

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


if 'hour_of_crash' in _df.columns:
    _df['kategori_waktu'] = _df['hour_of_crash'].apply(kategori_waktu)

# Tipe hari

def tipe_hari(hari):

    if hari in ['Sabtu', 'Minggu']:
        return 'Akhir Pekan'

    return 'Hari Kerja'


if 'nama_hari' in _df.columns:
    _df['tipe_hari'] = _df['nama_hari'].apply(tipe_hari)

# =========================================
# HEADER DASHBOARD
# =========================================

st.title("🚗 Analisis Pola Kecelakaan Fatal di Amerika Serikat Tahun 2015")

st.markdown("""
Dashboard ini menampilkan hasil Exploratory Data Analysis (EDA) terkait pola kecelakaan fatal di Amerika Serikat tahun 2015 berdasarkan faktor waktu dan geografis.
""")

# =========================================
# SIDEBAR FILTER
# =========================================

st.sidebar.header("🔍 Filter Dashboard")

# FILTER STATE
if 'state_name' in _df.columns:

    selected_state = st.sidebar.multiselect(
        "Pilih State",
        options=sorted(_df['state_name'].dropna().unique()),
        default=sorted(_df['state_name'].dropna().unique())
    )

    _df = _df[_df['state_name'].isin(selected_state)]

# FILTER KATEGORI WAKTU
if 'kategori_waktu' in _df.columns:

    selected_waktu = st.sidebar.multiselect(
        "Pilih Kategori Waktu",
        options=['Dini Hari', 'Pagi', 'Siang', 'Malam'],
        default=['Dini Hari', 'Pagi', 'Siang', 'Malam']
    )

    _df = _df[_df['kategori_waktu'].isin(selected_waktu)]

# FILTER HARI
if 'nama_hari' in _df.columns:

    urutan_hari = ['Senin', 'Selasa', 'Rabu', 'Kamis', 'Jumat', 'Sabtu', 'Minggu']

    selected_hari = st.sidebar.multiselect(
        "Pilih Hari",
        options=urutan_hari,
        default=urutan_hari
    )

    _df = _df[_df['nama_hari'].isin(selected_hari)]

# =========================================
# METRIC
# =========================================

st.subheader("📌 Ringkasan Data")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "Total Kecelakaan",
        f"{len(_df):,}"
    )

with col2:
    st.metric(
        "Jumlah State",
        _df['state_name'].nunique()
    )

with col3:
    st.metric(
        "Total Fatalitas",
        int(_df['number_of_fatalities'].sum())
    )

with col4:
    st.metric(
        "Total Drunk Driver",
        int(_df['number_of_drunk_drivers'].sum())
    )

# =========================================
# DISTRIBUSI KATEGORI WAKTU
# =========================================

st.subheader("⏰ Distribusi Kecelakaan Berdasarkan Kategori Waktu")

per_waktu = _df['kategori_waktu'].value_counts().reset_index()
per_waktu.columns = ['Kategori Waktu', 'Jumlah']

fig_waktu = px.bar(
    per_waktu,
    x='Kategori Waktu',
    y='Jumlah',
    color='Kategori Waktu',
    text_auto=True
)

fig_waktu.update_layout(
    xaxis_title='Kategori Waktu',
    yaxis_title='Jumlah Kecelakaan'
)

st.plotly_chart(fig_waktu, use_container_width=True)

# =========================================
# DISTRIBUSI HARI
# =========================================

st.subheader("📅 Distribusi Kecelakaan Berdasarkan Hari")

urutan_hari = ['Senin', 'Selasa', 'Rabu', 'Kamis', 'Jumat', 'Sabtu', 'Minggu']

per_hari = (
    _df['nama_hari']
    .value_counts()
    .reindex(urutan_hari)
    .reset_index()
)

per_hari.columns = ['Hari', 'Jumlah']

fig_hari = px.bar(
    per_hari,
    x='Hari',
    y='Jumlah',
    color='Hari',
    text_auto=True
)

fig_hari.update_layout(
    xaxis_title='Hari',
    yaxis_title='Jumlah Kecelakaan'
)

st.plotly_chart(fig_hari, use_container_width=True)

# =========================================
# DISTRIBUSI JAM
# =========================================

st.subheader("🕒 Distribusi Kecelakaan Berdasarkan Jam")

fig_jam = px.histogram(
    _df,
    x='hour_of_crash',
    nbins=24,
    title='Distribusi Kecelakaan per Jam'
)

fig_jam.update_layout(
    xaxis_title='Jam',
    yaxis_title='Jumlah Kecelakaan'
)

st.plotly_chart(fig_jam, use_container_width=True)

# =========================================
# DISTRIBUSI BULAN
# =========================================

st.subheader("📊 Distribusi Kecelakaan Berdasarkan Bulan")

urutan_bulan = ['Jan', 'Feb', 'Mar', 'Apr', 'Mei', 'Jun',
                'Jul', 'Agu', 'Sep', 'Okt', 'Nov', 'Des']

per_bulan = (
    _df['nama_bulan']
    .value_counts()
    .reindex(urutan_bulan)
    .reset_index()
)

per_bulan.columns = ['Bulan', 'Jumlah']

fig_bulan = px.line(
    per_bulan,
    x='Bulan',
    y='Jumlah',
    markers=True
)

fig_bulan.update_layout(
    xaxis_title='Bulan',
    yaxis_title='Jumlah Kecelakaan'
)

st.plotly_chart(fig_bulan, use_container_width=True)

# =========================================
# ANALISIS GEOGRAFIS
# =========================================

st.subheader("🗺️ Top 10 State dengan Fatalitas Tertinggi")

per_state = (
    _df.groupby('state_name')['number_of_fatalities']
    .sum()
    .sort_values(ascending=False)
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

```

## requirements.txt

```txt
streamlit
pandas
plotly
```

## Struktur Repository GitHub

```bash
analisis-kecelakaan/
│
├── app.py
├── df_clean.csv
├── requirements.txt
└── README.md
```
