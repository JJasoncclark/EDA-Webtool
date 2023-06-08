import streamlit as st
import pandas as pd
from matplotlib import pyplot as plt
import numpy as np
import io

st.title("Exploratory Data Analysis Web Tool")

st.subheader("File Upload")
uploaded_file = st.file_uploader("Choose a file")

if uploaded_file is not None:
    # Can be used wherever a "file-like" object is accepted:
    df = pd.read_csv(uploaded_file)
    show_df = st.checkbox("Show Data Frame", key="enabled")

    if show_df:
      st.write(df)

    analysis_type = st.sidebar.selectbox("Select Analysis Type", 
                                         ("Univariate", "Bivariate"))


    col1, col2, col3, col4, col5 = st.columns(5)
    col1.text("Columns")
    col1.text(df.shape[0])
    col2.text("Rows")
    col2.text(df.shape[1])
    col3.text("Numerical")
    col3.text(df.select_dtypes(include=['int64', 'float64']).shape[1])
    col4.text("Categorical")
    col4.text(df.select_dtypes(include=['object']).shape[1])
    col5.text("Boolean")
    col5.text(df.select_dtypes(include=['bool']).shape[1])

    if analysis_type == "Univariate":
        column_type = st.sidebar.selectbox('Select Data Type',
                                       ("Numerical", "Categorical"))
        if column_type == "Numerical":
            numerical_column = st.sidebar.selectbox(
            'Select a Column', df.select_dtypes(include=['int64', 'float64']).columns)

        # summary statistics
            st.divider()
            st.subheader("Summary Statistics")  
            col1, col2, col3, col4, col5 = st.columns(5)
            col1.text("Minimum")
            col2.text("Lower Quartile")
            col3.text("Median")
            col4.text("Upper Quartile")
            col5.text("Maximum")
            col1.text(np.min(df[numerical_column]))
            col2.text(np.percentile(df[numerical_column], 25))
            col3.text(np.median(df[numerical_column]))
            col4.text(np.percentile(df[numerical_column], 75))
            col5.text(np.max(df[numerical_column]))

        # histogram
            st.divider()
            st.subheader("Histogram")
            col1, col2 = st.columns(2)
            choose_color = col1.color_picker('Pick a Color', "#69b3a2")

            hist_bins = col2.slider('Number of bins', min_value=5,
                                    max_value=150, value=30)
            hist_title = st.text_input('Set Title', 'Histogram')
            hist_xtitle = st.text_input('Set x-axis Title', numerical_column)

            fig, ax = plt.subplots()
            ax.hist(df[numerical_column], bins=hist_bins,
                    edgecolor="black", color=choose_color)
            ax.set_title(hist_title)
            ax.set_xlabel(hist_xtitle)
            ax.set_ylabel('Count')

            st.pyplot(fig)
            filename = "plot.png"
            fig.savefig(filename,dpi = 300)

            # Display the download button
            with open("plot.png", "rb") as file:
                btn = st.download_button(
                    label="Download image",
                    data=file,
                    file_name=numerical_column,
                    mime="image/png"
                )

        if column_type == "Categorical":
            categorical_column = st.sidebar.selectbox(
            'Select a Column', df.select_dtypes(include=['object']).columns)
        
            st.divider()

            st.subheader("Proportions Table")
            head_value = st.slider('Number to display', min_value=1,
                                    max_value=df[categorical_column].nunique(), value=5)
            st.table(df[categorical_column].value_counts(normalize=True).head(head_value))
            
            st.divider()

            st.subheader("Barplot")
            col1, col2 = st.columns(2)
            choose_color = col1.color_picker('Pick a Color', "#69b3a2")

            fig, ax = plt.subplots()
            to_display = col2.slider('How many to display', min_value=1,
                                    max_value=df[categorical_column].nunique(), value=5)
            bar_title = st.text_input('Set Title', 'Barplot')
            bar_xtitle = st.text_input('Set x-axis Title', categorical_column)
            test = df[categorical_column].value_counts(normalize=True)
            ax.bar(test.index[0:to_display], test.values[0:to_display],
                    edgecolor="black", color=choose_color)
            ax.set_title(bar_title)
            ax.set_xlabel(bar_xtitle)
            ax.set_ylabel('Proportion')

            st.pyplot(fig)
            filename = "plot.png"
            fig.savefig(filename,dpi = 300)

            # Display the download button
            with open("plot.png", "rb") as file:
                btn = st.download_button(
                    label="Download image",
                    data=file,
                    file_name=categorical_column,
                    mime="image/png"
                )
    if analysis_type == "Bivariate":
        x_variable = st.sidebar.selectbox("Choose X Variable",
                                          df.select_dtypes(include=['int64', 'float64']).columns)
        y_variable = st.sidebar.selectbox("Choose Y Variable",
                                          df.select_dtypes(include=['int64', 'float64']).columns)
        st.divider()
        st.subheader("Scatterplot")
        show_line = st.checkbox("Show Regression Line", key="disabled")
        fig, ax = plt.subplots()
        x = str(x_variable)
        y = str(y_variable)
        title =  y + ' vs ' + x
        scatter_title = st.text_input('Set Title', title)
        scatter_xtitle = st.text_input('Set x-axis Title', x_variable)
        scatter_ytitle = st.text_input('Set y-axis Title', y_variable)
        ax.scatter(df[x_variable], df[y_variable])
        ax.set_title(scatter_title)
        ax.set_xlabel(scatter_xtitle)
        ax.set_ylabel(scatter_ytitle)
        if show_line:
            coefficients = np.polyfit(df[x_variable], df[y_variable], 1)
            slope = coefficients[0]
            intercept = coefficients[1]
            regression_line = slope * np.array(df[x_variable]) + intercept
            ax.plot(df[x_variable], regression_line, color = "red")

        st.pyplot(fig)
        filename = "plot.png"
        fig.savefig(filename,dpi = 300)

            # Display the download button
        with open("plot.png", "rb") as file:
            btn = st.download_button(
                label="Download image",
                data=file,
                file_name=scatter_title,
                mime="image/png"
            )       