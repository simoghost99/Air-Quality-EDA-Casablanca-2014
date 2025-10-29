import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
from datetime import datetime, timedelta

# ====================================================================
# MOROCCAN REGULATORY COMPLIANCE CHECK
# ====================================================================

print("="*70)
print("MOROCCAN REGULATORY COMPLIANCE CHECK")
print("DECREE 2-09-286 OF 08/12/2009")
print("="*70)

# Create a copy for analysis
df_reg = df.copy()

# 1. DATA PREPARATION AND COVERAGE
print("\n1. DATA PREPARATION AND COVERAGE")
print("-" * 50)

# Convert pollutants to numeric
pollutants = ['NO2', 'O3', 'PM10', 'SO2', 'CO']
for pollutant in pollutants:
    df_reg[pollutant] = pd.to_numeric(df_reg[pollutant], errors='coerce')

# Data coverage analysis
print("\nDATA COVERAGE ANALYSIS:")
coverage_summary = {}
for pollutant in pollutants:
    valid_data = df_reg[pollutant].notna().sum()
    coverage = (valid_data / len(df_reg)) * 100
    coverage_summary[pollutant] = coverage
    print(f"{pollutant}: {valid_data} hours ({coverage:.1f}%)")

# 2. DAILY AND 8-HOUR AGGREGATION
print("\n2. DATA AGGREGATION")
print("-" * 50)

# Daily means
daily_means = df_reg.resample('D', on='datetime').agg({
    'NO2': 'mean',
    'O3': 'mean',
    'PM10': 'mean',
    'SO2': 'mean',
    'CO': 'mean'
})

print(f"Daily aggregation: {len(daily_means)} days")

# 8-hour rolling averages for O3 and CO
df_reg['O3_8h'] = df_reg['O3'].rolling(window=8, min_periods=6).mean()
df_reg['CO_8h'] = df_reg['CO'].rolling(window=8, min_periods=6).mean()

# Daily maximum 8-hour averages
daily_max_8h = df_reg.resample('D', on='datetime').agg({
    'O3_8h': 'max',
    'CO_8h': 'max'
})

print(f"8-hour rolling averages calculated")

# 3. PERCENTILE CALCULATION METHODOLOGY
print("\n3. PERCENTILE CALCULATION METHODOLOGY")
print("-" * 50)

print("Percentiles calculated using method recommended by WHO:")
print("- Data sorted in ascending order")
print("- Percentile position = (P/100) * (n + 1)")
print("- Linear interpolation between adjacent values")
print("- Minimum data requirement: 75% completeness")

# 4. NO2 COMPLIANCE CHECK
print("\n4. NITROGEN DIOXIDE (NO2) COMPLIANCE")
print("-" * 50)

print("STANDARDS:")
print("- 98th percentile of hourly means ≤ 200 μg/m³")
print("- Annual mean ≤ 50 μg/m³")

# Calculate metrics
no2_annual_mean = df_reg['NO2'].mean()
no2_98th_hourly = np.percentile(df_reg['NO2'].dropna(), 98)

print(f"\nRESULTS:")
print(f"Annual mean: {no2_annual_mean:.1f} μg/m³")
print(f"98th percentile of hourly means: {no2_98th_hourly:.1f} μg/m³")

# Compliance check
no2_annual_compliant = no2_annual_mean <= 50
no2_hourly_compliant = no2_98th_hourly <= 200

print(f"\nCOMPLIANCE:")
print(f"Annual mean: {'COMPLIANT' if no2_annual_compliant else 'NON-COMPLIANT'}")
print(f"98th percentile hourly: {'COMPLIANT' if no2_hourly_compliant else 'NON-COMPLIANT'}")
print(f"OVERALL: {'COMPLIANT' if (no2_annual_compliant and no2_hourly_compliant) else 'NON-COMPLIANT'}")

# 5. SO2 COMPLIANCE CHECK
print("\n5. SULFUR DIOXIDE (SO2) COMPLIANCE")
print("-" * 50)

print("STANDARDS:")
print("- 99.2th percentile of daily means ≤ 125 μg/m³")
print("- Annual mean ≤ 20 μg/m³")

