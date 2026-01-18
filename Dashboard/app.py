"""
Retail Loyalty Analytics Platform - Streamlit Dashboard
Team Member 3: Visualization & Integration
Includes: RFM Analysis, Loyalty Points Engine, Promotional Effectiveness
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from data_processor import DataProcessor
from loyalty_engine import LoyaltyPointsEngine
from datetime import datetime, timedelta

# Page configuration
st.set_page_config(
    page_title="Retail Loyalty Analytics",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
    <style>
    .metric-card {
        background-color: #f0f2f6;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    .header-title {
        color: #1f77b4;
        font-size: 2.5em;
        font-weight: bold;
        margin-bottom: 10px;
    }
    </style>
""", unsafe_allow_html=True)

# Initialize session state and load data
@st.cache_resource
def load_data():
    processor = DataProcessor()
    processor.load_all_data()
    return processor

processor = load_data()

# Sidebar navigation
st.sidebar.markdown("# 📊 Navigation")
page = st.sidebar.radio(
    "Select a page:",
    [
        "Dashboard Overview",
        "RFM Analysis",
        "Customer Segmentation",
        "Loyalty Points Engine",
        "Dynamic Rules & Recommendations",
        "Promotional Effectiveness",
        "Sales Analytics",
        "Product Performance",
        "Data Summary"
    ]
)

# Title
st.markdown("<div class='header-title'>🏪 Retail Loyalty Analytics Platform</div>", unsafe_allow_html=True)
st.markdown("---")

# PAGE 1: DASHBOARD OVERVIEW
if page == "Dashboard Overview":
    st.subheader("📈 Executive Dashboard")
    
    # Get summary metrics
    metrics = processor.get_summary_metrics()
    
    # Display metrics in columns
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        st.metric("Total Sales", metrics['Total Sales'])
    with col2:
        st.metric("Transactions", metrics['Total Transactions'])
    with col3:
        st.metric("Active Customers", metrics['Total Customers'])
    with col4:
        st.metric("Points Earned", metrics['Total Points Earned'])
    with col5:
        st.metric("Avg Transaction", metrics['Avg Transaction Value'])
    
    st.markdown("---")
    
    # Sales trend
    st.subheader("📊 Sales Trend Over Time")
    sales_trend = processor.get_sales_trend()
    
    fig_trend = go.Figure()
    fig_trend.add_trace(go.Scatter(
        x=sales_trend['Date'],
        y=sales_trend['Total_Sales'],
        mode='lines+markers',
        name='Daily Sales',
        line=dict(color='#1f77b4', width=2),
        fill='tozeroy'
    ))
    
    fig_trend.update_layout(
        title='Daily Sales Value',
        xaxis_title='Date',
        yaxis_title='Sales ($)',
        hovermode='x unified',
        height=400
    )
    st.plotly_chart(fig_trend, use_container_width=True)
    
    # Sales by store and category
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("🏬 Sales by Store")
        store_sales = processor.get_sales_by_store()
        fig_store = px.bar(
            store_sales,
            x='Location',
            y='Total_Sales',
            color='Tier',
            hover_data=['Store_ID', 'Transactions'],
            title='Sales Revenue by Store Location'
        )
        st.plotly_chart(fig_store, use_container_width=True)
    
    with col2:
        st.subheader("🛍️ Sales by Category")
        category_sales = processor.get_sales_by_category()
        fig_category = px.pie(
            category_sales,
            values='Total_Sales',
            names='Category',
            title='Sales Distribution by Product Category'
        )
        st.plotly_chart(fig_category, use_container_width=True)
    
    # Top customers
    st.subheader("⭐ Top 10 Customers")
    top_customers = processor.get_top_customers(limit=10)
    
    fig_top = px.bar(
        top_customers,
        x='Cust_ID',
        y='Total_Spend',
        color='Segment',
        hover_data=['Transaction_Count', 'Total_Points'],
        title='Top 10 Customers by Total Spend'
    )
    st.plotly_chart(fig_top, use_container_width=True)

