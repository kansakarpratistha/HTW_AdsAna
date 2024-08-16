import streamlit as st
import pandas as pd
import numpy as np
from process_data import *
from calculations import *
from common_widgets import sidebar_creds
st.set_page_config(page_title="Data Input")


st.markdown("""
<style>
	.stTabs [data-baseweb="tab-list"] {
		background-color: #527a8a;
        padding: 0px 10px 0px 10px;
        border-radius: 10px
    }

    .stTabs [data-baseweb="tab"] p{
        font-size: 1rem;
        color: white;
        font-weight: 700;
    }

	.stTabs [aria-selected="true"] p{
        font-size: 1.1rem;
        font-weight: 700;
        text-shadow: black 2px 2px 5px;
	}

    div[data-testid="stExpander"] p {
        font-size: 1rem;
    }
</style>""", unsafe_allow_html=True)

if 'comp_data_input' in st.session_state.keys():
    comp_data_input = st.session_state['comp_data_input']
else:
    comp_data_input = False
    st.session_state['comp_data_input'] = False

tab3 = False
tab4 = False

def flip_sorption_opt():
    if st.session_state['comp_data_input'] == False:
        st.session_state['comp_data_input'] = True
    else:
        st.session_state['comp_data_input'] = False

with st.sidebar:
    comp_data_input = st.checkbox("Add Competetive Sorption Data", value=comp_data_input, on_change = flip_sorption_opt)
    st.write("")
    with st.expander("Need Sample Data?"):
        with open('./sample_data/sample_iso.csv') as f:
            st.download_button('Isotherm Data', f, file_name = 'sample_isotherm_data.csv', use_container_width=True) 
        with open('./sample_data/sample_mp.csv') as f:
            st.download_button('Micropollutant Data', f, file_name = 'sample_micropollutant_data.csv', use_container_width=True) 
        with open('./sample_data/sample_ss.csv') as f:
            st.download_button('Single Solute Data', f, file_name = 'sample_singlesolute_data.csv', use_container_width=True) 

sidebar_creds()        

if comp_data_input == False:
    sorption_data = ['mA_VL_mp', 'c_mp', 'q_mp', 'c0_mp', 'name_mp', 'mA_VL_ss', 'c_ss', 'c0_ss']
    for item in sorption_data:
        if item in st.session_state.keys():
            del st.session_state[item]



st.write("# Data Input")


if comp_data_input:
    tab1, tab2, tab3, tab4 = st.tabs(["Isotherm Data", "View Isotherm Data", "Competetive Sorption Data","View Competetive Sorption Data"])
else:
    tab1, tab2 = st.tabs(["Isotherm Data", "View Isotherm Data"])

