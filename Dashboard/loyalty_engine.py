"""
Loyalty Points Engine - Dynamic Rules & Real-Time Accrual
Handles loyalty points earning, redemption, and customer balance updates
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import os
import json

class LoyaltyPointsEngine:
    """
    Comprehensive loyalty points engine with:
    - Dynamic rule-based earning
    - Real-time balance updates
    - Promotional multipliers
    - Redemption tracking
    - Customer balance history
    """
    
    def __init__(self, data_path="SampleData"):
        self.data_path = data_path
        self.loyalty_rules_df = None
        self.sales_header_df = None
        self.sales_line_items_df = None
        self.customers_df = None
        self.customer_balances_df = None
        self.points_history_df = None
        self.promo_effectiveness_df = None
        
    def load_loyalty_data(self):
        """Load all loyalty-related data"""
        try:
            self.loyalty_rules_df = pd.read_csv(os.path.join(self.data_path, 'loyalty_rules_master.csv'))
            self.sales_header_df = pd.read_csv(os.path.join(self.data_path, 'sales_header.csv'))
            self.sales_line_items_df = pd.read_csv(os.path.join(self.data_path, 'sales_line_items.csv'))
            self.customers_df = pd.read_csv(os.path.join(self.data_path, 'customers_master.csv'))
            
            # Convert dates
            self.sales_header_df['Date'] = pd.to_datetime(self.sales_header_df['Date'])
            self.customers_df['Enrollment_Date'] = pd.to_datetime(self.customers_df['Enrollment_Date'])
            
            return True
        except Exception as e:
            print(f"Error loading loyalty data: {e}")
            return False
    
    def calculate_dynamic_points(self, quantity, line_total, rule_id, category=None, is_promotion=False, promo_multiplier=1.0):
        """
        Calculate points with dynamic rules
        
        Rules:
        - Base: 1 point per $1 spent
        - Category multipliers (Health=2x, Premium=1.5x)
        - Promotional boosts
        - Quantity bonuses (10+ items = +0.5x)
        """
        
        # Get rule multiplier
        rule_row = self.loyalty_rules_df[self.loyalty_rules_df['Rule_ID'] == rule_id]
        rule_multiplier = rule_row['Multiplier'].values[0] if len(rule_row) > 0 else 1.0
        
        # Base points: $1 = 1 point
        base_points = line_total
        
        # Apply rule multiplier
        rule_points = base_points * rule_multiplier
        
        # Apply promotional multiplier
        promo_points = rule_points * promo_multiplier
        
        # Quantity bonus (10+ items = 1.5x)
        if quantity >= 10:
            quantity_multiplier = 1.5
        elif quantity >= 5:
            quantity_multiplier = 1.25
        else:
            quantity_multiplier = 1.0
        
        final_points = promo_points * quantity_multiplier
        
        return round(final_points, 2)
    
    def calculate_customer_balances(self):
        """
        Calculate real-time customer loyalty point balances
        Includes: earned points, redeemed points, current balance
        """
        
        # Merge to get all transaction details with rules
        transactions = self.sales_line_items_df.merge(
            self.sales_header_df[['Ticket_ID', 'Cust_ID', 'Date', 'Store_ID']], 
            on='Ticket_ID'
        )
        
        transactions = transactions.merge(
            self.loyalty_rules_df[['Rule_ID', 'Multiplier']], 
            on='Rule_ID'
        )
        
        # Calculate points for each transaction
        transactions['Calculated_Points'] = transactions.apply(
            lambda row: self.calculate_dynamic_points(
                quantity=row['Qty'],
                line_total=row['Line_Total'],
                rule_id=row['Rule_ID'],
                is_promotion=False,
                promo_multiplier=1.0
            ),
            axis=1
        )
        
        # Aggregate by customer
        customer_points = transactions.groupby('Cust_ID').agg({
            'Calculated_Points': 'sum',
            'Ticket_ID': 'count',
            'Date': 'max',
            'Line_Total': 'sum'
        }).reset_index()
        
        customer_points.columns = ['Cust_ID', 'Total_Points_Earned', 'Transaction_Count', 'Last_Purchase_Date', 'Total_Spent']
        
        # Add membership info
        customer_points = customer_points.merge(
            self.customers_df[['Cust_ID', 'Enrollment_Date']],
            on='Cust_ID',
            how='left'
        )
        
        # Calculate membership duration
        latest_date = self.sales_header_df['Date'].max()
        customer_points['Days_As_Member'] = (latest_date - customer_points['Enrollment_Date']).dt.days
        
        # Estimate redeemed points (assume 20% of earned are redeemed for purchases)
        customer_points['Estimated_Redeemed_Points'] = (customer_points['Total_Points_Earned'] * 0.2).round(2)
        customer_points['Current_Balance'] = (customer_points['Total_Points_Earned'] - customer_points['Estimated_Redeemed_Points']).round(2)
        
        # Determine loyalty tier based on balance
        customer_points['Loyalty_Tier'] = customer_points['Current_Balance'].apply(self._assign_loyalty_tier)
        
        self.customer_balances_df = customer_points
        return customer_points
    
    def _assign_loyalty_tier(self, points):
        """Assign loyalty tier based on points"""
        if points >= 5000:
            return 'Platinum'
        elif points >= 3000:
            return 'Gold'
        elif points >= 1000:
            return 'Silver'
        else:
            return 'Bronze'
    
    def calculate_points_history(self):
        """Track points accrual over time"""
        
        # Merge all necessary data
        transactions = self.sales_line_items_df.merge(
            self.sales_header_df[['Ticket_ID', 'Cust_ID', 'Date']], 
            on='Ticket_ID'
        )
        
        transactions = transactions.merge(
            self.loyalty_rules_df[['Rule_ID', 'Multiplier', 'Rule_Name']], 
            on='Rule_ID'
        )
        
        # Calculate points
        transactions['Points_Earned'] = transactions.apply(
            lambda row: self.calculate_dynamic_points(
                quantity=row['Qty'],
                line_total=row['Line_Total'],
                rule_id=row['Rule_ID']
            ),
            axis=1
        )
        
        # Sort by date
        transactions = transactions.sort_values(['Cust_ID', 'Date'])
        
        # Calculate cumulative points per customer
        transactions['Cumulative_Points'] = transactions.groupby('Cust_ID')['Points_Earned'].cumsum()
        
        # Select relevant columns
        history = transactions[[
            'Cust_ID', 'Ticket_ID', 'Date', 'Rule_Name', 'Qty', 
            'Line_Total', 'Points_Earned', 'Cumulative_Points'
        ]].reset_index(drop=True)
        
        self.points_history_df = history
        return history
    
    def calculate_promo_effectiveness(self):
        """Measure promotional effectiveness across products and stores"""
        
        # Merge to get promotion data
        transactions = self.sales_line_items_df.merge(
            self.sales_header_df[['Ticket_ID', 'Cust_ID', 'Store_ID', 'Date', 'Total_Value']], 
            on='Ticket_ID'
        )
        
        transactions = transactions.merge(
            self.loyalty_rules_df[['Rule_ID', 'Rule_Name', 'Multiplier']], 
            on='Rule_ID'
        )
        
        # Calculate points earned
        transactions['Points_Earned'] = transactions.apply(
            lambda row: self.calculate_dynamic_points(
                quantity=row['Qty'],
                line_total=row['Line_Total'],
                rule_id=row['Rule_ID']
            ),
            axis=1
        )
        
        # Group by promotion and store
        promo_by_store = transactions.groupby(['Rule_Name', 'Store_ID']).agg({
            'Ticket_ID': 'count',
            'Line_Total': 'sum',
            'Points_Earned': 'sum',
            'Qty': 'sum'
        }).reset_index()
        
        promo_by_store.columns = ['Promotion', 'Store_ID', 'Transaction_Count', 'Sales_Uplift', 'Points_Activity', 'Units_Sold']
        
        # Calculate metrics
        promo_by_store['Avg_Transaction_Value'] = (promo_by_store['Sales_Uplift'] / promo_by_store['Transaction_Count']).round(2)
        promo_by_store['Points_per_Sale'] = (promo_by_store['Points_Activity'] / promo_by_store['Sales_Uplift']).round(4)
        promo_by_store['Effectiveness_Score'] = (
            (promo_by_store['Avg_Transaction_Value'] * 0.5) +
            (promo_by_store['Points_per_Sale'] * 100 * 0.3) +
            ((promo_by_store['Units_Sold'] / promo_by_store['Transaction_Count']) * 0.2)
        ).round(2)
        
        self.promo_effectiveness_df = promo_by_store
        return promo_by_store
    
    def calculate_sales_uplift_by_product(self):
        """Measure sales uplift by product category"""
        
        transactions = self.sales_line_items_df.merge(
            self.sales_header_df[['Ticket_ID', 'Date']], 
            on='Ticket_ID'
        )
        
        transactions = transactions.merge(
            self.loyalty_rules_df[['Rule_ID', 'Rule_Name']], 
            on='Rule_ID'
        )
        
        # Group by rule (promotion) and SKU
        uplift = transactions.groupby(['Rule_Name', 'SKU']).agg({
            'Line_Total': 'sum',
            'Qty': 'sum',
            'Ticket_ID': 'count'
        }).reset_index()
        
        uplift.columns = ['Promotion', 'SKU', 'Sales_Value', 'Units_Sold', 'Transaction_Count']
        uplift['Avg_Price'] = (uplift['Sales_Value'] / uplift['Units_Sold']).round(2)
        
        return uplift.sort_values('Sales_Value', ascending=False).head(15)
    
    def update_customer_balances_csv(self):
        """Update customer balances in CSV"""
        if self.customer_balances_df is not None:
            csv_path = os.path.join(self.data_path, 'customer_loyalty_balances.csv')
            self.customer_balances_df.to_csv(csv_path, index=False)
            return csv_path
        return None
    
    def update_points_history_csv(self):
        """Update points history in CSV"""
        if self.points_history_df is not None:
            csv_path = os.path.join(self.data_path, 'points_transaction_history.csv')
            self.points_history_df.to_csv(csv_path, index=False)
            return csv_path
        return None
    
    def update_promo_effectiveness_csv(self):
        """Update promotional effectiveness in CSV"""
        if self.promo_effectiveness_df is not None:
            csv_path = os.path.join(self.data_path, 'promo_effectiveness_metrics.csv')
            self.promo_effectiveness_df.to_csv(csv_path, index=False)
            return csv_path
        return None
    
    def generate_loyalty_report(self):
        """Generate comprehensive loyalty report"""
        report = {
            'timestamp': datetime.now().isoformat(),
            'summary': {
                'total_customers': len(self.customer_balances_df),
                'total_points_earned': self.customer_balances_df['Total_Points_Earned'].sum(),
                'total_points_redeemed': self.customer_balances_df['Estimated_Redeemed_Points'].sum(),
                'total_active_balance': self.customer_balances_df['Current_Balance'].sum(),
                'avg_customer_balance': self.customer_balances_df['Current_Balance'].mean(),
            },
            'tier_distribution': self.customer_balances_df['Loyalty_Tier'].value_counts().to_dict(),
            'top_earners': self.customer_balances_df.nlargest(10, 'Total_Points_Earned')[
                ['Cust_ID', 'Total_Points_Earned', 'Current_Balance', 'Loyalty_Tier']
            ].to_dict('records'),
        }
        return report

