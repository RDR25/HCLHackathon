# 📁 Project Structure - Retail Loyalty Analytics Platform

## Directory Layout

```
Dashboard/
│
├── 📄 app.py                           # Main Streamlit application (KEEP AT ROOT)
├── 📄 requirements.txt                 # Python dependencies
├── 📄 setup.sh                         # Setup script
├── 📄 .gitignore                       # Git ignore file
│
├── 📁 src/                             # Source code
│   ├── app.py                          # Copy of main app (for import)
│   ├── __init__.py                     # Package marker
│   │
│   ├── 📁 core/                        # Core business logic
│   │   ├── __init__.py
│   │   ├── data_processor.py           # RFM analysis & data loading
│   │   └── loyalty_engine.py           # Loyalty points & tier management
│   │
│   ├── 📁 engines/                     # Advanced engines
│   │   ├── __init__.py
│   │   └── dynamic_rules_engine.py     # Dynamic business rules (8 rules)
│   │
│   └── 📁 utils/                       # Utility functions
│       ├── __init__.py
│       └── helpers.py                  # Common functions
│
├── 📁 config/                          # Configuration files
│   ├── settings.py                     # App settings
│   ├── constants.py                    # Global constants
│   └── logging.yaml                    # Logging configuration
│
├── 📁 data/                            # Data management
│   ├── 📁 input/                       # Input data (read-only)
│   │   ├── customers_master.csv
│   │   ├── products_master.csv
│   │   ├── sales_header.csv
│   │   ├── sales_line_items.csv
│   │   ├── stores_master.csv
│   │   ├── loyalty_rules_master.csv
│   │   └── promo_effectiveness_metrics.csv
│   │
│   └── 📁 output/                      # Generated output data
│       ├── products_master_dynamic.csv
│       ├── customer_recommendations_dynamic.csv
│       ├── dashboard_suggestions_dynamic.csv
│       ├── customer_loyalty_balances.csv
│       ├── points_transaction_history.csv
│       └── rfm_analysis_results.csv
│
├── 📁 docs/                            # Documentation
│   ├── README_ROOT.md                  # Root documentation
│   ├── README_DASHBOARD.md             # Dashboard guide
│   ├── INDEX.md                        # Documentation index
│   ├── QUICKSTART.md                   # Quick start guide
│   ├── DEPLOYMENT_COMPLETE.md          # Deployment notes
│   ├── PROJECT_COMPLETION.md           # Project summary
│   │
│   ├── 📁 guides/                      # Detailed guides
│   │   ├── DYNAMIC_RULES_DOCUMENTATION.md    # Rules engine specs
│   │   ├── IMPLEMENTATION_SUMMARY.md         # Architecture details
│   │   ├── EXECUTION_COMPLETE.md             # Delivery checklist
│   │   ├── README_DYNAMIC_RULES.md           # Quick reference
│   │   ├── LOYALTY_IMPLEMENTATION.md         # Loyalty system
│   │   └── RFM_SEGMENTATION_UPDATE.md        # RFM details
│   │
│   ├── 📁 specs/                       # Technical specifications
│   │   ├── api_specs.md
│   │   ├── data_schema.md
│   │   └── business_rules.md
│   │
│   └── 📁 api/                         # API documentation
│       └── endpoints.md
│
├── 📁 tests/                           # Test files
│   ├── __init__.py
│   ├── test_data_processor.py
│   ├── test_loyalty_engine.py
│   └── test_dynamic_rules.py
│
├── 📁 scripts/                         # Utility scripts
│   ├── run_engine.sh                   # Run dynamic rules
│   ├── generate_reports.sh             # Generate reports
│   └── backup_data.sh                  # Backup script
│
├── 📁 logs/                            # Application logs
│   ├── app.log
│   ├── errors.log
│   └── performance.log
│
└── 📁 __pycache__/                     # Python cache (auto-generated)
```

---

## File Purpose Reference

### 🎯 Root Level Files

| File | Purpose |
|------|---------|
| `app.py` | **Main Streamlit app - DO NOT MOVE** |
| `requirements.txt` | Python package dependencies |
| `setup.sh` | Initial setup script |

### 💻 Source Code (`src/`)

#### Core (`src/core/`)
- **data_processor.py** - RFM analysis, customer segmentation, data loading
- **loyalty_engine.py** - Points earning, redemption, tier management

#### Engines (`src/engines/`)
- **dynamic_rules_engine.py** - 8 business rules, auto-discounts, recommendations

#### Utils (`src/utils/`)
- **helpers.py** - Common utility functions

### 📊 Data (`data/`)

#### Input (`data/input/`)
- Master data files (read-only)
- CSV files loaded at startup
- Original customer/product/sales data