with tab1:
    st.subheader("Experimental Data Files")
    input_file = st.file_uploader("Upload a file", accept_multiple_files = False)
    K=[]
    n=[]
    c0=0
    sac0=0
    mA_VL = []
    ci = []
    qi = [] 
    if input_file:
        try:
            mA_VL, ci, qi, K, n, c0 = read_csv_and_extract_columns(input_file)    
        except Exception as e:
            # print("Error in reading file:", e)
            st.error('Invalid File Format')
    elif input_file == None and 'dosage_lst' not in st.session_state.keys():
        input_file = './sample_data/sample_iso.csv'
        try:
            mA_VL, ci, qi, K, n, c0 = read_csv_and_extract_columns(input_file)    
        except Exception as e:
            # print("Error in reading file:", e)
            st.error('Invalid File Format')
    elif input_file == None and 'dosage_lst' in st.session_state.keys():
        mA_VL = st.session_state['dosage_lst']
        ci = st.session_state['c_exp_lst']
        qi = st.session_state['q_exp_lst']
        K = st.session_state['K']
        n = st.session_state['n']
        c0 = st.session_state['c0']
        # sac0 = st.session_state['sac0']
    st.divider()

    col1, col2 = st.columns(2, gap="large")
    with col1:    
        st.subheader("Initial Concentrations")
        c0 = st.number_input(r"$c_O$", value=c0, key='iso_c0')
        # sac0 = st.number_input("SAC0", value=sac0)

        st.subheader("Adsorption Parameters")
        # adsorbable_num = st.selectbox("Number of Adsorption Components", [1,2,3,4,5,6])
                
        ads_df = pd.DataFrame({"K":K, "n":n}, columns=("K", "n"))
        ads_df = ads_df.astype({'K':float, 'n':float})
        ads_df = st.data_editor(ads_df,
        column_config={
            "K": st.column_config.NumberColumn("K", help="About K parameter"),
            "n": st.column_config.NumberColumn("n", help="About n parameter")},
        num_rows="dynamic", use_container_width=True)

        

    with col2:
        st.subheader("Isotherm Data")
        isotherm_df = pd.DataFrame({"mA/VL":mA_VL, "c{}".format('\N{LATIN SUBSCRIPT SMALL LETTER I}'):ci, "q{}".format('\N{LATIN SUBSCRIPT SMALL LETTER I}'):qi}, columns=("mA/VL", "c{}".format('\N{LATIN SUBSCRIPT SMALL LETTER I}') , "q{}".format('\N{LATIN SUBSCRIPT SMALL LETTER I}')))
        isotherm_df = isotherm_df.astype({'mA/VL':float, "c{}".format('\N{LATIN SUBSCRIPT SMALL LETTER I}'):float, "q{}".format('\N{LATIN SUBSCRIPT SMALL LETTER I}'):float})
        styled_df = isotherm_df.style.set_properties(**{'font-size': '25pt'})
        isotherm_df = st.data_editor(styled_df,
        column_config={
            "mA/VL": st.column_config.NumberColumn("mA/VL", help="About mA/VL parameter"),
            "c{}".format('\N{LATIN SUBSCRIPT SMALL LETTER I}'): st.column_config.NumberColumn("c{}".format('\N{LATIN SUBSCRIPT SMALL LETTER I}'), help="About ci parameter"),
            "q{}".format('\N{LATIN SUBSCRIPT SMALL LETTER I}'): st.column_config.NumberColumn("q{}".format('\N{LATIN SUBSCRIPT SMALL LETTER I}'), help="About qi parameter")},
        use_container_width=True)
    
    st.divider()
    iso_submit_btn = st.button("Submit", key='submit_iso')

    if iso_submit_btn: #process input data and store to session state
        try:
            for key in st.session_state.keys(): #clear corrected c values calculated for prev dataset
                if key in ['corr_c_exp_lst', 'corr_c0']:
                    del st.session_state[key]

            st.session_state['K'] = ads_df['K'].to_numpy()
            st.session_state['n'] = ads_df['n'].to_numpy()

            st.session_state['dosage_lst'] = isotherm_df['mA/VL'].to_numpy()
            st.session_state['c_exp_lst'] = isotherm_df["c{}".format('\N{LATIN SUBSCRIPT SMALL LETTER I}')].to_numpy()
            st.session_state['q_exp_lst'] = isotherm_df["q{}".format('\N{LATIN SUBSCRIPT SMALL LETTER I}')].to_numpy()

            st.session_state['c0'] = c0
            # st.session_state['sac0'] = sac0

            st.session_state['c_calc_lst']=[]
            st.session_state['q_calc_lst']=[]

            st.success("Data input successfully.")
        except Exception as e:
            st.error(f"Something went wrong while loading the input data. Please try again. {e}")

    # if 'dosage_lst' in st.session_state.keys():
    #     with st.popover("Data Correction"):
    #         a0, a1, r, fig = data_correction(st.session_state['q_exp_lst'], st.session_state['c_exp_lst'])
    #         st.markdown(f"""
    #             <h5>a0: {a0}</h5>
    #             <h5>a1: {a1}</h5>
    #             <h5>r: {r}</h5>
    #         """, unsafe_allow_html=True)
    #         st.pyplot(fig)
    #         apply_corr_btn = st.button("Apply Correction")
    #         if apply_corr_btn:
    #             corr_c_exp_lst = a0 + a1 * st.session_state['q_exp_lst']
    #             corr_c0 = a0 + a1 * st.session_state['sac0']
    #             st.session_state['corr_c_exp_lst'] = corr_c_exp_lst
    #             st.session_state['corr_c0'] = corr_c0

    if 'dosage_lst' in st.session_state.keys():
        with st.popover("Data Correction"):
            data_corr_btn = st.checkbox("Apply Data Correction to Input Data")
            if data_corr_btn:
                corr_q = freundlich_isotherm_iast(st.session_state['c_exp_lst'],  st.session_state['K'],  st.session_state['n'])
                st.session_state['corr_q'] = corr_q
            st.info("Please note that the correction will be applied to the input experimental q data w.r.t K and n values to assure smoother input dataset.", icon="ℹ️")