# PAGE 2: RFM ANALYSIS
elif page == "RFM Analysis":
    st.subheader("🎯 RFM (Recency, Frequency, Monetary) Analysis")
    
    rfm_data = processor.get_rfm_analysis()
    
    # RFM Metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        avg_recency = rfm_data['Recency'].mean()
        st.metric("Avg Days Since Purchase", f"{int(avg_recency)} days")
    
    with col2:
        avg_frequency = rfm_data['Frequency'].mean()
        st.metric("Avg Transactions", f"{avg_frequency:.1f}")
    
    with col3:
        avg_monetary = rfm_data['Monetary'].mean()
        st.metric("Avg Customer Spend", f"${avg_monetary:,.2f}")
    
    with col4:
        total_customers = len(rfm_data)
        st.metric("Total Customers", total_customers)
    
    st.markdown("---")
    
    # RFM Scatter plot
    st.subheader("📊 RFM Positioning")
    fig_rfm = px.scatter(
        rfm_data,
        x='Recency',
        y='Monetary',
        size='Frequency',
        color='RFM_Segment',
        hover_data=['Cust_ID', 'Recency', 'Frequency', 'Monetary'],
        title='Customer RFM Positioning (Size = Frequency)',
        labels={
            'Recency': 'Days Since Last Purchase',
            'Monetary': 'Total Customer Spend ($)',
            'Frequency': 'Number of Transactions'
        }
    )
    st.plotly_chart(fig_rfm, use_container_width=True)
    
    # Segment distribution
    st.subheader("📈 Customer Segment Distribution")
    segment_dist = processor.get_segment_distribution()
    
    col1, col2 = st.columns(2)
    
    with col1:
        fig_segment_pie = px.pie(
            segment_dist,
            values='Count',
            names='Segment',
            title='Customer Segment Distribution'
        )
        st.plotly_chart(fig_segment_pie, use_container_width=True)
    
    with col2:
        fig_segment_bar = px.bar(
            segment_dist,
            x='Segment',
            y='Count',
            color='Segment',
            title='Customer Count by Segment'
        )
        st.plotly_chart(fig_segment_bar, use_container_width=True)
    
    # RFM data table
    st.subheader("📋 RFM Data")
    st.dataframe(rfm_data.sort_values('Monetary', ascending=False).head(20), use_container_width=True)

# PAGE 3: CUSTOMER SEGMENTATION
elif page == "Customer Segmentation":
    st.subheader("👥 Customer Segmentation Analysis")
    
    # At-Risk Customers
    st.subheader("⚠️ At-Risk Customers (Retention Focus)")
    at_risk_customers = processor.get_at_risk_customers()
    
    col1, col2 = st.columns([1, 3])
    with col1:
        st.metric("At-Risk Count", len(at_risk_customers))
        potential_loss = at_risk_customers['Monetary'].sum()
        st.metric("Potential Revenue Loss", f"${potential_loss:,.2f}")
    
    with col2:
        if len(at_risk_customers) > 0:
            fig_at_risk = px.bar(
                at_risk_customers.head(15),
                x='Cust_ID',
                y='Monetary',
                title='Top 15 At-Risk Customers by Historical Spend'
            )
            st.plotly_chart(fig_at_risk, use_container_width=True)
    
    st.markdown("---")
    
    # Customer segment details
    rfm_data = processor.get_rfm_analysis()
    
    # Segment statistics
    st.subheader("📊 Segment Statistics")
    segment_stats = rfm_data.groupby('RFM_Segment').agg({
        'Recency': 'mean',
        'Frequency': 'mean',
        'Monetary': 'mean',
        'Cust_ID': 'count'
    }).reset_index()
    
    segment_stats.columns = ['Segment', 'Avg Recency', 'Avg Frequency', 'Avg Spend', 'Customer Count']
    segment_stats = segment_stats.round(2)
    
    fig_stats = go.Figure(data=[
        go.Bar(name='Avg Recency (days)', x=segment_stats['Segment'], y=segment_stats['Avg Recency']),
        go.Bar(name='Avg Frequency', x=segment_stats['Segment'], y=segment_stats['Avg Frequency']),
        go.Bar(name='Avg Spend ($)', x=segment_stats['Segment'], y=segment_stats['Avg Spend'])
    ])
    fig_stats.update_layout(barmode='group', title='Segment Characteristics Comparison')
    st.plotly_chart(fig_stats, use_container_width=True)
    
    st.markdown("---")
    
    st.subheader("📋 Segment Statistics Table")
    st.dataframe(segment_stats, use_container_width=True)
    
    # At-Risk customers table
    st.subheader("📋 At-Risk Customers Details")
    st.dataframe(at_risk_customers.head(20), use_container_width=True)

