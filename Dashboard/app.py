"""
Retail Loyalty Analytics Platform - Streamlit Dashboard
Simplified version with fixed data paths and column references
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta
import sys
import os

# Add src directory to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src/core'))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src/engines'))

from data_processor import DataProcessor

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
    processor = DataProcessor(data_path='data/input')
    processor.load_all_data()
    return processor

try:
    processor = load_data()
    data_loaded = True
except Exception as e:
    st.error(f"Error loading data: {e}")
    data_loaded = False

# Sidebar navigation
st.sidebar.markdown("# 📊 Navigation")
page = st.sidebar.radio(
    "Select a page:",
    [
        "Dashboard Overview",
        "RFM Analysis",
        "Customer Segmentation",
        "Sales Analytics",
        "Product Performance",
        "Promotional Effectiveness",
        "Admin Panel",
        "Data Summary"
    ]
)

# Title
st.markdown("<div class='header-title'>🏪 Retail Loyalty Analytics Platform</div>", unsafe_allow_html=True)
st.markdown("---")

if not data_loaded:
    st.warning("⚠️ Unable to load data. Please check data files.")
    st.stop()

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
        y=sales_trend['Sales'],
        mode='lines+markers',
        name='Daily Sales',
        line=dict(color='#1f77b4', width=2)
    ))
    fig_trend.update_layout(
        title="Daily Sales Trend",
        xaxis_title="Date",
        yaxis_title="Sales ($)",
        height=400,
        hovermode='x unified'
    )
    st.plotly_chart(fig_trend, use_container_width=True)
    
    st.markdown("---")
    
    # Sales by store and category
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("🏪 Sales by Store")
        store_sales = processor.get_sales_by_store()
        fig_store = px.bar(
            store_sales,
            x='Store_ID',
            y='Sales',
            title="Store-wise Sales",
            labels={'Sales': 'Total Sales ($)'}
        )
        st.plotly_chart(fig_store, use_container_width=True)
    
    with col2:
        st.subheader("📦 Sales by Category")
        category_sales = processor.get_sales_by_category()
        if not category_sales.empty:
            fig_cat = px.pie(
                category_sales,
                values='Sales',
                names='Category',
                title="Category Distribution"
            )
            st.plotly_chart(fig_cat, use_container_width=True)
        else:
            st.info("No category data available")
    
    st.markdown("---")
    
    # Top customers
    st.subheader("👥 Top Customers")
    top_customers = processor.get_top_customers(limit=10)
    st.dataframe(top_customers, use_container_width=True)

# PAGE 2: RFM ANALYSIS
elif page == "RFM Analysis":
    st.subheader("📊 RFM Analysis - Customer Value Segmentation")
    st.markdown("Understanding customer behavior through Recency, Frequency, and Monetary value")
    
    rfm_data = processor.get_rfm_analysis()
    
    if rfm_data is not None and len(rfm_data) > 0:
        # RFM Scatter Plot
        fig_rfm = px.scatter(
            rfm_data,
            x='Recency',
            y='Frequency',
            size='Monetary',
            color='RFM_Segment',
            hover_data=['Customer_ID', 'Monetary'],
            title="RFM Segmentation Scatter Plot",
            labels={'Recency': 'Days Since Last Purchase', 'Frequency': 'Purchase Count'},
            height=500
        )
        st.plotly_chart(fig_rfm, use_container_width=True)
        
        st.markdown("---")
        
        # Segment Distribution
        st.subheader("📈 Customer Segment Distribution")
        segment_dist = processor.get_segment_distribution()
        
        col1, col2 = st.columns(2)
        with col1:
            fig_seg = px.pie(
                segment_dist,
                values='Count',
                names='Segment',
                title="Customer Segments"
            )
            st.plotly_chart(fig_seg, use_container_width=True)
        
        with col2:
            st.dataframe(segment_dist, use_container_width=True)
        
        st.markdown("---")
        
        # Detailed RFM Stats
        st.subheader("📊 RFM Statistics by Segment")
        segment_stats = rfm_data.groupby('RFM_Segment').agg({
            'Recency': ['mean', 'min', 'max'],
            'Frequency': ['mean', 'min', 'max'],
            'Monetary': ['mean', 'min', 'max'],
            'Customer_ID': 'count'
        }).round(2)
        st.dataframe(segment_stats, use_container_width=True)
    else:
        st.warning("No RFM data available")

# PAGE 3: CUSTOMER SEGMENTATION
elif page == "Customer Segmentation":
    st.subheader("👥 Customer Segmentation Analysis")
    
    rfm_data = processor.get_rfm_analysis()
    
    if rfm_data is not None and len(rfm_data) > 0:
        segment_dist = processor.get_segment_distribution()
        
        st.markdown("---")
        st.subheader("Segment Breakdown")
        
        # Display each segment
        for idx, row in segment_dist.iterrows():
            segment_name = row['Segment']
            count = row['Count']
            
            col1, col2 = st.columns([3, 1])
            with col1:
                st.write(f"**{segment_name}**")
            with col2:
                st.metric("Customers", count)
            
            # Get segment details
            seg_data = rfm_data[rfm_data['RFM_Segment'] == segment_name]
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.metric("Avg Recency", f"{seg_data['Recency'].mean():.0f} days")
            with col2:
                st.metric("Avg Frequency", f"{seg_data['Frequency'].mean():.1f}")
            with col3:
                st.metric("Avg Monetary", f"${seg_data['Monetary'].mean():.2f}")
            
            st.markdown("---")
        
        # At-risk customers
        st.subheader("⚠️ At-Risk Customers")
        at_risk = processor.get_at_risk_customers()
        if not at_risk.empty:
            st.dataframe(at_risk, use_container_width=True)
        else:
            st.info("No at-risk customers identified")
    else:
        st.warning("No segmentation data available")

# PAGE 4: SALES ANALYTICS
elif page == "Sales Analytics":
    st.subheader("📈 Sales Analytics")
    
    st.markdown("---")
    st.subheader("Sales Trend")
    sales_trend = processor.get_sales_trend()
    
    fig_trend = px.line(
        sales_trend,
        x='Date',
        y='Sales',
        title="Daily Sales Trend",
        labels={'Sales': 'Total Sales ($)', 'Date': 'Date'},
        height=400
    )
    st.plotly_chart(fig_trend, use_container_width=True)
    
    st.markdown("---")
    st.subheader("Store Performance")
    store_sales = processor.get_sales_by_store()
    
    col1, col2 = st.columns(2)
    with col1:
        fig_store = px.bar(
            store_sales,
            x='Store_ID',
            y='Sales',
            title="Sales by Store",
            labels={'Sales': 'Total Sales ($)'}
        )
        st.plotly_chart(fig_store, use_container_width=True)
    
    with col2:
        fig_trans = px.bar(
            store_sales,
            x='Store_ID',
            y='Transactions',
            title="Transactions by Store",
            labels={'Transactions': 'Count'}
        )
        st.plotly_chart(fig_trans, use_container_width=True)
    
    st.markdown("---")
    st.subheader("Category Analysis")
    category_sales = processor.get_sales_by_category()
    if not category_sales.empty:
        fig_cat = px.bar(
            category_sales,
            x='Category',
            y='Sales',
            title="Sales by Category",
            labels={'Sales': 'Total Sales ($)'}
        )
        st.plotly_chart(fig_cat, use_container_width=True)

# PAGE 5: PROMOTIONAL EFFECTIVENESS
elif page == "Promotional Effectiveness":
    st.subheader("📊 Promotional Effectiveness Tracking")
    st.markdown("Track impact of bonus points and promotions on sales uplift")
    
    # Load promo effectiveness data
    try:
        promo_df = pd.read_csv('data/output/promo_effectiveness_after_bonus.csv')
        
        # Key Metrics
        st.markdown("### 📈 Overall Performance Metrics")
        col1, col2, col3, col4, col5 = st.columns(5)
        
        with col1:
            avg_sales_uplift = promo_df['Sales_Uplift_Percent'].mean()
            st.metric("Avg Sales Uplift", f"{avg_sales_uplift:.1f}%")
        
        with col2:
            avg_transaction_uplift = promo_df['Transaction_Uplift_Percent'].mean()
            st.metric("Avg Transaction Uplift", f"{avg_transaction_uplift:.1f}%")
        
        with col3:
            avg_effectiveness = promo_df['Effectiveness_Score'].mean()
            st.metric("Avg Effectiveness Score", f"{avg_effectiveness:.2f}")
        
        with col4:
            avg_roi = promo_df['ROI_Percent'].mean()
            st.metric("Avg ROI", f"{avg_roi:.1f}%")
        
        with col5:
            total_promos = len(promo_df)
            st.metric("Total Promotions", total_promos)
        
        st.markdown("---")
        
        # Sales Uplift by Promotion Type
        st.markdown("### 💰 Sales Uplift by Promotion Type")
        promo_uplift = promo_df.groupby('Promotion_Type').agg({
            'Sales_Uplift_Percent': 'mean',
            'After_Sales': 'sum',
            'Before_Sales': 'sum'
        }).reset_index()
        
        fig_uplift = px.bar(
            promo_uplift,
            x='Promotion_Type',
            y='Sales_Uplift_Percent',
            title='Average Sales Uplift by Promotion Type',
            labels={'Sales_Uplift_Percent': 'Uplift %', 'Promotion_Type': 'Promotion Type'},
            color='Sales_Uplift_Percent',
            color_continuous_scale='Greens'
        )
        st.plotly_chart(fig_uplift, use_container_width=True)
        
        st.markdown("---")
        
        # Store Performance
        st.markdown("### 🏪 Performance by Store")
        store_perf = promo_df.groupby('Store_Location').agg({
            'Sales_Uplift_Percent': 'mean',
            'Transaction_Uplift_Percent': 'mean',
            'Effectiveness_Score': 'mean',
            'ROI_Percent': 'mean'
        }).reset_index()
        
        col1, col2 = st.columns(2)
        
        with col1:
            fig_store_sales = px.bar(
                store_perf,
                x='Store_Location',
                y='Sales_Uplift_Percent',
                title='Sales Uplift by Store',
                labels={'Sales_Uplift_Percent': 'Uplift %'},
                color='Sales_Uplift_Percent',
                color_continuous_scale='Blues'
            )
            st.plotly_chart(fig_store_sales, use_container_width=True)
        
        with col2:
            fig_store_roi = px.bar(
                store_perf,
                x='Store_Location',
                y='ROI_Percent',
                title='ROI by Store',
                labels={'ROI_Percent': 'ROI %'},
                color='ROI_Percent',
                color_continuous_scale='Purples'
            )
            st.plotly_chart(fig_store_roi, use_container_width=True)
        
        st.markdown("---")
        
        # Before vs After Comparison
        st.markdown("### 📊 Before vs After Comparison")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            total_before_sales = promo_df['Before_Sales'].sum()
            total_after_sales = promo_df['After_Sales'].sum()
            overall_uplift = ((total_after_sales - total_before_sales) / total_before_sales * 100)
            
            st.metric(
                "Overall Sales Uplift",
                f"${total_after_sales:,.0f}",
                f"+{overall_uplift:.1f}%"
            )
        
        with col2:
            total_before_trans = promo_df['Before_Transaction_Count'].sum()
            total_after_trans = promo_df['After_Transaction_Count'].sum()
            trans_uplift = ((total_after_trans - total_before_trans) / total_before_trans * 100)
            
            st.metric(
                "Overall Transaction Uplift",
                f"{int(total_after_trans)}",
                f"+{trans_uplift:.1f}%"
            )
        
        with col3:
            total_before_units = promo_df['Units_Sold_Before'].sum()
            total_after_units = promo_df['Units_Sold_After'].sum()
            units_uplift = ((total_after_units - total_before_units) / total_before_units * 100)
            
            st.metric(
                "Overall Units Uplift",
                f"{int(total_after_units)}",
                f"+{units_uplift:.1f}%"
            )
        
        st.markdown("---")
        
        # Effectiveness Score Distribution
        st.markdown("### 🎯 Effectiveness Score Distribution")
        
        fig_effectiveness = px.scatter(
            promo_df,
            x='Sales_Uplift_Percent',
            y='Effectiveness_Score',
            color='Promotion_Type',
            size='ROI_Percent',
            hover_data=['Store_Location', 'ROI_Percent'],
            title='Effectiveness Score vs Sales Uplift',
            labels={'Sales_Uplift_Percent': 'Sales Uplift %', 'Effectiveness_Score': 'Effectiveness Score'}
        )
        st.plotly_chart(fig_effectiveness, use_container_width=True)
        
        st.markdown("---")
        
        # Detailed Promo Data Table
        st.markdown("### 📋 Detailed Promotion Results")
        
        display_cols = ['Promotion_ID', 'Promotion_Type', 'Store_Location', 'Target_Segment', 
                       'Bonus_Points_Offered', 'Sales_Uplift_Percent', 'Transaction_Uplift_Percent',
                       'Effectiveness_Score', 'ROI_Percent', 'Status']
        
        st.dataframe(
            promo_df[display_cols].sort_values('ROI_Percent', ascending=False),
            use_container_width=True,
            height=400
        )
        
        st.markdown("---")
        
        # Top Performing Promos
        st.markdown("### 🏆 Top Performing Promotions")
        
        top_promos = promo_df.nlargest(5, 'ROI_Percent')[['Promotion_ID', 'Promotion_Type', 'Store_Location', 'ROI_Percent', 'Sales_Uplift_Percent']]
        
        for idx, row in top_promos.iterrows():
            st.success(f"✅ **{row['Promotion_ID']}** - {row['Promotion_Type']} ({row['Store_Location']}): ROI {row['ROI_Percent']:.1f}%, Sales Uplift {row['Sales_Uplift_Percent']:.1f}%")
        
    except Exception as e:
        st.error(f"Error loading promotional effectiveness data: {e}")

# PAGE 6: ADMIN PANEL
elif page == "Admin Panel":
    st.subheader("⚙️ Admin Control Panel")
    st.markdown("Manage promotions, discounts, loyalty points, and special offers")
    
    admin_tab1, admin_tab2, admin_tab3, admin_tab4 = st.tabs(
        ["Least Sold Products", "Least Active Customers", "Special Day Promotions", "Promotional Rates"]
    )
    
    # TAB 1: LEAST SOLD PRODUCTS
    with admin_tab1:
        st.subheader("📦 Least Sold Products - Add Bonus Points")
        st.markdown("Boost sales of low-performing products by adding bonus loyalty points")
        
        product_perf = processor.get_product_performance(limit=50)
        least_products = product_perf.tail(10)
        
        st.write("**10 Least Sold Products:**")
        col1, col2, col3 = st.columns(3)
        
        bonus_points_dict = {}
        for idx, (i, row) in enumerate(least_products.iterrows()):
            if idx % 3 == 0:
                col1, col2, col3 = st.columns(3)
            
            col = [col1, col2, col3][idx % 3]
            with col:
                st.write(f"**{row['SKU']}**")
                st.write(f"Revenue: ${row['Revenue']:.2f}")
                bonus_pts = st.number_input(
                    f"Bonus Points for {row['SKU']}",
                    min_value=0,
                    max_value=1000,
                    value=0,
                    key=f"bonus_{row['SKU']}"
                )
                bonus_points_dict[row['SKU']] = bonus_pts
        
        if st.button("💾 Save Bonus Points to CSV", key="save_bonus"):
            # Create output file
            bonus_df = pd.DataFrame([
                {'SKU': sku, 'Bonus_Points': pts} 
                for sku, pts in bonus_points_dict.items() if pts > 0
            ])
            
            if not bonus_df.empty:
                bonus_df.to_csv('data/output/product_bonus_points.csv', index=False)
                st.success(f"✅ Saved {len(bonus_df)} products with bonus points!")
                st.dataframe(bonus_df)
    
    # TAB 2: LEAST ACTIVE CUSTOMERS
    with admin_tab2:
        st.subheader("👥 Least Active Customers - Add Loyalty Points")
        st.markdown("Re-engage inactive customers by adding loyalty points")
        
        at_risk = processor.get_at_risk_customers()
        if not at_risk.empty:
            at_risk_sorted = at_risk.sort_values('Monetary', ascending=True).head(15)
            
            st.write("**15 Least Active/Valuable Customers:**")
            
            loyalty_points_dict = {}
            for idx, (i, row) in enumerate(at_risk_sorted.iterrows()):
                col1, col2, col3, col4 = st.columns(4)
                
                with col1:
                    st.write(f"**ID: {row['Customer_ID']}**")
                with col2:
                    st.write(f"Spend: ${row['Monetary']:.2f}")
                with col3:
                    st.write(f"Last Visit: {row['Recency']} days ago")
                with col4:
                    loyalty_pts = st.number_input(
                        f"Add Points for {row['Customer_ID']}",
                        min_value=0,
                        max_value=5000,
                        value=0,
                        key=f"loyalty_{row['Customer_ID']}"
                    )
                    loyalty_points_dict[row['Customer_ID']] = loyalty_pts
            
            if st.button("💾 Save Loyalty Points to CSV", key="save_loyalty"):
                loyalty_df = pd.DataFrame([
                    {'Customer_ID': cid, 'Bonus_Loyalty_Points': pts}
                    for cid, pts in loyalty_points_dict.items() if pts > 0
                ])
                
                if not loyalty_df.empty:
                    loyalty_df.to_csv('data/output/customer_bonus_loyalty_points.csv', index=False)
                    st.success(f"✅ Saved loyalty points for {len(loyalty_df)} customers!")
                    st.dataframe(loyalty_df)
    
    # TAB 3: SPECIAL DAY PROMOTIONS
    with admin_tab3:
        st.subheader("🎉 Special Day Promotions - Apply Category Discounts")
        st.markdown("Create special promotions for specific days and categories")
        
        special_days = [
            "New Year (Jan 1)",
            "Valentine's Day (Feb 14)",
            "St. Patrick's Day (Mar 17)",
            "Easter",
            "Mother's Day",
            "Father's Day",
            "Independence Day (Jul 4)",
            "Back to School (Aug-Sep)",
            "Halloween (Oct 31)",
            "Black Friday (Nov)",
            "Cyber Monday (Nov)",
            "Christmas (Dec 25)",
            "Boxing Day (Dec 26)",
            "New Year's Eve (Dec 31)"
        ]
        
        col1, col2 = st.columns(2)
        
        with col1:
            selected_day = st.selectbox("📅 Select Special Day", special_days)
        
        categories = processor.products_df['Category'].unique().tolist() if 'Category' in processor.products_df.columns else []
        
        with col2:
            selected_category = st.selectbox("📦 Select Category", categories if categories else ["General"])
        
        discount_rate = st.slider(
            "💰 Discount Rate (%)",
            min_value=0,
            max_value=100,
            value=15,
            step=1
        )
        
        if st.button("🎊 Apply Special Day Promotion", key="apply_special"):
            promo_df = pd.DataFrame([{
                'Special_Day': selected_day,
                'Category': selected_category,
                'Discount_Rate': discount_rate,
                'Applied_Date': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            }])
            
            promo_df.to_csv('data/output/special_day_promotions.csv', mode='a', header=False, index=False)
            st.success(f"✅ Applied {discount_rate}% discount to {selected_category} for {selected_day}!")
            st.dataframe(promo_df)
    
    # TAB 4: PROMOTIONAL RATES
    with admin_tab4:
        st.subheader("📊 Configure Promotional Rates & Discounts")
        st.markdown("Set base rates for all promotions and discounts")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("💳 Loyalty Point Rates")
            base_points_per_dollar = st.number_input(
                "Base Points per $1 Spent",
                min_value=0.0,
                max_value=10.0,
                value=1.0,
                step=0.1
            )
            
            bonus_multiplier = st.number_input(
                "Bonus Point Multiplier for Special Days",
                min_value=1.0,
                max_value=5.0,
                value=2.0,
                step=0.1
            )
        
        with col2:
            st.subheader("🏷️ Discount Rates")
            standard_discount = st.number_input(
                "Standard Discount (%)",
                min_value=0,
                max_value=100,
                value=10,
                step=1
            )
            
            vip_discount = st.number_input(
                "VIP/Champion Discount (%)",
                min_value=0,
                max_value=100,
                value=20,
                step=1
            )
        
        st.markdown("---")
        
        if st.button("💾 Save Promotional Rates", key="save_rates"):
            rates_df = pd.DataFrame([{
                'Base_Points_Per_Dollar': base_points_per_dollar,
                'Bonus_Multiplier': bonus_multiplier,
                'Standard_Discount': standard_discount,
                'VIP_Discount': vip_discount,
                'Configured_Date': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            }])
            
            rates_df.to_csv('data/output/promotional_rates_config.csv', index=False)
            st.success("✅ Promotional rates saved successfully!")
            st.dataframe(rates_df)
    
    st.markdown("---")
    
    # GENERATE RECOMMENDATIONS WITH DISCOUNTS
    st.subheader("🎯 Generate User Recommendations with Discounts")
    
    if st.button("📧 Generate Personalized Recommendations", key="gen_recs"):
        recs_data = []
        rfm_data = processor.get_rfm_analysis()
        
        for idx, row in rfm_data.head(20).iterrows():
            cust_id = row['Customer_ID']
            segment = row['RFM_Segment']
            
            # Determine discount based on segment
            if segment == "Champions":
                discount = vip_discount
                rec = "Premium products with VIP discount"
            elif segment == "Loyal Customers":
                discount = standard_discount
                rec = "Continue with preferred categories"
            elif segment == "At-Risk Customers":
                discount = vip_discount
                rec = "Re-engagement offer - exclusive discount"
            else:
                discount = standard_discount
                rec = "Personalized recommendations"
            
            # Get recommended product
            if not processor.products_df.empty:
                rec_product = processor.products_df.sample(1).iloc[0]
                product_id = rec_product['SKU'] if 'SKU' in rec_product.index else "N/A"
            else:
                product_id = "N/A"
            
            recs_data.append({
                'Customer_ID': cust_id,
                'Segment': segment,
                'Product_ID': product_id,
                'Discount_Percentage': discount,
                'Recommendation': rec,
                'Generated_Date': datetime.now().strftime('%Y-%m-%d')
            })
        
        recs_df = pd.DataFrame(recs_data)
        recs_df.to_csv('data/output/personalized_recommendations_with_discounts.csv', index=False)
        
        st.success(f"✅ Generated {len(recs_df)} personalized recommendations!")
        st.dataframe(recs_df)

# PAGE 6: PRODUCT PERFORMANCE
elif page == "Product Performance":
    st.subheader("🎯 Product Performance")
    
    product_perf = processor.get_product_performance(limit=20)
    
    if not product_perf.empty:
        st.markdown("---")
        st.subheader("Top Products by Revenue")
        
        fig_prod = px.bar(
            product_perf,
            x='SKU',
            y='Revenue',
            title="Top 20 Products by Revenue",
            labels={'Revenue': 'Total Revenue ($)'},
            height=500
        )
        st.plotly_chart(fig_prod, use_container_width=True)
        
        st.markdown("---")
        st.subheader("Product Details")
        st.dataframe(product_perf, use_container_width=True)
    else:
        st.info("No product performance data available")

# PAGE 7: DATA SUMMARY
elif page == "Data Summary":
    st.subheader("📋 Data Summary")
    
    st.markdown("---")
    st.subheader("Customers")
    with st.expander("View Customer Data"):
        st.write(f"Total Records: {len(processor.customers_df)}")
        st.write(f"Columns: {processor.customers_df.columns.tolist()}")
        st.dataframe(processor.customers_df.head(20), use_container_width=True)
        
        if 'Enrollment_Date' in processor.customers_df.columns:
            date_range = processor.customers_df['Enrollment_Date'].max() - processor.customers_df['Enrollment_Date'].min()
            st.write(f"Date Range: {date_range.days} days")
    
    st.markdown("---")
    st.subheader("Products")
    with st.expander("View Product Data"):
        st.write(f"Total Records: {len(processor.products_df)}")
        st.write(f"Columns: {processor.products_df.columns.tolist()}")
        st.dataframe(processor.products_df.head(20), use_container_width=True)
    
    st.markdown("---")
    st.subheader("Sales Header")
    with st.expander("View Sales Transactions"):
        st.write(f"Total Records: {len(processor.sales_header_df)}")
        st.write(f"Columns: {processor.sales_header_df.columns.tolist()}")
        st.dataframe(processor.sales_header_df.head(20), use_container_width=True)
        
        if 'Date' in processor.sales_header_df.columns:
            st.write(f"Date Range: {processor.sales_header_df['Date'].min().date()} to {processor.sales_header_df['Date'].max().date()}")
    
    st.markdown("---")
    st.subheader("Data Quality")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("**Customers**")
        st.write(f"- Missing Values: {processor.customers_df.isnull().sum().sum()}")
        st.write(f"- Duplicates: {processor.customers_df.duplicated().sum()}")
    
    with col2:
        st.write("**Sales**")
        st.write(f"- Missing Values: {processor.sales_header_df.isnull().sum().sum()}")
        st.write(f"- Duplicates: {processor.sales_header_df.duplicated().sum()}")

# Footer
st.markdown("---")
st.markdown(f"""
<p style="text-align: center; color: #888; font-size: 0.9em;">
Data Source: data/ folder | Last Updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
</p>
""", unsafe_allow_html=True)
