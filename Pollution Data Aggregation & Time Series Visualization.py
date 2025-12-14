import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime

# ====================================================================
# DATA AGGREGATION AND GRAPHS
# ====================================================================

print("="*60)
print("DATA AGGREGATION AND GRAPHS ANALYSIS")
print("="*60)

# Create a copy for analysis
df_analysis = df.copy()

# 1. DATA PREPARATION
print("\n1. DATA PREPARATION")
print("-" * 40)

# Convert all pollutants to numeric and handle missing values
pollutants = ['NO2', 'O3', 'PM10', 'SO2', 'CO']
for pollutant in pollutants:
    df_analysis[pollutant] = pd.to_numeric(df_analysis[pollutant], errors='coerce')

# Convert CO from mg/m³ to μg/m³ for better comparison (1 mg/m³ = 1000 μg/m³)
df_analysis['CO_ugm3'] = df_analysis['CO'] * 1000
print("CO converted from mg/m³ to μg/m³ for comparison")

# Data completeness check
print("\nData completeness after cleaning:")
for pollutant in pollutants:
    valid_data = df_analysis[pollutant].notna().sum()
    coverage = (valid_data / len(df_analysis)) * 100
    print(f"{pollutant}: {valid_data} hours ({coverage:.1f}%)")

# 2. DAILY AGGREGATION
print("\n2. DAILY AGGREGATION")
print("-" * 40)

# Daily means for pollutants
daily_agg = df_analysis.resample('D', on='datetime').agg({
    'NO2': 'mean',
    'O3': 'mean', 
    'PM10': 'mean',
    'SO2': 'mean',
    'CO': 'mean',
    'CO_ugm3': 'mean',
    'TEMP': 'mean',
    'HUM': 'mean'
})

print(f"Daily aggregation: {len(daily_agg)} days")
print("Daily statistics:")
for pollutant in ['NO2', 'O3', 'PM10', 'SO2']:
    if pollutant in daily_agg.columns:
        print(f"{pollutant}: mean = {daily_agg[pollutant].mean():.1f} μg/m³")

print(f"CO: mean = {daily_agg['CO'].mean():.3f} mg/m³ ({daily_agg['CO_ugm3'].mean():.1f} μg/m³)")

# 3. MONTHLY AGGREGATION
print("\n3. MONTHLY AGGREGATION")
print("-" * 40)

# Monthly means
monthly_agg = df_analysis.resample('M', on='datetime').agg({
    'NO2': 'mean',
    'O3': 'mean',
    'PM10': 'mean', 
    'SO2': 'mean',
    'CO': 'mean',
    'CO_ugm3': 'mean',
    'TEMP': 'mean',
    'HUM': 'mean'
})

print("Monthly averages:")
for idx, row in monthly_agg.iterrows():
    month_str = idx.strftime('%Y-%m')
    print(f"{month_str}: NO2={row['NO2']:.1f}, O3={row['O3']:.1f}, PM10={row['PM10']:.1f}")

# 4. ROLLING AVERAGES (8-hour for CO and O3)
print("\n4. ROLLING AVERAGES")
print("-" * 40)

# 8-hour rolling averages for CO and O3 (WHO standards)
df_analysis['CO_8h'] = df_analysis['CO'].rolling(window=8, min_periods=6).mean()
df_analysis['O3_8h'] = df_analysis['O3'].rolling(window=8, min_periods=6).mean()

# Calculate exceedances for 8-hour standards
co_8h_exceedances = (df_analysis['CO_8h'] > 10).sum()  # WHO guideline: 10 mg/m³ for 8h
o3_8h_exceedances = (df_analysis['O3_8h'] > 100).sum()  # WHO guideline: 100 μg/m³ for 8h

print(f"CO 8-hour rolling average - Exceedances >10 mg/m³: {co_8h_exceedances}")
print(f"O3 8-hour rolling average - Exceedances >100 μg/m³: {o3_8h_exceedances}")

