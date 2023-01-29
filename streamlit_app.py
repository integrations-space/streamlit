import streamlit as st
import pandas as pd
import numpy as np
import ifcopenshell
import os
import plotly.express as px

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
+ Guide for blender-python with ifcopenshell: https://blenderbim.org/docs-python/ifcopenshell/installation.html
+ Guide to load python interpreter in VSC: https://python.plainenglish.io/how-to-set-default-python-interpreter-in-vs-code-76c38c210dc3''')

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
    ifc = open(file_path, "r")
    print("File opened successfully!")
except FileNotFoundError:
    print("The file could not be found. Please check the file path and try again.")
except:
    print("An error occurred while trying to open the file.")
    
# Load the IFC file
ifc_file = ifcopenshell.open(ifc)

# Get all Pset elements
psets = ifc_file.by_type("IfcPropertySet")

# Initialize an empty DataFrame to store the information
df = pd.DataFrame(columns=["Pset", "Property", "Value"])

# Loop through the Pset elements and append their properties to the DataFrame
for pset in psets:
    for prop in pset.HasProperties:
        df = pd.concat([df, pd.DataFrame({"Pset": [pset.Name], "Property": [prop.Name], "Value": [prop.NominalValue.wrappedValue]})], ignore_index=True)

# Show the DataFrame in a table using Streamlit
st.write(df)
