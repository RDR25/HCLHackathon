# Retail Loyalty Analytics Platform (Hackathon MVP)

## 🚀 Quick Start

**New to this project?** Start here:

### Installation & Setup (2 minutes)
```bash
# Clone the repository
git clone https://github.com/RDR25/HCLHackathon.git
cd HCLHackathon

# Install dependencies
pip install -r requirements.txt

# Verify installation
python verify_structure.py
```

### Run the Dashboard (1 minute)
```bash
cd Dashboard
streamlit run app.py
```

Then open your browser to: **http://localhost:8501**

### Key Features
- ✅ **7-Page Dashboard** with KPIs, RFM Analysis, Customer Segmentation, Sales Analytics, Product Performance
- ✅ **Admin Panel** for managing bonuses, loyalty points, promotions, and generating recommendations
- ✅ **CSV Export** for all configurations and recommendations
- ✅ **Interactive Visualizations** with Plotly
- ✅ **Data Validation** and quality checks

**For detailed instructions, see [START_HERE.md](START_HERE.md)**

---

##  Project Overview
The **Retail Loyalty Analytics Platform** is an end-to-end data engineering and analytics solution designed to help retailers analyze customer behavior, calculate loyalty points, and segment customers using RFM (Recency, Frequency, Monetary) analysis.  

The platform ingests raw retail transaction data, applies data quality validations, computes loyalty metrics, identifies high-value and at-risk customers, and presents insights through analytics-ready data marts and dashboards.

---

##  Business Use Case
Retailers deal with large volumes of transactional data across stores and channels. This project enables retailers to:
- Automate ingestion and validation of sales data
- Calculate loyalty points accurately
- Segment customers for targeted promotions
- Identify high spenders and at-risk customers
- Drive data-driven marketing and retention strategies

---

##  High-Level Architecture
**Data Flow:**

Source Data (CSV / GenAI)  
→ Data Ingestion Layer  
→ Landing (Raw) Tables  
→ Data Quality Engine  
→ Clean Tables + Reject Tables  
→ Loyalty Points Engine  
→ RFM Engine  
→ Segmentation Engine  
→ Analytics Data Marts  
→ Dashboard / Visualization Layer

---

##  Key Components

### 1. Data Ingestion Layer
- Loads CSV or GenAI-generated datasets
- Uses Python-based ETL scripts
- No transformations applied at this stage

### 2. Landing (Raw) Tables
- Stores unprocessed source data
- Acts as an audit and recovery layer

### 3. Data Quality Engine
Applies validation rules such as:
- Null checks
- Duplicate record checks
- Foreign key/reference validation
- Invalid or negative value detection

Outputs:
- **Clean Tables** – validated data
- **Reject/Error Tables** – failed records

### 4. Loyalty Points Engine
- Calculates loyalty points per transaction
- Applies promotional or bonus rules
- Updates total loyalty balance and last purchase date

### 5. RFM Engine
Calculates:
- **Recency** – Days since last purchase
- **Frequency** – Number of transactions
- **Monetary** – Total customer spend

### 6. Segmentation Engine
Customer segments include:
- **High Spenders** – Top 10% customers by monetary value
- **At Risk** – No purchase in last 30+ days with existing loyalty points
- **Others** – Remaining customers

### 7. Analytics Data Marts
- Aggregated and reporting-optimized tables
- Supports dashboards and business insights

### 8. Dashboard & Visualization
- Built using Power BI / Tableau / Streamlit
- Displays loyalty trends, RFM segments, and sales insights

---

##  Technology Stack
- **Language:** Python
- **Database:** PostgreSQL / Snowflake / MySQL
- **ETL:** Python (Pandas)
- **Visualization:** Power BI / Tableau / Streamlit
- **Version Control:** Git & GitHub

---

##  Team Task Breakdown (3-Member Team)

To ensure parallel development and timely delivery of the MVP, tasks were divided across team members based on system layers and responsibilities.

###  Team Member 1 – Data Engineering & Ingestion
**Responsibilities:**
- Design source data formats (Customers, Products, Promotions, Sales)
- Implement CSV / GenAI data ingestion using Python
- Create Landing (Raw) tables in the database
- Ensure schema consistency and data loading reliability

**Key Deliverables:**
- Ingestion scripts
- Raw data tables
- Sample datasets
- Documentation for data sources

---

###  Team Member 2 – Data Quality, Business Logic & Analytics
**Responsibilities:**
- Implement Data Quality Engine (null checks, duplicates, FK validation)
- Build Loyalty Points Engine
- Implement RFM (Recency, Frequency, Monetary) calculations
- Develop customer segmentation logic (High Spenders, At-Risk, Others)
- Create clean tables and analytics-ready data marts

**Key Deliverables:**
- Data validation scripts
- Loyalty and RFM calculation modules
- Segmentation logic
- Aggregated data mart tables

---

###  Team Member 3 – Visualization, Integration & Documentation
**Responsibilities:**
- Design and build dashboards (Power BI / Tableau / Streamlit)
- Integrate dashboards with analytics data marts
- Create architecture and ER diagrams
- Maintain README and project documentation
- Coordinate GitHub version control and final integration

