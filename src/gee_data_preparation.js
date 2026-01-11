/*
 * Google Earth Engine Script: Environmental Dataset Preparation for NDVI Prediction
 * 
 * Purpose:
 *   Extract and preprocess environmental variables for NDVI prediction using
 *   gradient boosting machine learning models. Data includes MODIS NDVI, LST, ET,
 *   and CHIRPS precipitation for the Chittagong region.
 * 
 * Study Area: Chittagong Division, Bangladesh
 * Temporal Range: 2002-2024
 * Spatial Resolution: 250m (all variables resampled)
 * Temporal Aggregation: Monthly means
 * 
 * Data Sources:
 *   - MODIS/006/MOD13Q1: NDVI (250m, 16-day)
 *   - MODIS/006/MOD11A2: Land Surface Temperature (1km, 8-day)
 *   - MODIS/006/MOD16A2: Evapotranspiration (500m, 8-day)
 *   - UCSB-CHG/CHIRPS/DAILY: Precipitation (5.5km, daily)
 * 
 * Output:
 *   CSV file exported to Google Drive containing monthly aggregated data with
 *   columns: year, month, LST, ET, precipitation, NDVI, geometry
 * 
 * Usage:
 *   1. Import or define the 'chittagong' geometry (study area boundary)
 *   2. Adjust startDate and endDate if needed
 *   3. Run the script
 *   4. Export the data from the Tasks tab
 *   5. Download CSV from Google Drive
 * 
 * Author: Golam Murad
 * Date: 2026
 * License: MIT
 */

// 1. Study Area Definition
// NOTE: Import your study area geometry as 'chittagong' or define it here
Map.addLayer(chittagong);


// 2. Define Date Range
var startDate = '2002-01-01';
var endDate = '2024-12-31';

// 3. Load Datasets
var ndvi = ee.ImageCollection('MODIS/006/MOD13Q1')
  .filterDate(startDate, endDate)
  .filterBounds(chittagong)
  .select('NDVI');

var lst = ee.ImageCollection('MODIS/006/MOD11A2')
  .filterDate(startDate, endDate)
  .filterBounds(chittagong)
  .select('LST_Day_1km');

var et = ee.ImageCollection('MODIS/006/MOD16A2')
  .filterDate(startDate, endDate)
  .filterBounds(chittagong)
  .select('ET');

var precip = ee.ImageCollection('UCSB-CHG/CHIRPS/DAILY')
  .filterDate(startDate, endDate)
  .filterBounds(chittagong);

// 4. Preprocessing
// Resample and convert units
var lstResampled = lst.map(function(image) {
  return image
    .resample('bilinear')
    .reproject({crs: 'EPSG:4326', scale: 250})
    .multiply(0.02)
    .subtract(273.15)
    .rename('LST');
});

var etResampled = et.map(function(image) {
  return image
    .resample('bilinear')
    .reproject({crs: 'EPSG:4326', scale: 250})
    .rename('ET');
});

var precipResampled = precip.map(function(image) {
  return image
    .resample('bilinear')
    .reproject({crs: 'EPSG:4326', scale: 250})
    .rename('precipitation');
});

// 5. Temporal Aggregation (Monthly)
var months = ee.List.sequence(1, 12);
var years = ee.List.sequence(2002, 2022);

var monthlyData = ee.ImageCollection.fromImages(
  years.map(function(year) {
    return months.map(function(month) {
      // Filter by month/year
      var ndviMonthly = ndvi.filter(ee.Filter.calendarRange(year, year, 'year'))
        .filter(ee.Filter.calendarRange(month, month, 'month'))
        .mean();
      
      var lstMonthly = lstResampled.filter(ee.Filter.calendarRange(year, year, 'year'))
        .filter(ee.Filter.calendarRange(month, month, 'month'))
        .mean();
      
      var etMonthly = etResampled.filter(ee.Filter.calendarRange(year, year, 'year'))
        .filter(ee.Filter.calendarRange(month, month, 'month'))
        .mean();
      
      var precipMonthly = precipResampled.filter(ee.Filter.calendarRange(year, year, 'year'))
        .filter(ee.Filter.calendarRange(month, month, 'month'))
        .mean();
      
      return ee.Image.cat([
        lstMonthly,
        etMonthly,
        precipMonthly,
        ndviMonthly
      ]).set({
        'year': year,
        'month': month,
        'system:time_start': ee.Date.fromYMD(year, month, 1)
      });
    });
  }).flatten()
);

// 6. Export Data
var samples = monthlyData.map(function(image) {
  return image.clip(chittagong)
    .sampleRegions({
      collection: chittagong,
      scale: 250,
      geometries: true
    });
}).flatten();

Export.table.toDrive({
  collection: samples,
  description: 'Chittagong_ML_Data',
  fileFormat: 'CSV'
});
