# Unemployment Analysis with Python

This repository contains a Python-based data cleaning, exploration, and visualization analysis of India's unemployment rate data, with a focus on the impact of Covid-19, seasonal/monthly patterns, regional disparities, and policy insights.

## Project Files
- `unemployment_analysis.py` — Main Python script for data cleaning, statistical analysis, and chart generation.
- `Unemployment in India.csv` — Dataset covering May 2019 – June 2020 across 28 states (Rural & Urban).
- `Unemployment_Rate_upto_11_2020.csv` — Dataset covering January 2020 – October 2020 across 27 states and 5 zones.
- `plots/` — Generated visualizations:
  - `01_monthly_unemployment_trend.png`
  - `02_rural_vs_urban_covid.png`
  - `03_state_covid_impact.png`
  - `04_regional_zone_heatmap.png`

---

## 1. Data Cleaning & Exploration
- **Dataset 1 (`Unemployment in India.csv`)** (May 2019 – Jun 2020, 28 states, Rural & Urban):
  - Removed 28 completely empty rows (`768` raw → `740` clean rows), stripped whitespace from column names and string values, and parsed `Date` to datetime.
  - Overall mean unemployment rate: **11.79%** (median **8.35%**, max **76.74%**).
- **Dataset 2 (`Unemployment_Rate_upto_11_2020.csv`)** (Jan 2020 – Oct 2020, 27 states, 5 zones):
  - No missing values (`267` rows), renamed the duplicate `Region` column to `Zone`, and parsed `Date`.
  - Overall mean unemployment rate: **12.24%** (median **9.65%**, max **75.85%**).

---

## 2. Impact of Covid-19 on Unemployment Rates
- **Sharp Lockdown Spike (Mar–Jun 2020):**
  - In Dataset 1, mean unemployment nearly doubled from **9.51%** (Pre-Covid: May 2019–Feb 2020) to **17.77%** during the lockdown (Mar–Jun 2020).
  - In Dataset 2, mean unemployment jumped from **9.23%** (Jan–Feb 2020) to **16.74%** (Mar–Jun 2020), peaking in **April 2020 (22.24%–23.64%)** and **May 2020 (23.24%–24.88%)**.
- **V-Shaped Post-Lockdown Recovery (Jul–Oct 2020):**
  - By Jul–Oct 2020, mean unemployment in Dataset 2 returned to **9.22%** (and **8.03%** in October 2020), closely matching pre-Covid levels, though labour participation remained slightly depressed.

---

## 3. Seasonal & Monthly Patterns
- **Pre-Covid Stability (May 2019 – Feb 2020):** Monthly unemployment stayed within a narrow band of **8.87% to 9.96%**, with mild seasonal upticks around **October–November 2019 (~9.87%–9.90%)** and **January–February 2020 (~9.95%–9.96%)**.
- **Structural Break vs. Seasonality:** The April–May 2020 surge (**>23%**) was an exogenous pandemic shock rather than a seasonal cycle, followed by rapid normalization from June 2020 (**10.91%–11.90%**) onward.

---

## 4. Regional & Rural-Urban Disparities
- **Urban vs. Rural Divide:** Urban areas experienced consistently higher unemployment both before (**10.84%** vs. **8.09%** rural) and during the lockdown (**19.28%** vs. **16.18%** rural), alongside a steeper drop in urban labour participation (**42.31% → 37.21%**).
- **Hardest-Hit States (2020 Mean / Peak):**
  - **Haryana** (27.48% mean, 43.22% max)
  - **Tripura** (25.06% mean, 41.23% max)
  - **Jharkhand** (19.54% mean, 59.23% max)
  - **Bihar** (19.47% mean, 46.64% max)
  - **Puducherry** (17.94% mean, 75.85% max)
- **Zonal Impact:** **East** (7.53% → 22.65%) and **South** (4.21% → 18.36%) saw the sharpest relative lockdown spikes, whereas **West** (6.00% → 11.03%) and **Northeast** (12.56% → 13.37%) were comparatively more resilient.

---

## 5. Policy Insights
1. **Targeted Urban & Informal Sector Safety Nets:** Because urban unemployment surged to **19.28%** and labour participation fell sharply, crisis-response policies should prioritize urban wage subsidies, portable social security, and cash transfers for informal/service-sector workers.
2. **State-Specific & Zonal Interventions:** High-unemployment states (e.g., Haryana, Tripura, Jharkhand, Bihar) require structural job-creation programs and localized skill-matching rather than uniform national policies.
3. **Rapid-Response Stabilization:** The V-shaped recovery after June 2020 shows that temporary liquidity support and MSME credit guarantees during acute shocks can prevent short-term lockdowns from turning into long-term structural unemployment.
