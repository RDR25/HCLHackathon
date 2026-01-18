# Retail Loyalty Analytics Platform (Hackathon MVP)

## 📌 Project Overview
The **Retail Loyalty Analytics Platform** is an end-to-end data engineering and analytics solution designed to help retailers analyze customer behavior, calculate loyalty points, and segment customers using RFM (Recency, Frequency, Monetary) analysis.  

The platform ingests raw retail transaction data, applies data quality validations, computes loyalty metrics, identifies high-value and at-risk customers, and presents insights through analytics-ready data marts and dashboards.

---

## 🎯 Business Use Case
Retailers deal with large volumes of transactional data across stores and channels. This project enables retailers to:
- Automate ingestion and validation of sales data
- Calculate loyalty points accurately
- Segment customers for targeted promotions
- Identify high spenders and at-risk customers
- Drive data-driven marketing and retention strategies

---

## 🏗️ High-Level Architecture
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

## 🧩 Key Components

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

## 🛠️ Technology Stack
- **Language:** Python
- **Database:** PostgreSQL / Snowflake / MySQL
- **ETL:** Python (Pandas)
- **Visualization:** Power BI / Tableau / Streamlit
- **Version Control:** Git & GitHub

---

## 📂 Project Structure
