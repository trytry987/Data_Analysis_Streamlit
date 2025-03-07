import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load dataset
file_id = '18qWmN8q3vuUBbQm8Frz4LbbniPjiJI7y'
download_url = f"https://drive.google.com/uc?id={file_id}"
main_df = pd.read_csv(download_url)
main_df['dteday'] = pd.to_datetime(main_df['dteday'])

main_df = main_df[['dteday', 'season', 'yr', 'mnth', 'holiday', 'weekday', 'workingday', 'hr', 'cnt_x', 'cnt_y', 'temp_x']]
main_df.rename(columns={'cnt_x': 'cnt_daily', 'cnt_y': 'cnt_hourly', 'temp_x': 'temp_daily'}, inplace=True)

# Sidebar - Rentang Waktu
min_date = main_df["dteday"].min()
max_date = main_df["dteday"].max()
start_date, end_date = st.sidebar.date_input("Rentang Waktu", [min_date, max_date], min_value=min_date, max_value=max_date)

# Filter data
filtered_df = main_df[(main_df["dteday"] >= pd.Timestamp(start_date)) & (main_df["dteday"] <= pd.Timestamp(end_date))]

# Header Dashboard
st.title("Dashboard Peminjaman Sepeda")

# Tren Peminjaman Sepeda per Hari
st.subheader("Tren Peminjaman Sepeda per Hari")
fig, ax = plt.subplots(figsize=(10, 5))
ax.plot(filtered_df['dteday'], filtered_df['cnt_daily'], marker='o', color='#90CAF9', linestyle='-')
ax.set_xlabel("Tanggal")
ax.set_ylabel("Jumlah Peminjaman Sepeda")
ax.set_title("Tren Peminjaman Sepeda per Hari")
ax.grid(True, linestyle="--", alpha=0.7, axis="x")
ax.grid(True, linestyle="--", alpha=0.7, axis="y")
plt.xticks(rotation=45)
st.pyplot(fig)

# Distribusi Peminjaman berdasarkan Musim
st.subheader("Distribusi Rata-rata Peminjaman berdasarkan Musim")
fig, ax = plt.subplots(figsize=(8, 5))
seasonal_trend = filtered_df.groupby("season")["cnt_daily"].mean().reset_index()
season_labels = {1: "Spring", 2: "Summer", 3: "Fall", 4: "Winter"}
seasonal_trend["season"] = seasonal_trend["season"].map(season_labels)
sns.barplot(x='season', y='cnt_daily', data=seasonal_trend, hue='season', palette=['#90EE90', '#FFD700', '#FF8C00', '#4682B4'], ax=ax)
ax.set_xlabel("Musim")
ax.set_ylabel("Rata-rata Jumlah Peminjaman")
ax.set_title("Distribusi Rata-rata Peminjaman per Musim")
ax.grid(True, linestyle="--", alpha=0.7, axis="y")
st.pyplot(fig)

# Hubungan antara Suhu dan Jumlah Peminjaman
st.subheader("Pengaruh Suhu terhadap Peminjaman Sepeda")
fig, ax = plt.subplots(figsize=(8, 5))
temp_trend = filtered_df.copy()
temp_trend['temp_daily'] = temp_trend['temp_daily'] * 41  # inverse normalization dari nilai temp
sns.scatterplot(x='temp_daily', y='cnt_daily', data=temp_trend, color='#90CAF9', alpha=0.6, s=40, edgecolor='black')
ax.set_xlabel("Suhu Harian (°C)")
ax.set_ylabel("Jumlah Peminjaman Sepeda")
ax.set_title("Pengaruh Suhu terhadap Jumlah Peminjaman Sepeda")
ax.grid(True, linestyle="--", alpha=0.7, axis="x")
ax.grid(True, linestyle="--", alpha=0.7, axis="y")
st.pyplot(fig)

# Jam Sibuk Peminjaman Sepeda
st.subheader("Jam Sibuk Peminjaman Sepeda")
busy_hours = filtered_df.groupby("hr")["cnt_hourly"].mean().reset_index()
fig, ax = plt.subplots(figsize=(8, 5))
sns.lineplot(x='hr', y='cnt_hourly', data=busy_hours, marker='o', color='#90CAF9')
ax.set_xlabel("Jam")
ax.set_ylabel("Rata-rata Peminjaman Sepeda")
ax.set_title("Jam Sibuk Peminjaman Sepeda")
ax.grid(True, linestyle="--", alpha=0.7, axis="x")
ax.grid(True, linestyle="--", alpha=0.7, axis="y")
st.pyplot(fig)
