import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from pandas.api.types import CategoricalDtype

# Load data
day_df = pd.read_csv("dashboard/penyewaan_sepeda_cleaning.csv")

st.sidebar.header("Filter Data Berdasarkan Tahun")
years = st.sidebar.multiselect("Pilih Tahun", options=[2011, 2012], default=[2011, 2012])

filtered_df = day_df[day_df["yr"].isin(years)]

if filtered_df.empty:
    st.write("### Tidak ada visualisasi data yang ditampilkan")
else:
    st.title("Bike Sharing Data Dashboard")

    st.write("Jumlah Penyewaan Sepeda Berdasarkan Musim")
    season_visual = filtered_df.groupby("season")["cnt"].sum().reset_index()
    plt.figure(figsize=(8, 5))
    ax = sns.barplot(x=season_visual["season"], y=season_visual["cnt"], palette="Reds_r")
    for i, value in enumerate(season_visual["cnt"]):
        ax.text(i, value + 500, f"{int(value)}", ha="center", va="bottom", fontsize=10, color="black")
    st.pyplot(plt)

    st.write("Siklus perkembangan jumlah penyewaan sepeda selama bulan Januari-Desember")
    bulan_urut = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
    filtered_df["mnth"] = filtered_df["mnth"].astype(CategoricalDtype(categories=bulan_urut, ordered=True))
    month_cnt = filtered_df.groupby(["yr", "mnth"])["cnt"].sum().unstack()
    month_cnt = month_cnt.reindex(columns=bulan_urut)
    plt.figure(figsize=(10, 5))
    for year, color in zip(years, ["blue", "red"]):
        plt.plot(month_cnt.columns, month_cnt.loc[year], marker='o', linestyle='-', color=color, linewidth=2, label=str(year))
    plt.xticks(rotation=45)
    plt.legend(title="Tahun", loc="upper left", fontsize=10, title_fontsize=12, frameon=True)
    st.pyplot(plt)

    st.write("Perbandingan jumlah penyewa sepeda bertipe casual dan registered berdasarkan tahun")
    type_customer_yearly = filtered_df.groupby("yr")[["registered", "casual"]].sum()
    if len(years) == 1:
        fig, ax = plt.subplots(figsize=(5, 5))
        values = type_customer_yearly.loc[years[0]]
        ax.pie(values, labels=["Registered", "Casual"], autopct=lambda pct: f"{pct:.1f}%\n({int(pct*sum(values)/100):,})", colors=["red", "grey"], startangle=90, textprops={'fontsize': 10, 'weight': 'bold'})
        ax.set_title(f"Penyewaan Sepeda per Tipe Pengguna Tahun {years[0]}", fontsize=12, fontweight="bold")
        st.pyplot(fig)
    else:
        fig, axes = plt.subplots(1, len(years), figsize=(10, 5))
        colors, labels = ["red", "grey"], ["Registered", "Casual"]
        for i, year in enumerate(years):
            values = type_customer_yearly.loc[year]
            axes[i].pie(values, labels=labels, autopct=lambda pct: f"{pct:.1f}%\n({int(pct*sum(values)/100):,})", colors=colors, startangle=90, textprops={'fontsize': 10, 'weight': 'bold'})
            axes[i].set_title(f"Penyewaan Sepeda per Tipe Pengguna Tahun {year}", fontsize=12, fontweight="bold")
        plt.tight_layout()
        st.pyplot(fig)
