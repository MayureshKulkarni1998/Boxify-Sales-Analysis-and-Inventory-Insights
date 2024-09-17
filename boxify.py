# -*- coding: utf-8 -*-
"""
Spyder Editor

"""
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import os

df_raw = pd.read_csv('Boxify Dataset.csv')
df_cleaned = df_raw.dropna()
df_cleaned1 = df_cleaned.isnull().sum()

duplicates = df_cleaned[df_cleaned.duplicated()]
df_cleaned2 = df_cleaned.drop_duplicates()
print(f"Found {len(duplicates)} duplicate rows:\n{duplicates}")

df = df_cleaned2;

#Module 1: Analyze sales trends and variations over time.

valid_years = df['ReleaseYear'] >= 1900
cleaned_data = df[valid_years]

sales_trends = cleaned_data.groupby('ReleaseYear')['SoldCount'].sum()

plt.figure(figsize=(12, 6))
sns.lineplot(x=sales_trends.index, y=sales_trends.values)
plt.title('Sales Trends Over Time')
plt.xlabel('Year')
plt.ylabel('Total Sold Count')
plt.grid(True)
plt.tight_layout()
plt.savefig('Sales_Trend_Over_Time.png', dpi=300, bbox_inches='tight')
plt.show()

#Module 1 Ends

#Module 2: Identify top-selling products and categories.

top_selling_products = cleaned_data.groupby('SKU_number')['SoldCount'].sum().sort_values(ascending=False).head(10)

# Plot top-selling products
plt.figure(figsize=(12, 6))
sns.barplot(x=top_selling_products.index, y=top_selling_products.values)
plt.title('Top 10 Selling Products')
plt.xlabel('SKU Number')
plt.ylabel('Total Sold Count')
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig('Top_10_Selling_Products.png', dpi=300, bbox_inches='tight')
plt.show()

# Step 2: Identify the top categories
top_categories = cleaned_data.groupby('MarketingType')['SoldCount'].sum().sort_values(ascending=False).head(10)

# Plot top categories
plt.figure(figsize=(12, 6))
sns.barplot(x=top_categories.index, y=top_categories.values)
plt.title('Top Categories')
plt.xlabel('Marketing Type')
plt.ylabel('Total Sold Count')
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig('Top_Categories.png', dpi=300, bbox_inches='tight')
plt.show()

#Module 2 Ends

#Module 3: Investigate stock levels and low-stock items.

# Step 1: Analyze the distribution of stock levels (ItemCount)
plt.figure(figsize=(12, 6))
sns.histplot(cleaned_data['ItemCount'], bins=30, kde=True)
plt.title('Distribution of ItemCount')
plt.xlabel('Item Count')
plt.ylabel('Frequency')
plt.grid(True)
plt.tight_layout()
plt.savefig('Distribution_Of_ItemCount.png', dpi=300, bbox_inches='tight')
plt.show()

# Step 2: Identify low-stock items (considering items with ItemCount < 10 as low stock)
low_stock_items = cleaned_data[cleaned_data['ItemCount'] < 10]

# Display a summary of low stock items
low_stock_summary = low_stock_items[['SKU_number', 'ItemCount']].sort_values(by='ItemCount')

# Show the first few rows of low-stock items
print(low_stock_summary.head(10))

#Module 3 Ends 

#Module 4: Calculate key performance indicators (e.g., inventory turnover, stock-to-sales ratio, reorder points).

# Calculate Net Sales
cleaned_data['Net_Sales'] = cleaned_data['SoldCount'] * cleaned_data['PriceReg']

# Calculate Average Inventory
average_inventory = cleaned_data['ItemCount'].mean()

# Assuming an average profit margin of 30% to approximate COGS
profit_margin = 0.30
cleaned_data['COGS'] = cleaned_data['Net_Sales'] * (1 - profit_margin)

# Calculate Inventory Turnover
inventory_turnover = cleaned_data['COGS'].sum() / average_inventory

# Calculate Stock-to-Sales Ratio
stock_to_sales_ratio = average_inventory / cleaned_data['Net_Sales'].sum()

# Assume a lead time of 2 weeks and average weekly demand (approximated from total SoldCount)
lead_time_weeks = 2
average_weekly_demand = cleaned_data['SoldCount'].sum() / 52
lead_time_demand = lead_time_weeks * average_weekly_demand

# Assume safety stock is 20% of lead time demand
safety_stock = 0.20 * lead_time_demand

# Calculate Reorder Points
reorder_point = lead_time_demand + safety_stock

# Identify peak sales periods
cleaned_data['Month'] = pd.to_datetime(cleaned_data['ReleaseYear'], format='%Y').dt.month
monthly_sales = cleaned_data.groupby('Month')['SoldCount'].sum()


# Print KPI results
print(f"Inventory Turnover: {inventory_turnover:.2f}")
print("Stock-to-Sales Ratio:", stock_to_sales_ratio)
print(f"Reorder Point: {reorder_point:.2f}")

# Recommendations summary
recommendations = {
    'Inventory Turnover': inventory_turnover,
    'Stock-to-Sales Ratio': stock_to_sales_ratio,
    'Reorder Point': reorder_point,
    'Monthly Sales': monthly_sales,
    'Top Selling Products': top_selling_products,
    'Low Stock Items': low_stock_items
}

# Print recommendations summary
for key, value in recommendations.items():
    print(f"{key}:\n{value}\n")