import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from windrose import WindroseAxes
import matplotlib.cm as cm

# ====================================================================
# WIND ROSES BY POLLUTANT ANALYSIS
# ====================================================================

print("="*60)
print("WIND ROSES BY POLLUTANT ANALYSIS")
print("="*60)

# Create a copy for analysis
df_wind = df.copy()

# 1. DATA PREPARATION
print("\n1. DATA PREPARATION")
print("-" * 40)

# Convert pollutants to numeric
pollutants = ['NO2', 'O3', 'PM10', 'SO2', 'CO']
for pollutant in pollutants:
    df_wind[pollutant] = pd.to_numeric(df_wind[pollutant], errors='coerce')

# Clean wind data
df_wind['WS'] = pd.to_numeric(df_wind['WS'], errors='coerce')
df_wind = df_wind.dropna(subset=['WD', 'WS'])

# Map wind directions to degrees - USING YOUR COMPREHENSIVE MAPPING
WD_TO_DEGREES_MAP = {
    'N': 0.0, 'NNE': 22.5, 'NE': 45.0, 'ENE': 67.5,
    'E': 90.0, 'ESE': 112.5, 'SE': 135.0, 'SSE': 157.5,
    'S': 180.0, 'SSW': 202.5, 'SW': 225.0, 'WSW': 247.5,
    'W': 270.0, 'WNW': 292.5, 'NW': 315.0, 'NNW': 337.5,
    'Calme': np.nan  # Handle calm conditions
}

df_wind['WD_degrees'] = df_wind['WD'].map(WD_TO_DEGREES_MAP)
df_wind = df_wind.dropna(subset=['WD_degrees'])

print(f"Wind data available: {len(df_wind)} hours")
print(f"Wind speed statistics:")
print(f"  Mean: {df_wind['WS'].mean():.2f} m/s")
print(f"  Max: {df_wind['WS'].max():.2f} m/s")
print(f"  Min: {df_wind['WS'].min():.2f} m/s")
print(f"  Calm (<0.5 m/s): {(df_wind['WS'] < 0.5).sum()} hours ({(df_wind['WS'] < 0.5).sum()/len(df_wind)*100:.1f}%)")

# 2. BASIC WIND ROSES FOR EACH POLLUTANT
print("\n2. GENERATING BASIC WIND ROSES BY POLLUTANT")
print("-" * 40)

# Create a figure with subplots for each pollutant
fig = plt.figure(figsize=(20, 15))

# Define concentration bins for each pollutant based on data percentiles
pollutant_bins = {}

for pollutant in pollutants:
    if pollutant in df_wind.columns:
        poll_data = df_wind[df_wind[pollutant].notna()]
        if len(poll_data) > 0:
            # Use percentiles to create appropriate bins for each pollutant
            percentiles = [0, 25, 50, 75, 90, 95, 99]
            bins = np.percentile(poll_data[pollutant], percentiles)
            pollutant_bins[pollutant] = bins
            print(f"{pollutant} bins: {bins}")

pollutant_units = {
    'NO2': 'μg/m³',
    'O3': 'μg/m³', 
    'PM10': 'μg/m³',
    'SO2': 'μg/m³',
    'CO': 'mg/m³'
}

# Plot wind roses
for i, pollutant in enumerate(pollutants, 1):
    # Filter data for current pollutant
    poll_data = df_wind[df_wind[pollutant].notna()]
    
    if len(poll_data) > 0:
        ax = fig.add_subplot(2, 3, i, projection='windrose')
        
        # Use wind speed bins that match the data range
        ws_bins = np.linspace(poll_data['WS'].min(), poll_data['WS'].max(), 6)
        
        # Create wind rose with proper bin handling
        try:
            ax.bar(poll_data['WD_degrees'], poll_data[pollutant], 
                   normed=True, 
                   bins=ws_bins,
                   nsector=16,
                   cmap=cm.viridis,
                   opening=0.8)
            
            ax.set_legend()
            ax.set_title(f'{pollutant} Concentration by Wind Direction\n({pollutant_units[pollutant]})', 
                        fontsize=12, fontweight='bold')
            
            print(f"Generated wind rose for {pollutant}: {len(poll_data)} data points")
            
        except Exception as e:
            print(f"Error creating wind rose for {pollutant}: {e}")
            # Create a simple frequency wind rose instead
            ax.bar(poll_data['WD_degrees'], poll_data['WS'], 
                   normed=True, 
                   bins=6,
                   nsector=16,
                   cmap=cm.Blues,
                   opening=0.8)
            ax.set_title(f'Wind Frequency - {pollutant} Data Available', fontsize=12)

