# Retail Loyalty Analytics Dashboard - Streamlit Implementation

## 📊 Project Status: Team Member 3 Contribution

This is the **visualization and integration layer** of the Retail Loyalty Analytics Platform, developed by Team Member 3.

---

## 🎯 Features Implemented

### 1. **Dashboard Overview**
- Executive summary metrics (Total Sales, Transactions, Active Customers, Points Earned)
- Daily sales trend visualization
- Sales distribution by store location and tier
- Sales breakdown by product category
- Top 10 customers by spend

### 2. **RFM Analysis**
- Recency, Frequency, and Monetary value calculations
- RFM positioning scatter plot (interactive 2D analysis)
- Customer segment distribution (pie and bar charts)
- Segment-wise statistics and comparisons
- Historical customer transaction data

### 3. **Customer Segmentation**
- At-risk customers identification and monitoring
- Segment-wise statistics (Recency, Frequency, Spend)
- Retention focus metrics showing potential revenue loss
- Comparative analysis across all segments
- Detailed at-risk customer list with historical spend

### 4. **Sales Analytics**
- Store performance comparison (location, tier, revenue)
- Category-wise sales performance
- Daily sales trend with transaction count overlay
- Top performing stores and categories
- Transaction frequency analysis

### 5. **Product Performance**
- Top 20 products by revenue
- Category-wise product distribution
- Loyalty points earned by rule type
- Product quantity sold analysis
- Revenue contribution by category

### 6. **Data Summary**
- All master data tables (Customers, Products, Stores, Loyalty Rules)
- Sales transaction details
- Data quality metrics (missing values, duplicates)
- Statistical summaries and data ranges

---

## 🛠️ Technical Stack

- **Framework:** Streamlit 1.28.1
- **Data Processing:** Pandas 2.0.3, NumPy 1.24.3
- **Visualization:** Plotly 5.17.0, Altair 5.0.1
- **Language:** Python 3.8+

---

## 📁 Project Structure

```
HCLHackathon/
├── app.py                    # Main Streamlit dashboard application
├── data_processor.py         # Data loading and processing module
├── requirements.txt          # Python dependencies
├── SampleData/              # Sample CSV data files
│   ├── customers_master.csv
│   ├── products_master.csv
│   ├── stores_master.csv
│   ├── sales_header.csv
│   ├── sales_line_items.csv
│   └── loyalty_rules_master.csv
└── README_DASHBOARD.md      # This file
```

---

## 📊 Data Model

### Master Tables
1. **customers_master.csv**
   - Cust_ID: Unique customer identifier
   - Enrollment_Date: Date when customer joined loyalty program
   - RFM_Segment: Customer segment (New, At Risk, Loyalist, Champion)

2. **products_master.csv**
   - SKU: Product identifier
   - Category: Product category (Apparel, Home, Health, Electronics, Grocery)
   - Base_Price: Product price

3. **stores_master.csv**
   - Store_ID: Unique store identifier
   - Location: Store location/city
   - Tier: Store tier classification (A, B)

4. **loyalty_rules_master.csv**
   - Rule_ID: Rule identifier
   - Rule_Name: Rule description (Standard Earn, Health Bonus, Electronics Bonus)
   - Multiplier: Points multiplier factor
   - Trigger_Category: Category triggering the rule

### Transactional Tables
5. **sales_header.csv**
   - Ticket_ID: Transaction identifier
   - Cust_ID: Customer reference
   - Store_ID: Store reference
   - Date: Transaction date
   - Total_Points_Earned: Loyalty points for transaction
   - Total_Value: Transaction amount

6. **sales_line_items.csv**
   - Ticket_ID: Transaction reference
   - SKU: Product reference
   - Qty: Quantity purchased
   - Rule_ID: Loyalty rule applied
   - Points_Per_Item: Points earned per item
   - Line_Total: Line item total value

---

## 🚀 How to Run

### Installation

1. **Install Python dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Ensure sample data is in place:**
   ```bash
   ls SampleData/  # Verify all 6 CSV files exist
   ```

### Running the Dashboard

```bash
streamlit run app.py
```

The dashboard will open in your browser at `http://localhost:8501`

---

## 📈 Key Metrics Tracked

| Metric | Description |
|--------|-------------|
| **Total Sales** | Sum of all transaction values |
| **Total Transactions** | Count of all sales tickets |
| **Active Customers** | Unique customers in dataset |
| **Total Points Earned** | Sum of loyalty points from all transactions |
| **Avg Transaction Value** | Average value per transaction |
| **Recency** | Days since last purchase |
| **Frequency** | Number of transactions per customer |
| **Monetary** | Total customer lifetime value |

