import os
import warnings
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

warnings.filterwarnings("ignore")
plt.style.use("ggplot")

OUTPUT_DIR = "plots"
os.makedirs(OUTPUT_DIR, exist_ok=True)


def load_and_clean_data():
    # 1. Load Unemployment in India.csv (May 2019 - Jun 2020, Rural & Urban)
    df1 = pd.read_csv("Unemployment in India.csv")
    df1.columns = df1.columns.str.strip()
    df1_raw_shape = df1.shape
    df1_missing_before = df1.isna().sum().to_dict()

    df1 = df1.dropna().copy()
    for col in df1.select_dtypes(include="object").columns:
        df1[col] = df1[col].str.strip()

    df1["Date"] = pd.to_datetime(df1["Date"], format="%d-%m-%Y")
    df1 = df1.rename(
        columns={
            "Region": "State",
            "Estimated Unemployment Rate (%)": "Unemployment_Rate",
            "Estimated Employed": "Employed",
            "Estimated Labour Participation Rate (%)": "Labour_Participation_Rate",
        }
    )
    df1 = df1.drop_duplicates()

    # 2. Load Unemployment_Rate_upto_11_2020.csv (Jan 2020 - Oct 2020, State + Zone)
    df2 = pd.read_csv("Unemployment_Rate_upto_11_2020.csv")
    df2.columns = df2.columns.str.strip()
    # Handle duplicate 'Region' column (pandas renames second to 'Region.1')
    if "Region.1" in df2.columns:
        df2 = df2.rename(columns={"Region": "State", "Region.1": "Zone"})
    df2_raw_shape = df2.shape
    df2_missing_before = df2.isna().sum().to_dict()

    df2 = df2.dropna().copy()
    for col in df2.select_dtypes(include="object").columns:
        df2[col] = df2[col].str.strip()

    df2["Date"] = pd.to_datetime(df2["Date"], format="%d-%m-%Y")
    df2 = df2.rename(
        columns={
            "Estimated Unemployment Rate (%)": "Unemployment_Rate",
            "Estimated Employed": "Employed",
            "Estimated Labour Participation Rate (%)": "Labour_Participation_Rate",
        }
    )
    df2 = df2.drop_duplicates()

    print("=== DATA CLEANING SUMMARY ===")
    print(f"Dataset 1 (Unemployment in India.csv): raw={df1_raw_shape}, clean={df1.shape}")
    print(f"  Missing values before dropna: { {k: v for k, v in df1_missing_before.items() if v > 0} }")
    print(f"  Date range: {df1['Date'].min().strftime('%Y-%m-%d')} to {df1['Date'].max().strftime('%Y-%m-%d')}")
    print(f"  States: {df1['State'].nunique()}, Areas: {df1['Area'].unique().tolist()}")

    print(f"\nDataset 2 (Unemployment_Rate_upto_11_2020.csv): raw={df2_raw_shape}, clean={df2.shape}")
    print(f"  Missing values before dropna: { {k: v for k, v in df2_missing_before.items() if v > 0} }")
    print(f"  Date range: {df2['Date'].min().strftime('%Y-%m-%d')} to {df2['Date'].max().strftime('%Y-%m-%d')}")
    print(f"  States: {df2['State'].nunique()}, Zones: {df2['Zone'].unique().tolist()}")

    return df1, df2


