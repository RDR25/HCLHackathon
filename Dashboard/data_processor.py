"""
Data Processing Module for Retail Loyalty Analytics Platform
Handles loading, cleaning, and aggregating sample data
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import os

class DataProcessor:
    def __init__(self, data_path="SampleData"):
        self.data_path = data_path
        self.customers_df = None
        self.products_df = None
        self.stores_df = None
        self.sales_header_df = None
        self.sales_line_items_df = None
        self.loyalty_rules_df = None
        
    def load_all_data(self):
        """Load all CSV files"""
        try:
            self.customers_df = pd.read_csv(os.path.join(self.data_path, 'customers_master.csv'))
            self.products_df = pd.read_csv(os.path.join(self.data_path, 'products_master.csv'))
            self.stores_df = pd.read_csv(os.path.join(self.data_path, 'stores_master.csv'))
            self.sales_header_df = pd.read_csv(os.path.join(self.data_path, 'sales_header.csv'))
            self.sales_line_items_df = pd.read_csv(os.path.join(self.data_path, 'sales_line_items.csv'))
            self.loyalty_rules_df = pd.read_csv(os.path.join(self.data_path, 'loyalty_rules_master.csv'))
            
            # Convert date columns
            self.customers_df['Enrollment_Date'] = pd.to_datetime(self.customers_df['Enrollment_Date'])
            self.sales_header_df['Date'] = pd.to_datetime(self.sales_header_df['Date'])
            
            return True
        except Exception as e:
            print(f"Error loading data: {e}")
            return False
    
    def get_summary_metrics(self):
        """Get overall summary metrics"""
        total_sales = self.sales_header_df['Total_Value'].sum()
        total_transactions = len(self.sales_header_df)
        total_customers = len(self.customers_df)
        total_points_earned = self.sales_header_df['Total_Points_Earned'].sum()
        avg_transaction_value = total_sales / total_transactions if total_transactions > 0 else 0
        
        return {
            'Total Sales': f"${total_sales:,.2f}",
            'Total Transactions': total_transactions,
            'Total Customers': total_customers,
            'Total Points Earned': int(total_points_earned),
            'Avg Transaction Value': f"${avg_transaction_value:,.2f}"
        }
    
    def get_rfm_analysis(self):
        """Get RFM (Recency, Frequency, Monetary) analysis with dynamic segmentation"""
        # Get the latest date in sales data
        latest_date = self.sales_header_df['Date'].max()
        
        # Merge sales data with customer data (only get Cust_ID and Enrollment_Date)
        sales_with_cust = self.sales_header_df.merge(
            self.customers_df[['Cust_ID', 'Enrollment_Date']], 
            on='Cust_ID', 
            how='left'
        )
        
        rfm_data = sales_with_cust.groupby('Cust_ID').agg({
            'Date': 'max',
            'Ticket_ID': 'count',
            'Total_Value': 'sum'
        }).reset_index()
        
        # Calculate Recency (days since last purchase)
        rfm_data['Recency'] = (latest_date - rfm_data['Date']).dt.days
        rfm_data.rename(columns={
            'Ticket_ID': 'Frequency',
            'Total_Value': 'Monetary'
        }, inplace=True)
        
        # Calculate RFM Scores (1-5 scale)
        # Lower recency is better (5 is best, 1 is worst)
        rfm_data['R_Score'] = pd.cut(rfm_data['Recency'], bins=5, labels=[5, 4, 3, 2, 1], duplicates='drop')
        # Higher frequency is better (1 is worst, 5 is best)
        rfm_data['F_Score'] = pd.qcut(rfm_data['Frequency'].rank(method='first'), q=5, labels=[1, 2, 3, 4, 5], duplicates='drop')
        # Higher monetary is better (1 is worst, 5 is best)
        rfm_data['M_Score'] = pd.qcut(rfm_data['Monetary'].rank(method='first'), q=5, labels=[1, 2, 3, 4, 5], duplicates='drop')
        
        # Convert scores to numeric
        rfm_data['R_Score'] = pd.to_numeric(rfm_data['R_Score'], errors='coerce').fillna(3).astype(int)
        rfm_data['F_Score'] = pd.to_numeric(rfm_data['F_Score'], errors='coerce').fillna(3).astype(int)
        rfm_data['M_Score'] = pd.to_numeric(rfm_data['M_Score'], errors='coerce').fillna(3).astype(int)
        
        # Calculate RFM Segment based on scores
        rfm_data['RFM_Segment'] = rfm_data.apply(self._calculate_segment_row, axis=1)
        
        return rfm_data.drop('Date', axis=1)
    
    def _calculate_segment_row(self, row):
        """Calculate customer segment for a single row based on RFM scores"""
        r_score = row['R_Score']
        f_score = row['F_Score']
        m_score = row['M_Score']
        
        # Segment logic based on RFM scores
        if r_score >= 4 and f_score >= 4 and m_score >= 4:
            return 'Champion'
        elif r_score >= 3 and f_score >= 3 and m_score >= 3:
            return 'Loyalist'
        elif r_score <= 2 and f_score >= 3:
            return 'At Risk'
        elif r_score >= 4 and f_score <= 2 and m_score <= 2:
            return 'New'
        elif r_score <= 2 and f_score <= 2:
            return 'Lost'
        else:
            return 'Potential'
    
    def get_segment_distribution(self):
        """Get customer segment distribution based on calculated RFM"""
        rfm_data = self.get_rfm_analysis()
        segment_dist = rfm_data['RFM_Segment'].value_counts().reset_index()
        segment_dist.columns = ['Segment', 'Count']
        return segment_dist
    
    def get_sales_by_category(self):
        """Get sales by product category"""
        sales_with_products = self.sales_line_items_df.merge(self.products_df, on='SKU', how='left')
        sales_with_products = sales_with_products.merge(
            self.sales_header_df[['Ticket_ID', 'Date']], on='Ticket_ID', how='left'
        )
        
        category_sales = sales_with_products.groupby('Category').agg({
            'Line_Total': 'sum',
            'Ticket_ID': 'count',
            'Qty': 'sum'
        }).reset_index()
        
        category_sales.columns = ['Category', 'Total_Sales', 'Transactions', 'Quantity']
        return category_sales.sort_values('Total_Sales', ascending=False)
    
    def get_sales_by_store(self):
        """Get sales by store"""
        sales_with_store = self.sales_header_df.merge(self.stores_df, on='Store_ID', how='left')
        
        store_sales = sales_with_store.groupby(['Store_ID', 'Location', 'Tier']).agg({
            'Total_Value': 'sum',
            'Ticket_ID': 'count',
            'Total_Points_Earned': 'sum'
        }).reset_index()
        
        store_sales.columns = ['Store_ID', 'Location', 'Tier', 'Total_Sales', 'Transactions', 'Points_Earned']
        return store_sales
    
    def get_sales_trend(self):
        """Get daily sales trend"""
        sales_trend = self.sales_header_df.groupby('Date').agg({
            'Total_Value': 'sum',
            'Ticket_ID': 'count'
        }).reset_index()
        
        sales_trend.columns = ['Date', 'Total_Sales', 'Transaction_Count']
        return sales_trend.sort_values('Date')
    
    def get_top_customers(self, limit=20):
        """Get top customers by spend"""
        # Get sales aggregation
        top_customers = self.sales_header_df.groupby('Cust_ID').agg({
            'Total_Value': 'sum',
            'Ticket_ID': 'count',
            'Total_Points_Earned': 'sum'
        }).reset_index()
        
        # Get RFM segmentation data
        rfm_data = self.get_rfm_analysis()[['Cust_ID', 'RFM_Segment']]
        
        # Merge to get segments
        top_customers = top_customers.merge(rfm_data, on='Cust_ID', how='left')
        
        top_customers.columns = ['Cust_ID', 'Total_Spend', 'Transaction_Count', 'Total_Points', 'Segment']
        return top_customers.sort_values('Total_Spend', ascending=False).head(limit)
    
    def get_at_risk_customers(self):
        """Get at-risk customers based on calculated RFM segmentation"""
        rfm_data = self.get_rfm_analysis()
        at_risk = rfm_data[rfm_data['RFM_Segment'] == 'At Risk'].copy()
        
        return at_risk.sort_values('Monetary', ascending=False)
    
    def get_loyalty_points_distribution(self):
        """Get loyalty points earned distribution"""
        points_by_rule = self.sales_line_items_df.merge(
            self.loyalty_rules_df, on='Rule_ID', how='left'
        ).groupby('Rule_Name').agg({
            'Points_Per_Item': 'sum',
            'Ticket_ID': 'count'
        }).reset_index()
        
        points_by_rule.columns = ['Rule_Name', 'Total_Points', 'Transactions']
        return points_by_rule
    
    def get_product_performance(self, limit=15):
        """Get top performing products"""
        product_perf = self.sales_line_items_df.merge(self.products_df, on='SKU', how='left').groupby(['SKU', 'Category']).agg({
            'Line_Total': 'sum',
            'Qty': 'sum',
            'Ticket_ID': 'count'
        }).reset_index()
        
        product_perf.columns = ['SKU', 'Category', 'Total_Revenue', 'Quantity_Sold', 'Transactions']
        return product_perf.sort_values('Total_Revenue', ascending=False).head(limit)
