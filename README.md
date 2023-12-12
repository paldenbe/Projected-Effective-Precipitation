# Projected-Effective-Precipitation
This code generates the projected effective precipitation for a study area. Before running the code, you should create a data folder for your ArcPro project with your desired study area shapefile, the NEX precipitation data for the future years you want, and a county-level irrigation raster for your study area.

The NEX data can be downloaded here: https://www.nccs.nasa.gov/services/data-collections/land-based-products/nex-dcp30

The study area shapefile can be downloaded from Data.gov

The county-level irrigation raster can be created through the following steps:
  1. Download this csv file: https://www.sciencebase.gov/catalog/item/get/5af3311be4b0da30c1b245d8
  2. Delete all columns except IR-WGWFr, IC-WGWFr, and IG-WGWFr
  3. Download the US counties shapefile: https://catalog.data.gov/dataset/tiger-line-shapefile-2019-nation-u-s-current-county-and-equivalent-national-shapefile
  4. Add FIPS field to US counties for a join between counties and the irrigation table
  5. Change the units of the irrigation table to cubed meters per year (Mil_m3_yr = IR_WGRFr*1.3815...m3_yr = Mil_m3_yr*1,000,000)
  6. Change the Shape_Area units to squared meters
  7. Download the NLCD (https://www.mrlc.gov/data/nlcd-2021-land-cover-conus)
  8. Use "Tabulate Area" tool to calculate area of each county that is each land cover type
    a. Zone input = counties_ir; zone = FIPS
    b. Feature raster = NLCD raster
    d. Join this table back to the polygons (counties_ir)
  9. Calculate new field (TOTAL) = add all land cover class columns together
  10. Calculate new field (Area_Ag_OpenUrban) = Cultivated Crops + Hay/Pasture + Developed Open Space
  11. Calculate m of irrigation for each county by dividing m3_yr by the m2 of irrigated land (Area_Ag_OpenUrban) for each county
  12. Use Polygon to Raster to make raster of irrigation values

The symbology section of the code is optional. You can make your own .lyrx file and add it to your data folder, or just adjust the symbology after running the code. Your symbology should capture the high and low values.
