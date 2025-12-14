import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
import os

# ====================================================================
# 1. DATA LOADING - PUT YOUR FILE PATH HERE
# ====================================================================

# Replace this with the full path to your Excel file
file_path = r'C:\Users\moham\OneDrive\Documents\poluution_atmospherique\moyhoraire hayhassani 2014.xlsx'

try:
    print(f"Loading file: {file_path}")
    # Load with proper column names and skip the first 2 rows (header + units row)
    df = pd.read_excel(file_path, sheet_name='horaire', decimal=',', skiprows=2, header=None)
    
    # Set proper column names based on your data structure
    column_names = [
        'datetime',
        'NO2', 
        'O3',
        'PM10',
        'SO2',
        'CO',
        'WD',
        'WS',
        'TEMP',
        'HUM'
    ]
    
    df.columns = column_names
    print("File loaded successfully!")
    
except FileNotFoundError:
    print(f"Error: File '{file_path}' not found.")
    print("Please check the path and try again.")
    exit()
except Exception as e:
    print(f"Error during loading: {e}")
    exit()

# ====================================================================
# 2. DATA INSPECTION
# ====================================================================

print("\n" + "="*50)
print("DATA INSPECTION")
print("="*50)

print(f"Dimensions: {df.shape[0]} rows x {df.shape[1]} columns")
print(f"Available columns: {list(df.columns)}")

print("\nFirst rows preview:")
print(df.head())

print("\nData types information:")
print(df.info())

# ====================================================================
# 3. DATA CONVERSION AND CLEANING
# ====================================================================

print("\n" + "="*50)
print("DATA PREPARATION")
print("="*50)

# Check what's in the datetime column
print(f"First few datetime values: {df['datetime'].head()}")

# Convert datetime
try:
    df['datetime'] = pd.to_datetime(df['datetime'])
    print("Datetime conversion successful")
except Exception as e:
    print(f"Datetime conversion error: {e}")
    # Try to convert the first column as datetime
    try:
        df['datetime'] = pd.to_datetime(df.iloc[:, 0])
        print("Conversion with first column successful")
    except Exception as e2:
        print(f"Second conversion attempt error: {e2}")
        exit()

# Create time variables
df['month'] = df['datetime'].dt.month
df['hour'] = df['datetime'].dt.hour
df['dayofweek'] = df['datetime'].dt.dayofweek
df['year'] = df['datetime'].dt.year
df['day'] = df['datetime'].dt.day

print(f"Covered period: {df['datetime'].min()} to {df['datetime'].max()}")

# ====================================================================
# 4. COMPLETE STATISTICAL ANALYSIS
# ====================================================================

print("\n" + "="*50)
print("COMPLETE STATISTICAL ANALYSIS 2014")
print("="*50)

print(f"Total hours: {len(df):,}")
print(f"Total days: {df['datetime'].dt.date.nunique():,}")
print(f"Year(s): {df['year'].unique()}")

# Pollutant columns
pollutant_columns = ['NO2', 'O3', 'PM10', 'SO2', 'CO']

print(f"\nPollutant columns: {pollutant_columns}")

# Statistics for each pollutant
for pollutant in pollutant_columns:
    if pollutant in df.columns:
        # Convert to numeric, handling any non-numeric values
        data = pd.to_numeric(df[pollutant], errors='coerce').dropna()
        if len(data) > 0:
            print(f"\n--- {pollutant} ---")
            print(f"Valid data: {len(data)} ({len(data)/len(df)*100:.1f}%)")
            print(f"Mean: {data.mean():.2f}")
            print(f"Median: {data.median():.2f}")
            print(f"Std: {data.std():.2f}")
            print(f"Min: {data.min():.2f}")
            print(f"Max: {data.max():.2f}")
            print(f"95th percentile: {data.quantile(0.95):.2f}")
            print(f"75th percentile: {data.quantile(0.75):.2f}")

# ====================================================================
# 5. METEOROLOGICAL DATA ANALYSIS
# ====================================================================

print("\n" + "="*50)
print("METEOROLOGICAL DATA ANALYSIS")
print("="*50)