# PAGE 4: SALES ANALYTICS
elif page == "Sales Analytics":
    st.subheader("💰 Sales Analytics")
    
    # Sales metrics
    col1, col2, col3 = st.columns(3)
    
    store_sales = processor.get_sales_by_store()
    category_sales = processor.get_sales_by_category()
    
    with col1:
        total_store_sales = store_sales['Total_Sales'].sum()
        st.metric("Total Store Revenue", f"${total_store_sales:,.2f}")
    
    with col2:
        top_category = category_sales.iloc[0]
        st.metric("Top Category", f"{top_category['Category']}: ${top_category['Total_Sales']:,.2f}")
    
    with col3:
        top_store = store_sales.loc[store_sales['Total_Sales'].idxmax()]
        st.metric("Top Store", f"{top_store['Location']}: ${top_store['Total_Sales']:,.2f}")
    
    st.markdown("---")
    
    # Sales by store and category
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Sales by Store & Tier")
        fig_store_tier = px.bar(
            store_sales.sort_values('Total_Sales', ascending=False),
            x='Location',
            y='Total_Sales',
            color='Tier',
            hover_data=['Transactions', 'Store_ID'],
            title='Store Performance by Location and Tier'
        )
        st.plotly_chart(fig_store_tier, use_container_width=True)
    
    with col2:
        st.subheader("Sales by Category")
        fig_category = px.bar(
            category_sales.sort_values('Total_Sales', ascending=False),
            x='Category',
            y='Total_Sales',
            color='Total_Sales',
            hover_data=['Transactions', 'Quantity'],
            title='Category Sales Performance'
        )
        st.plotly_chart(fig_category, use_container_width=True)
    
    st.markdown("---")
    
    # Transaction analysis
    st.subheader("📊 Sales Trend & Transaction Analysis")
    sales_trend = processor.get_sales_trend()
    
    fig_combined = go.Figure()
    fig_combined.add_trace(go.Scatter(
        x=sales_trend['Date'],
        y=sales_trend['Total_Sales'],
        name='Total Sales ($)',
        yaxis='y1',
        line=dict(color='#1f77b4')
    ))
    fig_combined.add_trace(go.Bar(
        x=sales_trend['Date'],
        y=sales_trend['Transaction_Count'],
        name='Transaction Count',
        yaxis='y2',
        marker=dict(color='#ff7f0e')
    ))
    
    fig_combined.update_layout(
        title='Daily Sales Value & Transaction Count',
        xaxis_title='Date',
        yaxis_title='Sales ($)',
        yaxis2=dict(
            title='Transaction Count',
            overlaying='y',
            side='right'
        ),
        hovermode='x unified',
        height=400
    )
    st.plotly_chart(fig_combined, use_container_width=True)
    
    st.markdown("---")
    
    st.subheader("📋 Store Performance Table")
    st.dataframe(store_sales.sort_values('Total_Sales', ascending=False), use_container_width=True)

