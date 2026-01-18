# 🚀 Getting Started - Quick Start Guide

Welcome to the **Retail Loyalty Analytics Platform**! This guide will help you get the dashboard up and running in minutes.

---

## 📋 Prerequisites

Before you start, ensure you have:
- **Python 3.8 or higher** (tested with Python 3.13.4)
- **pip** (Python package manager)
- **Git** (for version control)
- **Mac/Linux/Windows** with terminal access

### Verify Python Installation
```bash
python3 --version
pip --version
```

---

## 📦 Installation Steps

### Step 1: Clone the Repository
```bash
git clone https://github.com/RDR25/HCLHackathon.git
cd HCLHackathon
```

### Step 2: Create a Virtual Environment (Optional but Recommended)
```bash
python3 -m venv venv
source venv/bin/activate  # On macOS/Linux
# or
venv\Scripts\activate  # On Windows
```

### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

If `requirements.txt` is not available, install the key packages:
```bash
pip install streamlit==1.53.0
pip install pandas==2.3.3
pip install plotly==6.5.2
pip install numpy==2.4.1
```

### Step 4: Verify Project Structure
```bash
python verify_structure.py
```

Expected output:
```
✅ All checks PASSED
✓ Structure Check:      PASSED
✓ Import Check:         PASSED
✓ Data Loading Check:   PASSED
✓ RFM Analysis Check:   PASSED
```

---

## 🎯 Running the Dashboard

### Quick Start Command
```bash
cd Dashboard
streamlit run app.py
```

### What You Should See
```
  You can now view your Streamlit app in your browser.
  
  Local URL: http://localhost:8501
  Network URL: http://172.x.x.x:8501
```

### Access the Dashboard
Open your browser and go to: **http://localhost:8501**

---

## 📊 Dashboard Features

The dashboard includes 7 pages (accessible via the left sidebar):

### 1. **Dashboard Overview** 📈
   - Key Performance Indicators (KPIs)
   - Sales trend visualization
   - Quick business metrics

### 2. **RFM Analysis** 📊
   - Recency, Frequency, Monetary analysis
   - Customer segment scatter plot
   - RFM segment distribution

### 3. **Customer Segmentation** 👥
   - Customer breakdown by segment
   - Segment characteristics
   - Customer counts

### 4. **Sales Analytics** 💹
   - Sales trends over time
   - Performance by store
   - Performance by product category

### 5. **Product Performance** 📦
   - Top-performing products
   - Product sales analysis
   - Category insights

### 6. **Admin Panel** ⚙️
   - **Tab 1:** Add bonus points to least-sold products
   - **Tab 2:** Add loyalty points to least-active customers
   - **Tab 3:** Configure special day promotions with category-specific discounts
   - **Tab 4:** Set promotional rates and discount configurations
   - **Recommendations:** Generate personalized customer recommendations with discounts

### 7. **Data Summary** 📋
   - Raw data exploration
   - Dataset overview
   - Sample records

---

## 🔧 Admin Panel Features

### Managing Least Sold Products
1. Go to **Admin Panel** → **Least Sold Products**
2. View the 10 least-selling products
3. Enter bonus points (0-1000) for each product
4. Click **Save Bonus Points to CSV**
5. File saved: `data/output/product_bonus_points.csv`

### Managing Least Active Customers
1. Go to **Admin Panel** → **Least Active Customers**
2. View 15 customers with lowest recent activity
3. Enter loyalty points (0-5000) for each
4. Click **Save Loyalty Points to CSV**
5. File saved: `data/output/customer_bonus_loyalty_points.csv`

### Setting Up Special Day Promotions
1. Go to **Admin Panel** → **Special Day Promotions**
2. Select a special day from dropdown (14 options available)
3. Choose a product category
4. Set discount percentage (0-100%)
5. Click **Save Promotion to CSV**
6. File saved: `data/output/special_day_promotions.csv`

### Configuring Promotional Rates
1. Go to **Admin Panel** → **Promotional Rates**
2. Enter base rates:
   - Base Points per Dollar
   - Bonus Multiplier
   - Standard Discount %
   - VIP Discount %
3. Click **Save Configuration to CSV**
4. File saved: `data/output/promotional_rates_config.csv`