plt.tight_layout()
plt.show()

# 3. DETAILED SECTOR ANALYSIS WITH 16 DIRECTIONS
print("\n3. DETAILED 16-SECTOR ANALYSIS")
print("-" * 40)

# Define all 16 sectors for detailed analysis
sixteen_sectors = {
    'N': [348.75, 11.25],
    'NNE': [11.25, 33.75],
    'NE': [33.75, 56.25],
    'ENE': [56.25, 78.75],
    'E': [78.75, 101.25],
    'ESE': [101.25, 123.75],
    'SE': [123.75, 146.25],
    'SSE': [146.25, 168.75],
    'S': [168.75, 191.25],
    'SSW': [191.25, 213.75],
    'SW': [213.75, 236.25],
    'WSW': [236.25, 258.75],
    'W': [258.75, 281.25],
    'WNW': [281.25, 303.75],
    'NW': [303.75, 326.25],
    'NNW': [326.25, 348.75]
}

def get_detailed_sector(degrees):
    """Convert degrees to detailed 16-sector direction"""
    for sector, (min_deg, max_deg) in sixteen_sectors.items():
        if min_deg <= degrees < max_deg:
            return sector
    # Handle wrap-around for 0 degrees
    if degrees == 0 or degrees == 360:
        return 'N'
    return 'N'  # Default

df_wind['detailed_sector'] = df_wind['WD_degrees'].apply(get_detailed_sector)

# Analyze pollution by detailed sector
print("\nPOLLUTION BY DETAILED WIND SECTOR:")
for pollutant in pollutants:
    if pollutant in df_wind.columns:
        sector_stats = df_wind.groupby('detailed_sector')[pollutant].agg(['mean', 'count', 'max']).round(2)
        max_sector = sector_stats['mean'].idxmax()
        max_value = sector_stats['mean'].max()
        min_sector = sector_stats['mean'].idxmin()
        min_value = sector_stats['mean'].min()
        
        print(f"\n{pollutant}:")
        print(f"  Highest concentrations from: {max_sector} ({max_value} {pollutant_units[pollutant]})")
        print(f"  Lowest concentrations from: {min_sector} ({min_value} {pollutant_units[pollutant]})")
        
        # Print top 3 sectors
        top_sectors = sector_stats.nlargest(3, 'mean')
        print(f"  Top 3 sectors:")
        for sector, row in top_sectors.iterrows():
            print(f"    {sector}: {row['mean']} {pollutant_units[pollutant]} ({row['count']} hours)")

# 4. WIND SPEED AND POLLUTION ANALYSIS
print("\n4. WIND SPEED AND POLLUTION RELATIONSHIP")
print("-" * 40)

# Define wind speed categories
def wind_speed_category(ws):
    if ws < 1: return 'Calm (<1 m/s)'
    elif ws < 3: return 'Light (1-3 m/s)'
    elif ws < 5: return 'Moderate (3-5 m/s)'
    else: return 'Strong (>5 m/s)'

df_wind['ws_category'] = df_wind['WS'].apply(wind_speed_category)

print("POLLUTION BY WIND SPEED CATEGORY:")
for pollutant in pollutants:
    if pollutant in df_wind.columns:
        ws_stats = df_wind.groupby('ws_category')[pollutant].mean().round(2)
        print(f"\n{pollutant}:")
        for category, value in ws_stats.items():
            print(f"  {category}: {value} {pollutant_units[pollutant]}")

# 5. SOURCE IDENTIFICATION ANALYSIS
print("\n5. SOURCE IDENTIFICATION")
print("-" * 40)

print("POTENTIAL POLLUTION SOURCES:")

# Analyze high concentration events
high_pollution_thresholds = {
    'NO2': 50,    # μg/m³
    'PM10': 75,   # μg/m³
    'SO2': 20,    # μg/m³
    'CO': 2.0,    # mg/m³
    'O3': 100     # μg/m³
}

for pollutant, threshold in high_pollution_thresholds.items():
    if pollutant in df_wind.columns:
        high_pollution = df_wind[df_wind[pollutant] > threshold]
        if len(high_pollution) > 0:
            high_poll_sectors = high_pollution['detailed_sector'].value_counts()
            dominant_sector = high_poll_sectors.index[0] if len(high_poll_sectors) > 0 else 'N/A'
            dominant_percent = high_poll_sectors.iloc[0] / len(high_pollution) * 100 if len(high_poll_sectors) > 0 else 0
            
            print(f"\n{pollutant} (>{threshold} {pollutant_units[pollutant]}):")
            print(f"  Total high pollution hours: {len(high_pollution)}")
            print(f"  Dominant wind sector during high pollution: {dominant_sector} ({dominant_percent:.1f}%)")
            
            # Print sector distribution for top 3 sectors
            print(f"  Top sector distribution:")
            for sector, count in high_poll_sectors.head(3).items():
                percent = count / len(high_pollution) * 100
                print(f"    {sector}: {count} hours ({percent:.1f}%)")