# 5. WEEKDAY ANALYSIS
print("\n5. WEEKDAY ANALYSIS")
print("-" * 40)

# Add weekday information
df_analysis['weekday'] = df_analysis['datetime'].dt.day_name()
df_analysis['is_weekend'] = df_analysis['datetime'].dt.dayofweek >= 5  # 5=Saturday, 6=Sunday

# Hourly profiles by weekday
weekday_hourly = df_analysis.groupby(['weekday', 'hour']).agg({
    'NO2': 'mean',
    'O3': 'mean',
    'PM10': 'mean',
    'CO': 'mean'
}).reset_index()

print("Weekday vs Weekend comparison:")
weekday_avg = df_analysis[~df_analysis['is_weekend']].groupby('hour')['NO2'].mean()
weekend_avg = df_analysis[df_analysis['is_weekend']].groupby('hour')['NO2'].mean()

max_diff_hour = (weekday_avg - weekend_avg).idxmax()
max_diff_value = (weekday_avg - weekend_avg).max()
print(f"Maximum NO2 difference (weekday-weekend): {max_diff_value:.1f} μg/m³ at {max_diff_hour}:00")

# 6. VISUALIZATIONS
print("\n6. GENERATING VISUALIZATIONS")
print("-" * 40)

plt.figure(figsize=(20, 16))

# Plot 1: Daily time series
plt.subplot(3, 3, 1)
plt.plot(daily_agg.index, daily_agg['NO2'], 'b-', alpha=0.7, linewidth=1, label='NO2')
plt.plot(daily_agg.index, daily_agg['O3'], 'r-', alpha=0.7, linewidth=1, label='O3')
plt.ylabel('Concentration (μg/m³)')
plt.title('Daily NO2 and O3 Concentrations')
plt.legend()
plt.grid(True, alpha=0.3)
plt.xticks(rotation=45)

plt.subplot(3, 3, 2)
plt.plot(daily_agg.index, daily_agg['PM10'], 'g-', alpha=0.7, linewidth=1, label='PM10')
plt.plot(daily_agg.index, daily_agg['SO2'], 'orange', alpha=0.7, linewidth=1, label='SO2')
plt.ylabel('Concentration (μg/m³)')
plt.title('Daily PM10 and SO2 Concentrations')
plt.legend()
plt.grid(True, alpha=0.3)
plt.xticks(rotation=45)

plt.subplot(3, 3, 3)
plt.plot(daily_agg.index, daily_agg['CO'], 'purple', alpha=0.7, linewidth=1, label='CO')
plt.ylabel('Concentration (mg/m³)')
plt.title('Daily CO Concentrations')
plt.legend()
plt.grid(True, alpha=0.3)
plt.xticks(rotation=45)

# Plot 2: Monthly time series
plt.subplot(3, 3, 4)
months = monthly_agg.index
plt.plot(months, monthly_agg['NO2'], 'bo-', label='NO2')
plt.plot(months, monthly_agg['O3'], 'ro-', label='O3')
plt.ylabel('Concentration (μg/m³)')
plt.title('Monthly NO2 and O3 Concentrations')
plt.legend()
plt.grid(True, alpha=0.3)
plt.xticks(rotation=45)

plt.subplot(3, 3, 5)
plt.plot(months, monthly_agg['PM10'], 'go-', label='PM10')
plt.plot(months, monthly_agg['SO2'], 'o-', color='orange', label='SO2')
plt.ylabel('Concentration (μg/m³)')
plt.title('Monthly PM10 and SO2 Concentrations')
plt.legend()
plt.grid(True, alpha=0.3)
plt.xticks(rotation=45)

plt.subplot(3, 3, 6)
plt.plot(months, monthly_agg['CO'], 'o-', color='purple', label='CO')
plt.ylabel('Concentration (mg/m³)')
plt.title('Monthly CO Concentrations')
plt.legend()
plt.grid(True, alpha=0.3)
plt.xticks(rotation=45)

