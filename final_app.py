import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import io

# --- Page Config ---
st.set_page_config(page_title="Quick Viz Studio", layout="wide", page_icon="📈")

# --- Custom CSS Styling ---
st.markdown("""
    <style>
    .main {
        background-color: #0f1117;
    }

    .stApp {
        font-family: 'Segoe UI', sans-serif;
        background: url("https://wallpapers.com/images/hd/plain-grey-background-h9vimscs4l3cl53t.jpg");
        background-size: cover;
    }

    /* Quick Checks Section */
    .css-1aumxhk {
        background-color: #1e1e1e !important;
        padding: 10px;
        border-radius: 12px;
        color: #ffffff !important;
    }

    /* Markdown paragraphs */
    .stMarkdown > div > p {
        color: #ffffff;
    }

    /* Change all text color inside main container */
    .block-container {
        color: #eeeeee;
    }

    /* DataFrame and Table font colors */
    .stDataFrame, .stTable, .css-1d391kg {
        color: #e6e6e6 !important;
        background-color: #121212 !important;
    }

    /* Dataframe header text */
    .stDataFrame div[data-testid="stDataFrame"] thead tr th {
        color: #FFD700 !important;
        background-color: #222222 !important;
    }

    /* Headings */
    h1, h2, h3, h4 {
        color: #ffffff;
    }

    /* Tabs Styling */
    .stTabs [data-baseweb="tab"] {
        background-color: #333;
        color: white;
        border-radius: 8px;
        margin-right: 10px;
    }

    .stTabs [aria-selected="true"] {
        background-color: #00A86B;
        color: white;
        font-weight: bold;
    }

    /* SIDEBAR background */
    section[data-testid="stSidebar"] {
        background-color:#7A7878 !important;
        color: white !important;
        border-right: 2px solid #444;
    }

    /* --- 📦 ADDED: Custom Categorical and Numerical Box --- */
    .custom-box {
        background-color: #444;
        padding: 10px 15px;
        border-radius: 10px;
        margin-bottom: 15px;
        color: white;
    }

    .custom-box h5 {
        color: #00c6ff;
        font-weight: bold;
        margin: 0;
    }

    .custom-box.num h5 {
        color: #ffb347;
    }
    </style>
""", unsafe_allow_html=True)

# --- Centered Title with Icon ---
st.markdown("""
<div style="text-align: center; margin-top: 20px;">
    <img src="https://cdn-icons-png.flaticon.com/512/3209/3209265.png" width="50" style="vertical-align: middle; margin-right: 10px;">
    <span style="font-size: 70px; font-weight: bold; color: white;"> Quick Viz Studio </span></div>
""", unsafe_allow_html=True)

# --- Title ---
st.title("📊 Smart Data Visualizer")
st.markdown("Upload your **CSV file** and perform quick visual and statistical analysis effortlessly.")

# --- Sidebar ---
st.sidebar.header("📁 Upload and Configuration")
uploaded_file = st.sidebar.file_uploader("Upload CSV File", type=["csv"])

