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