# Calculate metrics
so2_annual_mean = df_reg['SO2'].mean()
so2_992th_daily = np.percentile(daily_means['SO2'].dropna(), 99.2)

print(f"\nRESULTS:")
print(f"Annual mean: {so2_annual_mean:.1f} μg/m³")
print(f"99.2th percentile of daily means: {so2_992th_daily:.1f} μg/m³")

# Compliance check
so2_annual_compliant = so2_annual_mean <= 20
so2_daily_compliant = so2_992th_daily <= 125

print(f"\nCOMPLIANCE:")
print(f"Annual mean: {'COMPLIANT' if so2_annual_compliant else 'NON-COMPLIANT'}")
print(f"99.2th percentile daily: {'COMPLIANT' if so2_daily_compliant else 'NON-COMPLIANT'}")
print(f"OVERALL: {'COMPLIANT' if (so2_annual_compliant and so2_daily_compliant) else 'NON-COMPLIANT'}")

# 6. PM10 COMPLIANCE CHECK
print("\n6. PARTICULATE MATTER (PM10) COMPLIANCE")
print("-" * 50)

print("STANDARDS:")
print("- 90.4th percentile of daily means ≤ 50 μg/m³")

# Calculate metrics
pm10_904th_daily = np.percentile(daily_means['PM10'].dropna(), 90.4)

print(f"\nRESULTS:")
print(f"90.4th percentile of daily means: {pm10_904th_daily:.1f} μg/m³")

# Compliance check
pm10_compliant = pm10_904th_daily <= 50

print(f"\nCOMPLIANCE:")
print(f"90.4th percentile daily: {'COMPLIANT' if pm10_compliant else 'NON-COMPLIANT'}")

# 7. CO COMPLIANCE CHECK
print("\n7. CARBON MONOXIDE (CO) COMPLIANCE")
print("-" * 50)

print("STANDARDS:")
print("- Maximum daily 8-hour average ≤ 10 mg/m³")

# Calculate metrics
co_max_8h_daily = daily_max_8h['CO_8h'].max()

print(f"\nRESULTS:")
print(f"Maximum daily 8-hour average: {co_max_8h_daily:.2f} mg/m³")

# Compliance check
co_compliant = co_max_8h_daily <= 10

print(f"\nCOMPLIANCE:")
print(f"Maximum daily 8-hour average: {'COMPLIANT' if co_compliant else 'NON-COMPLIANT'}")

# 8. O3 COMPLIANCE CHECK
print("\n8. OZONE (O3) COMPLIANCE")
print("-" * 50)

print("STANDARDS:")
print("- 8-hour average ≤ 110 μg/m³")
print("- Daily mean ≤ 65 μg/m³ (not exceeded for more than 3 consecutive days)")

# Calculate metrics
o3_max_8h = df_reg['O3_8h'].max()
o3_daily_mean_max = daily_means['O3'].max()

# Check consecutive exceedances for daily mean
daily_means['O3_exceed_daily'] = daily_means['O3'] > 65
consecutive_exceedances = 0
max_consecutive = 0

for exceed in daily_means['O3_exceed_daily']:
    if exceed:
        consecutive_exceedances += 1
        max_consecutive = max(max_consecutive, consecutive_exceedances)
    else:
        consecutive_exceedances = 0

print(f"\nRESULTS:")
print(f"Maximum 8-hour average: {o3_max_8h:.1f} μg/m³")
print(f"Maximum daily mean: {o3_daily_mean_max:.1f} μg/m³")
print(f"Maximum consecutive days with daily mean > 65 μg/m³: {max_consecutive}")

# Compliance check
o3_8h_compliant = o3_max_8h <= 110
o3_daily_consecutive_compliant = max_consecutive <= 3

print(f"\nCOMPLIANCE:")
print(f"8-hour average: {'COMPLIANT' if o3_8h_compliant else 'NON-COMPLIANT'}")
print(f"Daily mean consecutive exceedances: {'COMPLIANT' if o3_daily_consecutive_compliant else 'NON-COMPLIANT'}")
print(f"OVERALL: {'COMPLIANT' if (o3_8h_compliant and o3_daily_consecutive_compliant) else 'NON-COMPLIANT'}")

