import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats

# ====================================================================
# TEMPERATURE AND HUMIDITY ANALYSIS
# ====================================================================

print("="*60)
print("TEMPERATURE AND HUMIDITY ANALYSIS")
print("="*60)

# 1. DESCRIPTIVE STATISTICS
print("\n1. DESCRIPTIVE STATISTICS")
print("-" * 40)

# Hourly statistics
print("Hourly statistics:")
temp_stats = df['TEMP'].describe()
hum_stats = df['HUM'].describe()

print(f"TEMPERATURE:")
print(f"  Mean: {temp_stats['mean']:.1f}°C")
print(f"  Std:  {temp_stats['std']:.1f}°C")
print(f"  Min:  {temp_stats['min']:.1f}°C")
print(f"  Max:  {temp_stats['max']:.1f}°C")

print(f"HUMIDITY:")
print(f"  Mean: {hum_stats['mean']:.1f}%")
print(f"  Std:  {hum_stats['std']:.1f}%")
print(f"  Min:  {hum_stats['min']:.1f}%")
print(f"  Max:  {hum_stats['max']:.1f}%")

# Daily statistics
print("\nDaily statistics:")
daily_data = df.groupby(df['datetime'].dt.date).agg({
    'TEMP': ['mean', 'min', 'max', 'std'],
    'HUM': ['mean', 'min', 'max', 'std']
}).round(1)

print(f"Temperature - Daily mean: {daily_data['TEMP']['mean'].mean():.1f}°C")
print(f"Temperature - Daily amplitude: {(daily_data['TEMP']['max'] - daily_data['TEMP']['min']).mean():.1f}°C")
print(f"Humidity - Daily mean: {daily_data['HUM']['mean'].mean():.1f}%")

# Monthly statistics
print("\nMonthly statistics:")
monthly_temp = df.groupby('month')['TEMP'].agg(['mean', 'min', 'max', 'std']).round(1)
monthly_hum = df.groupby('month')['HUM'].agg(['mean', 'min', 'max', 'std']).round(1)

print("Monthly temperature means:")
for month, row in monthly_temp.iterrows():
    print(f"  Month {month}: {row['mean']}°C")

print("Monthly humidity means:")
for month, row in monthly_hum.iterrows():
    print(f"  Month {month}: {row['mean']}%")

# 2. DIURNAL PROFILES
print("\n2. DIURNAL PROFILES")
print("-" * 40)

# Hourly averages
hourly_temp = df.groupby('hour')['TEMP'].mean()
hourly_hum = df.groupby('hour')['HUM'].mean()

print("Temperature diurnal variation:")
min_temp_hour = hourly_temp.idxmin()
max_temp_hour = hourly_temp.idxmax()
print(f"  Minimum: {hourly_temp.min():.1f}°C at {min_temp_hour}:00")
print(f"  Maximum: {hourly_temp.max():.1f}°C at {max_temp_hour}:00")
print(f"  Daily amplitude: {hourly_temp.max() - hourly_temp.min():.1f}°C")

print("Humidity diurnal variation:")
min_hum_hour = hourly_hum.idxmin()
max_hum_hour = hourly_hum.idxmax()
print(f"  Minimum: {hourly_hum.min():.1f}% at {min_hum_hour}:00")
print(f"  Maximum: {hourly_hum.max():.1f}% at {max_hum_hour}:00")

# 3. SEASONAL PROFILES
print("\n3. SEASONAL PROFILES")
print("-" * 40)

# Define seasons
def get_season(month):
    if month in [12, 1, 2]:
        return 'Winter'
    elif month in [3, 4, 5]:
        return 'Spring'
    elif month in [6, 7, 8]:
        return 'Summer'
    else:
        return 'Autumn'

df['season'] = df['month'].apply(get_season)

seasonal_stats = df.groupby('season').agg({
    'TEMP': ['mean', 'min', 'max'],
    'HUM': ['mean', 'min', 'max']
}).round(1)

print("Seasonal statistics:")
for season in ['Winter', 'Spring', 'Summer', 'Autumn']:
    temp_mean = seasonal_stats.loc[season, ('TEMP', 'mean')]
    hum_mean = seasonal_stats.loc[season, ('HUM', 'mean')]
    print(f"  {season}: {temp_mean}°C, {hum_mean}% humidity")