# PAGE 5: PRODUCT PERFORMANCE
elif page == "Product Performance":
    st.subheader("🛍️ Product Performance Analysis")
    
    product_perf = processor.get_product_performance(limit=20)
    loyalty_points = processor.get_loyalty_points_distribution()
    
    # Top metrics
    col1, col2, col3 = st.columns(3)
    
    with col1:
        top_product = product_perf.iloc[0]
        st.metric("Top Product", top_product['SKU'])
    
    with col2:
        st.metric("Top Revenue", f"${top_product['Total_Revenue']:,.2f}")
    
    with col3:
        st.metric("Total Products", len(processor.products_df))
    
    st.markdown("---")
    
    # Product performance charts
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Top 15 Products by Revenue")
        fig_products = px.bar(
            product_perf.head(15),
            x='SKU',
            y='Total_Revenue',
            color='Category',
            hover_data=['Quantity_Sold', 'Transactions'],
            title='Top 15 Products by Revenue'
        )
        st.plotly_chart(fig_products, use_container_width=True)
    
    with col2:
        st.subheader("Product Category Distribution")
        category_dist = product_perf.groupby('Category').agg({
            'Total_Revenue': 'sum',
            'SKU': 'count'
        }).reset_index()
        category_dist.columns = ['Category', 'Total_Revenue', 'Product_Count']
        
        fig_cat_dist = px.pie(
            category_dist,
            values='Total_Revenue',
            names='Category',
            title='Revenue Distribution by Category'
        )
        st.plotly_chart(fig_cat_dist, use_container_width=True)
    
    st.markdown("---")
    
    # Loyalty points by rule
    st.subheader("🎁 Loyalty Points Distribution by Rule")
    fig_points = px.bar(
        loyalty_points,
        x='Rule_Name',
        y='Total_Points',
        color='Rule_Name',
        hover_data=['Transactions'],
        title='Total Points Earned by Loyalty Rule'
    )
    st.plotly_chart(fig_points, use_container_width=True)
    
    st.markdown("---")
    
    st.subheader("📋 Top 20 Products Details")
    st.dataframe(product_perf.head(20), use_container_width=True)

# PAGE 6: DATA SUMMARY
elif page == "Data Summary":
    st.subheader("📊 Data Summary & Statistics")
    
    tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
        "Customers", "Products", "Stores", "Sales", "Loyalty Rules", "Data Quality"
    ])
    
    with tab1:
        st.subheader("Customers Master")
        st.write(f"Total Records: {len(processor.customers_df)}")
        st.dataframe(processor.customers_df.head(20), use_container_width=True)
        
        # Customer statistics
        st.subheader("Customer Statistics")
        st.write(f"Enrollment Date Range: {processor.customers_df['Enrollment_Date'].min().date()} to {processor.customers_df['Enrollment_Date'].max().date()}")
        rfm_segments = processor.get_rfm_analysis()['RFM_Segment'].unique().tolist()
        st.write(f"RFM Segments: {rfm_segments}")
    
    with tab2:
        st.subheader("Products Master")
        st.write(f"Total Products: {len(processor.products_df)}")
        st.dataframe(processor.products_df.head(20), use_container_width=True)
        
        # Product statistics
        st.subheader("Product Statistics")
        st.write(f"Categories: {processor.products_df['Category'].unique().tolist()}")
        st.write(f"Price Range: ${processor.products_df['Base_Price'].min():.2f} - ${processor.products_df['Base_Price'].max():.2f}")
    
    with tab3:
        st.subheader("Stores Master")
        st.write(f"Total Stores: {len(processor.stores_df)}")
        st.dataframe(processor.stores_df, use_container_width=True)
    
    with tab4:
        st.subheader("Sales Header")
        st.write(f"Total Transactions: {len(processor.sales_header_df)}")
        st.dataframe(processor.sales_header_df.head(20), use_container_width=True)
        
        # Sales statistics
        st.subheader("Sales Statistics")
        col1, col2, col3 = st.columns(3)
        with col1:
            st.write(f"Date Range: {processor.sales_header_df['Date'].min().date()} to {processor.sales_header_df['Date'].max().date()}")
        with col2:
            st.write(f"Total Value: ${processor.sales_header_df['Total_Value'].sum():,.2f}")
        with col3:
            st.write(f"Avg Transaction: ${processor.sales_header_df['Total_Value'].mean():,.2f}")
    
    with tab5:
        st.subheader("Loyalty Rules Master")
        st.dataframe(processor.loyalty_rules_df, use_container_width=True)
    
    with tab6:
        st.subheader("📋 Data Quality Report")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.write("**Customers Master**")
            st.write(f"- Total Records: {len(processor.customers_df)}")
            st.write(f"- Missing Values: {processor.customers_df.isnull().sum().sum()}")
            st.write(f"- Duplicates: {processor.customers_df.duplicated().sum()}")
        
        with col2:
            st.write("**Sales Header**")
            st.write(f"- Total Records: {len(processor.sales_header_df)}")
            st.write(f"- Missing Values: {processor.sales_header_df.isnull().sum().sum()}")
            st.write(f"- Duplicates: {processor.sales_header_df.duplicated().sum()}")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.write("**Products Master**")
            st.write(f"- Total Records: {len(processor.products_df)}")
            st.write(f"- Missing Values: {processor.products_df.isnull().sum().sum()}")
            st.write(f"- Duplicates: {processor.products_df.duplicated().sum()}")
        
        with col2:
            st.write("**Sales Line Items**")
            st.write(f"- Total Records: {len(processor.sales_line_items_df)}")
            st.write(f"- Missing Values: {processor.sales_line_items_df.isnull().sum().sum()}")
            st.write(f"- Duplicates: {processor.sales_line_items_df.duplicated().sum()}")

