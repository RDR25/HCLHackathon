"""
Dynamic Rules Engine for Retail Loyalty Platform
Automatically applies discounts, promotions, points, and recommendations based on real-time business rules
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import os

class DynamicRulesEngine:
    """
    Dynamic Business Rules Engine:
    - Category multipliers for points
    - Low sales detection & automatic discounts
    - Inactive customer detection & bonus points
    - Special date promotions
    - Real-time recommendations
    - CSV persistence
    """
    
    def __init__(self, data_path="SampleData"):
        self.data_path = data_path
        self.products_df = None
        self.customers_df = None
        self.sales_header_df = None
        self.sales_line_items_df = None
        self.customer_balances_df = None
        self.recommendations_df = None
        self.current_date = datetime.now()
        
    def load_data(self):
        """Load all necessary data files"""
        try:
            self.products_df = pd.read_csv(os.path.join(self.data_path, 'products_master.csv'))
            self.customers_df = pd.read_csv(os.path.join(self.data_path, 'customers_master.csv'))
            self.sales_header_df = pd.read_csv(os.path.join(self.data_path, 'sales_header.csv'))
            self.sales_line_items_df = pd.read_csv(os.path.join(self.data_path, 'sales_line_items.csv'))
            self.customer_balances_df = pd.read_csv(os.path.join(self.data_path, 'customer_loyalty_balances.csv'))
            
            # Convert dates
            self.sales_header_df['Date'] = pd.to_datetime(self.sales_header_df['Date'])
            self.customers_df['Enrollment_Date'] = pd.to_datetime(self.customers_df['Enrollment_Date'])
            self.customer_balances_df['Last_Purchase_Date'] = pd.to_datetime(self.customer_balances_df['Last_Purchase_Date'])
            
            return True
        except Exception as e:
            print(f"Error loading data: {e}")
            return False
    
    # ============================================================================
    # RULE 1: CATEGORY MULTIPLIERS FOR POINTS EARNING
    # ============================================================================
    
    def calculate_category_multipliers(self):
        """
        Calculate multipliers for each product category
        Logic: Premium categories get higher multipliers to incentivize purchases
        """
        multipliers = {
            'Health': 2.0,           # High priority for customer wellness
            'Electronics': 1.5,      # Premium products
            'Home': 1.2,             # Balanced category
            'Fashion': 1.1,          # Standard category
            'Groceries': 1.0,        # Base multiplier
            'Sports': 1.3,           # Active lifestyle promotion
            'Books': 1.1,            # Education encouragement
        }
        return multipliers
    
    # ============================================================================
    # RULE 2: DETECT LOW SALES PRODUCTS & APPLY DISCOUNTS
    # ============================================================================
    
    def identify_low_selling_products(self, threshold_percentile=25):
        """
        Identify products with low sales (bottom 25%)
        These products get automatic discounts
        """
        # Calculate sales per product
        product_sales = self.sales_line_items_df.groupby('SKU').agg({
            'Line_Total': 'sum',
            'Qty': 'sum',
            'Ticket_ID': 'count'
        }).reset_index()
        
        product_sales.columns = ['SKU', 'Total_Sales', 'Units_Sold', 'Transactions']
        
        # Find threshold
        threshold = np.percentile(product_sales['Total_Sales'], threshold_percentile)
        low_selling = product_sales[product_sales['Total_Sales'] < threshold]['SKU'].tolist()
        
        return low_selling, product_sales
    
    def apply_dynamic_discounts(self, low_sales_discount=15, very_low_sales_discount=25):
        """
        Apply discounts to low-selling products
        - Bottom 25% sales: 15% discount
        - Bottom 10% sales: 25% discount
        """
        products_updated = self.products_df.copy()
        
        # Get low-selling products
        low_selling, product_sales = self.identify_low_selling_products(threshold_percentile=25)
        very_low_selling, _ = self.identify_low_selling_products(threshold_percentile=10)
        
        # Add discount columns if not present
        if 'Discount_Percent' not in products_updated.columns:
            products_updated['Discount_Percent'] = 0.0
        if 'Discounted_Price' not in products_updated.columns:
            products_updated['Discounted_Price'] = products_updated['Base_Price']
        
        # Apply discounts
        for idx, row in products_updated.iterrows():
            sku = row['SKU']
            base_price = row['Base_Price']
            
            if sku in very_low_selling:
                # Very low sales: 25% discount
                discount_percent = very_low_sales_discount / 100
                products_updated.at[idx, 'Discount_Percent'] = very_low_sales_discount / 100
                products_updated.at[idx, 'Discounted_Price'] = base_price * (1 - discount_percent)
            elif sku in low_selling:
                # Low sales: 15% discount
                discount_percent = low_sales_discount / 100
                products_updated.at[idx, 'Discount_Percent'] = low_sales_discount / 100
                products_updated.at[idx, 'Discounted_Price'] = base_price * (1 - discount_percent)
            else:
                # No discount
                products_updated.at[idx, 'Discount_Percent'] = 0.0
                products_updated.at[idx, 'Discounted_Price'] = base_price
        
        return products_updated
    
    # ============================================================================
    # RULE 3: DETECT INACTIVE CUSTOMERS & OFFER BONUS POINTS
    # ============================================================================
    
    def identify_inactive_customers(self, days_inactive=30):
        """
        Identify customers inactive for 30+ days
        Offer bonus points to re-engage them
        """
        # Calculate days since last purchase
        current_date = self.current_date
        self.customer_balances_df['Days_Inactive'] = (
            current_date - self.customer_balances_df['Last_Purchase_Date']
        ).dt.days
        
        # Find inactive (30+ days without purchase)
        inactive_customers = self.customer_balances_df[
            self.customer_balances_df['Days_Inactive'] >= days_inactive
        ].copy()
        
        # Add bonus points offer based on inactivity level
        inactive_customers['Bonus_Points_Offer'] = inactive_customers['Days_Inactive'].apply(
            lambda days: int((days // 10) * 100)  # 100 points per 10 days inactive
        )
        
        return inactive_customers
    
    # ============================================================================
    # RULE 4: SPECIAL DATE PROMOTIONS
    # ============================================================================
    
    def get_special_date_promotions(self):
        """
        Return active promotions based on special dates
        Examples: New Year, Republic Day, etc.
        """
        month = self.current_date.month
        day = self.current_date.day
        
        promotions = []
        
        # Republic Day (Jan 26)
        if month == 1 and day >= 20 and day <= 26:
            promotions.append({
                'name': 'Republic Day Special',
                'discount': 0.15,  # 15% discount
                'bonus_points_multiplier': 2.0,  # 2x bonus points
                'description': 'Celebrate India! 15% off + 2x points on all products'
            })
        
        # Independence Day (Aug 15)
        if month == 8 and day >= 10 and day <= 15:
            promotions.append({
                'name': 'Independence Day Sale',
                'discount': 0.20,  # 20% discount
                'bonus_points_multiplier': 2.5,  # 2.5x bonus points
                'description': 'Freedom Sale! 20% off + 2.5x points on all products'
            })
        
        # New Year (Jan 1)
        if month == 1 and day >= 1 and day <= 5:
            promotions.append({
                'name': 'New Year Bonanza',
                'discount': 0.25,  # 25% discount
                'bonus_points_multiplier': 3.0,  # 3x bonus points
                'description': 'New Year, New Rewards! 25% off + 3x points on all products'
            })
        
        # Diwali (Oct 29 in 2026)
        if month == 10 and day >= 25 and day <= 31:
            promotions.append({
                'name': 'Diwali Festival',
                'discount': 0.30,  # 30% discount
                'bonus_points_multiplier': 3.5,  # 3.5x bonus points
                'description': 'Diwali Lights! 30% off + 3.5x points on all products'
            })
        
        # Black Friday (Last Friday of Nov)
        if month == 11:
            from datetime import date
            black_friday = self._get_black_friday_date(self.current_date.year)
            if (black_friday - timedelta(days=1)).date() <= self.current_date.date() <= (black_friday + timedelta(days=1)).date():
                promotions.append({
                    'name': 'Black Friday Mega Sale',
                    'discount': 0.40,  # 40% discount
                    'bonus_points_multiplier': 4.0,  # 4x bonus points
                    'description': 'Black Friday! 40% off + 4x points on selected items'
                })
        
        return promotions
    
    def _get_black_friday_date(self, year):
        """Get Black Friday (4th Friday of November)"""
        from datetime import date
        november_1 = date(year, 11, 1)
        first_friday = november_1 + timedelta(days=(4 - november_1.weekday()))
        black_friday = first_friday + timedelta(weeks=3)
        return black_friday
    
    # ============================================================================
    # RULE 5: RFM-BASED RETENTION STRATEGIES
    # ============================================================================
    
    def generate_rfm_retention_rules(self):
        """
        Generate retention rules based on RFM segments
        """
        rules = {
            'Champion': {
                'description': 'Best customers - maintain VIP treatment',
                'action': 'VIP tier, exclusive deals, priority support',
                'bonus_points': 0,  # Already getting benefits
                'discount': 0.0
            },
            'Loyalist': {
                'description': 'Consistent buyers - encourage continued loyalty',
                'action': 'Tier upgrade opportunities, cross-sell offers',
                'bonus_points': 200,
                'discount': 0.05
            },
            'At Risk': {
                'description': 'Were active but inactive recently - urgent win-back',
                'action': 'Win-back campaign with special offer',
                'bonus_points': 500,
                'discount': 0.20
            },
            'New': {
                'description': 'Recent but low engagement - nurture',
                'action': 'Onboarding content, product recommendations',
                'bonus_points': 300,
                'discount': 0.10
            },
            'Lost': {
                'description': 'Churned customers - re-engagement needed',
                'action': 'Re-engagement campaign, significant incentive',
                'bonus_points': 1000,
                'discount': 0.30
            },
            'Potential': {
                'description': 'Mixed behavior - growth opportunity',
                'action': 'Personalized recommendations based on history',
                'bonus_points': 150,
                'discount': 0.08
            }
        }
        return rules
    
    # ============================================================================
    # RULE 6: GENERATE DYNAMIC CUSTOMER RECOMMENDATIONS
    # ============================================================================
    
    def generate_customer_recommendations(self):
        """
        Generate real-time recommendations for each customer
        Based on: RFM segment, inactivity, loyalty tier
        """
        recommendations = []
        
        # Get inactive customers
        inactive = self.identify_inactive_customers(days_inactive=30)
        
        # Get RFM info (merge with customer balances)
        rfm_data = self.customer_balances_df.copy()
        
        for idx, customer in rfm_data.iterrows():
            cust_id = customer['Cust_ID']
            segment = customer.get('RFM_Segment', 'Unknown')
            tier = customer['Loyalty_Tier']
            balance = customer['Current_Balance']
            
            recommendation = {
                'Cust_ID': cust_id,
                'Segment': segment,
                'Tier': tier,
                'Current_Balance': balance,
                'Recommendation': '',
                'Bonus_Points': 0,
                'Discount_Offer': 0.0,
                'Action': ''
            }
            
            # Check if inactive
            if cust_id in inactive['Cust_ID'].values:
                inactive_row = inactive[inactive['Cust_ID'] == cust_id].iloc[0]
                days_inactive = inactive_row['Days_Inactive']
                bonus = inactive_row['Bonus_Points_Offer']
                
                recommendation['Recommendation'] = f"Inactive for {days_inactive} days - Re-engagement needed"
                recommendation['Bonus_Points'] = int(bonus)
                recommendation['Discount_Offer'] = 0.15
                recommendation['Action'] = 'Send re-engagement email with offer'
            
            # RFM-based recommendations
            elif segment == 'Champion':
                recommendation['Recommendation'] = "VIP Customer - Offer exclusive early access"
                recommendation['Bonus_Points'] = 0
                recommendation['Action'] = 'VIP treatment'
            
            elif segment == 'At Risk':
                recommendation['Recommendation'] = "At Risk - Win-back campaign with special offer"
                recommendation['Bonus_Points'] = 500
                recommendation['Discount_Offer'] = 0.20
                recommendation['Action'] = 'Urgent: Send personalized offer'
            
            elif segment == 'Loyalist':
                recommendation['Recommendation'] = "Loyal Customer - Cross-sell opportunity"
                recommendation['Bonus_Points'] = 200
                recommendation['Discount_Offer'] = 0.05
                recommendation['Action'] = 'Recommend complementary products'
            
            elif segment == 'New':
                recommendation['Recommendation'] = "New Customer - Nurture and engage"
                recommendation['Bonus_Points'] = 300
                recommendation['Discount_Offer'] = 0.10
                recommendation['Action'] = 'Send welcome series + onboarding'
            
            elif segment == 'Risk':
                recommendation['Recommendation'] = "Risk Customer - Aggressive re-engagement"
                recommendation['Bonus_Points'] = 1000
                recommendation['Discount_Offer'] = 0.30
                recommendation['Action'] = 'Premium re-engagement campaign'
            
            else:  # Potential
                recommendation['Recommendation'] = "Potential Customer - Personalized targeting"
                recommendation['Bonus_Points'] = 150
                recommendation['Discount_Offer'] = 0.08
                recommendation['Action'] = 'Send personalized recommendations'
            
            recommendations.append(recommendation)
        
        self.recommendations_df = pd.DataFrame(recommendations)
        return self.recommendations_df
    
    # ============================================================================
    # RULE 7: DASHBOARD SUGGESTIONS - Real-time insights
    # ============================================================================
    
    def generate_dynamic_dashboard_suggestions(self):
        """
        Generate real-time dashboard suggestions for business users
        """
        suggestions = {
            'low_selling_products': [],
            'inactive_customers': [],
            'special_promotions': [],
            'recommendations': [],
            'revenue_boosters': [],
            'retention_alerts': []
        }
        
        # 1. Low-selling products that need promotion
        low_selling, product_sales = self.identify_low_selling_products(threshold_percentile=25)
        for sku in low_selling[:5]:  # Top 5 low sellers
            sales = product_sales[product_sales['SKU'] == sku]['Total_Sales'].values[0]
            suggestions['low_selling_products'].append({
                'SKU': sku,
                'Sales': f"${sales:.2f}",
                'Action': 'Apply 15-25% discount',
                'Impact': 'Boost inventory turnover'
            })
        
        # 2. Inactive customers with bonus point offers
        inactive = self.identify_inactive_customers(days_inactive=30)
        for idx, customer in inactive.head(5).iterrows():
            suggestions['inactive_customers'].append({
                'Cust_ID': customer['Cust_ID'],
                'Days_Inactive': int(customer['Days_Inactive']),
                'Bonus_Offer': f"{int(customer['Bonus_Points_Offer'])} points",
                'Action': 'Send re-engagement offer'
            })
        
        # 3. Special date promotions
        special_promos = self.get_special_date_promotions()
        for promo in special_promos:
            suggestions['special_promotions'].append({
                'Name': promo['name'],
                'Discount': f"{promo['discount']*100:.0f}%",
                'Bonus_Points': f"{promo['bonus_points_multiplier']:.1f}x",
                'Description': promo['description']
            })
        
        # 4. Top recommendations to implement
        if self.recommendations_df is not None:
            for idx, rec in self.recommendations_df.head(10).iterrows():
                suggestions['recommendations'].append({
                    'Customer': rec['Cust_ID'],
                    'Action': rec['Action'],
                    'Bonus': f"{int(rec['Bonus_Points'])} pts",
                    'Discount': f"{rec['Discount_Offer']*100:.0f}%"
                })
        
        # 5. Revenue boosters
        suggestions['revenue_boosters'] = [
            {'Strategy': 'Push low-selling products with discounts', 'Potential_Impact': 'High'},
            {'Strategy': 'Activate inactive customers with bonus points', 'Potential_Impact': 'Medium-High'},
            {'Strategy': 'Offer category multipliers for premium products', 'Potential_Impact': 'Medium'},
            {'Strategy': 'Leverage special date promotions', 'Potential_Impact': 'High'}
        ]
        
        # 6. Retention alerts
        low_balance = self.customer_balances_df[self.customer_balances_df['Current_Balance'] < 100]
        if len(low_balance) > 0:
            suggestions['retention_alerts'].append({
                'Alert': f"{len(low_balance)} customers with low point balance",
                'Action': 'Launch point multiplier campaign',
                'Priority': 'MEDIUM'
            })
        
        low_transactions = self.customer_balances_df[self.customer_balances_df['Transaction_Count'] < 3]
        if len(low_transactions) > 0:
            suggestions['retention_alerts'].append({
                'Alert': f"{len(low_transactions)} customers with low engagement",
                'Action': 'Send personalized offers',
                'Priority': 'HIGH'
            })
        
        return suggestions
    
    # ============================================================================
    # PERSISTENCE: Update CSV files with all dynamic rules
    # ============================================================================
    
    def update_products_csv(self):
        """Update products CSV with discounts and pricing"""
        products_with_discounts = self.apply_dynamic_discounts()
        csv_path = os.path.join(self.data_path, 'products_master_dynamic.csv')
        products_with_discounts.to_csv(csv_path, index=False)
        return csv_path
    
    def update_recommendations_csv(self):
        """Save recommendations to CSV for dashboard consumption"""
        if self.recommendations_df is not None:
            csv_path = os.path.join(self.data_path, 'customer_recommendations_dynamic.csv')
            self.recommendations_df.to_csv(csv_path, index=False)
            return csv_path
        return None
    
    def update_dashboard_suggestions_csv(self):
        """Save dashboard suggestions to CSV"""
        suggestions = self.generate_dynamic_dashboard_suggestions()
        
        # Convert suggestions to flat CSV format
        suggestion_records = []
        
        # Low selling products
        for item in suggestions['low_selling_products']:
            suggestion_records.append({
                'Category': 'Low_Selling_Products',
                'Item': item['SKU'],
                'Details': f"Sales: {item['Sales']}, Action: {item['Action']}",
                'Priority': 'HIGH'
            })
        
        # Inactive customers
        for item in suggestions['inactive_customers']:
            suggestion_records.append({
                'Category': 'Inactive_Customers',
                'Item': item['Cust_ID'],
                'Details': f"Inactive: {item['Days_Inactive']} days, Offer: {item['Bonus_Offer']}",
                'Priority': 'MEDIUM'
            })
        
        # Special promotions
        for item in suggestions['special_promotions']:
            suggestion_records.append({
                'Category': 'Special_Promotions',
                'Item': item['Name'],
                'Details': f"Discount: {item['Discount']}, Bonus: {item['Bonus_Points']}x",
                'Priority': 'MEDIUM'
            })
        
        # Retention alerts
        for item in suggestions['retention_alerts']:
            suggestion_records.append({
                'Category': 'Retention_Alert',
                'Item': item['Alert'],
                'Details': f"Action: {item['Action']}",
                'Priority': item['Priority']
            })
        
        suggestions_df = pd.DataFrame(suggestion_records)
        csv_path = os.path.join(self.data_path, 'dashboard_suggestions_dynamic.csv')
        suggestions_df.to_csv(csv_path, index=False)
        return csv_path
    
    def update_all_dynamic_rules(self):
        """Execute all dynamic rules and update CSVs"""
        # Generate recommendations first
        self.generate_customer_recommendations()
        
        results = {
            'products': self.update_products_csv(),
            'recommendations': self.update_recommendations_csv(),
            'dashboard_suggestions': self.update_dashboard_suggestions_csv()
        }
        return results