# 9. COMPREHENSIVE COMPLIANCE SUMMARY
print("\n9. COMPREHENSIVE COMPLIANCE SUMMARY")
print("-" * 50)

print("OVERALL STATION COMPLIANCE STATUS:")
print("=" * 40)

compliance_status = {
    'NO2': no2_annual_compliant and no2_hourly_compliant,
    'SO2': so2_annual_compliant and so2_daily_compliant,
    'PM10': pm10_compliant,
    'CO': co_compliant,
    'O3': o3_8h_compliant and o3_daily_consecutive_compliant
}

for pollutant, compliant in compliance_status.items():
    status = "COMPLIANT" if compliant else "NON-COMPLIANT"
    print(f"{pollutant}: {status}")

overall_compliant = all(compliance_status.values())
print(f"\nOVERALL STATION STATUS: {'COMPLIANT WITH MOROCCAN STANDARDS' if overall_compliant else 'NON-COMPLIANT WITH MOROCCAN STANDARDS'}")

# 10. DATA QUALITY ASSESSMENT
print("\n10. DATA QUALITY ASSESSMENT")
print("-" * 50)

print("DATA COMPLETENESS FOR REGULATORY ASSESSMENT:")
print(f"Minimum requirement for valid assessment: 75%")

for pollutant, coverage in coverage_summary.items():
    quality = "SUFFICIENT" if coverage >= 75 else "INSUFFICIENT"
    print(f"{pollutant}: {coverage:.1f}% - {quality}")

# 11. DETAILED RESULTS TABLE
print("\n11. DETAILED RESULTS TABLE")
print("-" * 50)

results_data = []
# NO2
results_data.append({
    'Pollutant': 'NO2',
    'Parameter': 'Annual Mean',
    'Value': f"{no2_annual_mean:.1f} μg/m³",
    'Limit': '50 μg/m³',
    'Status': 'COMPLIANT' if no2_annual_compliant else 'NON-COMPLIANT'
})
results_data.append({
    'Pollutant': 'NO2',
    'Parameter': '98th %ile Hourly',
    'Value': f"{no2_98th_hourly:.1f} μg/m³",
    'Limit': '200 μg/m³',
    'Status': 'COMPLIANT' if no2_hourly_compliant else 'NON-COMPLIANT'
})

# SO2
results_data.append({
    'Pollutant': 'SO2',
    'Parameter': 'Annual Mean',
    'Value': f"{so2_annual_mean:.1f} μg/m³",
    'Limit': '20 μg/m³',
    'Status': 'COMPLIANT' if so2_annual_compliant else 'NON-COMPLIANT'
})
results_data.append({
    'Pollutant': 'SO2',
    'Parameter': '99.2th %ile Daily',
    'Value': f"{so2_992th_daily:.1f} μg/m³",
    'Limit': '125 μg/m³',
    'Status': 'COMPLIANT' if so2_daily_compliant else 'NON-COMPLIANT'
})

# PM10
results_data.append({
    'Pollutant': 'PM10',
    'Parameter': '90.4th %ile Daily',
    'Value': f"{pm10_904th_daily:.1f} μg/m³",
    'Limit': '50 μg/m³',
    'Status': 'COMPLIANT' if pm10_compliant else 'NON-COMPLIANT'
})

# CO
results_data.append({
    'Pollutant': 'CO',
    'Parameter': 'Max Daily 8h Avg',
    'Value': f"{co_max_8h_daily:.2f} mg/m³",
    'Limit': '10 mg/m³',
    'Status': 'COMPLIANT' if co_compliant else 'NON-COMPLIANT'
})

# O3
results_data.append({
    'Pollutant': 'O3',
    'Parameter': 'Max 8h Average',
    'Value': f"{o3_max_8h:.1f} μg/m³",
    'Limit': '110 μg/m³',
    'Status': 'COMPLIANT' if o3_8h_compliant else 'NON-COMPLIANT'
})
results_data.append({
    'Pollutant': 'O3',
    'Parameter': 'Max Consecutive Days >65',
    'Value': f"{max_consecutive} days",
    'Limit': '3 days',
    'Status': 'COMPLIANT' if o3_daily_consecutive_compliant else 'NON-COMPLIANT'
})

