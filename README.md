# NDVI Prediction Using Soft Computing Techniques

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python](https://img.shields.io/badge/Python-3.8%2B-blue.svg)](https://www.python.org/)
[![Jupyter](https://img.shields.io/badge/Jupyter-Notebook-orange.svg)](https://jupyter.org/)

## Overview

This repository contains the implementation of gradient boosting-based soft computing techniques for predicting Normalized Difference Vegetation Index (NDVI) using satellite imagery and environmental data. The study focuses on vegetation health monitoring in the Chittagong region using multiple state-of-the-art machine learning models.

## Abstract

Vegetation monitoring through NDVI prediction plays a crucial role in understanding ecosystem health and environmental changes. This research implements and compares four gradient boosting algorithms—**CatBoost**, **GBM (Gradient Boosting Machine)**, **LightGBM**, and **XGBoost**—for NDVI prediction using satellite-derived environmental variables. The models utilize temporal data from MODIS and CHIRPS datasets spanning 2002-2024, incorporating Land Surface Temperature (LST), Evapotranspiration (ET), and Precipitation as predictor variables.

## Study Area

**Location:** Chittagong Division, Bangladesh  
**Data Source:** Google Earth Engine  
**Temporal Coverage:** 2002-2024  
**Spatial Resolution:** 250m

## Model Performance

Comparative analysis of model performance metrics:

| Model      | R² (Test) | R² (Train) | MAE (Test) | RMSE (Test) | MSE (Test) |
|------------|-----------|------------|------------|-------------|------------|
| **XGBoost**   | **0.905** | **0.912**  | **0.040**  | **0.071**   | **0.005**  |
| LightGBM   | 0.868     | 0.871      | 0.056      | 0.084       | 0.007      |
| CatBoost   | 0.867     | 0.871      | 0.054      | 0.084       | 0.007      |
| GBM        | 0.749     | 0.753      | 0.083      | 0.116       | 0.013      |

**Key Finding:** XGBoost demonstrated superior performance with R² of 0.905 and lowest error metrics.

## Repository Structure

```
NDVI-Prediction/
├── README.md                          # This file
├── LICENSE                            # MIT License
├── CITATION.cff                       # Citation information
├── requirements.txt                   # Python dependencies
├── .gitignore                         # Git ignore patterns
├── data/                              # Dataset directory
│   └── README.md                      # Data documentation
├── src/                               # Source code
│   └── gee_data_preparation.js        # Google Earth Engine data extraction script
├── notebooks/                         # Analysis notebooks
│   └── ndvi_prediction.ipynb          # Main analysis and modeling
├── results/                           # Model outputs and figures
│   ├── model_performance_comparison.csv
│   ├── correlation_heatmap.png
│   ├── CatBoost_diagnostic_plots.png
│   ├── CatBoost_shap_summary.png
│   ├── GBM_diagnostic_plots.png
│   ├── GBM_shap_summary.png
│   ├── LightGBM_diagnostic_plots.png
│   ├── LightGBM_shap_summary.png
│   ├── XGBoost_diagnostic_plots.png
│   └── XGBoost_shap_summary.png
└── docs/                              # Additional documentation
    └── methodology.md                 # Detailed methodology
```

## Features

- **Multi-Model Comparison:** Implementation of CatBoost, GBM, LightGBM, and XGBoost
- **SHAP Analysis:** Model interpretability using SHAP (SHapley Additive exPlanations) values
- **Comprehensive Diagnostics:** Residual plots, prediction vs actual, and error distribution analysis
- **Reproducible Workflow:** Complete pipeline from data extraction to model evaluation
- **Time Series Analysis:** Monthly aggregated satellite data over 20+ years

## Installation

### Prerequisites

- Python 3.8 or higher
- pip package manager
- Jupyter Notebook/Lab (optional, for running notebooks)

### Setup

1. Clone the repository:
```bash
git clone https://github.com/yourusername/NDVI-Prediction.git
cd NDVI-Prediction
```

2. Create a virtual environment (recommended):
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

### Data Preparation

1. **Google Earth Engine (GEE) Data Extraction:**
   - Open `src/gee_data_preparation.js` in the [Google Earth Engine Code Editor](https://code.earthengine.google.com/)
   - Define your study area or use the provided Chittagong region
   - Run the script to export environmental data to Google Drive
   - Download the CSV file and place it in the `data/` directory

2. **Data Documentation:**
   - Refer to `data/README.md` for detailed information about variables and preprocessing

### Model Training and Evaluation

Open and run the Jupyter notebook:
```bash
jupyter notebook notebooks/ndvi_prediction.ipynb
```

The notebook includes:
- Data loading and preprocessing
- Exploratory data analysis
- Feature engineering
- Model training (CatBoost, GBM, LightGBM, XGBoost)
- Model evaluation and comparison
- SHAP analysis for interpretability
- Visualization generation

## Methodology

The analysis follows a structured workflow:

1. **Data Collection:** Satellite data extraction from MODIS and CHIRPS
2. **Preprocessing:** Temporal aggregation, resampling, and unit conversion
3. **Feature Engineering:** Creating lag features and temporal indicators
4. **Model Training:** Hyperparameter tuning using cross-validation
5. **Evaluation:** Comprehensive metrics including R², MAE, RMSE, MSE, and EVS
6. **Interpretability:** SHAP analysis to understand feature importance

For detailed methodology, see [`docs/methodology.md`](docs/methodology.md).

## Results

### Model Diagnostics

Diagnostic plots are available in `figures/model_diagnostics/` showing:
- Predicted vs Actual values
- Residual distribution
- Q-Q plots for normality assessment
- Residual vs Fitted values

### Feature Importance

SHAP analysis reveals the most influential environmental variables for NDVI prediction. Summary plots are available in `figures/shap_analysis/`.

## Citation

If you use this code or methodology in your research, please cite:

```bibtex
@software{murad2026ndvi,
  author = {Golam Murad},
  title = {NDVI Prediction Using Soft Computing Techniques},
  year = {2026},
  url = {https://github.com/yourusername/NDVI-Prediction}
}
```

See [`CITATION.cff`](CITATION.cff) for more citation formats.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contact

**Golam Murad**  
Email: golammurad19@gmail.com  
Portfolio: [https://alarnaarchives.my.canva.site/golam-murad](https://alarnaarchives.my.canva.site/golam-murad)  
LinkedIn: [Golam Murad](https://linkedin.com/in/golam-murad)

## Acknowledgments

- Google Earth Engine for providing satellite imagery and computational resources
- MODIS and CHIRPS teams for maintaining high-quality environmental datasets
- Open-source machine learning community for developing the algorithms used in this study

## Keywords

NDVI, Vegetation Monitoring, Machine Learning, Gradient Boosting, XGBoost, LightGBM, CatBoost, Remote Sensing, Google Earth Engine, Environmental Modeling, Time Series Analysis

---

**Note:** This is a research project. Data availability and specific implementation details are documented in the respective directories.
