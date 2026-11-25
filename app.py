
# Import libraries
import streamlit as st
import pandas as pd
import plotly.express as px

# Load the dataset
df = pd.read_csv('coffee_shop_sales.csv')

# Calculate total sales
df['sales'] = df['transaction_qty'] * df['unit_price']

# Add dashboard title
st.title('Coffee Shop Sales Dashboard')

# Add dashboard description
st.write('Explore coffee shop sales through charts and filters.')

# Add store filter
store = st.sidebar.selectbox(
    'Select Store',
    df['store_location'].unique()
)

# Filter data by store
df = df[df['store_location'] == store]

# Add product category filter
category = st.sidebar.selectbox(
    'Select Product Category',
    df['product_category'].unique()
)

# Filter data by category
df = df[df['product_category'] == category]

# Show key metrics
col1, col2, col3, col4 = st.columns(4)

col1.metric('Total Sales', round(df['sales'].sum(), 2))
col2.metric('Total Transactions', len(df))
col3.metric('Total Quantity', df['transaction_qty'].sum())
col4.metric('Average Price', round(df['unit_price'].mean(), 2))

# Sales by product category
sales_category = df.groupby('product_category')['sales'].sum().reset_index()

fig = px.bar(sales_category, x='product_category', y='sales',
             title='Sales by Product Category')

st.plotly_chart(fig)

# Sales by store location
sales_store = df.groupby('store_location')['sales'].sum().reset_index()

fig = px.bar(sales_store, x='store_location', y='sales',
             title='Sales by Store Location')

st.plotly_chart(fig)

# Monthly sales
df['month'] = pd.to_datetime(df['transaction_date']).dt.month_name()
monthly_sales = df.groupby('month')['sales'].sum().reset_index()

fig = px.bar(monthly_sales, x='month', y='sales',
             title='Monthly Sales')

st.plotly_chart(fig)

# Top 10 products
top_products = df['product_detail'].value_counts().head(10).reset_index()
top_products.columns = ['product_detail', 'count']

fig = px.bar(top_products, x='product_detail', y='count',
             title='Top 10 Products')

st.plotly_chart(fig)

# Sales by product type
sales_type = df.groupby('product_type')['sales'].sum().reset_index()

fig = px.bar(sales_type, x='product_type', y='sales',
             title='Sales by Product Type')

st.plotly_chart(fig)

# Show raw data
if st.checkbox('Show Raw Data'):
    st.dataframe(df)

# Show key findings
st.subheader('Key Findings')
st.write('Coffee is the most popular product category.')
st.write('June has the highest total sales.')
st.write("Hell's Kitchen has the highest total sales among store locations.")
