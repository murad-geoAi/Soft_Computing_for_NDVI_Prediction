# Methodology

## Research Objective

To predict Normalized Difference Vegetation Index (NDVI) using environmental variables through the application and comparison of gradient boosting-based soft computing techniques.

## Conceptual Framework

```
Environmental Variables → Machine Learning Models → NDVI Prediction
      (LST, ET, Precip)    (CatBoost, GBM, LightGBM, XGBoost)
```

## Data Collection and Preprocessing

### 1. Data Extraction

Environmental data was extracted from Google Earth Engine using the following datasets:

- **MODIS MOD13Q1:** 16-day NDVI at 250m resolution
- **MODIS MOD11A2:** 8-day Land Surface Temperature at 1km resolution
- **MODIS MOD16A2:** 8-day Evapotranspiration at 500m resolution
- **UCSB CHIRPS:** Daily precipitation at ~5.5km resolution

### 2. Preprocessing Steps

1. **Spatial Processing:**
   - All datasets resampled to 250m resolution using bilinear interpolation
   - Clipped to Chittagong Division boundary
   - Reprojected to EPSG:4326

2. **Temporal Processing:**
   - Monthly aggregation using mean values
   - Temporal range: 2002-2024 (23 years)
   - Total: 276 monthly observations per pixel

3. **Unit Conversion:**
   - LST: Converted from Kelvin (scaled) to Celsius: `(value × 0.02) - 273.15`
   - ET: Maintained in kg/m²/8day
   - Precipitation: Aggregated from daily to monthly totals

4. **Data Quality:**
   - Cloud masking applied automatically by MODIS products
   - Gap filling through temporal interpolation
   - Outlier detection and removal

## Feature Engineering

### Input Features (X)

1. **Land Surface Temperature (LST)** - Continuous
2. **Evapotranspiration (ET)** - Continuous
3. **Precipitation** - Continuous

### Target Variable (y)

- **NDVI** - Continuous, range: -1 to +1 (typically 0 to 1 for vegetated areas)

### Additional Features (if applicable)

- **Temporal Features:** Month, Season
- **Lag Features:** Previous month's values
- **Interaction Features:** LST × Precipitation, etc.

## Machine Learning Models

### Model Selection Rationale

Gradient boosting algorithms were selected due to their:
- Superior performance on tabular data
- Ability to capture non-linear relationships
- Built-in feature importance analysis
- Robustness to outliers

### 1. XGBoost (Extreme Gradient Boosting)

**Algorithm:** Regularized gradient boosting framework

**Key Parameters:**
- `n_estimators`: Number of boosting rounds
- `max_depth`: Maximum tree depth
- `learning_rate`: Step size shrinkage
- `subsample`: Fraction of samples for tree training
- `colsample_bytree`: Fraction of features for tree training

**Advantages:**
- Regularization to prevent overfitting
- Parallel processing capability
- Handles missing values automatically

### 2. LightGBM (Light Gradient Boosting Machine)

**Algorithm:** Leaf-wise tree growth with histogram-based learning

**Key Parameters:**
- `num_leaves`: Maximum number of leaves
- `learning_rate`: Boosting learning rate
- `feature_fraction`: Feature sampling ratio
- `bagging_fraction`: Data sampling ratio

**Advantages:**
- Faster training speed
- Lower memory usage
- Better accuracy with large datasets

### 3. CatBoost (Categorical Boosting)

**Algorithm:** Gradient boosting with ordered boosting and categorical feature handling

**Key Parameters:**
- `iterations`: Number of boosting iterations
- `depth`: Tree depth
- `learning_rate`: Learning step size
- `l2_leaf_reg`: L2 regularization

**Advantages:**
- Handles categorical features natively
- Reduces overfitting through ordered boosting
- No need for extensive preprocessing

### 4. GBM (Gradient Boosting Machine)

**Algorithm:** Classical gradient boosting (scikit-learn implementation)

**Key Parameters:**
- `n_estimators`: Number of boosting stages
- `max_depth`: Maximum depth of trees
- `learning_rate`: Learning rate
- `subsample`: Sample fraction for training

