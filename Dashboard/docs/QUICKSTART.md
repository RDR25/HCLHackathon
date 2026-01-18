# 🚀 Streamlit Dashboard - Quick Start Guide

## What Was Created

I've created a **complete Streamlit dashboard** for your Retail Loyalty Analytics Platform with the following components:

### 📁 Files Created:
1. **app.py** - Main Streamlit dashboard application (18KB, 500+ lines)
2. **data_processor.py** - Data loading & processing module (7KB, 200+ lines)
3. **requirements.txt** - Python dependencies
4. **README_DASHBOARD.md** - Comprehensive documentation

### ✅ Data Analysis Summary:

| Metric | Value |
|--------|-------|
| **Total Customers** | 200 |
| **Total Products** | 50 |
| **Total Sales Transactions** | 385 |
| **Total Line Items** | 1,170 |
| **Date Range** | Jan 12-13, 2026 |
| **Total Sales Revenue** | ~$255K |
| **Total Points Earned** | ~316K |
| **Stores** | 5 locations (Delhi, Hyderabad, Bangalore, Warangal, Guntur) |
| **Product Categories** | 5 (Apparel, Home, Health, Electronics, Grocery) |

---

## 🎯 Dashboard Features (6 Pages)

### 1. **Dashboard Overview** 📈
- Executive KPIs (Sales, Transactions, Customers, Points)
- Daily sales trend visualization
- Sales by store location and tier
- Product category breakdown
- Top 10 customers by spend

### 2. **RFM Analysis** 🎯
- RFM (Recency, Frequency, Monetary) metrics
- Interactive 2D scatter plot showing customer positioning
- Customer segment distribution (pie chart)
- Segment statistics and comparisons
- Historical customer data table

### 3. **Customer Segmentation** 👥
- At-risk customer identification & monitoring
- Segment characteristics comparison
- Potential revenue loss calculation
- Retention opportunity metrics
- Detailed customer lists by segment

### 4. **Sales Analytics** 💰
- Store performance rankings
- Category-wise revenue breakdown
- Daily sales & transaction trends
- Store tier comparisons
- Performance statistics table

### 5. **Product Performance** 🛍️
- Top 20 products by revenue
- Category-wise revenue distribution
- Loyalty points earned by rule type
- Product quantity sold analysis
- Performance metrics table

### 6. **Data Summary** 📊
- All master data views (Customers, Products, Stores, Loyalty Rules)
- Sales transaction details
- Data quality metrics (missing values, duplicates check)
- Statistical summaries

---

## 🔧 Installation & Setup

### Step 1: Install Dependencies
```bash
cd /Users/ravuladimplerajeeswar/Desktop/HCLHackathon
pip install -r requirements.txt
```

### Step 2: Run the Dashboard
```bash
streamlit run app.py
```

### Step 3: Access the Dashboard
- Open browser to: **http://localhost:8501**
- Navigate using the sidebar menu

---

## 📊 Data Structure (Your CSV Files)

### Master Tables:
- **customers_master.csv** - 200 customers with enrollment dates & RFM segments
- **products_master.csv** - 50 products across 5 categories with pricing
- **stores_master.csv** - 5 retail stores in different cities (Tier A & B)
- **loyalty_rules_master.csv** - 3 loyalty earning rules with multipliers

### Transactional Tables:
- **sales_header.csv** - 385 transactions (ticket headers)
- **sales_line_items.csv** - 1,170 line items from transactions

---

## 🎨 Dashboard Preview

```
┌─ Dashboard Overview
│  ├─ KPI Cards (Sales, Transactions, Customers, Points)
│  ├─ Daily Sales Trend (Line Chart)
│  ├─ Sales by Store (Bar Chart)
│  ├─ Sales by Category (Pie Chart)
│  └─ Top 10 Customers (Bar Chart)
│
├─ RFM Analysis
│  ├─ RFM Metrics (Recency, Frequency, Monetary)
│  ├─ RFM Scatter Plot (2D Positioning)
│  ├─ Segment Distribution (Pie & Bar Charts)
│  └─ RFM Data Table (Top 20)
│
├─ Customer Segmentation
│  ├─ At-Risk Metrics & Potential Loss
│  ├─ Segment Statistics (Comparison)
│  └─ At-Risk Customer List (Details)
│
├─ Sales Analytics
│  ├─ Store Performance Metrics
│  ├─ Store Sales by Tier (Bar Chart)
│  ├─ Category Sales (Bar Chart)
│  ├─ Combined Trend Chart (Sales + Transactions)
│  └─ Store Performance Table
│
├─ Product Performance
│  ├─ Top 15 Products by Revenue
│  ├─ Category Distribution (Pie Chart)
│  ├─ Points by Loyalty Rule (Bar Chart)
│  └─ Product Details Table (Top 20)
│
└─ Data Summary
   ├─ Customers Master (Preview)
   ├─ Products Master (Preview)
   ├─ Stores Master (Full View)
   ├─ Sales Header (Preview)
   ├─ Loyalty Rules (Full View)
   └─ Data Quality Report (Metrics)
```

