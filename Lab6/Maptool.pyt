import time
import arcpy


class Toolbox(object):

    def __init__(self):
        """Define the toolbox (the name of the toolbox is the name of the .pyt file)."""
        self.label = "Toolbox"
        self.alias = ""
        self.tools = [GraduatedColorsRenderer]


class GraduatedColorsRenderer(object):

    def __init__(self):
        """Define the tool (tool name is the name of the class)."""
        self.label = "graduatedcolor"
        self.description = "Create a graduated colored map based on a specific attribute of a layer"
        self.canRunInBackground = False
        self.category = "MapTools"

    def getParameterInfo(self):
        """Define parameter definitions."""
        # Layer you want to classify to create a color map
        param0 = arcpy.Parameter(
            displayName="Layer to Classify",
            name="LayerToClassify",
            datatype="GPLayer",
            parameterType="Required",
            direction="Input",
        )

        return [param0]

    def isLicensed(self):
        """Set whether the tool is licensed to execute."""
        return True

    def updateParameters(self, parameters):
        return

    def updateMessages(self, parameters):
        return

    def execute(self, parameters, messages):
        """The source code of the tool."""
        readTime = 3
        start = 0
        max = 100
        step = 33

        arcpy.SetProgressor(
            "step", "Validating Project File...", start, max, step
        )
        time.sleep(readTime)
        arcpy.AddMessage("Validating Project File...")

        # Reference the CURRENT active ArcGIS Pro project
        project = arcpy.mp.ArcGISProject("CURRENT")

        # Extract target layer name using arcpy.Describe
        target_layer_name = arcpy.Describe(parameters[0].value).name

        # Grab the first instance of Map from .aprx
        campus = project.listMaps("Map")[0]

        arcpy.SetProgressorPosition(start + step)
        arcpy.SetProgressorLabel("Finding your map layer...")
        time.sleep(readTime)
        arcpy.AddMessage("Finding your map layer...")

        for layer in campus.listLayers():
            if layer.isFeatureLayer:
                symbology = layer.symbology
                if hasattr(symbology, "renderer"):
                    if (
                        layer.name == target_layer_name
                        or layer.name == parameters[0].valueAsText
                    ):

                        arcpy.SetProgressorPosition(start + step * 2)
                        arcpy.SetProgressorLabel(
                            "Calculating and Classifying..."
                        )
                        time.sleep(readTime)
                        arcpy.AddMessage("Calculating and Classifying...")

                        # Update renderer
                        symbology.updateRenderer("GraduatedColorsRenderer")
                        symbology.renderer.classificationField = "Shape_Area"
                        symbology.renderer.breakCount = 5
                        symbology.renderer.colorRamp = (
                            project.listColorRamps("Oranges (5 Classes)")[0]
                        )

                        # Apply symbology back to the layer
                        layer.symbology = symbology

                        arcpy.AddMessage("Finish Generating Layer...")
                    else:
                        print("No layers found")

        arcpy.SetProgressorPosition(start + step * 3)
        arcpy.SetProgressorLabel("Saving project...")
        time.sleep(readTime)
        arcpy.AddMessage("Saving...")

        # Save changes directly into the current project file
        project.save()

        return