if uploaded_file is not None:
    st.sidebar.success("✅ File uploaded successfully!")

    try:
        df = pd.read_csv(uploaded_file)

        # Identify columns
        all_cat_cols = df.select_dtypes(include=["object", "category"]).columns.tolist()
        all_num_cols = df.select_dtypes(include=["int64", "float64"]).columns.tolist()

        st.sidebar.subheader("🧮 Choose Columns")
        selected_cat_col = st.sidebar.selectbox("Categorical Column", all_cat_cols) if all_cat_cols else None
        selected_num_col = st.sidebar.selectbox("Numerical Column", all_num_cols) if all_num_cols else None

        st.sidebar.subheader("📊 Choose Plot Type")
        cat_plot_type = None
        num_plot_type = None

        if selected_cat_col:
            cat_plot_type = st.sidebar.radio(" 📑Categorical Plot Type", ["Frequency Table", "Bar Chart", "Pie Chart"])

        if selected_num_col:
            num_plot_type = st.sidebar.radio(" 📈 Numerical Plot Type", [
                "Statistical Analysis", "Histogram", "Box Plot",
                "Distribution Plot", "Correlation Heatmap", "Scatter Plot"
            ])

        # --- TABS ---
        tab1, tab2, tab3 = st.tabs(["🗃️ Data Overview", "📑 Categorical Analysis", "📈 Numerical Analysis"])

        # ========== TAB 1 ==========
        with tab1:
            st.subheader("🔍 Raw Data Preview")
            st.dataframe(df, use_container_width=True)

            st.subheader("📌 Quick Checks")
            st.write("**Shape:**", df.shape)
            st.write("**Number of Rows:**", df.shape[0])
            st.write("**Number of Columns:**", df.shape[1])
            st.write("**Number of Values (Size):**", df.size)
            st.write("**Length:**", len(df))
            st.write("**Null Values (Column-wise):**")
            st.write(df.isnull().sum())
            st.write("**Column Names:**", df.columns.tolist())

            with st.expander("ℹ️ Data Info"):
                buffer = io.StringIO()
                df.info(buf=buffer)
                s = buffer.getvalue()
                st.text(s)

        # ========== TAB 2 ==========
        with tab2:
            if not all_cat_cols:
                st.warning("⚠️ No categorical columns found.")
            elif selected_cat_col and cat_plot_type:
                st.subheader(f"📊 Categorical Analysis: `{selected_cat_col}`")
                value_counts = df[selected_cat_col].value_counts()

                if cat_plot_type == "Frequency Table":
                    st.dataframe(value_counts.to_frame(name="Count"))

                elif cat_plot_type == "Bar Chart":
                    fig, ax = plt.subplots()
                    colors = sns.color_palette("Set2", len(value_counts))
                    bars = ax.bar(value_counts.index.astype(str), value_counts.values, color=colors)
                    ax.set_title(f"Bar Chart of {selected_cat_col}")
                    ax.set_xlabel(selected_cat_col)
                    ax.set_ylabel("Count")
                    ax.bar_label(bars)
                    plt.xticks(rotation=45)
                    st.pyplot(fig)

                elif cat_plot_type == "Pie Chart":
                    fig, ax = plt.subplots()
                    ax.pie(value_counts.values,
                           labels=value_counts.index.astype(str),
                           autopct='%0.2f%%',
                           explode=[0.02] * len(value_counts),
                           startangle=90)
                    ax.set_title(f"Pie Chart of {selected_cat_col}")
                    st.pyplot(fig)

        # ========== TAB 3 ==========
        with tab3:
            if not all_num_cols:
                st.warning("⚠️ No numerical columns found.")
            elif selected_num_col and num_plot_type:
                st.subheader(f"📈 Numerical Analysis: `{selected_num_col}`")

                if num_plot_type == "Statistical Analysis":
                    st.write(df[selected_num_col].describe())

                elif num_plot_type == "Histogram":
                    fig, ax = plt.subplots()
                    sns.histplot(df[selected_num_col], bins=30, ax=ax, color="steelblue")
                    ax.set_title(f"Histogram of {selected_num_col}")
                    st.pyplot(fig)

                elif num_plot_type == "Box Plot":
                    fig, ax = plt.subplots()
                    ax.boxplot(df[selected_num_col], vert=False)
                    ax.set_title(f"Box Plot of {selected_num_col}")
                    st.pyplot(fig)

                elif num_plot_type == "Distribution Plot":
                    fig, ax = plt.subplots()
                    sns.histplot(df[selected_num_col], kde=True)
                    ax.set_title(f"Distribution Plot of {selected_num_col}")
                    st.pyplot(fig)

                elif num_plot_type == "Correlation Heatmap":
                    corr = df[all_num_cols].corr()
                    fig, ax = plt.subplots(figsize=(10, 6))
                    sns.heatmap(corr, annot=True)
                    ax.set_title("Correlation Heatmap")
                    st.pyplot(fig)

                elif num_plot_type == "Scatter Plot":
                    st.info("📌 Scatter plot requires two numerical columns.")
                    x_col = st.selectbox("X-axis Column", all_num_cols, index=0)
                    y_col = st.selectbox("Y-axis Column", all_num_cols, index=1 if len(all_num_cols) > 1 else 0)

                    if x_col and y_col:
                        fig, ax = plt.subplots()
                        sns.scatterplot(data=df, x=x_col, y=y_col)
                        ax.set_title(f"Scatter Plot: {x_col} vs {y_col}")
                        st.pyplot(fig)

    except Exception as e:
        st.error(f"❌ Failed to read the file. Error: {e}")

else:
    st.sidebar.warning("⚠️ No file uploaded yet.")
    st.info("📤 Please upload a CSV file to get started.")


# EDA Streamlit Application