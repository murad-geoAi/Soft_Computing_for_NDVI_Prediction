# Dataset Documentation

## Overview

This directory contains the environmental dataset used for NDVI prediction. The data is extracted from Google Earth Engine using multiple satellite products.

## Data Source

The dataset is prepared using the Google Earth Engine script located at: [`src/gee_data_preparation.js`](../src/gee_data_preparation.js)

### Satellite Products Used

| Product | Variable | Description | Spatial Resolution | Temporal Resolution |
|---------|----------|-------------|-------------------|---------------------|
| MODIS/006/MOD13Q1 | NDVI | Normalized Difference Vegetation Index | 250m | 16-day |
| MODIS/006/MOD11A2 | LST | Land Surface Temperature | 1km → 250m (resampled) | 8-day |
| MODIS/006/MOD16A2 | ET | Evapotranspiration | 500m → 250m (resampled) | 8-day |
| UCSB-CHG/CHIRPS/DAILY | Precipitation | Daily precipitation | 5.5km → 250m (resampled) | Daily |

## Study Area

- **Location:** Chittagong Division, Bangladesh
- **Coordinates:** Defined by the `chittagong` geometry in GEE script
- **Coverage:** Full administrative division

## Temporal Coverage

- **Start Date:** 2002-01-01
- **End Date:** 2024-12-31
- **Aggregation:** Monthly mean values

## Variables

### Predictor Variables (Features)

1. **LST (Land Surface Temperature)**
   - Original unit: Kelvin × 50 (scaled)
   - Processed unit: Celsius
   - Conversion: `(value × 0.02) - 273.15`
   - Description: Day-time land surface temperature

2. **ET (Evapotranspiration)**
   - Unit: kg/m²/8day
   - Description: Total evapotranspiration

3. **Precipitation**
   - Unit: mm
   - Description: Monthly accumulated precipitation from daily data

### Target Variable

4. **NDVI (Normalized Difference Vegetation Index)**
   - Range: -1 to +1 (scaled by 10000 in MODIS)
   - Description: Vegetation health indicator
   - Higher values indicate healthier, denser vegetation

## Data Processing Pipeline

1. **Extraction:** Data extracted using Google Earth Engine
2. **Filtering:** Temporal and spatial filtering for study area
3. **Resampling:** All variables resampled to 250m resolution using bilinear interpolation
4. **Aggregation:** Monthly mean calculation from higher temporal resolution data
5. **Export:** CSV export to Google Drive
6. **Quality Control:** Missing value handling and outlier detection

## Data Structure

Expected CSV structure after GEE export:

```
year, month, LST, ET, precipitation, NDVI, .geo
2002, 1, 25.3, 45.2, 150.0, 0.65, ...
2002, 2, 26.1, 43.8, 130.5, 0.68, ...
...
```

## Usage Instructions

### Obtaining the Data

1. Open [`src/gee_data_preparation.js`](../src/gee_data_preparation.js) in the [Google Earth Engine Code Editor](https://code.earthengine.google.com/)
2. Import or define your study area boundary (default: Chittagong region)
3. Run the script
4. Export task will appear in the Tasks tab
5. Download the exported CSV from Google Drive
6. Place the CSV file in this `data/` directory

### File Naming Convention

Recommended: `chittagong_ndvi_data_2002_2024.csv` or similar descriptive name

## Data Characteristics

- **Sample Size:** Depends on study area size and temporal range
- **Features:** 3 environmental variables (LST, ET, Precipitation)
- **Target:** NDVI
- **Temporal Units:** Monthly aggregations
- **Missing Values:** Handled during preprocessing in the analysis notebook

## Citation

If you use this dataset, please cite both the original data sources and this methodology:

- **MODIS Products:** [NASA LP DAAC](https://lpdaac.usgs.gov/)
- **CHIRPS:** [UCSB Climate Hazards Center](https://www.chc.ucsb.edu/data/chirps)
- **Google Earth Engine:** Gorelick et al., 2017

## References

1. Didan, K. (2015). MOD13Q1 MODIS/Terra Vegetation Indices 16-Day L3 Global 250m SIN Grid V006.
2. Wan, Z., Hook, S., & Hulley, G. (2015). MOD11A2 MODIS/Terra Land Surface Temperature/Emissivity 8-Day L3 Global 1km SIN Grid V006.
3. Running, S., & Mu, Q. (2017). MOD16A2 MODIS/Terra Net Evapotranspiration 8-Day L4 Global 500m SIN Grid V006.
4. Funk, C. et al. (2015). The climate hazards infrared precipitation with stations—a new environmental record for monitoring extremes. Scientific Data, 2, 150066.

## Notes

- Data is not included in the repository due to size constraints
- Users must generate their own dataset using the provided GEE script
- For questions about data access, contact the repository maintainer
