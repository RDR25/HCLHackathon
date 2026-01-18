"""
Data Processing Module
Handles RFM analysis, data loading, and aggregations for the dashboard
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import os

class DataProcessor:
    """Process and analyze retail loyalty data"""
    
    def __init__(self, data_path="data/input"):
        """Initialize data processor with path to data files"""
        self.data_path = data_path
        
        # Initialize dataframes
        self.customers_df = None
        self.products_df = None
        self.sales_header_df = None
        self.sales_line_items_df = None
        self.stores_df = None
        self.loyalty_rules_df = None
        self.rfm_data = None
    
    def load_all_data(self):
        """Load all required data files"""
        try:
            # Load customers
            self.customers_df = pd.read_csv(f"{self.data_path}/customers_master.csv")
            if 'Enrollment_Date' in self.customers_df.columns:
                self.customers_df['Enrollment_Date'] = pd.to_datetime(self.customers_df['Enrollment_Date'])
            
            # Load products
            self.products_df = pd.read_csv(f"{self.data_path}/products_master.csv")
            
            # Load sales header
            self.sales_header_df = pd.read_csv(f"{self.data_path}/sales_header.csv")
            if 'Date' in self.sales_header_df.columns:
                self.sales_header_df['Date'] = pd.to_datetime(self.sales_header_df['Date'])
            
            # Load sales line items
            self.sales_line_items_df = pd.read_csv(f"{self.data_path}/sales_line_items.csv")
            
            # Load stores (may not exist)
            try:
                self.stores_df = pd.read_csv(f"{self.data_path}/stores_master.csv")
            except:
                self.stores_df = pd.DataFrame()
            
            # Load loyalty rules (may not exist)
            try:
                self.loyalty_rules_df = pd.read_csv(f"{self.data_path}/loyalty_rules_master.csv")
            except:
                self.loyalty_rules_df = pd.DataFrame()
            
            # Calculate RFM analysis
            self._calculate_rfm()
            
        except FileNotFoundError as e:
            print(f"Error loading data: {e}")
            raise
    
    def _calculate_rfm(self):
        """Calculate RFM (Recency, Frequency, Monetary) analysis"""
        reference_date = datetime.now()
        
        # Determine correct column names
        cust_col = 'Cust_ID' if 'Cust_ID' in self.customers_df.columns else 'Customer_ID'
        
        # Create RFM data
        rfm_data = []
        
        for customer_id in self.customers_df[cust_col].unique():
            customer_sales = self.sales_header_df[self.sales_header_df[cust_col] == customer_id]
            
            if len(customer_sales) == 0:
                continue
            
            # Recency: days since last purchase
            last_purchase = customer_sales['Date'].max()
            recency = (reference_date - last_purchase).days
            
            # Frequency: number of purchases
            frequency = len(customer_sales)
            
            # Monetary: total spend
            monetary = customer_sales['Total_Value'].sum()
            
            rfm_data.append({
                'Customer_ID': customer_id,
                'Recency': recency,
                'Frequency': frequency,
                'Monetary': monetary
            })
        
        self.rfm_data = pd.DataFrame(rfm_data)
        
        if len(self.rfm_data) > 0:
            # Calculate RFM scores (1-5, where 5 is best)
            try:
                self.rfm_data['R_Score'] = pd.qcut(self.rfm_data['Recency'], 5, labels=[5,4,3,2,1], duplicates='drop')
                self.rfm_data['F_Score'] = pd.qcut(self.rfm_data['Frequency'].rank(method='first'), 5, labels=[1,2,3,4,5], duplicates='drop')
                self.rfm_data['M_Score'] = pd.qcut(self.rfm_data['Monetary'], 5, labels=[1,2,3,4,5], duplicates='drop')
            except:
                # If qcut fails due to identical values, use simpler ranking
                self.rfm_data['R_Score'] = pd.cut(self.rfm_data['Recency'], 5, labels=[5,4,3,2,1], duplicates='drop')
                self.rfm_data['F_Score'] = pd.cut(self.rfm_data['Frequency'].rank(method='first'), 5, labels=[1,2,3,4,5], duplicates='drop')
                self.rfm_data['M_Score'] = pd.cut(self.rfm_data['Monetary'], 5, labels=[1,2,3,4,5], duplicates='drop')
            
            # Calculate RFM Segment
            self.rfm_data['RFM_Segment'] = self._assign_rfm_segment(self.rfm_data)
    
    def _assign_rfm_segment(self, rfm_df):
        """Assign customer segments based on RFM scores"""
        segments = []
        
        for idx, row in rfm_df.iterrows():
            try:
                r_score = int(row['R_Score']) if pd.notna(row['R_Score']) else 0
                f_score = int(row['F_Score']) if pd.notna(row['F_Score']) else 0
                m_score = int(row['M_Score']) if pd.notna(row['M_Score']) else 0
            except:
                r_score = f_score = m_score = 0
            
            # High-value loyal customers
            if (r_score >= 4 and f_score >= 4 and m_score >= 4):
                segment = "Champions"
            # Loyal customers
            elif (r_score >= 3 and f_score >= 4 and m_score >= 3):
                segment = "Loyal Customers"
            # At-risk high-value
            elif (r_score <= 2 and f_score >= 3 and m_score >= 4):
                segment = "At-Risk Customers"
            # Can't lose them
            elif (r_score <= 2 and f_score >= 4 and m_score >= 3):
                segment = "At-Risk Lost"
            # Potential loyalists
            elif (r_score >= 4 and f_score <= 2 and m_score >= 3):
                segment = "Potential Loyalists"
            # New customers
            elif (r_score >= 4 and f_score <= 2 and m_score <= 2):
                segment = "New Customers"
            # At Risk
            else:
                segment = "Risk Customers"
            
            segments.append(segment)
        
        return pd.Series(segments)
    
    def get_summary_metrics(self):
        """Get dashboard summary metrics"""
        total_sales = self.sales_header_df['Total_Value'].sum()
        total_transactions = len(self.sales_header_df)
        total_customers = len(self.customers_df)
        total_points = self.sales_header_df['Total_Points_Earned'].sum() if 'Total_Points_Earned' in self.sales_header_df.columns else 0
        avg_transaction = self.sales_header_df['Total_Value'].mean()
        
        return {
            'Total Sales': f"${total_sales:,.2f}",
            'Total Transactions': f"{total_transactions:,}",
            'Total Customers': f"{total_customers:,}",
            'Total Points Earned': f"{int(total_points):,}",
            'Avg Transaction Value': f"${avg_transaction:,.2f}"
        }
    
    def get_sales_trend(self):
        """Get daily sales trend"""
        daily_sales = self.sales_header_df.groupby(self.sales_header_df['Date'].dt.date).agg({
            'Total_Value': 'sum',
            'Cust_ID': 'count'
        }).reset_index()
        daily_sales.columns = ['Date', 'Sales', 'Transactions']
        return daily_sales
    
    def get_sales_by_store(self):
        """Get sales breakdown by store"""
        store_sales = self.sales_header_df.groupby('Store_ID').agg({
            'Total_Value': 'sum',
            'Cust_ID': 'count'
        }).reset_index()
        store_sales.columns = ['Store_ID', 'Sales', 'Transactions']
        
        # Merge with store names if available
        if self.stores_df is not None and not self.stores_df.empty:
            store_sales = store_sales.merge(self.stores_df, on='Store_ID', how='left')
        return store_sales
    
    def get_sales_by_category(self):
        """Get sales breakdown by category"""
        # Merge sales lines with products
        sales_with_category = self.sales_line_items_df.merge(
            self.products_df, 
            left_on='SKU', 
            right_on='SKU', 
            how='left'
        )
        
        if 'Category' in sales_with_category.columns:
            category_sales = sales_with_category.groupby('Category').agg({
                'Line_Total': 'sum',
                'Qty': 'sum'
            }).reset_index()
            category_sales.columns = ['Category', 'Sales', 'Quantity']
            return category_sales.sort_values('Sales', ascending=False)
        else:
            return pd.DataFrame()
    
    def get_top_customers(self, limit=10):
        """Get top customers by spend"""
        top_customers = self.sales_header_df.groupby('Cust_ID').agg({
            'Total_Value': 'sum'
        }).reset_index()
        top_customers.columns = ['Cust_ID', 'Total_Spend']
        
        return top_customers.nlargest(limit, 'Total_Spend')
    
    def get_rfm_analysis(self):
        """Get full RFM analysis"""
        if self.rfm_data is None or len(self.rfm_data) == 0:
            self._calculate_rfm()
        
        return self.rfm_data.copy()
    
    def get_segment_distribution(self):
        """Get distribution of customers by RFM segment"""
        if self.rfm_data is None or len(self.rfm_data) == 0:
            self._calculate_rfm()
        
        segment_dist = self.rfm_data['RFM_Segment'].value_counts().reset_index()
        segment_dist.columns = ['Segment', 'Count']
        return segment_dist
    
    def get_at_risk_customers(self):
        """Get at-risk customers (low recency, high frequency/monetary)"""
        if self.rfm_data is None or len(self.rfm_data) == 0:
            self._calculate_rfm()
        
        at_risk = self.rfm_data[self.rfm_data['RFM_Segment'].isin(['At-Risk Customers', 'At-Risk Lost'])]
        return at_risk.sort_values('Monetary', ascending=False)
    
    def get_product_performance(self, limit=20):
        """Get product performance metrics"""
        product_perf = self.sales_line_items_df.groupby('SKU').agg({
            'Qty': 'sum',
            'Line_Total': 'sum'
        }).reset_index()
        product_perf.columns = ['SKU', 'Units_Sold', 'Revenue']
        product_perf['Avg_Price'] = product_perf['Revenue'] / product_perf['Units_Sold']
        
        # Merge with product details
        product_perf = product_perf.merge(
            self.products_df, 
            on='SKU', 
            how='left'
        )
        
        return product_perf.nlargest(limit, 'Revenue')
    
    def get_loyalty_points_distribution(self):
        """Get loyalty points distribution"""
        if 'Total_Points_Earned' in self.sales_header_df.columns:
            points_dist = self.sales_header_df['Total_Points_Earned'].describe()
            return points_dist
        else:
            return pd.Series({
                'count': len(self.sales_header_df),
                'mean': 0,
                'std': 0,
                'min': 0,
                '25%': 0,
                '50%': 0,
                '75%': 0,
                'max': 0
            })