**Advantages:**
- Baseline implementation
- Well-established and stable
- Good interpretability

## Hyperparameter Tuning

**Method:** Grid Search or Randomized Search with Cross-Validation

**Cross-Validation Strategy:** 5-fold time series cross-validation

**Evaluation Metric for Tuning:** Root Mean Squared Error (RMSE)

## Model Training

### Data Split

- **Training Set:** 80% of data
- **Test Set:** 20% of data
- **Split Strategy:** Temporal split to prevent data leakage

### Training Process

1. Load and preprocess data
2. Split into train/test sets
3. Hyperparameter tuning on training set
4. Train models with optimal parameters
5. Evaluate on test set

## Model Evaluation

### Performance Metrics

1. **R² (Coefficient of Determination)**
   - Measures proportion of variance explained
   - Range: 0 to 1 (higher is better)
   - Formula: `1 - (SS_res / SS_tot)`

2. **MAE (Mean Absolute Error)**
   - Average absolute difference between predictions and actual values
   - Units: Same as target variable
   - Formula: `mean(|y_true - y_pred|)`

3. **RMSE (Root Mean Squared Error)**
   - Square root of average squared differences
   - Penalizes larger errors more heavily
   - Formula: `sqrt(mean((y_true - y_pred)²))`

4. **MSE (Mean Squared Error)**
   - Average of squared differences
   - Formula: `mean((y_true - y_pred)²)`

5. **EVS (Explained Variance Score)**
   - Measures explained variance proportion
   - Similar to R² but handles bias differently

### Diagnostic Analysis

1. **Residual Plots:** Check for patterns in prediction errors
2. **Q-Q Plots:** Assess normality of residuals
3. **Predicted vs Actual:** Visualize prediction accuracy
4. **Error Distribution:** Analyze error patterns

## Model Interpretability

### SHAP (SHapley Additive exPlanations)

**Purpose:** Explain individual predictions and overall feature importance

**Methods Used:**
- **SHAP Summary Plots:** Global feature importance
- **SHAP Dependence Plots:** Feature interaction effects
- **SHAP Force Plots:** Individual prediction explanations

**Interpretation:**
- Positive SHAP values: Feature increases NDVI prediction
- Negative SHAP values: Feature decreases NDVI prediction
- Magnitude: Importance of the effect

## Results Interpretation

### Model Comparison

Models are compared based on:
1. Primary metric: R² on test set
2. Secondary metrics: MAE, RMSE
3. Training vs test performance (overfitting check)
4. Computational efficiency
5. Interpretability

### Best Model Selection

The best performing model (XGBoost with R² = 0.905) was selected based on:
- Highest R² on test data
- Lowest error metrics (MAE, RMSE, MSE)
- Consistent performance between training and testing
- Robust to overfitting

## Limitations

1. **Temporal Limitations:** Monthly aggregation may miss short-term variations
2. **Spatial Resolution:** 250m may not capture fine-scale heterogeneity
3. **Feature Set:** Limited to three environmental variables
4. **Study Area:** Results specific to Chittagong region
5. **Missing Data:** Gaps in satellite coverage due to clouds

## Future Work

1. **Additional Features:** Soil moisture, solar radiation, elevation
2. **Deep Learning:** LSTM or Transformer models for time series
3. **Spatial Modeling:** Incorporate spatial autocorrelation
4. **Real-time Prediction:** Operational forecasting system
5. **Expanded Study Area:** Regional or national scale analysis

## References

1. Chen, T., & Guestrin, C. (2016). XGBoost: A scalable tree boosting system. In KDD '16.
2. Ke, G., et al. (2017). LightGBM: A highly efficient gradient boosting decision tree. In NIPS.
3. Prokhorenkova, L., et al. (2018). CatBoost: unbiased boosting with categorical features. In NeurIPS.
4. Lundberg, S. M., & Lee, S. I. (2017). A unified approach to interpreting model predictions. In NIPS.

## Contact

For questions about the methodology, please contact:
- **Golam Murad:** golammurad19@gmail.com
