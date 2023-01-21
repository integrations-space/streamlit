import streamlit as st
import pandas as pd
import numpy as np
import { IfcLoader } from "web-ifc-three";
import { Scene } from "three";
st.title('Programming with GitHub')
#multiline text
st.text('''tinkter - share program - share without relying on web, fundamental, Hardcore skillset
Plotly - webbased
Streamlit - quick start for programming
thunkeble - mobile for fun''')


// Creates THREE.js scene
const scene = new Scene();

// ...

// Loads IFC and adds it to the scene
const ifcLoader = new IfcLoader();
ifcLoader.load(ifcURL, (geometry) => scene.add(geometry));