def analyze_data(df1, df2):
    print("\n=== DESCRIPTIVE STATISTICS ===")
    print("\nDataset 1 (May 2019 - Jun 2020):")
    print(df1[["Unemployment_Rate", "Employed", "Labour_Participation_Rate"]].describe().round(2))

    print("\nDataset 2 (Jan 2020 - Oct 2020):")
    print(df2[["Unemployment_Rate", "Employed", "Labour_Participation_Rate"]].describe().round(2))

    # Covid-19 Phase Classification
    # Pre-Covid: <= Feb 2020 | Lockdown/Peak: Mar 2020 - Jun 2020 | Recovery: Jul 2020 - Oct 2020
    df1["Period"] = np.where(df1["Date"] < "2020-03-01", "Pre-Covid (May 2019-Feb 2020)", "Covid Lockdown (Mar-Jun 2020)")

    def classify_period_df2(d):
        if d < pd.Timestamp("2020-03-01"):
            return "Pre-Covid (Jan-Feb 2020)"
        elif d <= pd.Timestamp("2020-06-30"):
            return "Covid Lockdown (Mar-Jun 2020)"
        else:
            return "Post-Lockdown (Jul-Oct 2020)"

    df2["Period"] = df2["Date"].apply(classify_period_df2)

    print("\n=== COVID-19 IMPACT ANALYSIS ===")
    print("\nDataset 1 - Pre-Covid vs Covid Lockdown:")
    p1 = df1.groupby("Period")[["Unemployment_Rate", "Labour_Participation_Rate", "Employed"]].agg(["mean", "median", "max"])
    print(p1.round(2))

    print("\nDataset 1 - Rural vs Urban by Period:")
    ru = df1.groupby(["Area", "Period"])[["Unemployment_Rate", "Labour_Participation_Rate"]].mean()
    print(ru.round(2))

    print("\nDataset 2 - 2020 Phases (Pre-Covid vs Lockdown vs Post-Lockdown):")
    p2 = df2.groupby("Period")[["Unemployment_Rate", "Labour_Participation_Rate", "Employed"]].agg(["mean", "median", "max"])
    print(p2.round(2))

    # Monthly Trends
    print("\n=== MONTHLY UNEMPLOYMENT RATE (%) ===")
    m1 = df1.groupby(df1["Date"].dt.to_period("M"))["Unemployment_Rate"].mean().round(2)
    m2 = df2.groupby(df2["Date"].dt.to_period("M"))["Unemployment_Rate"].mean().round(2)
    monthly_combined = pd.DataFrame({"Dataset1_RuralUrban_Avg": m1, "Dataset2_State_Avg": m2})
    print(monthly_combined)

    # State-level impact
    print("\n=== TOP 10 STATES BY PEAK UNEMPLOYMENT (Dataset 2, 2020) ===")
    state_stats = df2.groupby("State")["Unemployment_Rate"].agg(["mean", "max", "min"]).sort_values("mean", ascending=False)
    print(state_stats.head(10).round(2))

    print("\n=== BOTTOM 5 STATES BY MEAN UNEMPLOYMENT (Dataset 2, 2020) ===")
    print(state_stats.tail(5).round(2))

    # Zone-level impact
    print("\n=== ZONAL UNEMPLOYMENT BY PERIOD (Dataset 2, 2020) ===")
    zone_period = df2.pivot_table(index="Zone", columns="Period", values="Unemployment_Rate", aggfunc="mean")
    print(zone_period.round(2))

    return monthly_combined, state_stats, zone_period