# 4. RELATIONSHIPS WITH POLLUTANTS
print("\n4. RELATIONSHIPS WITH POLLUTANTS")
print("-" * 40)

# Calculate correlations
pollutants = ['O3', 'PM10', 'NO2', 'SO2', 'CO']
correlation_results = {}

for pollutant in pollutants:
    if pollutant in df.columns:
        # Clean data
        temp_clean = pd.to_numeric(df['TEMP'], errors='coerce')
        hum_clean = pd.to_numeric(df['HUM'], errors='coerce')
        poll_clean = pd.to_numeric(df[pollutant], errors='coerce')
        
        # Calculate correlations
        corr_temp = temp_clean.corr(poll_clean)
        corr_hum = hum_clean.corr(poll_clean)
        
        correlation_results[pollutant] = {
            'temp_corr': corr_temp,
            'hum_corr': corr_hum
        }
        
        print(f"{pollutant}:")
        print(f"  Correlation with temperature: {corr_temp:.3f}")
        print(f"  Correlation with humidity: {corr_hum:.3f}")

# 5. TEMPERATURE INVERSIONS ANALYSIS
print("\n5. TEMPERATURE INVERSIONS ANALYSIS")
print("-" * 40)

# Identify nocturnal inversions (cooling at night)
df['hour'] = df['datetime'].dt.hour
nocturnal_hours = [20, 21, 22, 23, 0, 1, 2, 3, 4, 5]  # 8 PM to 5 AM
daytime_hours = [6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19]  # 6 AM to 7 PM

nocturnal_data = df[df['hour'].isin(nocturnal_hours)]
daytime_data = df[df['hour'].isin(daytime_hours)]

# Calculate inversion strength (temperature drop at night)
inversion_strength = daytime_data['TEMP'].mean() - nocturnal_data['TEMP'].mean()
print(f"Average nocturnal inversion strength: {inversion_strength:.1f}°C")

# Analyze pollution during inversions
print("\nPollution levels during inversions:")
for pollutant in ['PM10', 'NO2', 'O3']:
    if pollutant in df.columns:
        nocturnal_poll = nocturnal_data[pollutant].mean()
        daytime_poll = daytime_data[pollutant].mean()
        ratio = nocturnal_poll / daytime_poll if daytime_poll > 0 else 0
        
        print(f"{pollutant}:")
        print(f"  Nocturnal: {nocturnal_poll:.1f}")
        print(f"  Daytime: {daytime_poll:.1f}")
        print(f"  Nocturnal/Daytime ratio: {ratio:.2f}")

# 6. VISUALIZATIONS
print("\n6. GENERATING VISUALIZATIONS")
print("-" * 40)

plt.figure(figsize=(20, 15))

# Plot 1: Diurnal profiles
plt.subplot(3, 3, 1)
plt.plot(hourly_temp.index, hourly_temp.values, 'r-', linewidth=2, label='Temperature')
plt.xlabel('Hour of Day')
plt.ylabel('Temperature (°C)')
plt.title('Diurnal Temperature Profile')
plt.grid(True, alpha=0.3)
plt.legend()

plt.subplot(3, 3, 2)
plt.plot(hourly_hum.index, hourly_hum.values, 'b-', linewidth=2, label='Humidity')
plt.xlabel('Hour of Day')
plt.ylabel('Humidity (%)')
plt.title('Diurnal Humidity Profile')
plt.grid(True, alpha=0.3)
plt.legend()

# Plot 2: Monthly profiles
plt.subplot(3, 3, 3)
months = range(1, 13)
plt.plot(months, monthly_temp['mean'], 'ro-', linewidth=2, label='Temperature')
plt.xlabel('Month')
plt.ylabel('Temperature (°C)')
plt.title('Monthly Temperature Profile')
plt.grid(True, alpha=0.3)

plt.subplot(3, 3, 4)
plt.plot(months, monthly_hum['mean'], 'bo-', linewidth=2, label='Humidity')
plt.xlabel('Month')
plt.ylabel('Humidity (%)')
plt.title('Monthly Humidity Profile')
plt.grid(True, alpha=0.3)

