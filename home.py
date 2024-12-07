import streamlit as st
import pandas as pd
import plotly.express as px

# Load cleaned data

def load_data():
    return pd.read_csv('cleaned_budget_data.csv')

df = load_data()

# Title and description
st.title("Union Budget 2023-24 Analytics Dashboard")
st.markdown("""
### Analyze India's Budget Allocations
Explore insights into government spending across various ministries.
""")

# Sidebar menu
st.sidebar.title("Menu")
menu = st.sidebar.radio("Navigation", ["Overview", "Insights", "Visualizations", "Dynamic Analysis"])

if menu == "Overview":
    st.header("Dataset Overview")
    st.write("The dataset provides details of budget allocations across ministries.")
    st.dataframe(df)
    st.write("**Total Ministries:**", len(df['Ministry'].unique()))
    st.write("**Total Budget (in Cr):** ₹", round(df['Budget_2023_Total'].sum(), 2))

elif menu == "Insights":
    st.header("Key Insights")
    top_ministries = df.sort_values(by='Budget_2023_Total', ascending=False).head(5)
    st.subheader("Top 5 Ministries by Budget Allocation")
    st.table(top_ministries[['Ministry', 'Budget_2023_Total']])
    
    st.subheader("Ministries with Least Allocation")
    least_ministries = df.sort_values(by='Budget_2023_Total', ascending=True).head(5)
    st.table(least_ministries[['Ministry', 'Budget_2023_Total']])
    
    st.metric("Total Revenue Budget", f"₹{df['Budget_2023_Revenue'].sum():,.2f} Cr")
    st.metric("Total Capital Budget", f"₹{df['Budget_2023_Capital'].sum():,.2f} Cr")

elif menu == "Visualizations":
    st.header("Visualizations")

    # Budget Distribution
    fig1 = px.pie(df, names='Ministry', values='Budget_2023_Total', title='Total Budget Allocation')
    st.plotly_chart(fig1)

    # Revenue vs Capital
    fig2 = px.bar(df, x='Ministry', y=['Budget_2023_Revenue', 'Budget_2023_Capital'], 
                  title="Revenue vs Capital Budgets", barmode='group')
    st.plotly_chart(fig2)

    # Treemap Visualization
    fig3 = px.treemap(df, path=['Ministry', 'Demand'], values='Budget_2023_Total',
                      title="Budget Allocation Hierarchy")
    st.plotly_chart(fig3)

elif menu == "Dynamic Analysis":
    st.header("Dynamic Analysis")
    
    # Filter by Budget Category
    budget_category = st.sidebar.selectbox("Select Budget Category", ['Low', 'Medium', 'High'])
    filtered_df = df[df['Budget_Category'] == budget_category]
    st.write(f"Ministries in **{budget_category} Budget** category:")
    st.dataframe(filtered_df)

    # Scatter plot
    x_col = st.sidebar.selectbox("X-axis", df.select_dtypes(include='number').columns)
    y_col = st.sidebar.selectbox("Y-axis", df.select_dtypes(include='number').columns)
    fig4 = px.scatter(df, x=x_col, y=y_col, color='Budget_Category', title=f"{x_col} vs {y_col}")
    st.plotly_chart(fig4)