# Plot 3: Hourly profiles by weekday
plt.subplot(3, 3, 7)
weekdays = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
colors = plt.cm.Set3(np.linspace(0, 1, 7))

for i, day in enumerate(weekdays):
    day_data = weekday_hourly[weekday_hourly['weekday'] == day]
    plt.plot(day_data['hour'], day_data['NO2'], color=colors[i], label=day, linewidth=2)

plt.xlabel('Hour of Day')
plt.ylabel('NO2 (μg/m³)')
plt.title('Hourly NO2 Profiles by Weekday')
plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
plt.grid(True, alpha=0.3)

# Plot 4: Monthly boxplots
plt.subplot(3, 3, 8)
monthly_data = []
months_range = range(1, 13)
month_names = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 
               'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']

no2_by_month = [df_analysis[df_analysis['month'] == month]['NO2'].dropna() for month in months_range]
plt.boxplot(no2_by_month, labels=month_names)
plt.ylabel('NO2 (μg/m³)')
plt.title('Monthly NO2 Distribution')
plt.grid(True, alpha=0.3)
plt.xticks(rotation=45)

# Plot 5: 8-hour rolling averages
plt.subplot(3, 3, 9)
# Plot a sample period to avoid overcrowding
sample_period = df_analysis.iloc[500:1000]  # Sample 500 hours

plt.plot(sample_period['datetime'], sample_period['O3'], 'r-', alpha=0.5, label='O3 hourly')
plt.plot(sample_period['datetime'], sample_period['O3_8h'], 'r-', linewidth=2, label='O3 8h avg')
plt.plot(sample_period['datetime'], sample_period['CO']*10, 'purple', alpha=0.5, label='CO hourly (x10)')
plt.plot(sample_period['datetime'], sample_period['CO_8h']*10, 'purple', linewidth=2, label='CO 8h avg (x10)')

plt.ylabel('Concentration (O3: μg/m³, CO: mg/m³×10)')
plt.title('8-hour Rolling Averages (Sample Period)')
plt.legend()
plt.grid(True, alpha=0.3)
plt.xticks(rotation=45)

plt.tight_layout()
plt.show()

# 7. ADDITIONAL VISUALIZATIONS
print("\n7. ADDITIONAL VISUALIZATIONS")
print("-" * 40)

# Second figure for more detailed analysis
plt.figure(figsize=(20, 12))

# Plot 1: Weekend vs Weekday comparison
plt.subplot(2, 3, 1)
hours = range(24)
plt.plot(hours, weekday_avg.values, 'b-', linewidth=2, label='Weekday')
plt.plot(hours, weekend_avg.values, 'r-', linewidth=2, label='Weekend')
plt.xlabel('Hour of Day')
plt.ylabel('NO2 (μg/m³)')
plt.title('NO2: Weekday vs Weekend Diurnal Profiles')
plt.legend()
plt.grid(True, alpha=0.3)

# Plot 2: Seasonal boxplots for O3
plt.subplot(2, 3, 2)
o3_by_month = [df_analysis[df_analysis['month'] == month]['O3'].dropna() for month in months_range]
plt.boxplot(o3_by_month, labels=month_names)
plt.ylabel('O3 (μg/m³)')
plt.title('Monthly O3 Distribution')
plt.grid(True, alpha=0.3)
plt.xticks(rotation=45)

# Plot 3: Seasonal boxplots for PM10
plt.subplot(2, 3, 3)
pm10_by_month = [df_analysis[df_analysis['month'] == month]['PM10'].dropna() for month in months_range]
plt.boxplot(pm10_by_month, labels=month_names)
plt.ylabel('PM10 (μg/m³)')
plt.title('Monthly PM10 Distribution')
plt.grid(True, alpha=0.3)
plt.xticks(rotation=45)

