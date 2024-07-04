import streamlit as st
import pandas as pd
from numerize.numerize import numerize
import plotly.express as px


st.set_page_config(page_title="Business Analytics Dashboard", page_icon="🌎", layout="wide")  
st.subheader("📈 Business Analytics Dashboard ")


with open('style.css') as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)


df = pd.read_csv('customers.csv')


df['HireDate'] = pd.to_datetime(df['HireDate'])


st.sidebar.header("Filter Section")
department = st.sidebar.multiselect(
    "Filter Department",
    options=df["Department"].unique(),
    default=df["Department"].unique(),
)
country = st.sidebar.multiselect(
    "Filter Country",
    options=df["Country"].unique(),
    default=df["Country"].unique(),
)
businessunit = st.sidebar.multiselect(
    "Filter Business",
    options=df["BusinessUnit"].unique(),
    default=df["BusinessUnit"].unique(),
)

df_selection = df.query(
    "Department == @department & Country == @country & BusinessUnit == @businessunit"
)


def metrics():
    from streamlit_extras.metric_cards import style_metric_cards
    col1, col2, col3 = st.columns(3)

    col1.metric(label="Total Customers", value=df_selection.Gender.count(), delta="All customers")

    col2.metric(label="Total Annual Salary", value=f"{df_selection.AnnualSalary.sum():,.0f}", delta=df.AnnualSalary.median())

    col3.metric(label="Annual Salary", value=f"{df_selection.AnnualSalary.max()-df.AnnualSalary.min():,.0f}", delta="Annual Salary Range")

    style_metric_cards(background_color="#121270", border_left_color="#f20045", box_shadow="3px")


div1, div2 = st.columns(2)

# Pie chart
def pie():
    with div1:
        theme_plotly = None 
        fig = px.pie(df_selection, values='AnnualSalary', names='City', title='Customers by City')
        fig.update_layout(legend_title="Country", legend_y=0.9)
        fig.update_traces(textinfo='percent+label', textposition='inside')
        st.plotly_chart(fig, use_container_width=True, theme=theme_plotly)

# Donut chart
def donut_chart():
    with div1:
        theme_plotly = None 
        fig = px.pie(df_selection, values='AnnualSalary', names='Department', title='Customers by Department', hole=0.3)
        fig.update_layout(legend_title="Department", legend_y=0.9)
        fig.update_traces(textinfo='percent+label', textposition='inside')
        st.plotly_chart(fig, use_container_width=True, theme=theme_plotly)

# Bar chart
def barchart():
    theme_plotly = None

    fig = px.bar(df_selection, y='AnnualSalary', x='JobTitle', text_auto='.2s', title="Controlled text sizes, positions and angles",
                     color='JobTitle',
                     color_discrete_sequence=px.colors.qualitative.Dark24)  
    fig.update_traces(textfont_size=18, textangle=0, textposition="outside", cliponaxis=False)
    st.plotly_chart(fig, use_container_width=True, theme="streamlit")

# Scatter plot 
def scatter_plot():
    theme_plotly = None 
    with div2:
        fig = px.scatter(df_selection, x='HireDate', y='AnnualSalary', title="Annual Salary vs Hire Date")
        fig.update_layout(xaxis_title='Hire Date', yaxis_title='Annual Salary')
        st.plotly_chart(fig, use_container_width=True, theme=theme_plotly)

# 100% Stacked bar chart 
def stacked_barchart():
    with div2:
        gender_counts = df_selection.groupby(['Department', 'Gender']).size().reset_index(name='Count')
        gender_counts['Percentage'] = gender_counts.groupby('Department')['Count'].apply(lambda x: x / x.sum() * 100).values
    
        fig = px.bar(gender_counts, x='Department', y='Percentage', color='Gender', 
                 title="Gender Distribution by Department (100% Stacked)",
                 labels={'Percentage':'Percentage', 'Department':'Department'},
                 color_discrete_sequence=px.colors.qualitative.Dark24)
    
        fig.update_layout(barmode='stack', xaxis={'categoryorder':'total descending'})
        st.plotly_chart(fig, use_container_width=True)


def table():
    with st.expander("Tabular"):
        shwdata = st.multiselect('Filter :', df.columns, default=["EEID", "FullName", "JobTitle", "Department", "BusinessUnit", "Gender", "Ethnicity", "Age", "HireDate", "AnnualSalary", "Bonus", "Country", "City", "id"])
        st.dataframe(df_selection[shwdata], use_container_width=True)

# menu
from streamlit_option_menu import option_menu
with st.sidebar:
    selected = option_menu(
        menu_title="Main Menu",
        options=["Home", "Table"],
        icons=["house", "book"],
        menu_icon="cast", 
        default_index=0,
        orientation="vertical",
    )

if selected == "Home":
    metrics()
    pie()
    donut_chart()  
    barchart()
    scatter_plot()  
    stacked_barchart()  
    
if selected == "Table":
    metrics()
    table()
    st.dataframe(df_selection.describe().T, use_container_width=True)