# 6. SIMPLIFIED WIND ROSES WITH FIXED BINS
print("\n6. SIMPLIFIED WIND ROSE ANALYSIS")
print("-" * 40)

# Create enhanced wind roses with fixed bins - REMOVED THE 3 WIND ROSES
fig2 = plt.figure(figsize=(20, 12))

# Use fixed wind speed bins that work with the data
ws_min = df_wind['WS'].min()
ws_max = df_wind['WS'].max()
fixed_ws_bins = np.linspace(ws_min, ws_max, 6)

print(f"Using fixed wind speed bins: {fixed_ws_bins}")

# REMOVED: The 3 wind roses for NO2, PM10, O3 concentration

# Add summary statistics plot - NOW IN POSITION 1
ax_summary = fig2.add_subplot(2, 3, 1)

# Calculate mean concentrations by detailed sector for main pollutants
sector_data = []
for pollutant in ['NO2', 'PM10', 'O3']:
    if pollutant in df_wind.columns:
        sector_means = df_wind.groupby('detailed_sector')[pollutant].mean()
        for sector, value in sector_means.items():
            sector_data.append({
                'Pollutant': pollutant,
                'Sector': sector,
                'Concentration': value,
                'Unit': pollutant_units[pollutant]
            })

sector_df = pd.DataFrame(sector_data)

# Create heatmap of concentrations by sector and pollutant
if not sector_df.empty:
    pivot_data = sector_df.pivot(index='Sector', columns='Pollutant', values='Concentration')
    # Reorder sectors clockwise
    sector_order = ['N', 'NNE', 'NE', 'ENE', 'E', 'ESE', 'SE', 'SSE', 
                   'S', 'SSW', 'SW', 'WSW', 'W', 'WNW', 'NW', 'NNW']
    pivot_data = pivot_data.reindex([s for s in sector_order if s in pivot_data.index])
    sns.heatmap(pivot_data, annot=True, cmap='YlOrRd', fmt='.1f', ax=ax_summary)
    ax_summary.set_title('Mean Concentration by Detailed Wind Sector\n(μg/m³)', fontweight='bold')
    ax_summary.tick_params(axis='x', rotation=45)
    ax_summary.tick_params(axis='y', rotation=0)

# Add wind frequency rose - NOW IN POSITION 2
ax_freq = fig2.add_subplot(2, 3, 2, projection='windrose')
ax_freq.bar(df_wind['WD_degrees'], df_wind['WS'], 
           normed=True, 
           bins=6,
           nsector=16,
           cmap=cm.Blues,
           opening=0.8)
ax_freq.set_legend(title='Wind Speed (m/s)')
ax_freq.set_title('Wind Frequency Distribution', fontweight='bold')

# Add pollution roses by season - NOW IN POSITION 3
ax_season = fig2.add_subplot(2, 3, 3)

# Define seasons
def get_season(month):
    if month in [12, 1, 2]: return 'Winter'
    elif month in [3, 4, 5]: return 'Spring'
    elif month in [6, 7, 8]: return 'Summer'
    else: return 'Autumn'

df_wind['season'] = df_wind['datetime'].dt.month.apply(get_season)

# Plot seasonal NO2 by detailed sector
seasonal_no2 = df_wind.groupby(['season', 'detailed_sector'])['NO2'].mean().unstack()
# Reorder seasons and sectors
seasonal_no2 = seasonal_no2.reindex(index=['Winter', 'Spring', 'Summer', 'Autumn'],
                                   columns=['N', 'NNE', 'NE', 'ENE', 'E', 'ESE', 'SE', 'SSE', 
                                           'S', 'SSW', 'SW', 'WSW', 'W', 'WNW', 'NW', 'NNW'])

sns.heatmap(seasonal_no2, annot=True, cmap='YlOrRd', fmt='.1f', ax=ax_season)
ax_season.set_title('Seasonal NO2 by Detailed Wind Sector\n(μg/m³)', fontweight='bold')
ax_season.tick_params(axis='x', rotation=45)

# Add wind speed vs pollution analysis - NEW PLOT IN POSITION 4
ax_ws = fig2.add_subplot(2, 3, 4)

