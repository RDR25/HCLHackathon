# 📊 Streamlit Dashboard - Retail Loyalty Analytics Platform

## 🎯 Overview

This folder contains the complete Streamlit Dashboard for the **Retail Loyalty Analytics Platform**, developed by **Team Member 3** (Visualization & Integration).

---

## 📁 Folder Structure

```
Dashboard/
├── 📄 app.py                      ← Main Streamlit application (run this!)
├── 📄 data_processor.py           ← Data processing & analytics module
├── 📄 requirements.txt            ← Python dependencies
│
├── 📚 Documentation/
│   ├── INDEX.md                   ← Complete navigation guide
│   ├── README_DASHBOARD.md        ← Technical documentation
│   ├── QUICKSTART.md              ← Quick start guide (5 mins)
│   └── DEPLOYMENT_COMPLETE.md     ← Project status & summary
│
├── 📊 SampleData/
│   ├── customers_master.csv       ← Customer data (200 records)
│   ├── products_master.csv        ← Product catalog (50 items)
│   ├── stores_master.csv          ← Store locations (5 stores)
│   ├── sales_header.csv           ← Transaction headers (385 records)
│   ├── sales_line_items.csv       ← Line items (1,170 records)
│   └── loyalty_rules_master.csv   ← Loyalty point rules (3 rules)
│
└── 🔧 Utilities/
    └── setup.sh                   ← Automated setup script
```

---

## 🚀 Quick Start (3 Steps)

### 1️⃣ Install Dependencies
```bash
cd /Users/ravuladimplerajeeswar/Desktop/HCLHackathon/Dashboard
pip install -r requirements.txt
```

### 2️⃣ Launch Dashboard
```bash
streamlit run app.py
```

### 3️⃣ Open Browser
Navigate to: **http://localhost:8501**

---

## 📊 Dashboard Features (6 Pages)

| Page | Purpose | Key Metrics |
|------|---------|------------|
| **Overview** | Executive dashboard | KPIs, trends, top customers |
| **RFM Analysis** | Customer value positioning | Recency, Frequency, Monetary |
| **Segmentation** | Retention focus | At-risk detection, segment comparison |
| **Sales Analytics** | Revenue analysis | Store/category performance, trends |
| **Product Performance** | SKU insights | Top products, category distribution |
| **Data Summary** | Data quality | Master data, quality metrics |

---

## 📈 Data Summary

- **Total Customers:** 200
- **Total Transactions:** 385
- **Total Revenue:** $185,713.84
- **Loyalty Points:** 239,447
- **At-Risk Customers:** 70 (35%)

---

## 🛠️ Technical Stack

- **Framework:** Streamlit 1.53.0
- **Data Processing:** Pandas 2.3.3
- **Visualization:** Plotly 6.5.2
- **Numerical:** NumPy 2.4.1
- **Machine Learning:** Scikit-learn 1.8.0

---

## 📚 Documentation Files

### Quick References:
- **QUICKSTART.md** - 5-minute setup guide
- **INDEX.md** - Complete navigation index

### Detailed Guides:
- **README_DASHBOARD.md** - Technical documentation
- **DEPLOYMENT_COMPLETE.md** - Project status & insights

---

## 🔄 Integration Ready

### For Real Data:
1. Update data source path in `data_processor.py` (line 9)
2. Or replace CSV files in `SampleData/` folder
3. Dashboard automatically uses new data

### No Code Changes Needed in `app.py`!

---

## 💡 Key Features

✅ 6 interactive pages  
✅ 15+ visualizations (Plotly charts)  
✅ RFM analysis implementation  
✅ Customer segmentation  
✅ Data quality reporting  
✅ Performance optimization (caching)  
✅ Professional UI/UX  
✅ Production-ready code  

---

## 🐛 Troubleshooting

| Issue | Solution |
|-------|----------|
| Streamlit not found | `pip install streamlit` |
| CSV files not found | Ensure `SampleData/` folder exists |
| Port 8501 in use | `streamlit run app.py --server.port 8502` |
| Dashboard loads slowly | Restart: `Ctrl+C` then run again |

---

## 📞 Support

- **Quick Questions?** → Read QUICKSTART.md
- **Setup Issues?** → Check requirements.txt
- **Technical Details?** → See README_DASHBOARD.md
- **Project Status?** → Check DEPLOYMENT_COMPLETE.md

---

## ✅ Checklist

- [x] App created and tested
- [x] Data processing module working
- [x] 6 pages with visualizations
- [x] Sample data included
- [x] Dependencies configured
- [x] Documentation complete
- [x] Ready for integration
- [x] Ready for production

---

## 🎓 Next Steps

1. ✅ Run `streamlit run app.py`
2. ✅ Explore all 6 pages
3. ✅ Review data summary
4. ⏳ Wait for Members 1 & 2 data
5. ⏳ Integrate real data sources
6. 🚀 Deploy to production

---

**Team Member 3 - Visualization & Integration**  
*Hackathon Project | January 18, 2026 | Version 1.0*
