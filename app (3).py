# app.py

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load your cleaned dataset
df = pd.read_csv('kleaned_afrimarket_dataset.csv')

st.set_page_config(page_title="AfriMarket Dashboard", layout="wide")

st.title("🛒 AfriMarket Seller Trust Dashboard")
st.markdown("This dashboard presents insights from the Dataverse Africa July Challenge. It focuses on seller risk patterns, complaint trends, and predictive modeling outcomes.")

# Sidebar filters
st.sidebar.header("🔍 Filter Options")
category_filter = st.sidebar.multiselect("Select Product Categories", df['product_category'].dropna().unique())
region_filter = st.sidebar.multiselect("Select Customer Regions", df['customer_region'].unique())

# Apply filters
filtered_df = df.copy()
if category_filter:
    filtered_df = filtered_df[filtered_df['product_category'].isin(category_filter)]
if region_filter:
    filtered_df = filtered_df[filtered_df['customer_region'].isin(region_filter)]

# Section 1: Complaint by Category
st.subheader("📦 Complaints by Product Category")
complaints = filtered_df.groupby('product_category')['complaint_code'].count().sort_values(ascending=False)
fig1, ax1 = plt.subplots()
sns.barplot(x=complaints.values, y=complaints.index, ax=ax1, palette="Reds_r")
ax1.set_xlabel("Number of Complaints")
st.pyplot(fig1)

# Section 2: Regional Delivery Delay
st.subheader("⏱️ Average Delivery Delay by Region")
delay = filtered_df.groupby('customer_region')['delivery_delay'].mean().sort_values(ascending=False)
fig2, ax2 = plt.subplots()
sns.barplot(x=delay.values, y=delay.index, ax=ax2, palette="Blues")
ax2.set_xlabel("Avg Delivery Delay (days)")
st.pyplot(fig2)

# Section 3: High-Risk Sellers
st.subheader("🚨 Top 5 High-Risk Sellers")
risk_cols = ['seller_id', 'return_rate', 'complaint_rate', 'avg_delay', 'seller_risk_score']
if all(col in df.columns for col in risk_cols):
    top_sellers = df[risk_cols].sort_values('seller_risk_score', ascending=False).drop_duplicates('seller_id').head(5)
    st.dataframe(top_sellers.reset_index(drop=True))
else:
    st.warning("Seller risk metrics not found in the dataset.")

st.markdown("---")
st.caption("Dataverse Africa July Challenge — Submitted by Zainab Balarabe Adam")