# Wind analysis
if 'WD' in df.columns:
    wind_data = df['WD'].dropna()
    if len(wind_data) > 0:
        print(f"Dominant wind direction: {wind_data.mode().iloc[0] if not wind_data.mode().empty else 'N/A'}")
        wind_counts = df['WD'].value_counts()
        print("\nTop 5 wind directions:")
        for direction, count in wind_counts.head(5).items():
            print(f"  {direction}: {count} hours ({count/len(df)*100:.1f}%)")

if 'WS' in df.columns:
    ws_data = pd.to_numeric(df['WS'], errors='coerce').dropna()
    if len(ws_data) > 0:
        print(f"Wind speed - Mean: {ws_data.mean():.2f} m/s")
        print(f"Wind speed - Max: {ws_data.max():.2f} m/s")
        print(f"Wind speed - Std: {ws_data.std():.2f} m/s")

# Temperature and humidity
if 'TEMP' in df.columns:
    temp_data = pd.to_numeric(df['TEMP'], errors='coerce').dropna()
    if len(temp_data) > 0:
        print(f"Temperature - Mean: {temp_data.mean():.1f} C")
        print(f"Temperature - Min: {temp_data.min():.1f} C")
        print(f"Temperature - Max: {temp_data.max():.1f} C")

if 'HUM' in df.columns:
    hum_data = pd.to_numeric(df['HUM'], errors='coerce').dropna()
    if len(hum_data) > 0:
        print(f"Humidity - Mean: {hum_data.mean():.1f}%")
        print(f"Humidity - Min: {hum_data.min():.1f}%")
        print(f"Humidity - Max: {hum_data.max():.1f}%")

# ====================================================================
# 6. THRESHOLD EXCEEDANCE ANALYSIS
# ====================================================================

print("\n" + "="*50)
print("THRESHOLD EXCEEDANCE ANALYSIS")
print("="*50)

thresholds = {
    'NO2': 40,    # WHO guideline (μg/m³)
    'PM10': 45,   # WHO guideline (μg/m³)
    'SO2': 20,    # WHO guideline (μg/m³)
    'CO': 4       # WHO guideline (mg/m³)
}

for pollutant, threshold in thresholds.items():
    if pollutant in df.columns:
        pollutant_data = pd.to_numeric(df[pollutant], errors='coerce')
        exceedances = (pollutant_data > threshold).sum()
        if exceedances > 0:
            print(f"{pollutant}: {exceedances} hours > {threshold} ({exceedances/len(df)*100:.1f}%)")

# ====================================================================
# 7. TEMPORAL ANALYSIS
# ====================================================================

print("\n" + "="*50)
print("TEMPORAL ANALYSIS")
print("="*50)

# Monthly variations
print("\nMonthly averages:")
for pollutant in pollutant_columns[:3]:  # First 3 pollutants
    if pollutant in df.columns:
        pollutant_data = pd.to_numeric(df[pollutant], errors='coerce')
        monthly_avg = df.groupby('month')[pollutant].mean()
        print(f"{pollutant}:")
        for month, value in monthly_avg.items():
            print(f"  Month {month}: {value:.2f}")

# Hourly variations
print("\nDiurnal patterns (hourly averages):")
for pollutant in pollutant_columns[:2]:  # First 2 pollutants
    if pollutant in df.columns:
        pollutant_data = pd.to_numeric(df[pollutant], errors='coerce')
        hourly_avg = df.groupby('hour')[pollutant].mean()
        peak_hour = hourly_avg.idxmax()
        print(f"{pollutant}: Peak at {peak_hour}:00 ({hourly_avg.max():.1f})")

# ====================================================================
# 8. DATA VISUALIZATION
# ====================================================================

print("\n" + "="*50)
print("GENERATING VISUALIZATIONS")
print("="*50)

plt.figure(figsize=(15, 12))

# Plot 1: Monthly trends
plt.subplot(2, 2, 1)
for pollutant in ['NO2', 'O3']:
    if pollutant in df.columns:
        pollutant_data = pd.to_numeric(df[pollutant], errors='coerce')
        monthly = df.groupby('month')[pollutant].mean()
        plt.plot(monthly.index, monthly.values, marker='o', label=pollutant)
plt.title('Monthly Trends of Main Pollutants')
plt.xlabel('Month')
plt.ylabel('Concentration (μg/m³)')
plt.legend()
plt.grid(True)

