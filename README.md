# Air Quality Analysis - Hay Hassani 2014

A comprehensive analysis of atmospheric pollution data from the Hay Hassani monitoring station in Casablanca, Morocco for the year 2014. This project provides detailed insights into air quality patterns, meteorological relationships, and regulatory compliance assessment according to Moroccan environmental standards.

## Project Overview

This analysis examines hourly air quality data including:
- **Pollutants**: NO₂, O₃, PM10, SO₂, CO
- **Meteorological parameters**: Temperature, Humidity, Wind speed/direction
- **Time period**: January 1, 2014 to December 31, 2014
- **Data coverage**: 8,760 hours with excellent completeness (87-99% across pollutants)

## Key Features

### Comprehensive Data Analysis
- Statistical summaries and data quality assessment
- Temporal patterns (diurnal, monthly, seasonal)
- Threshold exceedance analysis
- Pollution episode identification

### Meteorological Relationships
- Temperature-humidity correlation analysis
- Wind rose analysis for pollution source identification
- Nocturnal inversion impact assessment
- Seasonal pattern analysis

### Regulatory Compliance
- Moroccan air quality standards assessment (Decree 2-09-286)
- Multi-pollutant compliance checking
- Data quality validation for regulatory purposes

## Key Findings

### Regulatory Compliance Status
- **Overall Assessment**: Non-compliant with Moroccan standards
- **Compliant Pollutants**: NO₂, SO₂, CO
- **Non-compliant Pollutants**: PM10, O₃

### Critical Regulatory Metrics
- **PM10**: 90.4th percentile daily = 62.7 μg/m³ (Limit: 50 μg/m³) - Non-compliant
- **O₃**: Maximum 8-hour average = 110.2 μg/m³ (Limit: 110 μg/m³) - Non-compliant
- **O₃**: 12 consecutive days >65 μg/m³ (Limit: 3 days) - Non-compliant

### Pollution Concentration Patterns
- **NO₂**: Highest in winter (31.6 μg/m³), peaks at 22:00 (traffic-related)
- **O₃**: Highest in summer (67.6 μg/m³), peaks at 15:00 (photochemical formation)
- **PM10**: Autumn/winter peaks (63.6 μg/m³ in December)
- **Annual means**: NO₂: 18.9 μg/m³, O₃: 50.6 μg/m³, PM10: 33.8 μg/m³

### Meteorological Analysis
- **Dominant wind direction**: ONO (19.7% of observation time)
- **Average wind speed**: 2.16 m/s
- **Temperature range**: 5.2°C to 31.5°C (annual mean: 16.9°C)
- **Humidity range**: 18.0% to 99.9% (annual mean: 77.1%)

### Source Identification
- **High NO₂/CO**: Northeast sector (traffic sources)
- **High PM10**: Northeast sector (dust/construction activities)
- **High SO₂**: Northeast sector (industrial/combustion sources)
- **Calm wind conditions**: Associated with highest pollution concentrations

## Technical Implementation

### Dependencies
```python
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from windrose import WindroseAxes
from scipy import stats
```

### Analysis Modules
1. **Data Loading & Preparation** - Raw data processing and quality control
2. **Statistical Analysis** - Descriptive statistics and data validation
3. **Temporal Analysis** - Diurnal, monthly, and seasonal pattern identification
4. **Meteorological Analysis** - Weather-pollution relationship quantification
5. **Wind Rose Analysis** - Directional pollution pattern mapping
6. **Regulatory Compliance** - Moroccan standards assessment and reporting

## Output Files

- `hayhassani_2014_analysis_results.csv` - Complete processed dataset with all derived variables
- `hayhassani_2014_analysis_summary.csv` - Comprehensive summary statistics
- Multiple visualization figures including wind roses, time series plots, and correlation matrices

## Usage

1. **Data Preparation**: Place the Excel data file in the specified directory path
2. **Execution**: Run the main analysis script
   ```python
   python air_quality_analysis.py
   ```
3. **Results Review**: Examine console output for statistical summaries and compliance status
4. **Data Export**: Utilize generated CSV files for further analysis or reporting

## Data Quality Assessment

| Pollutant | Data Coverage | Quality Assessment |
|-----------|---------------|-------------------|
| NO₂ | 99.0% | Excellent |
| O₃ | 94.7% | Good |
| PM10 | 87.2% | Good |
| SO₂ | 96.3% | Excellent |
| CO | 93.8% | Good |

All pollutants meet the minimum 75% data completeness requirement for regulatory assessment.

## Methodological Notes

- **Percentile Calculation**: WHO-recommended method with linear interpolation
- **Statistical Methods**: Arithmetic means, rolling averages, correlation analysis
- **Regulatory Framework**: Moroccan Decree 2-09-286 of 08/12/2009
- **Data Validation**: No interpolation or gap filling applied

## Limitations

- Assessment validity limited to the 2014 monitoring period
- Results specific to Hay Hassani monitoring station characteristics
- No adjustment for meteorological normalization in compliance assessment

## Applications

- Environmental regulatory compliance monitoring
- Urban air quality management planning
- Pollution source identification and characterization
- Public health impact assessment
- Environmental policy development support

This analysis provides a comprehensive foundation for evidence-based air quality management decisions and regulatory compliance verification.