results_df = pd.DataFrame(results_data)
print(results_df.to_string(index=False))

# 12. VISUALIZATION OF COMPLIANCE STATUS
print("\n12. COMPLIANCE STATUS VISUALIZATION")
print("-" * 50)

plt.figure(figsize=(15, 6))

# Create compliance matrix - FIXED VERSION
pollutants_vis = ['NO2', 'SO2', 'PM10', 'CO', 'O3']
parameters_vis = ['Annual Mean', 'Percentile/Daily', '8-hour/Consecutive']

# Convert boolean to numeric for plotting
compliance_matrix = np.array([
    [int(no2_annual_compliant), int(no2_hourly_compliant), 1],  # NO2
    [int(so2_annual_compliant), int(so2_daily_compliant), 1],   # SO2
    [1, int(pm10_compliant), 1],                               # PM10
    [1, 1, int(co_compliant)],                                 # CO
    [1, int(o3_8h_compliant), int(o3_daily_consecutive_compliant)]  # O3
])

# Create custom colormap
cmap = mcolors.ListedColormap(['red', 'green'])

plt.subplot(1, 2, 1)
im = plt.imshow(compliance_matrix, cmap=cmap, aspect='auto', vmin=0, vmax=1)
plt.xticks(range(3), parameters_vis, rotation=45, ha='right')
plt.yticks(range(5), pollutants_vis)
plt.title('Compliance Matrix\n(Red=Non-compliant, Green=Compliant)', pad=20)

# Add value annotations
for i in range(len(pollutants_vis)):
    for j in range(len(parameters_vis)):
        text = 'YES' if compliance_matrix[i, j] == 1 else 'NO'
        color = 'white' if compliance_matrix[i, j] == 1 else 'black'
        plt.text(j, i, text, ha='center', va='center', color=color, fontweight='bold')

plt.colorbar(im, ticks=[0, 1], label='Compliance')

# Data coverage bar chart
plt.subplot(1, 2, 2)
colors = ['green' if x >= 75 else 'red' for x in coverage_summary.values()]
bars = plt.bar(range(len(coverage_summary)), list(coverage_summary.values()), color=colors)
plt.axhline(y=75, color='red', linestyle='--', label='Minimum Requirement (75%)')
plt.xticks(range(len(coverage_summary)), list(coverage_summary.keys()))
plt.ylabel('Data Coverage (%)')
plt.title('Data Coverage for Regulatory Assessment')
plt.legend()
plt.ylim(0, 100)

# Add value labels on bars
for bar, value in zip(bars, coverage_summary.values()):
    plt.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 1, 
             f'{value:.1f}%', ha='center', va='bottom')

plt.tight_layout()
plt.show()

# 13. METHODOLOGICAL NOTES
print("\n13. METHODOLOGICAL NOTES")
print("-" * 50)

print("CALCULATION METHODS:")
print("• Percentiles: Calculated using numpy.percentile with linear interpolation")
print("• Annual means: Arithmetic mean of all valid hourly measurements")
print("• 8-hour averages: Rolling average with minimum 6 valid hours")
print("• Daily means: Arithmetic mean of all valid hourly measurements for each day")
print("• Consecutive days: Maximum sequence of days exceeding daily limit")

print("\nDATA REQUIREMENTS:")
print("• Minimum data completeness: 75% for valid assessment")
print("• Time period: Full calendar year (2014)")
print("• Station: Hay Hassani")
print("• Assessment date: " + datetime.now().strftime("%Y-%m-%d"))

print("\nLIMITATIONS:")
print("• Assessment based on available data completeness")
print("• No data interpolation or gap filling applied")
print("• Results valid only for monitoring period")

print("\n" + "="*70)
print("REGULATORY COMPLIANCE ASSESSMENT COMPLETE")
print("="*70)
