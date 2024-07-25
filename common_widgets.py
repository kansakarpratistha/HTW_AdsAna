import streamlit as st

def sidebar_creds():
    st.markdown("""
        <style>
            # .st-emotion-cache-1b5bib7{
            #     background-color: #dadfe91c;
            #     box-sizing: content-box;
            #     padding: 5px;
            #     border-radius: 5px;
            #     box-shadow: 0px 0px 15px 0px #171717;
            # }

            .cred{
                text-align: center;
            }
            .cred_li {
                text-align: center;
                display: contents;
                list-style-type: none;
            }
            .cred_li > li {
                padding: 0;
                margin: 0; 
                text-align: center;
                height: 20px;
            }
            .creds_uni{
                margin-top: 10px;
                line-height: 15px;
                font-size: 12px;
                font-style: italic;
                text-align: center;
            }

            .cred,.cred_li,.creds_uni{
                color:#ff9800;
            }

        </style>
    """, unsafe_allow_html=True)
    with st.sidebar:
        with st.container():
            st.markdown("""<h3 class='cred'>By</h3>
                <ul class='cred_li'>
                    <li>Khalid, A.</li>
                    <li>Kansakar, P.</li>
                    <li>Yadav, P. K.</li>
                    <li>Hoth, N.</li>
                    <li>Grischek, T.</li>
                </ul>  
                <p class='creds_uni'>Universität Tübingen<br>Hochschule für Technik und Wirtschaft Dresden<br>Technische Universität Bergakadamie Freiberg</p>
            """, unsafe_allow_html=True)