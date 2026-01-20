import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# --- CONFIGURATION ---
st.set_page_config(layout="wide", page_title="UIDAI Biometric Update Frequency Dashboard")

@st.cache_data
def load_data():
    try:
        # file from latest task output
        df = pd.read_csv("ABS_SRIS_Final_Action_Plan_final .csv")
        df['date'] = pd.to_datetime(df['date'], dayfirst=True, errors='coerce')
        df.columns = df.columns.str.strip()
        # Normalize text fields to prevent duplicates
        df['state'] = (
            df['state']
            .astype(str)
            .str.strip()
            .str.title()   # Kerala, Tamil Nadu, etc.
        )

        df['district'] = (
            df['district']
            .astype(str)
            .str.strip()
            .str.title()
        )
        return df
    except FileNotFoundError:
        st.error("source file not found. Please ensure the file is in the correct directory.")
        return pd.DataFrame()

df = load_data()

if not df.empty:
    #1. SIDEBAR FILTERS 
    st.sidebar.header("Geography Selection")
    
    # State Level
    state_list = sorted(df['state'].unique().tolist())
    state_choice = st.sidebar.selectbox("1. Select State", state_list)
    state_df = df[df['state'] == state_choice]

    # District Level (Default is "All")
    district_list = ["All"] + sorted(state_df['district'].unique().tolist())
    district_choice = st.sidebar.selectbox("2. Select District", district_list)

    # Pincode Level (Only enabled if a District is chosen)
    if district_choice != "All":
        temp_df = state_df[state_df['district'] == district_choice]
        pincode_list = ["All"] + sorted(temp_df['pincode'].astype(str).unique().tolist())
        pincode_choice = st.sidebar.selectbox("3. Select Pincode", pincode_list)
    else:
        pincode_choice = "All"
        st.sidebar.info("Select a District to enable Pincode drill-down.")

    #2. DATA PROCESSING FOR VISUALS
    if district_choice == "All":
        # State View: Group by District
        plot_df = state_df.groupby('district')[['BSI_17_plus', 'BSI_5_17']].mean().reset_index()
        x_col = 'district'
        title_text = f"Regional Stability Overview: {state_choice}"
    elif pincode_choice == "All":
        # District View: Group by Pincode
        plot_df = state_df[state_df['district'] == district_choice].groupby('pincode')[['BSI_17_plus', 'BSI_5_17']].mean().reset_index()
        plot_df['pincode'] = plot_df['pincode'].astype(str)
        x_col = 'pincode'
        title_text = f"Pincode Analysis: {district_choice}"
    else:
        # Pincode View: Time Series
        plot_df = state_df[(state_df['district'] == district_choice) & (state_df['pincode'].astype(str) == pincode_choice)]
        x_col = 'date'
        title_text = f"Monthly Trend: Pincode {pincode_choice}"

    #3. THE MAIN CHART 
    st.title("UIDAI Update Frequency Dashboard")
    st.subheader(title_text)

    if not plot_df.empty:
        if x_col == 'date':
            # Time series view 
            fig = px.line(plot_df, x=x_col, y=['BSI_17_plus', 'BSI_5_17'], 
                         markers=True, labels={"value": "BSI Frequency", "variable": "Age Group"})
        else:
            # Clustered Bar Chart with logic for Adult Risk coloring
            fig = go.Figure()

            # Adult Bar (Conditional Color: Red if > 2.0)
            adult_colors = ['#FF4B4B' if val > 2.0 else '#00CC96' for val in plot_df['BSI_17_plus']]
            fig.add_trace(go.Bar(
                x=plot_df[x_col], y=plot_df['BSI_17_plus'],
                name='Adults (17+)',
                marker_color=adult_colors
            ))

            # Adolescent Bar (Color: Blue)
            fig.add_trace(go.Bar(
                x=plot_df[x_col], y=plot_df['BSI_5_17'],
                name='Adolescents (5-17)',
                marker_color='#636EFA'
            ))

            fig.update_layout(barmode='group', xaxis_tickangle=-45)

        #THE VISIBLE THRESHOLD
        fig.add_hline(y=2.0, line_dash="dash", line_color="black", 
                      annotation_text="Adult BSI limit 2",
                      annotation_position="top left")

        fig.update_layout(template="plotly_white", yaxis_title="BSI (Update Frequency)")
        st.plotly_chart(fig, use_container_width=True)

        #5. ACTIONABLE ADVICE SECTION
        st.markdown("---")
        col1, col2 = st.columns(2)

        with col1:
            max_adult_bsi = plot_df['BSI_17_plus'].max()
            if max_adult_bsi > 2.0:
                st.error(f"###  High Update Traffic\n**Observation:** Adult BSI ({max_adult_bsi:.2f}) exceeds the given limit.\n\n**Action:** Prioritize for authority-led surveys and mobile update camps to ensure service continuity.  .")
            else:
                st.success("###  Adults Stable\n**Observation:** Biometric update for adults are within normal limits.\n\n**Action:** Continue routine monitoring.")

        with col2:
            max_child_bsi = plot_df['BSI_5_17'].max()
            if max_child_bsi > 5.0:
                st.info(f"### Adolescent Growth Trend\n**Observation:** High updates ({max_child_bsi:.2f}) in 5-17 group.\n\n**Note:** This is a normal biological phenomenon due to physical growth.providing more update facilities  .")
            
            # Scenario: Zero Frequency (Low Access)
            if plot_df['BSI_17_plus'].sum() == 0:
                st.warning("###  Low update Frequency\n**Observation:** Zero or near-zero updates recorded.\n\n**Action:** Recommend launching mobile awareness vans; this area may have poor access to update centers.")

    else:
        st.warning("No data found for the selected criteria.")
else:
    st.info("Please ensure 'task3_risk_output.xlsx - Sheet1.csv' is present to view the dashboard.")