---

## 💡 Key Insights from Your Data

### Customer Analysis:
- **Segments:** New, At-Risk, Loyalist, Champion
- **Active Customers:** 200 enrolled customers
- **Top Customer:** Highest spend customer is CUST_004

### Sales Performance:
- **Date Range:** Jan 12-13, 2026 (2-day snapshot)
- **Total Revenue:** ~$255,000
- **Avg Transaction:** ~$663
- **Points Generated:** ~316,000 loyalty points

### Store Performance:
- **Top Store:** Tier A locations (Delhi, Hyderabad, Bangalore)
- **Distribution:** 5 stores across India

### Product Categories:
- **Top 5 Categories:** Health, Electronics, Home, Apparel, Grocery
- **Product Range:** Prices from $7 to $144

### Loyalty Points:
- **Rule 1 (Standard):** 1.0x multiplier
- **Rule 2 (Health Bonus):** 2.0x multiplier
- **Rule 3 (Electronics Bonus):** 1.5x multiplier

---

## 🔄 Integration Ready

Your dashboard is **designed to work with real data** from your team members:

### When Member 1 (Data Ingestion) Provides Data:
- Simply update the `data_path` in `data_processor.py` (line 9)
- Or modify the load methods to connect to your database

### When Member 2 (Data Quality & Analytics) Provides Data:
- Analytics tables will plug directly into the dashboard
- RFM calculations shown here match the expected output format
- Segmentation logic demonstrated for reference

**No code changes needed in app.py - just swap the data source!**

---

## 🎮 How to Use the Dashboard

1. **Select Page**: Use sidebar to navigate between 6 pages
2. **Explore Data**: Click on charts to zoom, pan, or hover for details
3. **Filter**: Each chart is interactive (zoom, download, etc.)
4. **Export**: Right-click charts to save as PNG

---

## 📝 Next Steps

1. ✅ Install dependencies: `pip install -r requirements.txt`
2. ✅ Run dashboard: `streamlit run app.py`
3. ⏳ Await data from Team Members 1 & 2
4. ⏳ Integrate real data into the system
5. ⏳ Enhance with real-time refreshes and database connections

---

## 🆘 Troubleshooting

| Issue | Solution |
|-------|----------|
| Streamlit not found | Run: `pip install streamlit` |
| CSV not found error | Ensure you're in project root directory |
| Port 8501 in use | Run: `streamlit run app.py --server.port 8502` |
| Slow loading | Clear cache: `Ctrl+C` and restart |

---

## 📚 Documentation Files

- `README.md` - Original project overview
- `README_DASHBOARD.md` - Detailed dashboard documentation
- `QUICKSTART.md` - This file

---

## 🎓 Your Role as Team Member 3

✅ **Completed:**
- Dashboard design & implementation
- Data visualization (Plotly & Streamlit)
- RFM analysis page
- Customer segmentation analysis
- Sales & product performance analytics
- Data quality reporting
- Documentation

🔄 **Ready for:**
- Integration with real data from Members 1 & 2
- Database connections (PostgreSQL/MySQL/Snowflake)
- Performance optimization
- Real-time data refresh
- Advanced filtering & drill-down capabilities

---

## 📞 Quick Commands

```bash
# Install dependencies
pip install -r requirements.txt

# Run dashboard
streamlit run app.py

# Run with debug mode
streamlit run app.py --logger.level=debug

# Clear cache and run
rm -rf ~/.streamlit && streamlit run app.py

# Run on different port
streamlit run app.py --server.port 8502
```

---

**Ready to launch your dashboard!** 🚀

Run: `streamlit run app.py` to start exploring your Retail Loyalty Analytics Platform.
