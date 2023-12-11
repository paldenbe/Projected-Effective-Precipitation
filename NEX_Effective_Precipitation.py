import arcpy
import os
from arcpy.sa import *

# Set the path to the folder containing the raster files
input_folder = r"YOUR_INPUT_FOLDER_PATH"

# Set the output geodatabase
output_geodatabase = r"YOUR_OUTPUT_GDB_PATH"

# Print statement to check the contents of the input folder
print(f"Contents of {input_folder}: {os.listdir(input_folder)}")

# Get a list of all raster files in the folder with ".tif" extension
raster_list = [f for f in os.listdir(input_folder) if f.endswith('.tif')]

# Print statement to check if any raster files are found
print(f"Found {len(raster_list)} raster files.")

# Loop through each raster file
for raster in raster_list:
    # Construct the full path to the input raster file
    input_raster_path = os.path.join(input_folder, raster)

    # Use arcpy.conversion.RasterToGeodatabase to put the raster into the geodatabase
    arcpy.conversion.RasterToGeodatabase(
        Input_Rasters=input_raster_path,
        Output_Geodatabase=output_geodatabase,
        Configuration_Keyword=""
    )

    print(f"Raster {raster} successfully added to the geodatabase.")

# Set the path to the folder containing your raster files
input_folder = r"YOUR_INPUT_FOLDER_PATH"

# Get a list of all raster files in the folder with ".tif" extension
rasterlist = arcpy.ListRasters("*PrecipMean*")

# Set the output geodatabase
output_geodatabase = r"YOUR_OUTPUT_GDB_PATH"

# Set the clipping rectangle (this is set for Missouri, change this to apply to your project)
clip_rectangle = "-95.7747039998897 35.9956829997707 -89.0989679999732 40.6136400002858"

# Loop through each raster file
for raster in rasterlist:
    # Construct the full path to the input raster file
    input_raster_path = os.path.join(input_folder, raster)

    # Construct the output raster name with "_Clip" suffix
    out_raster = os.path.join(output_geodatabase, f"{os.path.splitext(raster)[0]}_Clip")

    # Perform the Clip operation
    arcpy.management.Clip(
        in_raster=input_raster_path,
        rectangle=clip_rectangle,
        out_raster=out_raster,
        in_template_dataset=r"YOUR_SHAPEFILE_PATH\Missouri_Counties.shp",
        nodata_value="3.4e+38",
        clipping_geometry="ClippingGeometry",
        maintain_clipping_extent="NO_MAINTAIN_EXTENT"
    )

    print(f"Clipping completed for: {raster}")

# Set the path to your geodatabase
geodatabase = r"YOUR_GDB_PATH"
arcpy.env.workspace = geodatabase

output_folder = r"YOUR_OUTPUT_FOLDER_PATH"
raster_list = arcpy.ListRasters("*Clip*")
print(raster_list)

for raster in raster_list:
    # Construct the full path to the input raster file
    input_raster_path = os.path.join(geodatabase, raster)

    # Perform the desired operation (multiply by 31536000)
    mmyr_raster = Raster(input_raster_path) * 31536000

    # Construct the output raster name with "_mmyr" suffix
    output_raster = f"{os.path.splitext(raster)[0]}_mmyr"

    # Save the result within the geodatabase
    output_raster_path = os.path.join(geodatabase, output_raster)
    mmyr_raster.save(output_raster_path)

    print(f"Processing completed for: {raster}")

# Divide mm/year NASA NEX DCP 30 raster by 1000 to get a precipitation raster with m/year values

geodatabase = r"YOUR_GDB_PATH"
arcpy.env.workspace = geodatabase

output_folder = r"YOUR_OUTPUT_FOLDER_PATH"
raster_list = arcpy.ListRasters("*mmyr*")
print(raster_list)

for raster in raster_list:
    # Construct the full path to the input raster file
    input_raster_path = os.path.join(geodatabase, raster)

    # Perform the desired operation
    myr_raster = Raster(input_raster_path) / 1000

    # Construct the output raster name with "_myr" suffix
    output_raster = f"{os.path.splitext(raster)[0].replace('_mmyr', '_myr')}"

    # Save the result within the geodatabase
    output_raster_path = os.path.join(geodatabase, output_raster)
    myr_raster.save(output_raster_path)

    print(f"Processing completed for: {raster}")

# Set the path to your geodatabase
geodatabase = r"YOUR_GDB_PATH"
arcpy.env.workspace = geodatabase

# List all the "*_myr*" rasters in the geodatabase
raster_list_myr = arcpy.ListRasters("*_myr*")

# Iterate over each "*_myr*" raster
for raster in raster_list_myr:
    # Extract RCP scenario and year from the raster name
    parts = os.path.splitext(raster)[0].split("_")
    rcp_scenario = parts[-3]
    year = parts[1]

    # Construct the full path to the input raster file
    input_raster_path = os.path.join(geodatabase, raster)
    counties_ir_m_yr = f"counties_ir_m_yr"

    # Perform the desired operation
    eff_precip_raster = Raster(input_raster_path) + Raster(counties_ir_m_yr)

    # Construct the output raster name
    output_raster_name = f"Eff_Precip_{year}_{rcp_scenario}"

    # Save the result within the geodatabase
    output_raster_path = os.path.join(geodatabase, output_raster_name)
    eff_precip_raster.save(output_raster_path)

    print(f"Effective precipitation calculation completed for: {output_raster_name}")

# Set the path to your geodatabase
geodatabase = r"YOUR_GDB_PATH"
arcpy.env.workspace = geodatabase

# List all the "Eff_Precip_*" rasters in the geodatabase
eff_precip_list = arcpy.ListRasters("Eff_Precip_*")

# Path to your layer file (.lyrx) in ArcGIS Pro
symbology_layer_path = r"YOUR_SYMBOLGY_LAYER_PATH\Eff_Precip_Symbology.lyrx"

# Iterate over each "Eff_Precip_*" raster
for eff_precip_raster in eff_precip_list:
    # Construct the full path to the eff_precip raster file
    eff_precip_path = os.path.join(geodatabase, eff_precip_raster)

    # Apply symbology from the layer file
    arcpy.management.ApplySymbologyFromLayer(eff_precip_path, symbology_layer_path)

    # Save the modified layer back to the raster dataset
    output_raster_path = eff_precip_path
    #arcpy.management.CopyRaster(eff_precip_path, output_raster_path)

    print(f"Symbology set for: {eff_precip_raster}")