#### Output (`data/output/`)
- Generated CSV files from analysis
- Dynamic products with discounts
- Customer recommendations
- Dashboard suggestions

### 📚 Documentation (`docs/`)

#### Main Docs
- **README_ROOT.md** - Main project overview
- **README_DASHBOARD.md** - Dashboard user guide
- **INDEX.md** - Documentation index
- **QUICKSTART.md** - Get started in 5 minutes

#### Guides (`docs/guides/`)
- **DYNAMIC_RULES_DOCUMENTATION.md** - Complete rule specifications
- **IMPLEMENTATION_SUMMARY.md** - Technical architecture
- **EXECUTION_COMPLETE.md** - Delivery checklist
- **README_DYNAMIC_RULES.md** - Quick reference guide
- **LOYALTY_IMPLEMENTATION.md** - Loyalty system details
- **RFM_SEGMENTATION_UPDATE.md** - RFM algorithm details

#### Specifications (`docs/specs/`)
- **api_specs.md** - API endpoints
- **data_schema.md** - Database schema
- **business_rules.md** - Business logic

### ✅ Tests (`tests/`)
- Unit tests for each module
- Integration tests
- Data validation tests

### 🔧 Scripts (`scripts/`)
- **run_engine.sh** - Execute dynamic rules
- **generate_reports.sh** - Create reports
- **backup_data.sh** - Data backup

### 📝 Logs (`logs/`)
- **app.log** - General application logs
- **errors.log** - Error logs only
- **performance.log** - Performance metrics

---

## How to Use This Structure

### Running the Dashboard
```bash
cd /Users/ravuladimplerajeeswar/Desktop/HCLHackathon/Dashboard
streamlit run app.py
```

### Running the Dynamic Rules Engine
```bash
python3 << 'EOF'
from src.engines.dynamic_rules_engine import DynamicRulesEngine

engine = DynamicRulesEngine(data_path="data/input")
engine.load_data()
engine.update_all_dynamic_rules()
EOF
```

### Accessing Data Files
```python
# Input data
import pandas as pd
products = pd.read_csv('data/input/products_master.csv')

# Output data
recommendations = pd.read_csv('data/output/customer_recommendations_dynamic.csv')
```

### Reading Documentation
1. Start with: `docs/QUICKSTART.md` (5-min overview)
2. Then: `docs/README_DASHBOARD.md` (dashboard guide)
3. For details: `docs/guides/DYNAMIC_RULES_DOCUMENTATION.md`

---

## Import Paths

When importing modules in your code:

```python
# Core modules
from src.core.data_processor import DataProcessor
from src.core.loyalty_engine import LoyaltyPointsEngine

# Engines
from src.engines.dynamic_rules_engine import DynamicRulesEngine

# Utils
from src.utils.helpers import helper_function
```

---

## Data Flow

```
data/input/
  (CSV files)
    │
    ▼
src/core/data_processor.py
  (Load & process)
    │
    ▼
src/core/loyalty_engine.py
  (Calculate points)
    │
    ▼
src/engines/dynamic_rules_engine.py
  (Apply business rules)
    │
    ▼
data/output/
  (Generated CSVs)
    │
    ▼
app.py (Streamlit)
  (Visualize)
```

---

## Key Features by Directory

### 🎯 `src/core/`
- ✅ RFM segmentation (6 segments)
- ✅ Loyalty tier calculation (Bronze/Silver/Gold/Platinum)
- ✅ Points earning logic
- ✅ Data aggregation

### ⚡ `src/engines/`
- ✅ Category multipliers (7 categories, 1.0x-2.0x)
- ✅ Low-selling product detection (13 products)
- ✅ Inactive customer detection (30+ days)
- ✅ Special date promotions (5 holidays)
- ✅ Dynamic discount application
- ✅ RFM-based retention strategies
- ✅ Customer recommendations (127 customers)
- ✅ Dashboard suggestions (7 real-time alerts)

### 📊 `data/input/`
- 50 products
- 127 customers
- 1,170 transactions
- 3 stores
- 15 promotion metrics

### 📈 `data/output/`
- Products with discounts
- Customer recommendations
- Dashboard suggestions
- Loyalty balances
- Transaction history

### 📚 `docs/`
- Complete technical documentation
- Business logic explanations
- Implementation guides
- API specifications
- Quick start guides

---

## Maintenance Notes

- **Do NOT move** `app.py` from root (Streamlit requires it there)
- **Update** `requirements.txt` when adding dependencies
- **Keep** `data/input/` files read-only (original data)
- **Clear** `logs/` periodically to manage disk space
- **Backup** `data/output/` regularly for safety

---

## Version Info
- **Created**: January 18, 2026
- **Version**: 1.0
- **Status**: Production Ready ✅
