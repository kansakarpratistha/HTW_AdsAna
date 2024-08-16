import streamlit as st
from common_widgets import sidebar_creds

st.set_page_config(
    page_title="Ideal Adsorption Solution Theory (IAST) App (Ver. Alpha)",
)

sidebar_creds()

st.write("# Ideal Adsorption Solution Theory (IAST) - Application")

st.markdown(
    """
        <p class='note'>Please note that this is an Alpha version and still under development</p>
        <h2>Current Features:</h2>
        <ul>
        <li>Data Input with File Upload and Editing</li>
        <li>IAST Result Calculation</li>
        <li>Competetive Adsorption Analysis with TRM Model</li>
        <li>Result Generation</li>
        <li>Result Visualization</li>
        </ul>    
        <h2>Step-by-Step Guide:</h2>
        <h3>Input Data Format:</h3>
        <ul>
        <li>Go to <strong>Data Input</strong> page and click on <strong>Need Sample Data?</strong>.</li>
        <li>Click on the options to download the respective data files.</li>
        <li>Use these formats for input data files.</li>  
        </ul>
        <h3>Data Input:</h3>
        <ul>
        <li>Go to <strong>Data Input</strong> page and then <strong>Isotherm Data</strong> tab.</li>
        <li>You can edit the preexisting input data or upload a new CSV data file.</li>
        <li>Press the <strong>Submit</strong> button to load the input data.</li>
        </ul>    
        <h3>Input Data Correction:</h3>
        <ul>
        <li>Click on the <strong>Data Correction</strong> button and check the <strong>Apply Data Correction to Input Data</strong> option.</li>
        <li>Select the <strong>Use Corrected Dataset</strong> option in the sidebar of <strong>Result</strong> page.</li>
        </ul>
        <h3>Competetive Adsorption Analysis:</h3>
        <ul>
        <li>Go to <strong>Data Input</strong> page and select the <strong>Add Competetive Sorption Data</strong> option on the sidebar.</li>
        <li>Go to <strong>Competetive Ads Data Input</strong> tab.</li>
        <li>Edit preexisting Micropollutant and Single Solute data or upload new files.</li>
        <li>Press the <strong>Submit</strong> button to load the input data.</li>
        </ul>
        <h3>View Input Data:</h3>
        <ul>
        <li>Go to <strong>View Isotherm Data</strong> or <strong>View Competetive Sorption Data</strong> tab on <strong>Data Input</strong> page to view the current input data along.</li>
        <li>Click on the <strong>Download</strong> button to download the respective input data as a CSV file.</li>
        </ul>
        <h3>Result Generation:</h3>
        <ul>
        <li>Go to <strong>Results</strong> page to view the calculated results.</li>
        <li><strong>IAST Result</strong> tab contains calculated concentration and adsorption, concentration distribution and calculated error. Additionally, it also presents calculated concentration and adsorption of the components as different dosages</li>
        <li><strong>Competetive Sorption Result</strong> tab contains the IAST calculation w.r.t to the provided Multipollutant and Single solute data and corrected data using TRM model.</li>
        </ul>
        <h3>Result Visualization:</h3>
        <ul>
        <li>Go to <strong>Plots</strong> tab on <strong>Results</strong> page to view the result plottings.</li>
        <li>Click on the expander with the plotting titles to view the respective plots.</li>
        </ul>""",
    unsafe_allow_html = True
)

st.markdown("""<style>
.note {
            color: #ff9800;
            font-weight: bold;
            font-style: italic;
        }
</style>
""", unsafe_allow_html=True)