**Key Deliverables:**
- Interactive dashboards
- Architecture & ER diagrams
- GitHub repository management
- Final documentation and demo preparation

---

##  Collaboration Model
- GitHub used for version control and collaboration
- Feature-based branching strategy
- Regular integration and testing
- Clear ownership with cross-review of code and outputs

---

## ⚙️ Installation & Startup Guide

### Prerequisites
- **Python 3.8+** (tested with 3.13.4)
- **pip** package manager
- **Git** version control

### Quick Setup (5 minutes)

#### Step 1: Clone Repository
```bash
git clone https://github.com/RDR25/HCLHackathon.git
cd HCLHackathon
```

#### Step 2: Create Virtual Environment (Recommended)
```bash
python3 -m venv venv
source venv/bin/activate  # macOS/Linux
# or
venv\Scripts\activate  # Windows
```

#### Step 3: Install Dependencies
```bash
pip install streamlit==1.53.0 pandas==2.3.3 plotly==6.5.2 numpy==2.4.1
```

Or use requirements.txt if available:
```bash
pip install -r requirements.txt
```

#### Step 4: Verify Installation
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

### Running the Dashboard

#### Start Command
```bash
cd Dashboard
streamlit run app.py
```

#### Access the Dashboard
Open your browser and navigate to: **http://localhost:8501**

You should see:
```
Local URL: http://localhost:8501
Network URL: http://172.x.x.x:8501
```

### Dashboard Overview (7 Pages)

**Page 1: Dashboard Overview**
- KPI metrics (Total Sales, Customers, Products)
- Sales trend visualization
- Quick business insights

**Page 2: RFM Analysis**
- Recency vs Frequency vs Monetary scatter plot
- Customer segment distribution
- RFM metrics summary

**Page 3: Customer Segmentation**
- Customer breakdown by segment (Champions, Loyal, At-Risk, Others)
- Segment characteristics
- Customer counts per segment

**Page 4: Sales Analytics**
- Sales trends over time
- Performance by store location
- Performance by product category

**Page 5: Product Performance**
- Top-selling products
- Sales by product category
- Product revenue analysis

**Page 6: Admin Panel** ⭐ *New Features*
- **Tab 1: Least Sold Products** – Add bonus points (0-1000) for each product, save to CSV
- **Tab 2: Least Active Customers** – Add loyalty points (0-5000), save to CSV
- **Tab 3: Special Day Promotions** – Select from 14 special days, choose category, set discount %, save to CSV
- **Tab 4: Promotional Rates** – Configure base points/dollar, multipliers, discount rates, save config
- **Recommendations** – Generate personalized recommendations with customer/product IDs and segment-based discounts

**Page 7: Data Summary**
- Raw data exploration
- Dataset overview
- Sample records

### CSV Exports from Admin Panel
The following files are generated when you save configurations:

1. `data/output/product_bonus_points.csv` – Bonus points for least-sold products
2. `data/output/customer_bonus_loyalty_points.csv` – Loyalty points for inactive customers
3. `data/output/special_day_promotions.csv` – Special day discount configurations
4. `data/output/promotional_rates_config.csv` – Base promotional rates
5. `data/output/personalized_recommendations_with_discounts.csv` – Personalized recommendations with Customer_ID, Product_ID, Discounts

### Troubleshooting

**Issue: ModuleNotFoundError: No module named 'streamlit'**
```bash
pip install streamlit
```

**Issue: Port 8501 already in use**
```bash
# Kill existing process
pkill -f streamlit

# Or run on different port
streamlit run Dashboard/app.py --server.port 8502
```

**Issue: FileNotFoundError: data/input/...**
Ensure you're in the correct directory:
```bash
cd /Users/ravuladimplerajeeswar/Desktop/HCLHackathon
streamlit run Dashboard/app.py
```

**Issue: Import errors**
Test imports directly:
```bash
python -c "from src.core.data_processor import DataProcessor; print('✓')"
```

### Project Structure
```
HCLHackathon/
├── Dashboard/
│   ├── app.py              # Main Streamlit dashboard (7 pages)
│   └── app_backup_old.py   # Previous version backup
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
│   ├── input/              # 12 master CSV files
│   └── output/             # Generated outputs & CSV exports
├── README.md               # This file
├── START_HERE.md          # Quick start guide
└── verify_structure.py    # Verification script
```

### Key Technologies
- **Framework:** Streamlit 1.53.0
- **Data:** Pandas 2.3.3, NumPy 2.4.1
- **Visualization:** Plotly 6.5.2
- **Language:** Python 3.13.4

### Support & Resources
- **Full Documentation:** [START_HERE.md](START_HERE.md)
- **GitHub:** https://github.com/RDR25/HCLHackathon
- **Architecture Diagrams:** See `Architecture/` folder
- **Dashboard Code:** `Dashboard/app.py`

---

## 🏁 Outcome
This task distribution enabled parallel development across ingestion, processing, and visualization layers, resulting in a fully functional end-to-end Retail Loyalty Analytics MVP within hackathon timelines.

