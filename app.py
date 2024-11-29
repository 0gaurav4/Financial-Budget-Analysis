import streamlit as st
import pandas as pd
import plotly.express as px
# UI Configuration

st.set_page_config(
    page_title="Financial",
    page_icon="🪙",
    layout="wide"
)
with open('style.css') as css:
    st.markdown(f"<style>{css.read()}</style>", unsafe_allow_html=True)

@st.cache_data
def load_data():
    return pd.read_csv("Indian Union Budget FY 21-22 till 23-24.csv")

# UI integration

#
with st.spinner("loading dataset..."):
    df = load_data().head(400)
    # st.snow()


st.title("Financial Data Analytics")
st.subheader("A simple data app to analyze Finance data")    

st.sidebar.title("Menu")
choice = st.sidebar.radio("Options", ["View Data","Visualize Data","Column Analysis"])
if choice == "View Data":
    st.markdown('''
        # About Dataset
The Indian Economy is currently the 5th Largest Economy in the world. And it aims to reach among the Top 3 in the next 3-4 years. It has registered tremendous economic growth over the last decade.

The 2023 Union Budget of India was presented by the Minister of Finance of India on February 01, 2023.

The Union Budget for FY 2023-24 aims to further strengthen India's economic status. In the 75th Year of India's Independence, the World has recognized the Indian Economy as a 'bright star' with its Economic Growth estimated at 7 per cent, which is the highest among all major economies.

The Vision for** 'Amrit Kaal'** articulated in the Union Budget for FY 2023-24 is centered around:

Opportunities for Citizens with focus on youth
Growth & Job creation
Strong & Stable Macro-Economic Environment
The seven priorities, termed Saptarishi, adopted in the Union Budget for FY 2023-24 to guide the country towards 'Amrit Kaal', thus providing a blueprint for an empowered and inclusive economy, are:

Inclusive Development
- Reaching the last mile
- Infrastructure & Investment
- Unleashing the potential
Green Growth
Youth Power
Financial Sector
The dataset provides details about India's allocation of budget to different schemes in various Ministries under Government of India since Fiscal Year 2021-22 to FY 23-24.

The exploratory analysis of the dataset will provide important views about where the Government is targeting in the last few years so as to bring about such drastic change in the economy.
    ''')
    st.header("Raw Dataset")
    st.dataframe(df)
elif choice == "Visualize Data":
    st.header("Visualization")
    cat_cols = df.select_dtypes(include="object").columns.tolist()
    num_cols = df.select_dtypes(exclude="object").columns.tolist()
    cat_cols.remove("Ministry/Department")
    # num_cols.remove("Scheme")
    num_cols.remove("Actuals 2021-2022 Total")
    cat_cols.append("Actuals 2021-2022 Total")
    # cat_cols.append("Scheme")

    snum_cols = st.sidebar.selectbox("Select a numeric column", num_cols)
    scat_cols = st.sidebar.selectbox("Select a catagorical column", cat_cols)

    c1, c2 = st.columns(2)

    # visualization

    fig1 = px.histogram(df.head(40),x=snum_cols,
                        title=f"Distribution of {snum_cols}")

    fig2 = px.pie(df.head(30),names=scat_cols,title=f"Distribution of {scat_cols}",hole=0.3)

    c1.plotly_chart(fig1)
    c2.plotly_chart(fig2)

    fig3 = px.box(df.head(10),x=scat_cols, y=snum_cols, color=scat_cols, title=f"{snum_cols} by {scat_cols}")
    st.plotly_chart(fig3)

    fig4 = px.treemap(
        df.head(40),path=["Ministry/Department","Actuals 2021-2022 Total"],
        title="financial type Distribution"
    )

    st.plotly_chart(fig4)

elif choice == "Column Analysis":
    columns = df.columns.tolist()
    columns.remove("Ministry/Department")
    scol = st.sidebar.selectbox("Select a column", columns)
    if df.head(40)[scol].dtype == "object":
        vc = df[scol].value_counts()
        most_common = vc.idxmax()
        c1, c2 = st.columns([3,1])
        fig5 = px.histogram(df.head(40),x=scol,title=f"Distribution of {scol}")
        c1.plotly_chart(fig5)
        c2.subheader("Total Data")
        c2.dataframe(vc,use_container_width=True)
        c2.metric("Most Common", most_common, int(vc[most_common]))

        c1, c2 = st.columns(2)
        fig2 = px.pie(df.head(30),names=scol,title=f"Percentage wise of{scol}",hole=.3)
        c1.plotly_chart(fig2)
        fig3 = px.box(df.head(30), x=scol,title=f"{scol} by {scol}")
        c2.plotly_chart(fig3)
        fig = px.funnel_area(names=vc.index, values=vc.values,title=f"{scol} Funnel Area", height=600)
        st.plotly_chart(fig, use_container_width=True)

    else:
        tab1 , tab2 = st.tabs([" Revised Estimates2022-2023 Total","Budget Estimates2023-2024 Total"])
        with tab1:
            score = df.head(10)[scol].describe() 
            fig1 = px.histogram(df.head(10), x=scol, title=f"Distribution of {scol}")
            fig2 = px.box(df.head(10), x=scol, title=f"{scol} by {scol}")
            c1,c2,c3 = st.columns([2,3,3])
            c1.dataframe(score)
            c2.plotly_chart(fig1)
            c3.plotly_chart(fig2)
        with tab2:
            c1, c2 = st.columns(2)
            col2 = c1.selectbox("Select a Column",df.select_dtypes(include="number").columns.tolist())
            color = c2.selectbox(
                "Select a Color", df.select_dtypes(exclude="number").columns.tolist()
            )
            fig3 = px.scatter(df.head(30),x=scol,y=col2,color=color,title=f"{scol} vs {col2}",height=600)
            st.plotly_chart(fig3, use_container_width=True)