# Plot 2: Diurnal variations
plt.subplot(2, 2, 2)
for pollutant in ['NO2', 'O3']:
    if pollutant in df.columns:
        pollutant_data = pd.to_numeric(df[pollutant], errors='coerce')
        hourly = df.groupby('hour')[pollutant].mean()
        plt.plot(hourly.index, hourly.values, marker='o', label=pollutant)
plt.title('Diurnal Variations')
plt.xlabel('Hour of Day')
plt.ylabel('Concentration (μg/m³)')
plt.legend()
plt.grid(True)

# Plot 3: Wind distribution
plt.subplot(2, 2, 3)
if 'WD' in df.columns:
    wind_counts = df['WD'].value_counts()
    plt.pie(wind_counts.values, labels=wind_counts.index, autopct='%1.1f%%', startangle=90)
    plt.title('Wind Direction Distribution')

# Plot 4: Correlation matrix
plt.subplot(2, 2, 4)
# Convert all pollutant data to numeric
corr_data = df[['NO2', 'O3', 'PM10', 'SO2', 'CO']].apply(lambda x: pd.to_numeric(x, errors='coerce'))
corr_matrix = corr_data.corr()
sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', center=0, fmt='.2f')
plt.title('Pollutant Correlations')

plt.tight_layout()
plt.show()

# ====================================================================
# 9. POLLUTION EPISODES ANALYSIS
# ====================================================================

print("\n" + "="*50)
print("POLLUTION EPISODES ANALYSIS")
print("="*50)

for pollutant in ['NO2', 'PM10', 'SO2']:
    if pollutant in df.columns:
        pollutant_data = pd.to_numeric(df[pollutant], errors='coerce')
        max_val = pollutant_data.max()
        max_idx = pollutant_data.idxmax()
        max_date = df.loc[max_idx, 'datetime']
        print(f"Maximum {pollutant}: {max_val:.1f} on {max_date}")

# ====================================================================
# 10. STATION ASSESSMENT SUMMARY
# ====================================================================

print("\n" + "="*50)
print("STATION ASSESSMENT SUMMARY")
print("="*50)

# Data coverage assessment
total_hours_year = 8760
data_coverage = (len(df) / total_hours_year) * 100

print(f"Station: Hay Hassani")
print(f"Data coverage: {data_coverage:.1f}% of year")
print(f"Station type: Urban background")
print(f"Main pollutants: {', '.join(pollutant_columns)}")

# Data quality flags
print("\nData quality assessment:")
for pollutant in pollutant_columns:
    if pollutant in df.columns:
        pollutant_data = pd.to_numeric(df[pollutant], errors='coerce')
        coverage = (pollutant_data.notna().sum() / len(df)) * 100
        status = "GOOD" if coverage > 80 else "MODERATE" if coverage > 50 else "POOR"
        print(f"  {pollutant}: {coverage:.1f}% coverage - {status}")

# ====================================================================
# 11. EXPORT RESULTS
# ====================================================================

print("\n" + "="*50)
print("EXPORTING RESULTS")
print("="*50)

# Create results summary
results_summary = {
    'analysis_date': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
    'data_file': file_path,
    'period_start': df['datetime'].min().strftime('%Y-%m-%d'),
    'period_end': df['datetime'].max().strftime('%Y-%m-%d'),
    'total_hours': len(df),
    'total_days': df['datetime'].dt.date.nunique(),
    'data_coverage_percent': data_coverage
}

# Add pollutant statistics
for pollutant in pollutant_columns:
    if pollutant in df.columns:
        pollutant_data = pd.to_numeric(df[pollutant], errors='coerce').dropna()
        if len(pollutant_data) > 0:
            results_summary[f'{pollutant}_mean'] = pollutant_data.mean()
            results_summary[f'{pollutant}_coverage'] = (len(pollutant_data)/len(df))*100
            results_summary[f'{pollutant}_max'] = pollutant_data.max()

# Export to CSV
output_filename = 'hayhassani_2014_analysis_results.csv'
df.to_csv(output_filename, index=False)
print(f"Data exported to: {output_filename}")

# Export summary
summary_df = pd.DataFrame([results_summary])
summary_filename = 'hayhassani_2014_analysis_summary.csv'
summary_df.to_csv(summary_filename, index=False)
print(f"Summary exported to: {summary_filename}")

print("\n" + "="*50)
print("ANALYSIS COMPLETE")
print("="*50)
print("Check the generated CSV files for detailed results")
print("Visualizations have been displayed above")