### Generating Personalized Recommendations
1. Go to **Admin Panel** → **Recommendations**
2. Click **Generate Recommendations**
3. View personalized suggestions with:
   - Customer ID
   - Segment (Champions, Loyal, At-Risk, Others)
   - Product recommendations
   - Discount percentages
4. Click **Download Recommendations as CSV**
5. File saved: `data/output/personalized_recommendations_with_discounts.csv`

---

## 📂 Project Structure

```
HCLHackathon/
├── README.md                 # Project documentation
├── START_HERE.md            # This file
├── verify_structure.py      # Verification script
├── Dashboard/
│   ├── app.py              # Main Streamlit dashboard
│   └── app_backup_old.py   # Backup of previous version
├── src/
│   ├── core/
│   │   ├── data_processor.py       # RFM analysis & data loading
│   │   ├── loyalty_engine.py       # Loyalty calculations
│   │   └── __init__.py
│   ├── engines/
│   │   ├── dynamic_rules_engine.py # Business rules
│   │   └── __init__.py
│   └── __init__.py
├── data/
│   ├── input/              # Master data files (12 CSVs)
│   └── output/             # Generated outputs
├── config/                 # Configuration files
├── tests/                  # Test files
├── docs/                   # Additional documentation
└── logs/                   # Application logs
```

---

## 🧪 Testing & Verification

### Verify All Imports
```bash
python -c "from src.core.data_processor import DataProcessor; print('✓ DataProcessor imported')"
python -c "from src.core.loyalty_engine import LoyaltyPointsEngine; print('✓ LoyaltyPointsEngine imported')"
python -c "from src.engines.dynamic_rules_engine import DynamicRulesEngine; print('✓ DynamicRulesEngine imported')"
```

### Run Data Loading Test
```bash
python -c "
from src.core.data_processor import DataProcessor
dp = DataProcessor()
dp.load_all_data()
print('✓ Data loaded successfully')
print(f'  - Customers: {len(dp.customers)}')
print(f'  - Products: {len(dp.products)}')
print(f'  - Transactions: {len(dp.sales)}')
"
```

---

## 🆘 Troubleshooting

### Issue: "ModuleNotFoundError: No module named 'streamlit'"
**Solution:**
```bash
pip install streamlit
```

### Issue: "FileNotFoundError: data/input/..."
**Solution:** Ensure you're in the correct directory:
```bash
cd /Users/ravuladimplerajeeswar/Desktop/HCLHackathon
# Then run: streamlit run Dashboard/app.py
```

### Issue: Port 8501 already in use
**Solution:**
```bash
# Kill existing Streamlit process
pkill -f streamlit

# Or run on a different port
streamlit run Dashboard/app.py --server.port 8502
```

### Issue: Warnings about `use_container_width`
**Solution:** These are deprecation warnings and don't affect functionality. They'll be fixed in future updates.

---

## 📊 Data Files

### Input Data (in `data/input/`)
- `customers_master.csv` – Customer information
- `products_master.csv` – Product catalog
- `sales_transactions.csv` – Transaction records
- And 9 other supporting files

### Output Data (generated in `data/output/`)
- `products_master_dynamic.csv`
- `customer_recommendations_dynamic.csv`
- `dashboard_suggestions_dynamic.csv`
- `product_bonus_points.csv` (from Admin Panel)
- `customer_bonus_loyalty_points.csv` (from Admin Panel)
- `special_day_promotions.csv` (from Admin Panel)
- `promotional_rates_config.csv` (from Admin Panel)
- `personalized_recommendations_with_discounts.csv` (from Admin Panel)

---

## 📞 Support & Resources

- **GitHub Repository:** https://github.com/RDR25/HCLHackathon
- **Project Documentation:** See `README.md`
- **Architecture Diagrams:** Check `Architecture/` folder
- **Dashboard Code:** See `Dashboard/app.py`

---

## ✅ Next Steps

1. ✅ Install dependencies
2. ✅ Run verification script
3. ✅ Start the dashboard
4. ✅ Explore all 7 pages
5. ✅ Try the Admin Panel features
6. ✅ Generate configurations and recommendations

---

## 🎉 Ready to Go!

Your dashboard is now fully operational. Start exploring customer insights, managing loyalty programs, and generating targeted recommendations!

**Questions?** Check the documentation or review the code in the `Dashboard/app.py` and `src/` folders.

Happy analyzing! 📊✨