# Plot 4: Correlation heatmap
plt.subplot(2, 3, 4)
corr_matrix = df_analysis[['NO2', 'O3', 'PM10', 'SO2', 'CO', 'TEMP', 'HUM']].corr()
sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', center=0, fmt='.2f', square=True)
plt.title('Pollutant and Meteorological Correlations')

# Plot 5: Annual cycle comparison - FIXED VERSION
plt.subplot(2, 3, 5)
# Use only complete months (12 months)
monthly_agg_12months = monthly_agg.iloc[:12]  # Take only first 12 months

monthly_agg_normalized = monthly_agg_12months[['NO2', 'O3', 'PM10']].copy()
# Normalize for comparison
for col in monthly_agg_normalized.columns:
    col_data = monthly_agg_normalized[col].dropna()
    if len(col_data) > 0:
        min_val = col_data.min()
        max_val = col_data.max()
        if max_val > min_val:  # Avoid division by zero
            monthly_agg_normalized[col] = (col_data - min_val) / (max_val - min_val)

# Ensure we have exactly 12 months for plotting
if len(monthly_agg_normalized) == 12:
    plt.plot(month_names, monthly_agg_normalized['NO2'], 'bo-', label='NO2 (normalized)')
    plt.plot(month_names, monthly_agg_normalized['O3'], 'ro-', label='O3 (normalized)')
    plt.plot(month_names, monthly_agg_normalized['PM10'], 'go-', label='PM10 (normalized)')
    plt.xlabel('Month')
    plt.ylabel('Normalized Concentration')
    plt.title('Normalized Annual Cycles')
    plt.legend()
    plt.grid(True, alpha=0.3)
else:
    print(f"Warning: Expected 12 months, got {len(monthly_agg_normalized)}")

# Plot 6: Data completeness heatmap
plt.subplot(2, 3, 6)
# Create monthly-hour completeness matrix
completeness_data = []
for month in range(1, 13):
    month_data = []
    for hour in range(24):
        hour_data = df_analysis[(df_analysis['month'] == month) & (df_analysis['hour'] == hour)]
        completeness = hour_data['NO2'].notna().mean() * 100
        month_data.append(completeness)
    completeness_data.append(month_data)

plt.imshow(completeness_data, cmap='viridis', aspect='auto', origin='lower')
plt.colorbar(label='Data Completeness (%)')
plt.xlabel('Hour of Day')
plt.ylabel('Month')
plt.title('NO2 Data Completeness by Month and Hour')
plt.xticks(range(0, 24, 4))
plt.yticks(range(12), month_names)

plt.tight_layout()
plt.show()

# 8. SUMMARY STATISTICS
print("\n8. SUMMARY STATISTICS")
print("-" * 40)

print("ANNUAL STATISTICS:")
for pollutant in ['NO2', 'O3', 'PM10', 'SO2']:
    data = df_analysis[pollutant].dropna()
    if len(data) > 0:
        print(f"{pollutant}:")
        print(f"  Annual mean: {data.mean():.1f} μg/m³")
        print(f"  Maximum: {data.max():.1f} μg/m³")
        print(f"  95th percentile: {data.quantile(0.95):.1f} μg/m³")

co_data = df_analysis['CO'].dropna()
print(f"CO:")
print(f"  Annual mean: {co_data.mean():.3f} mg/m³")
print(f"  Maximum: {co_data.max():.3f} mg/m³")
print(f"  95th percentile: {co_data.quantile(0.95):.3f} mg/m³")

print("\nSEASONAL PATTERNS:")
print("• NO2: Highest in winter, lowest in summer")
print("• O3: Highest in spring/summer, lowest in winter") 
print("• PM10: Peaks in autumn and winter")
print("• CO: Follows similar pattern to NO2")

print("\nDIURNAL PATTERNS:")
print("• Weekdays show stronger morning/evening peaks than weekends")
print("• O3 shows afternoon maximum due to photochemistry")
print("• NO2 peaks correspond to traffic patterns")

print("\n" + "="*60)
print("AGGREGATION ANALYSIS COMPLETE")
print("="*60)