def generate_plots(df1, df2):
    # Plot 1: Monthly Unemployment Rate Trend (May 2019 - Oct 2020)
    m1 = df1.groupby("Date")["Unemployment_Rate"].mean().reset_index()
    m2 = df2.groupby("Date")["Unemployment_Rate"].mean().reset_index()

    fig, ax = plt.subplots(figsize=(12, 5.5))
    ax.plot(m1["Date"], m1["Unemployment_Rate"], marker="o", linewidth=2.2, label="Dataset 1 (Rural/Urban Avg, May 2019–Jun 2020)", color="#1f77b4")
    ax.plot(m2["Date"], m2["Unemployment_Rate"], marker="s", linewidth=2.2, linestyle="--", label="Dataset 2 (State Avg, Jan–Oct 2020)", color="#d62728")
    ax.axvspan(pd.Timestamp("2020-03-15"), pd.Timestamp("2020-06-30"), color="#ff9896", alpha=0.25, label="Covid-19 Lockdown & Peak")
    ax.set_title("India Monthly Unemployment Rate Trend (May 2019 – Oct 2020)", fontsize=14, fontweight="bold")
    ax.set_xlabel("Date", fontsize=11)
    ax.set_ylabel("Estimated Unemployment Rate (%)", fontsize=11)
    ax.legend(frameon=True)
    fig.tight_layout()
    fig.savefig(os.path.join(OUTPUT_DIR, "01_monthly_unemployment_trend.png"), dpi=150)
    plt.close(fig)

    # Plot 2: Rural vs Urban Unemployment Over Time
    ru_trend = df1.groupby(["Date", "Area"])["Unemployment_Rate"].mean().unstack("Area")
    fig, ax = plt.subplots(figsize=(11, 5))
    for area, color in [("Rural", "#2ca02c"), ("Urban", "#ff7f0e")]:
        if area in ru_trend.columns:
            ax.plot(ru_trend.index, ru_trend[area], marker="o", linewidth=2.2, label=area, color=color)
    ax.axvspan(pd.Timestamp("2020-03-15"), pd.Timestamp("2020-06-30"), color="gray", alpha=0.18, label="Covid-19 Lockdown")
    ax.set_title("Rural vs. Urban Unemployment Rate in India (May 2019 – Jun 2020)", fontsize=14, fontweight="bold")
    ax.set_xlabel("Date", fontsize=11)
    ax.set_ylabel("Estimated Unemployment Rate (%)", fontsize=11)
    ax.legend(frameon=True)
    fig.tight_layout()
    fig.savefig(os.path.join(OUTPUT_DIR, "02_rural_vs_urban_covid.png"), dpi=150)
    plt.close(fig)

    # Plot 3: Top 10 States - Pre-Covid vs Lockdown Unemployment (Dataset 2)
    state_period = df2.pivot_table(index="State", columns="Period", values="Unemployment_Rate", aggfunc="mean")
    top10 = state_period.sort_values("Covid Lockdown (Mar-Jun 2020)", ascending=False).head(10)
    cols_order = [c for c in ["Pre-Covid (Jan-Feb 2020)", "Covid Lockdown (Mar-Jun 2020)", "Post-Lockdown (Jul-Oct 2020)"] if c in top10.columns]
    top10 = top10[cols_order]

    fig, ax = plt.subplots(figsize=(12, 6))
    top10.plot(kind="bar", ax=ax, width=0.78, color=["#4c72b0", "#c44e52", "#55a868"])
    ax.set_title("Top 10 States by Covid-19 Lockdown Unemployment Rate (2020)", fontsize=14, fontweight="bold")
    ax.set_xlabel("State", fontsize=11)
    ax.set_ylabel("Mean Unemployment Rate (%)", fontsize=11)
    plt.xticks(rotation=30, ha="right")
    ax.legend(title="Period", frameon=True)
    fig.tight_layout()
    fig.savefig(os.path.join(OUTPUT_DIR, "03_state_covid_impact.png"), dpi=150)
    plt.close(fig)

    # Plot 4: Zonal Monthly Heatmap (Jan 2020 - Oct 2020)
    df2["Month"] = df2["Date"].dt.strftime("%Y-%m")
    zone_month = df2.pivot_table(index="Zone", columns="Month", values="Unemployment_Rate", aggfunc="mean")
    fig, ax = plt.subplots(figsize=(11, 4.8))
    im = ax.imshow(zone_month.values, cmap="YlOrRd", aspect="auto")
    ax.set_xticks(range(len(zone_month.columns)))
    ax.set_xticklabels(zone_month.columns, rotation=30, ha="right")
    ax.set_yticks(range(len(zone_month.index)))
    ax.set_yticklabels(zone_month.index)
    for i in range(zone_month.shape[0]):
        for j in range(zone_month.shape[1]):
            val = zone_month.values[i, j]
            if not np.isnan(val):
                ax.text(j, i, f"{val:.1f}", ha="center", va="center", color="black", fontsize=9)
    fig.colorbar(im, ax=ax, label="Unemployment Rate (%)")
    ax.set_title("Regional (Zone) Monthly Unemployment Rate (%) Heatmap (2020)", fontsize=14, fontweight="bold")
    ax.set_xlabel("Month", fontsize=11)
    ax.set_ylabel("Zone", fontsize=11)
    fig.tight_layout()
    fig.savefig(os.path.join(OUTPUT_DIR, "04_regional_zone_heatmap.png"), dpi=150)
    plt.close(fig)

    print(f"\nSaved 4 visualization plots to '{OUTPUT_DIR}/'.")


if __name__ == "__main__":
    df1, df2 = load_and_clean_data()
    analyze_data(df1, df2)
    generate_plots(df1, df2)