# Analyze pollution by wind speed for main pollutants
ws_analysis_data = []
for pollutant in ['NO2', 'PM10', 'O3']:
    if pollutant in df_wind.columns:
        ws_stats = df_wind.groupby('ws_category')[pollutant].mean().reset_index()
        ws_stats['Pollutant'] = pollutant
        ws_analysis_data.append(ws_stats)

if ws_analysis_data:
    ws_df = pd.concat(ws_analysis_data, ignore_index=True)
    sns.barplot(data=ws_df, x='ws_category', y=pollutant, hue='Pollutant', ax=ax_ws)
    ax_ws.set_title('Pollution by Wind Speed Category', fontweight='bold')
    ax_ws.set_ylabel('Concentration (μg/m³)')
    ax_ws.set_xlabel('Wind Speed Category')
    ax_ws.legend(title='Pollutant')

# Add high pollution events analysis - NEW PLOT IN POSITION 5
ax_high = fig2.add_subplot(2, 3, 5)

# Analyze high pollution events by sector
high_poll_data = []
for pollutant in ['NO2', 'PM10']:
    if pollutant in df_wind.columns:
        threshold = high_pollution_thresholds[pollutant]
        high_pollution = df_wind[df_wind[pollutant] > threshold]
        if len(high_pollution) > 0:
            sector_counts = high_pollution['detailed_sector'].value_counts().head(5)
            for sector, count in sector_counts.items():
                high_poll_data.append({
                    'Pollutant': pollutant,
                    'Sector': sector,
                    'Count': count
                })

if high_poll_data:
    high_poll_df = pd.DataFrame(high_poll_data)
    sns.barplot(data=high_poll_df, x='Sector', y='Count', hue='Pollutant', ax=ax_high)
    ax_high.set_title('High Pollution Events by Sector\n(Top 5 sectors)', fontweight='bold')
    ax_high.set_ylabel('Number of Hours')
    ax_high.set_xlabel('Wind Sector')
    ax_high.tick_params(axis='x', rotation=45)
    ax_high.legend(title='Pollutant')

# Leave position 6 empty or add another analysis
ax_empty = fig2.add_subplot(2, 3, 6)
ax_empty.axis('off')
# Optionally add text summary
ax_empty.text(0.5, 0.5, 'Comprehensive Wind-Pollution Analysis\n\n• Heatmap shows concentration patterns\n• Wind frequency shows prevailing winds\n• Seasonal analysis reveals temporal patterns\n• Wind speed analysis shows dispersion effects\n• High events identify source directions', 
              ha='center', va='center', transform=ax_empty.transAxes, fontsize=12,
              bbox=dict(boxstyle="round,pad=0.3", facecolor="lightgray", alpha=0.7))

plt.tight_layout()
plt.show()

# 7. KEY FINDINGS SUMMARY
print("\n7. KEY FINDINGS SUMMARY")
print("-" * 40)

print("WIND-POLLUTION RELATIONSHIPS:")

# Summary for each pollutant
for pollutant in pollutants:
    if pollutant in df_wind.columns:
        # Find sectors with highest concentrations
        sector_means = df_wind.groupby('detailed_sector')[pollutant].mean()
        max_sector = sector_means.idxmax()
        max_value = sector_means.max()
        
        # Find wind speeds with highest concentrations
        ws_means = df_wind.groupby('ws_category')[pollutant].mean()
        max_ws = ws_means.idxmax()
        max_ws_value = ws_means.max()
        
        print(f"\n{pollutant}:")
        print(f"  • Highest concentrations from: {max_sector} sector ({max_value:.1f} {pollutant_units[pollutant]})")
        print(f"  • Peak levels during: {max_ws} winds ({max_ws_value:.1f} {pollutant_units[pollutant]})")
        print(f"  • Typical range: {df_wind[pollutant].min():.1f}-{df_wind[pollutant].max():.1f} {pollutant_units[pollutant]}")

print("\nSOURCE IDENTIFICATION:")
print("• High NO2/CO: Typically indicates traffic sources")
print("• High SO2: Often indicates industrial/combustion sources") 
print("• High PM10: Can indicate dust, construction, or regional transport")
print("• O3 patterns: Typically show photochemical formation patterns")

print("\nRECOMMENDATIONS:")
print("• Monitor sectors with consistently high pollution for source identification")
print("• Consider local topography and source locations relative to wind patterns")
print("• Use seasonal patterns to identify different source contributions")

print("\n" + "="*60)
print("WIND ROSE ANALYSIS COMPLETE")
print("="*60)
