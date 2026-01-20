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
                st.error(f"###  High Update Traffic\nObservation: Adult BSI ({max_adult_bsi:.2f}) exceeds the given limit.\n\nAction: Prioritize for authority-led surveys and mobile update camps to ensure service continuity.  .")
            else:
                st.success("###  Adults Stable\nObservation: Biometric update for adults are within normal limits.\n\nAction: Continue routine monitoring.")

        with col2:
            max_child_bsi = plot_df['BSI_5_17'].max()
            if max_child_bsi > 5.0:
                st.info(f"### Adolescent Growth Trend\nObservation: High updates ({max_child_bsi:.2f}) in 5-17 group.\n\nNote: This is a normal biological phenomenon due to physical growth.providing more update facilities  .")
            
            # Scenario: Zero Frequency (Low Access)
            if plot_df['BSI_17_plus'].sum() == 0:
                st.warning("###  Low update Frequency\nObservation: Zero or near-zero updates recorded.\n\nAction: Recommend launching mobile awareness vans; this area may have poor access to update centers.")

    else:
        st.warning("No data found for the selected criteria.")
else:
    st.info("Please ensure 'task3_risk_output.xlsx - Sheet1.csv' is present to view the dashboard.")