# PAGE 7: LOYALTY POINTS ENGINE
elif page == "Loyalty Points Engine":
    st.subheader("💰 Loyalty Points Engine")
    st.markdown("Real-time customer balance tracking, dynamic rules, and tier management")
    
    @st.cache_resource
    def load_loyalty_engine():
        engine = LoyaltyPointsEngine()
        engine.load_loyalty_data()
        balances = engine.calculate_customer_balances()
        return engine, balances
    
    engine, balances = load_loyalty_engine()
    
    st.markdown("---")
    st.subheader("📊 Loyalty Metrics Summary")
    
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        st.metric("Total Customers", len(balances))
    with col2:
        st.metric("Total Points Earned", f"{balances['Total_Points_Earned'].sum():,.0f}")
    with col3:
        st.metric("Active Balance", f"{balances['Current_Balance'].sum():,.0f}")
    with col4:
        st.metric("Avg Balance/Customer", f"{balances['Current_Balance'].mean():,.0f}")
    with col5:
        st.metric("Redemption Rate", f"{(balances['Estimated_Redeemed_Points'].sum() / balances['Total_Points_Earned'].sum() * 100):.1f}%")
    
    st.markdown("---")
    st.subheader("🏆 Loyalty Tier Distribution")
    
    col1, col2 = st.columns([1, 3])
    
    with col1:
        tier_dist = balances['Loyalty_Tier'].value_counts().sort_values(ascending=False)
        st.write("**Tier Counts:**")
        for tier, count in tier_dist.items():
            st.write(f"• {tier}: {count} customers")
    
    with col2:
        fig_tier = px.pie(
            balances['Loyalty_Tier'].value_counts().reset_index(),
            values='count',
            names='Loyalty_Tier',
            title='Customer Distribution by Tier',
            color_discrete_map={
                'Platinum': '#FFD700',
                'Gold': '#FFD700',
                'Silver': '#C0C0C0',
                'Bronze': '#CD7F32'
            }
        )
        st.plotly_chart(fig_tier, use_container_width=True)
    
    st.markdown("---")
    st.subheader("👑 Top 15 Loyalty Members")
    
    top_members = balances.nlargest(15, 'Current_Balance')[
        ['Cust_ID', 'Total_Points_Earned', 'Estimated_Redeemed_Points', 'Current_Balance', 'Loyalty_Tier', 'Days_As_Member']
    ].reset_index(drop=True)
    
    fig_top = go.Figure()
    fig_top.add_trace(go.Bar(
        y=top_members['Cust_ID'],
        x=top_members['Current_Balance'],
        orientation='h',
        marker=dict(color=top_members['Current_Balance'], colorscale='Viridis'),
        text=top_members['Loyalty_Tier'],
        textposition='auto',
    ))
    fig_top.update_layout(title='Top 15 Customers by Loyalty Balance', xaxis_title='Current Balance', yaxis_title='Customer ID')
    st.plotly_chart(fig_top, use_container_width=True)
    
    st.markdown("---")
    st.subheader("📋 Loyalty Member Details")
    st.dataframe(top_members, use_container_width=True)

