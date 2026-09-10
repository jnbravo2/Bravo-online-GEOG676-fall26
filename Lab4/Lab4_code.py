import arcpy 

arcpy.env.overwriteOutput = True

arcpy.env.workspace = r'C:\Users\jocel\DevSource\GEOG676Bravo\Lab4'
folder_path = r'C:\Users\jocel\DevSource\GEOG676Bravo\Lab4'
gdb_name = 'Test.gdb'
gdb_path = folder_path + "\\" + gdb_name
if arcpy.Exists(gdb_path):
    arcpy.management.Delete(gdb_path)

arcpy.CreateFileGDB_management(folder_path, gdb_name)  # Create a new file geodatabase


csv_path = r'C:\Users\jocel\DevSource\GEOG676Bravo\Lab4\garages.csv'
garage_layer_name = 'Garage_Points'
garages = arcpy.MakeXYEventLayer_management(csv_path, 'X', 'Y', garage_layer_name)  # Create a point layer from the CSV

input_layer = garages
arcpy.FeatureClassToFeatureClass_conversion(input_layer, gdb_path, garage_layer_name)  # Save the point layer to the geodatabase
garage_points = gdb_path + "/" + garage_layer_name  # Define the path to the saved point layer

#open campus gbd, copy building features to our gbd
campus = r'C:\Users\jocel\DevSource\GEOG676Bravo\Lab4\Campus.gdb'
buildings_campus = campus + "\Structures"
buildings = gdb_path + '\\' + 'Buildings'

arcpy.Copy_management(buildings_campus, buildings)  # Copy the building features from the campus geodatabase to our geodatabase

#re-project 
spatial_ref=arcpy.Describe(buildings).spatialReference  # Get the spatial reference of the buildings feature class
arcpy.Project_management(garage_points, gdb_path + '\Garage_Points_reprojected', spatial_ref)

#buffer the garages
garageBuffered = arcpy.Buffer_analysis(gdb_path + '\Garage_Points_reprojected', gdb_path + '\Garage_Points_Buffered', 150)  # Create a buffer of 150 meters around the garage points

#Intersect our buffer with the buildings 
arcpy.Intersect_analysis([garageBuffered, buildings], gdb_path + '\Garage_Building_Intersection','ALL')  # Intersect the buffered garages with the buildings

 # Convert the intersected features to a table
arcpy.conversion.TableToTable(gdb_path + '\Garage_Building_Intersection', folder_path, 'nearbyBuildings.csv')
