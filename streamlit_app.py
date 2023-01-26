import streamlit as st
import pandas as pd
import numpy as np
import ifcopenshell
import os

#import { IfcLoader } from "web-ifc-three";
#import { Scene } from "three";
st.title('Programming with GitHub')

st.text('''
Install anaconda first then goto command prompt
+ tinkter - share program - share without relying on web, fundamental, Hardcore skillset
+ Plotly - webbased
+ Streamlit - quick start for programming
+ thunkeble - mobile for fun
Downloadable healthcare models available online
https://www.wbdg.org/ffc/dha/mhs-space-templates
+ Create a BIM application with python in under 60 minutes: https://youtu.be/AfQztEUSQns
+ access ifc with Python:http://blog.ifcopenshell.org/
+ getting started with Visual Studio Code,VS Code, a source-code editor made by Microsoft with the Electron Framework, for Windows, Linux and macOS 
https://code.visualstudio.com/docs/python/python-tutorial
+ use of blender for ifc: https://blenderbim.org/docs-python/ifcconvert/installation.html
+ Guide for blender download: https://blenderbim.org/docs-python/ifcconvert/installation.html
+ Guide for blender-python with ifcopenshell: https://blenderbim.org/docs-python/ifcopenshell/installation.html''')

st.title('Dynamo')
st.text('''+ Pushing Shared parameters into family 
https://www.youtube.com/watch?v=lvO2_0IQ8vQ
https://www.youtube.com/watch?v=6Az1G0pla_k
+ access group parameter: https://dynamopythonprimer.gitbook.io/dynamo-python-primer/4-revit-specific-topics/working-with-parameters/instance-parameters
Automated modeling by placing models in points set in the model
https://www.youtube.com/watch?v=bvxeY60VGT8''')

st.title('IFC Parse')

file_path = input("Please enter the file path for the IFC file: ")

try:
    ifc_file = open(file_path, "r")
    print("File opened successfully!")
except FileNotFoundError:
    print("The file could not be found. Please check the file path and try again.")
except:
    print("An error occurred while trying to open the file.")
    
# Open the IFC file
ifc_file = ifcopenshell.open(file_path)

# Get the entities in the file
entities = ifc_file.by_type("IfcProduct")

# Define a recursive function to print the tree
def print_tree(entity, level=0):
    # Print the entity's name and type
    print("    " * level + entity.is_a() + ": " + entity.Name)

    # Check if the entity has children (contained objects)
    if hasattr(entity, "IsDecomposedBy"):
        # If it does, recursively call the function for each child
        for rel in entity.IsDecomposedBy:
            for child in rel.RelatedObjects:
                print_tree(child, level + 1)

# Call the function for each top-level entity in the file
for e in entities:
    print_tree(e)
