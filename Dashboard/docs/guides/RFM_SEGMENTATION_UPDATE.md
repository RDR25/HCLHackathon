# 📊 RFM Segmentation - Dynamic Calculation Update

## 🎯 Changes Made

### Problem Identified
The `customers_master.csv` contained a pre-defined `RFM_Segment` column, which is not ideal because:
- ❌ Pre-defined segments are static and don't reflect actual RFM calculations
- ❌ Segments should be calculated dynamically based on RFM metrics
- ❌ This doesn't match the actual workflow (Member 2 would calculate segments)

### Solution Implemented
✅ **Dynamic RFM Segmentation** - Removed dependency on pre-defined segments and implemented proper RFM calculation

---

## 📈 How RFM Segmentation Works Now

### 1. **RFM Scores Calculation (1-5 Scale)**

#### Recency (R_Score)
- **Definition:** Days since last purchase
- **Scoring:** Lower recency = Higher score (5 is best, 1 is worst)
- **Logic:** Customers who purchased recently (0-1 days) = Score 5
          Customers who haven't purchased in 5+ days = Score 1

#### Frequency (F_Score)  
- **Definition:** Number of transactions
- **Scoring:** Higher frequency = Higher score (1 is worst, 5 is best)
- **Logic:** Ranked by transaction count in 5 equal bins
           Top 20% of customers by frequency = Score 5

#### Monetary (M_Score)
- **Definition:** Total customer spend (lifetime value)
- **Scoring:** Higher spend = Higher score (1 is worst, 5 is best)
- **Logic:** Ranked by total spend in 5 equal bins
           Top 20% by spend = Score 5

---

## 🏷️ Segment Categories

Based on RFM Score combinations:

| Segment | R_Score | F_Score | M_Score | Description |
|---------|---------|---------|---------|-------------|
| **Champion** | ≥4 | ≥4 | ≥4 | Best customers - Buy frequently, recently, and spend a lot |
| **Loyalist** | ≥3 | ≥3 | ≥3 | Loyal customers - Consistent pattern |
| **At Risk** | ≤2 | ≥3 | Any | Were good customers but haven't purchased recently |
| **New** | ≥4 | ≤2 | ≤2 | Recent customers with low activity |
| **Lost** | ≤2 | ≤2 | Any | Haven't purchased recently with low frequency |
| **Potential** | Else | Else | Else | All other combinations |

---

## �� Segment Distribution (Current Sample Data)

```
Champion    - 42 customers (33.1%) ⭐⭐⭐ [Best]
New         - 26 customers (20.5%) 🆕
Loyalist    - 23 customers (18.1%) 💪
Potential   - 19 customers (15.0%) 📈
Lost        - 16 customers (12.6%) ⚠️
At Risk     - 1 customer  (0.8%)   🚨
```

---

## �� Code Changes

### Modified Functions in `data_processor.py`

#### 1. `get_rfm_analysis()`
- ✅ Calculates Recency, Frequency, Monetary dynamically
- ✅ Computes R_Score, F_Score, M_Score (1-5 scale)
- ✅ Applies `_calculate_segment_row()` for each customer
- ✅ Returns RFM data with calculated segments (no CSV segments used)

#### 2. `_calculate_segment_row(row)`
- ✅ Applies business logic to determine segment
- ✅ Uses RFM scores to classify each customer
- ✅ Handles all score combinations

#### 3. `get_segment_distribution()`
- ✅ Now uses dynamically calculated segments
- ✅ No longer relies on pre-defined CSV values

#### 4. `get_at_risk_customers()`
- ✅ Gets at-risk customers from RFM calculation
- ✅ Sorts by Monetary value

---

## 🚀 Usage

### Example Usage in Dashboard

```python
# Get RFM analysis with dynamic segmentation
rfm_data = processor.get_rfm_analysis()

# Get segment distribution
segments = processor.get_segment_distribution()

# Get at-risk customers
at_risk = processor.get_at_risk_customers()
```

### Output Sample
```
Cust_ID    Recency  Frequency  Monetary  R_Score  F_Score  M_Score  RFM_Segment
CUST_003        0         10   5333.66        5        5        5      Champion
CUST_006        0          4   2108.57        5        4        4      Champion
CUST_007        0          4    916.23        5        4        3      Loyalist
CUST_013        5          3   1511.30        1        3        4      At Risk
```

---

## ✅ Benefits

✓ **Dynamic Calculation** - Segments calculated based on actual data
✓ **Flexibility** - Easy to adjust segment thresholds/rules
✓ **Accuracy** - Reflects true customer value and behavior
✓ **Scalability** - Works with any dataset size
✓ **No CSV Dependencies** - Doesn't rely on pre-defined values
✓ **Member 2 Compatible** - Matches expected analytics output from Member 2

---

## 🎯 Next Steps

1. ✅ Dashboard automatically uses dynamic segmentation
2. ✅ All visualizations reflect calculated segments
3. ⏳ When Member 2 provides their analytics, can compare/validate
4. ⏳ Can adjust segment thresholds based on business requirements

---

## 📝 Notes

- **CSV Column Ignored:** The `RFM_Segment` column in `customers_master.csv` is now ignored
- **Pure Calculation:** All segments are calculated from sales transactions only
- **Consistent Results:** Same calculation logic across all functions
- **Ready for Integration:** Can easily swap in Member 2's calculated segments

---

**Last Updated:** January 18, 2026  
**Version:** 1.1 (Dynamic RFM Segmentation)
