
import streamlit as st
import pandas as pd
from io import BytesIO

st.set_page_config(
    page_title="Clean the Dataset",
    page_icon="🧹",
    layout="wide"
)

st.title("🧹 Clean the Dataset")
st.write(
    "Upload a CSV file, clean your data, "
    "review the results, and download the cleaned file."
)

uploaded_file = st.file_uploader(
    "Upload your dataset (CSV)",
    type=["csv"]
)

if uploaded_file is not None:
    try:
        df = pd.read_csv(uploaded_file)

        st.subheader("Original Dataset")
        st.dataframe(df, use_container_width=True)

        original_rows = len(df)
        original_duplicates = int(df.duplicated().sum())
        original_missing = int(df.isna().sum().sum())

        st.subheader("Cleaning Options")

        remove_duplicates = st.checkbox(
            "Remove duplicate rows", value=True
        )

        missing_option = st.selectbox(
            "How should missing values be handled?",
            [
                "Fill with suitable default values",
                "Remove rows with missing values",
                "Keep missing values"
            ]
        )

        if st.button("Clean Dataset", type="primary"):
            cleaned_df = df.copy()

            if remove_duplicates:
                cleaned_df = cleaned_df.drop_duplicates()

            if missing_option == "Fill with suitable default values":
                for column in cleaned_df.columns:
                    if cleaned_df[column].isna().any():
                        if pd.api.types.is_numeric_dtype(
                            cleaned_df[column]
                        ):
                            cleaned_df[column] = (
                                cleaned_df[column].fillna(
                                    cleaned_df[column].median()
                                )
                            )
                        else:
                            cleaned_df[column] = (
                                cleaned_df[column].fillna("Unknown")
                            )

            elif missing_option == "Remove rows with missing values":
                cleaned_df = cleaned_df.dropna()

            cleaned_rows = len(cleaned_df)
            duplicates_removed = original_rows - (
                len(df.drop_duplicates())
                if remove_duplicates else original_rows
            )
            missing_remaining = int(
                cleaned_df.isna().sum().sum()
            )

            st.success("Dataset cleaned successfully!")

            col1, col2, col3, col4 = st.columns(4)

            col1.metric("Original Rows", original_rows)
            col2.metric("Cleaned Rows", cleaned_rows)
            col3.metric(
                "Duplicate Rows Removed",
                duplicates_removed
            )
            col4.metric(
                "Missing Cells Remaining",
                missing_remaining
            )

            st.subheader("Cleaned Dataset")
            st.dataframe(
                cleaned_df,
                use_container_width=True
            )

            st.subheader("Cleaning Summary")

            summary = pd.DataFrame({
                "Metric": [
                    "Original rows",
                    "Original duplicate rows",
                    "Original missing cells",
                    "Final rows",
                    "Final missing cells"
                ],
                "Value": [
                    original_rows,
                    original_duplicates,
                    original_missing,
                    cleaned_rows,
                    missing_remaining
                ]
            })

            st.dataframe(summary, hide_index=True)

            csv_data = cleaned_df.to_csv(
                index=False
            ).encode("utf-8")

            st.download_button(
                label="Download Cleaned Dataset",
                data=csv_data,
                file_name="cleaned_dataset.csv",
                mime="text/csv"
            )

    except Exception as error:
        st.error(f"Could not process the dataset: {error}")

else:
    st.info("Upload a CSV file to start cleaning.")