# PAGE 5: DYNAMIC RULES & RECOMMENDATIONS
elif page == "Dynamic Rules & Recommendations":
    st.subheader("🎯 Dynamic Rules & Smart Recommendations")
    st.markdown("Real-time business rules, product discounts, and personalized customer recommendations")
    
    from dynamic_rules_engine import DynamicRulesEngine
    
    @st.cache_resource
    def load_dynamic_rules_engine():
        engine = DynamicRulesEngine()
        engine.load_data()
        engine.update_all_dynamic_rules()
        return engine
    
    rules_engine = load_dynamic_rules_engine()
    
    # Load generated CSV data
    products_dynamic = pd.read_csv('SampleData/products_master_dynamic.csv')
    recommendations = pd.read_csv('SampleData/customer_recommendations_dynamic.csv')
    dashboard_suggestions = pd.read_csv('SampleData/dashboard_suggestions_dynamic.csv')
    
    # Metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        discounted_products = len(products_dynamic[products_dynamic['Discount_Percent'] > 0])
        st.metric("🔴 Products with Discounts", discounted_products)
    
    with col2:
        avg_discount = (products_dynamic[products_dynamic['Discount_Percent'] > 0]['Discount_Percent'].mean() * 100) if discounted_products > 0 else 0
        st.metric("💰 Avg Discount Applied", f"{avg_discount:.1f}%")
    
    with col3:
        st.metric("👥 Customers Recommended", len(recommendations))
    
    with col4:
        alerts = len(dashboard_suggestions[dashboard_suggestions['Priority'] == 'HIGH'])
        st.metric("⚠️ High Priority Alerts", alerts)
    
    st.markdown("---")
    
    # Tab layout
    tab1, tab2, tab3, tab4 = st.tabs([
        "💿 Low-Selling Products",
        "🎁 Customer Recommendations",
        "📊 Smart Suggestions",
        "🎯 Category Multipliers"
    ])
    
    # TAB 1: LOW-SELLING PRODUCTS WITH DISCOUNTS
    with tab1:
        st.subheader("🛍️ Low-Selling Products - Automatic Discounts Applied")
        
        # Filter for discounted products
        discounted_products_df = products_dynamic[products_dynamic['Discount_Percent'] > 0].sort_values('Discount_Percent', ascending=False)
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("📊 Discount Distribution")
            fig_discount = px.histogram(
                discounted_products_df,
                x='Discount_Percent',
                nbins=5,
                color='Category',
                hover_data=['SKU', 'Base_Price'],
                title='Distribution of Applied Discounts',
                labels={'Discount_Percent': 'Discount %'}
            )
            fig_discount.update_xaxes(tickformat='.0%')
            st.plotly_chart(fig_discount, use_container_width=True)
        
        with col2:
            st.subheader("💵 Savings Analysis")
            discounted_products_df['Savings'] = discounted_products_df['Base_Price'] - discounted_products_df['Discounted_Price']
            fig_savings = px.bar(
                discounted_products_df.nlargest(10, 'Savings'),
                x='SKU',
                y='Savings',
                color='Category',
                hover_data=['Base_Price', 'Discounted_Price', 'Discount_Percent'],
                title='Top 10 Products by Maximum Customer Savings'
            )
            st.plotly_chart(fig_savings, use_container_width=True)
        
        st.markdown("---")
        
        st.subheader("📋 Low-Selling Products Details")
        display_cols = ['SKU', 'Category', 'Base_Price', 'Discount_Percent', 'Discounted_Price', 'Savings']
        st.dataframe(
            discounted_products_df[display_cols].sort_values('Discount_Percent', ascending=False),
            use_container_width=True
        )
        
        st.info("📌 **Rule Logic**: Bottom 25% of products by sales receive 15% discount | Bottom 10% receive 25% discount")
    
    # TAB 2: CUSTOMER RECOMMENDATIONS
    with tab2:
        st.subheader("👥 Personalized Customer Recommendations")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("📊 Bonus Points Distribution")
            fig_bonus = px.box(
                recommendations,
                y='Bonus_Points',
                color='Tier',
                hover_data=['Cust_ID'],
                title='Bonus Points Offered by Loyalty Tier'
            )
            st.plotly_chart(fig_bonus, use_container_width=True)
        
        with col2:
            st.subheader("💳 Discount Offers Distribution")
            fig_discount_off = px.box(
                recommendations,
                y='Discount_Offer',
                color='Tier',
                hover_data=['Cust_ID'],
                title='Discount Offers by Loyalty Tier'
            )
            fig_discount_off.update_yaxes(tickformat='.0%')
            st.plotly_chart(fig_discount_off, use_container_width=True)
        
        st.markdown("---")
        
        # Filter options
        col1, col2, col3 = st.columns(3)
        
        with col1:
            selected_tier = st.multiselect(
                "Filter by Loyalty Tier:",
                recommendations['Tier'].unique(),
                default=recommendations['Tier'].unique()
            )
        
        with col2:
            min_bonus = st.number_input("Min Bonus Points:", min_value=0, value=0, step=100)
        
        with col3:
            max_bonus = st.number_input("Max Bonus Points:", min_value=0, value=1000, step=100)
        
        # Filter data
        filtered_rec = recommendations[
            (recommendations['Tier'].isin(selected_tier)) &
            (recommendations['Bonus_Points'] >= min_bonus) &
            (recommendations['Bonus_Points'] <= max_bonus)
        ]
        
        st.subheader(f"📋 Recommendations ({len(filtered_rec)} customers)")
        st.dataframe(
            filtered_rec[['Cust_ID', 'Tier', 'Current_Balance', 'Recommendation', 'Bonus_Points', 'Discount_Offer', 'Action']].head(50),
            use_container_width=True
        )
    
    # TAB 3: SMART DASHBOARD SUGGESTIONS
    with tab3:
        st.subheader("📊 Real-Time Dashboard Suggestions")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            high_priority = len(dashboard_suggestions[dashboard_suggestions['Priority'] == 'HIGH'])
            st.metric("🔴 High Priority", high_priority)
        
        with col2:
            medium_priority = len(dashboard_suggestions[dashboard_suggestions['Priority'] == 'MEDIUM'])
            st.metric("🟡 Medium Priority", medium_priority)
        
        with col3:
            low_priority = len(dashboard_suggestions[dashboard_suggestions['Priority'] == 'LOW'])
            st.metric("🟢 Low Priority", low_priority)
        
        st.markdown("---")
        
        # Priority-based display
        for priority in ['HIGH', 'MEDIUM', 'LOW']:
            priority_items = dashboard_suggestions[dashboard_suggestions['Priority'] == priority]
            
            if len(priority_items) > 0:
                icon = '🔴' if priority == 'HIGH' else '🟡' if priority == 'MEDIUM' else '🟢'
                
                with st.expander(f"{icon} {priority} Priority Items ({len(priority_items)})"):
                    for idx, row in priority_items.iterrows():
                        st.write(f"**{row['Item']}**")
                        st.write(f"Category: {row['Category']}")
                        st.write(f"Details: {row['Details']}")
                        st.divider()
        
        st.markdown("---")
        st.info("💡 **Implementation Tip**: Focus on HIGH priority alerts first for maximum ROI")
    
    # TAB 4: CATEGORY MULTIPLIERS
    with tab4:
        st.subheader("⭐ Category Multipliers for Points Earning")
        st.markdown("Premium categories earn more loyalty points to incentivize purchases")
        
        multipliers = rules_engine.calculate_category_multipliers()
        
        # Convert to DataFrame for visualization
        multiplier_df = pd.DataFrame([
            {'Category': k, 'Points Multiplier': v}
            for k, v in sorted(multipliers.items(), key=lambda x: x[1], reverse=True)
        ])
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("📊 Multiplier Comparison")
            fig_mult = px.bar(
                multiplier_df,
                x='Category',
                y='Points Multiplier',
                color='Points Multiplier',
                hover_data=['Points Multiplier'],
                title='Points Multiplier by Category',
                color_continuous_scale='Viridis'
            )
            fig_mult.add_hline(y=1.0, line_dash="dash", line_color="red", annotation_text="Base Multiplier")
            st.plotly_chart(fig_mult, use_container_width=True)
        
        with col2:
            st.subheader("🎁 Earning Potential")
            st.markdown("**Example: $100 Purchase**")
            
            for idx, row in multiplier_df.iterrows():
                base_points = 100  # $1 = 1 point
                earned_points = int(base_points * row['Points Multiplier'])
                bonus = earned_points - base_points
                st.write(f"**{row['Category']}**: {earned_points} pts ({bonus:+d} bonus)")
        
        st.markdown("---")
        
        st.subheader("📋 Category Multiplier Table")
        st.dataframe(multiplier_df, use_container_width=True, hide_index=True)
        
        st.success("✅ Multipliers are applied automatically to all transactions in these categories")