with tab2:
    if 'dosage_lst' not in st.session_state.keys():
        st.info("No input data added yet.")
    else:
        col1, col2 = st.columns(2, gap="medium")
        
        with col1:
            st.subheader("Isotherm Data")
            if 'corr_q' in st.session_state.keys():
                iso_input_df = pd.DataFrame({"mA/VL (mg.C/L)":st.session_state['dosage_lst'], "c (mg.C/L)":st.session_state['c_exp_lst'], "q (mg.C/g)":st.session_state['q_exp_lst'], "Corrected qi": st.session_state['corr_q']})
            else:
                iso_input_df = pd.DataFrame({"mA/VL (mg.C/L)":st.session_state['dosage_lst'], "c (mg.C/L)":st.session_state['c_exp_lst'], "q (mg.C/g)":st.session_state['q_exp_lst']})
            iso_input_df.index += 1
            st.dataframe(iso_input_df, use_container_width=True)
        with col2:
            st.html('''<style>
                    p.value_text{
                            padding-top: 0.25rem;
                            font-size: 1.5rem;
                    }
                    </style>''')
            st.markdown(f'''
                <p class="value_text">c<sub>O</sub> Value : {round(st.session_state['c0'], 2)}</p>''', unsafe_allow_html=True)
            # st.markdown(f'''
            #     <p class="value_text">SAC0 Value : {round(st.session_state['sac0'], 2)}</p>''', unsafe_allow_html=True)
            # if 'corr_c0' in st.session_state.keys():
            #     st.markdown(f'''
            #         <p class="value_text">Corrected c<sub>O</sub> : {round(st.session_state['corr_c0'], 2)}</p>''', unsafe_allow_html=True)
            st.divider()
            st.subheader("Adsorption Components")
            ads_input_df = pd.DataFrame({"K": st.session_state['K'], "n":st.session_state['n']}, index=[f"Component {i}" for i in range(len(K))])
            st.dataframe(ads_input_df, use_container_width=True)
        st.divider()
        input_data_csv = download_input_csv()
        st.download_button("Download ISO Data", input_data_csv, "iso_input.csv", "text/csv", key='download-iso-csv')

if tab3:    
    with tab3:        

        st.markdown("""<h4>Micropollutant Data</h4>""", unsafe_allow_html=True)
        col1, col2 = st.columns(2, gap="medium")
        with col1:
            mp_input_file = st.file_uploader("Upload Micropollutant File", accept_multiple_files=False)
            mA_VL_mp=[]
            c_mp = []
            q_mp = []
            c0_mp = 0
            name_mp = ''
            if mp_input_file:
                try:
                    mA_VL_mp, c_mp, q_mp, c0_mp = read_mp_data_file(mp_input_file)
                    name_mp = ''
                except Exception as e:
                    st.error(f"Error: {e}") 
            elif mp_input_file == None and 'mA_VL_mp' not in st.session_state.keys():
                mp_input_file = './sample_data/sample_mp.csv'
                try:    
                    mA_VL_mp, c_mp, q_mp, c0_mp = read_mp_data_file(mp_input_file)
                    name_mp = "Napthaline" #default name for the default loaded dataset
                except Exception as e:
                    st.error(f"Error: {e}") 
            elif mp_input_file == None and 'mA_VL_mp' in st.session_state.keys():
                mA_VL_mp = st.session_state['mA_VL_mp']
                c_mp = st.session_state['c_mp']
                q_mp = st.session_state['q_mp']
                c0_mp = st.session_state['c0_mp']
                name_mp = st.session_state['name_mp']
            mp_name = st.text_input("Micropollutant Name", value=name_mp)
        with col2:
            c0_mp = st.number_input(r"$c_{O}$", value=c0_mp, key='comp_ads_c0_mp')

            mp_df = pd.DataFrame({"mA/VL":mA_VL_mp, "c":c_mp, "q":q_mp}, columns=("mA/VL", "c", "q"))
            mp_df = mp_df.astype({'mA/VL':float, 'c':float, 'q':float})
            mp_df = st.data_editor(mp_df,
            column_config={
                "mA/VL": st.column_config.NumberColumn("mA/VL", help="About mA/VL parameter"),
                "c": st.column_config.NumberColumn("c", help="About c parameter"),
                "q": st.column_config.NumberColumn("q", help="About q parameter")},
            num_rows="dynamic", use_container_width=True)
        st.divider()
        st.markdown("""<h4>Single Solute Data</h4>""", unsafe_allow_html=True)
        col1, col2 = st.columns(2, gap="medium")
        with col1:
            ss_input_file = st.file_uploader("Upload Single Solute File", accept_multiple_files=False)
            mA_VL_ss = []
            c_ss = []
            c0_ss = 0
            if ss_input_file:
                try:
                    mA_VL_ss, c_ss, c0_ss = read_ss_data_file(ss_input_file)
                except Exception as e:
                    st.error(f"Error: {e}")
            elif ss_input_file == None and 'mA_VL_ss' not in st.session_state.keys():
                ss_input_file = './sample_data/sample_ss.csv'
                try:
                    mA_VL_ss, c_ss, c0_ss = read_ss_data_file(ss_input_file)
                except Exception as e:
                    st.error(f"Error: {e}")
            elif ss_input_file == None and 'mA_VL_ss' in st.session_state.keys():
                mA_VL_ss = st.session_state['mA_VL_ss']
                c_ss = st.session_state['c_ss']
                c0_ss = st.session_state['c0_ss']
        
        with col2:
            c0_ss = st.number_input(r"$c_{O}$", value=c0_ss, key='comp_ads_c0_ss')

            ss_df = pd.DataFrame({"mA/VL":mA_VL_ss, "c":c_ss}, columns=("mA/VL", "c"))
            ss_df = ss_df.astype({'mA/VL':float, 'c':float})
            ss_df = st.data_editor(ss_df,
            column_config={
                "mA/VL": st.column_config.NumberColumn("mA/VL", help="About mA/VL parameter"),
                "c": st.column_config.NumberColumn("c", help="About c parameter")},
            num_rows="dynamic", use_container_width=True)
        st.divider()

        comp_ads_submit_btn = st.button("Submit", key='submit_comp_ads')
        if comp_ads_submit_btn:
            try:
                st.session_state['name_mp'] = mp_name
                st.session_state['c0_mp'] = c0_mp
                st.session_state['mA_VL_mp'] = mp_df['mA/VL'].to_numpy()
                st.session_state['c_mp'] = mp_df['c'].to_numpy()
                st.session_state['q_mp'] = mp_df['q'].to_numpy()

                st.session_state['c0_ss'] = c0_ss
                st.session_state['mA_VL_ss'] = ss_df['mA/VL'].to_numpy()
                st.session_state['c_ss'] = ss_df['c'].to_numpy()

                V = 1 
                q_ss = np.subtract(c0_ss, np.array(c_ss)) * V / mA_VL_ss
                st.session_state['q_ss'] = q_ss
                st.success("Data input successfully.")
            except Exception as e:
                st.error(f"Something went wrong while loading the input data. Please try again. {e}")
