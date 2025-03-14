import arcpy
import time

def intersect(layer_list, input_lyr_name):
    # Run an intersect analysis between the two buffer layers (needs to be a list of layers to intersect)
    arcpy.Intersect_analysis(layer_list, input_lyr_name)

def buffer_layer(input_gdb, input_layer, dist):
    # Run a buffer analysis on the input_layer with a user specified distance
    # Distance units are always miles
    units = " miles"
    dist = dist + units
    # Output layer will always be named input layer + "_buf"
    output_layer = r"C:\Users\thoma\Desktop\GIS3005\Week 1\3005_wk1\3005_wk1.gdb" + "\\" + input_layer + "_buf"
    # Always use buffer parameters FULL, ROUND, ALL
    buf_layer = input_gdb + "\\" + input_layer
    arcpy.Buffer_analysis(buf_layer, output_layer,
                          dist, "FULL", "ROUND", "ALL")
    return output_layer

def main():
    # Define your workspace and point it at the modelbuilder.gdb
    arcpy.env.workspace = r"C:\Users\thoma\Desktop\GIS3005\Week 1\3005_wk1\3005_wk1.gdb"
    arcpy.env.overwriteOutput = True

    # Buffer cities
    input_gdb = r"C:\Users\thoma\Documents\ArcGIS\GIS305\Data\Admin\Admin\AdminData.gdb"

    dist = arcpy.GetParameterAsText(0)

    buf_cities = buffer_layer(input_gdb, "cities", dist)

    arcpy.AddMessage(f"Buffer layer {buf_cities} created.")

    # Buffer rivers
    dist = arcpy.GetParameterAsText(1)  # Changed index to 1
    buf_rivers = buffer_layer(input_gdb, "us_rivers", dist)
    arcpy.AddMessage(f"Buffer layer {buf_rivers} created.")

    # Define lyr_list variable with names of input layers to intersect
    # Ask the user to define an output layer name
    intersect_lyr_name = arcpy.GetParameterAsText(2)  # Changed index to 2

    # Ensure the intersect layer name is valid
    if not intersect_lyr_name.isidentifier():
        arcpy.AddError("The output layer name contains invalid characters.")
        return

    lyr_list = [buf_rivers, buf_cities]
    intersect(lyr_list, intersect_lyr_name)
    arcpy.AddMessage(f"New intersect layer generated called: {intersect_lyr_name}")

    # Get the project
    aprx = arcpy.mp.ArcGISProject(
        r"C:\Users\thoma\Desktop\GIS3005\Week 1\3005_wk1\3005_wk1.aprx")
    map_doc = aprx.listMaps()[0]

    # Add data to map with the correct layer name
    map_doc.addDataFromPath(r"C:\Users\thoma\Desktop\GIS3005\Week 1\3005_wk1\3005_wk1.gdb" + "\\" + intersect_lyr_name)

    time.sleep(10) # added wait to assist save function
    aprx.save()
    # save produces error in ArcPRO geoprocessing widow but does successfully save the project

if __name__ == '__main__':
    main()