# PAGE 8: PROMOTIONAL EFFECTIVENESS
elif page == "Promotional Effectiveness":
    st.subheader("🎯 Promotional Effectiveness Analysis")
    st.markdown("Track promotional performance across products and stores")
    
    @st.cache_resource
    def load_promo_data():
        engine = LoyaltyPointsEngine()
        engine.load_loyalty_data()
        promo_eff = engine.calculate_promo_effectiveness()
        uplift = engine.calculate_sales_uplift_by_product()
        return promo_eff, uplift
    
    promo_eff, uplift = load_promo_data()
    
    st.markdown("---")
    st.subheader("📈 Promotional Effectiveness by Store")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Total Promotions", promo_eff['Promotion'].nunique())
    with col2:
        st.metric("Stores Covered", promo_eff['Store_ID'].nunique())
    with col3:
        st.metric("Total Sales Uplift", f"${promo_eff['Sales_Uplift'].sum():,.0f}")
    
    st.markdown("---")
    st.subheader("🏪 Promotion Performance Heatmap")
    
    pivot_table = promo_eff.pivot_table(
        values='Effectiveness_Score',
        index='Promotion',
        columns='Store_ID',
        aggfunc='first'
    )
    
    fig_heatmap = go.Figure(data=go.Heatmap(
        z=pivot_table.values,
        x=pivot_table.columns,
        y=pivot_table.index,
        colorscale='RdYlGn'
    ))
    fig_heatmap.update_layout(title='Promotion Effectiveness Score Heatmap (by Store)', xaxis_title='Store ID', yaxis_title='Promotion')
    st.plotly_chart(fig_heatmap, use_container_width=True)
    
    st.markdown("---")
    st.subheader("💲 Sales Uplift by Promotion")
    
    fig_uplift = px.bar(
        promo_eff.groupby('Promotion').agg({'Sales_Uplift': 'sum'}).reset_index(),
        x='Promotion',
        y='Sales_Uplift',
        title='Total Sales Uplift by Promotion',
        labels={'Sales_Uplift': 'Sales Value ($)'}
    )
    st.plotly_chart(fig_uplift, use_container_width=True)
    
    st.markdown("---")
    st.subheader("📊 Points Activity vs Sales")
    
    col1, col2 = st.columns(2)
    
    with col1:
        fig_points = px.scatter(
            promo_eff,
            x='Sales_Uplift',
            y='Points_Activity',
            size='Transaction_Count',
            color='Promotion',
            title='Sales Uplift vs Points Activity',
            labels={'Sales_Uplift': 'Sales ($)', 'Points_Activity': 'Points Earned'}
        )
        st.plotly_chart(fig_points, use_container_width=True)
    
    with col2:
        st.subheader("📋 Promo Effectiveness Metrics")
        st.dataframe(promo_eff.sort_values('Effectiveness_Score', ascending=False), use_container_width=True)
    
    st.markdown("---")
    st.subheader("🛍️ Top Products by Promotion Sales")
    
    fig_products = px.bar(
        uplift.head(10),
        x='SKU',
        y='Sales_Value',
        color='Promotion',
        title='Top 10 Products by Promotion Sales',
        labels={'Sales_Value': 'Sales Value ($)'}
    )
    st.plotly_chart(fig_products, use_container_width=True)
    
    st.markdown("---")
    st.subheader("📈 Product Details")
    st.dataframe(uplift.head(15), use_container_width=True)

# Footer
st.markdown("---")
st.markdown("""
    <div style='text-align: center; color: gray; font-size: 12px;'>
    <p>Retail Loyalty Analytics Platform | Team Member 3 - Visualization & Integration</p>
    <p>Data Source: SampleData folder | Last Updated: {}</p>
    </div>
""".format(datetime.now().strftime("%Y-%m-%d %H:%M:%S")), unsafe_allow_html=True)