if tab4:
    with tab4:
        if 'c0_mp' not in st.session_state.keys():
            st.info("No input data added yet.")
        else:
            col1, col2 = st.columns(2, gap="medium")
            
            with col1:
                st.subheader("Micro Pollutant Data")
                st.html('''<style>
                        p.value_text{
                                padding-top: 0.25rem;
                                font-size: 1.5rem;
                        }
                        </style>''')
                st.markdown(f'''
                    <p class="value_text">Name : {st.session_state['name_mp']}</p>''', unsafe_allow_html=True)
                st.markdown(f'''
                    <p class="value_text">c<sub>O</sub> Value : {round(st.session_state['c0_mp'], 2)}</p>''', unsafe_allow_html=True)
                mp_input_df = pd.DataFrame({"mA/VL (mg.C/L)":st.session_state['mA_VL_mp'], "c (mg.C/L)":st.session_state['c_mp'], "q (mg.C/g)":st.session_state['q_mp']})
                mp_input_df.index += 1
                st.dataframe(mp_input_df, use_container_width=True)
                st.divider()
                mp_input_data_csv = download_mp_csv()
                st.download_button("Download Micro Pollutant Data", mp_input_data_csv, f"micropollutant_input.csv", "text/csv", key='download-mp-csv')
            with col2:            
                st.subheader("Single Solute Data")
                st.html('''<style>
                        p.value_text{
                                padding-top: 0.25rem;
                                font-size: 1.5rem;
                        }
                        </style>''')
                st.markdown(f'''
                    <p class="value_text">c<sub>O</sub> Value : {round(st.session_state['c0_ss'], 2)}</p>''', unsafe_allow_html=True)
                ss_input_df = pd.DataFrame({"mA/VL (mg.C/L)":st.session_state['mA_VL_ss'], "c (mg.C/L)":st.session_state['c_ss']})
                ss_input_df.index += 1
                st.dataframe(ss_input_df, use_container_width=True)
                st.divider()
                ss_input_data_csv = download_ss_csv()
                st.download_button("Download Single Solute Data", ss_input_data_csv, "singlesolute_input.csv", "text/csv", key='download-ss-csv')







#     st.markdown("""
# <style>
#     [data-testid="stSidebar"]{
#         background-color: #f5f5dc;
#         color: coral;
#         margin: 0.5rem;
#         border-radius: 10px
#     }

#     [data-testid="stSidebar"] span, [data-testid="stSidebar"] label{
#         color: #082e5a;
#     }

#     h1{
#         color: #f5f5dc
#     }

# 	.stTabs [data-baseweb="tab-list"] {
# 		background-color: #527a8a;
#         padding: 0px 10px 0px 10px;
#         border-radius: 10px
#     }

#     .stTabs [data-baseweb="tab"] p{
#         font-size: 1rem;
#         color: white;
#         font-weight: 700;
#     }

# 	.stTabs [aria-selected="true"] p{
#         font-size: 1.1rem;
#         font-weight: 700;
#         text-shadow: black 2px 2px 5px;
# 	}

# </style>""", unsafe_allow_html=True)
    # st.write(theme.get("base"))
    # if theme.get("base") == "light":
    #     st.markdown(
    #         """<style>
    #             h1{
    #                 color: black
    #             }
    #         </style>""", unsafe_allow_html=True
    #     )