---

## 🎨 Dashboard Pages

### 1️⃣ Dashboard Overview
- Quick view of key metrics
- Sales trends over time
- Store and category performance
- Top customers identification

### 2️⃣ RFM Analysis
- RFM scatter plot for customer positioning
- Customer segment distribution
- Segment statistics and comparisons
- Interactive filtering by segment

### 3️⃣ Customer Segmentation
- At-risk customer identification
- Segment characteristics comparison
- Potential revenue loss calculation
- Retention opportunity analysis

### 4️⃣ Sales Analytics
- Store performance ranking
- Category-wise sales breakdown
- Daily sales and transaction trends
- Store tier comparison

### 5️⃣ Product Performance
- Top-performing SKUs
- Category-wise revenue distribution
- Loyalty points by rule type
- Product sales statistics

### 6️⃣ Data Summary
- Master data preview
- Data quality metrics
- Statistical summaries
- Completeness verification

---

## 🔄 Data Dependencies (Assumed from Team Members)

> **Current Status**: Dashboard is built with **mock sample data**. When actual data arrives from Team Members 1 & 2:

### From Member 1 (Data Ingestion)
- Clean, validated customer master data
- Product catalog and pricing
- Store directory
- Transaction history

### From Member 2 (Data Quality & Analytics)
- Validated and cleaned data
- RFM calculations
- Customer segmentation results
- Loyalty points calculations
- Quality assurance reports

### Integration Points
The dashboard is designed to seamlessly integrate real data by:
- Modifying data source paths in `data_processor.py`
- Connecting to database tables (PostgreSQL/Snowflake/MySQL)
- Using data APIs from downstream systems
- No code changes needed in `app.py`

---

## 💡 Future Enhancements

1. **Real Database Integration**
   - PostgreSQL/MySQL/Snowflake connection
   - Dynamic data refresh
   - Real-time dashboards

2. **Advanced Analytics**
   - Predictive churn models
   - Customer lifetime value (CLV) projections
   - Next-best-action recommendations

3. **Interactive Features**
   - Date range filters
   - Customer search and drill-down
   - Export to CSV/PDF
   - Automated alerts for at-risk customers

4. **Performance Optimization**
   - Data caching strategies
   - Query optimization
   - Incremental data loading

5. **Multi-language Support**
   - English, Hindi, Regional languages
   - Localized metrics and formats

---

## 📝 Notes for Team Integration

### For Member 1 (Data Ingestion)
- Expected data format matches `SampleData/` structure
- CSV files can be easily replaced with database queries
- Path configuration in `data_processor.py` line 9

### For Member 2 (Data Quality & Analytics)
- RFM calculations are demonstrated in this dashboard
- Segmentation logic is clearly implemented
- Quality metrics displayed in "Data Summary" tab
- Integration ready for your calculated tables

### For Team Coordination
- Use GitHub branches: `feature/member1`, `feature/member2`, `feature/member3`
- Testing data in `SampleData/` folder
- Production data connections can be added without breaking existing code
- Documentation in Architecture/ folder

---

## 🐛 Troubleshooting

### Error: "ModuleNotFoundError: No module named 'streamlit'"
**Solution:** Run `pip install -r requirements.txt`

### Error: "FileNotFoundError: SampleData/customers_master.csv"
**Solution:** Ensure you're in the project root directory when running `streamlit run app.py`

### Dashboard loads slowly
**Solution:** Use Streamlit's caching with `@st.cache_resource` (already implemented)

### Data not updating
**Solution:** Clear cache with `Ctrl+C` and restart Streamlit, or use `--logger.level=debug`

---

## 📞 Support & Documentation

- **Streamlit Docs:** https://docs.streamlit.io
- **Plotly Docs:** https://plotly.com/python
- **Project README:** ../README.md
- **Architecture Diagrams:** ../Architecture/

---

## 🎓 Learning Resources

- Streamlit App Development: https://docs.streamlit.io/library/get-started
- RFM Analysis: https://en.wikipedia.org/wiki/RFM_(customer_value)
- Pandas Data Processing: https://pandas.pydata.org/docs

---

## ✅ Checklist for Completion

- [x] Dashboard Overview page implemented
- [x] RFM Analysis page implemented
- [x] Customer Segmentation page implemented
- [x] Sales Analytics page implemented
- [x] Product Performance page implemented
- [x] Data Summary page implemented
- [x] Data processing module created
- [x] Sample data loaded and analyzed
- [x] Requirements.txt configured
- [x] Documentation completed

---

**Team Member 3 - Visualization & Integration**  
*Hackathon Project | January 2026*