# Plot 3: Temperature vs O3
plt.subplot(3, 3, 5)
plt.scatter(df['TEMP'], df['O3'], alpha=0.3, s=1)
plt.xlabel('Temperature (°C)')
plt.ylabel('O3 (μg/m³)')
plt.title('Temperature vs Ozone')
plt.grid(True, alpha=0.3)

# Plot 4: Humidity vs PM10
plt.subplot(3, 3, 6)
plt.scatter(df['HUM'], df['PM10'], alpha=0.3, s=1)
plt.xlabel('Humidity (%)')
plt.ylabel('PM10 (μg/m³)')
plt.title('Humidity vs PM10')
plt.grid(True, alpha=0.3)

# Plot 5: Seasonal boxplots
plt.subplot(3, 3, 7)
season_order = ['Winter', 'Spring', 'Summer', 'Autumn']
df_boxplot = df[df['season'].isin(season_order)]
sns.boxplot(data=df_boxplot, x='season', y='TEMP', order=season_order)
plt.title('Temperature by Season')
plt.ylabel('Temperature (°C)')

plt.subplot(3, 3, 8)
sns.boxplot(data=df_boxplot, x='season', y='HUM', order=season_order)
plt.title('Humidity by Season')
plt.ylabel('Humidity (%)')

# Plot 6: Heatmap of correlations
plt.subplot(3, 3, 9)
# Prepare correlation matrix
corr_matrix = df[['TEMP', 'HUM', 'O3', 'PM10', 'NO2']].corr()
sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', center=0, fmt='.2f')
plt.title('Temperature/Humidity-Pollutant Correlations')

plt.tight_layout()
plt.show()

# 7. INTERPRETATION AND INSIGHTS
print("\n7. INTERPRETATION AND INSIGHTS")
print("-" * 40)

print("KEY FINDINGS:")

# Temperature patterns
print("\nTEMPERATURE PATTERNS:")
print(f"• Annual range: {temp_stats['max'] - temp_stats['min']:.1f}°C")
print(f"• Diurnal amplitude: {hourly_temp.max() - hourly_temp.min():.1f}°C")
print(f"• Warmest month: {monthly_temp['mean'].idxmax()} ({monthly_temp['mean'].max():.1f}°C)")
print(f"• Coldest month: {monthly_temp['mean'].idxmin()} ({monthly_temp['mean'].min():.1f}°C)")

# Humidity patterns
print("\nHUMIDITY PATTERNS:")
print(f"• Annual average: {hum_stats['mean']:.1f}%")
print(f"• Driest month: {monthly_hum['mean'].idxmin()} ({monthly_hum['mean'].min():.1f}%)")
print(f"• Most humid month: {monthly_hum['mean'].idxmax()} ({monthly_hum['mean'].max():.1f}%)")

# Pollutant relationships
print("\nPOLLUTANT RELATIONSHIPS:")
for pollutant, corrs in correlation_results.items():
    temp_corr = corrs['temp_corr']
    hum_corr = corrs['hum_corr']
    
    temp_relation = "positive" if temp_corr > 0.1 else "negative" if temp_corr < -0.1 else "weak"
    hum_relation = "positive" if hum_corr > 0.1 else "negative" if hum_corr < -0.1 else "weak"
    
    print(f"• {pollutant}: {temp_relation} correlation with temperature, {hum_relation} correlation with humidity")

# Inversion impacts
print("\nNOCTURNAL INVERSIONS:")
print(f"• Average inversion strength: {inversion_strength:.1f}°C")
print("• Primary pollutants affected by inversions:")
for pollutant in ['PM10', 'NO2']:
    if pollutant in df.columns:
        nocturnal_ratio = nocturnal_data[pollutant].mean() / daytime_data[pollutant].mean()
        if nocturnal_ratio > 1.2:
            print(f"  - {pollutant}: accumulates during inversions (ratio: {nocturnal_ratio:.2f})")

# Ozone formation conditions
print("\nOZONE FORMATION CONDITIONS:")
o3_temp_corr = correlation_results.get('O3', {}).get('temp_corr', 0)
o3_hum_corr = correlation_results.get('O3', {}).get('hum_corr', 0)
print(f"• Ozone shows strong temperature dependence (correlation: {o3_temp_corr:.3f})")
print(f"• Ozone-humidity relationship: {o3_hum_corr:.3f}")

print("\n" + "="*60)
print("ANALYSIS COMPLETE")
print("="*60)
