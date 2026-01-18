#!/bin/bash
# Retail Loyalty Analytics - Dashboard Setup Script

echo "🎯 Retail Loyalty Analytics Platform - Dashboard Setup"
echo "========================================================"
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3 is not installed. Please install Python 3.8+"
    exit 1
fi

echo "✅ Python3 found: $(python3 --version)"
echo ""

# Navigate to project directory
PROJECT_DIR="/Users/ravuladimplerajeeswar/Desktop/HCLHackathon"
cd "$PROJECT_DIR" || exit 1
echo "✅ Working directory: $PROJECT_DIR"
echo ""

# Check if SampleData exists
if [ ! -d "SampleData" ]; then
    echo "❌ SampleData folder not found!"
    exit 1
fi

CSV_COUNT=$(ls SampleData/*.csv 2>/dev/null | wc -l)
echo "✅ SampleData folder found with $CSV_COUNT CSV files:"
ls -1 SampleData/*.csv | sed 's/^/   /'
echo ""

# Install/upgrade pip
echo "📦 Upgrading pip..."
python3 -m pip install --upgrade pip > /dev/null 2>&1

# Install dependencies
echo "📦 Installing dependencies from requirements.txt..."
if python3 -m pip install -r requirements.txt > /dev/null 2>&1; then
    echo "✅ All dependencies installed successfully"
else
    echo "⚠️  Some dependencies may have issues, but continuing..."
fi
echo ""

# Verify imports
echo "🔍 Verifying package imports..."
python3 << 'EOF'
try:
    import streamlit
    print("✅ streamlit imported successfully")
    import pandas
    print("✅ pandas imported successfully")
    import plotly
    print("✅ plotly imported successfully")
    import numpy
    print("✅ numpy imported successfully")
except ImportError as e:
    print(f"❌ Import error: {e}")
    exit(1)
EOF
echo ""

# Test data loading
echo "🧪 Testing data loading..."
python3 << 'EOF'
try:
    from data_processor import DataProcessor
    dp = DataProcessor()
    if dp.load_all_data():
        print(f"✅ Data loaded successfully")
        print(f"   - Customers: {len(dp.customers_df)}")
        print(f"   - Products: {len(dp.products_df)}")
        print(f"   - Sales: {len(dp.sales_header_df)}")
        print(f"   - Line Items: {len(dp.sales_line_items_df)}")
    else:
        print("❌ Failed to load data")
        exit(1)
except Exception as e:
    print(f"❌ Error: {e}")
    exit(1)
EOF
echo ""

# Ready to launch
echo "=================================================="
echo "✅ SETUP COMPLETE - READY TO LAUNCH!"
echo "=================================================="
echo ""
echo "🚀 To start the dashboard, run:"
echo ""
echo "   streamlit run app.py"
echo ""
echo "📱 Then open your browser to:"
echo "   http://localhost:8501"
echo ""
echo "📊 Available Pages:"
echo "   1. Dashboard Overview - KPIs and trends"
echo "   2. RFM Analysis - Customer value"
echo "   3. Customer Segmentation - Retention focus"
echo "   4. Sales Analytics - Revenue analysis"
echo "   5. Product Performance - SKU insights"
echo "   6. Data Summary - Data quality"
echo ""
echo "📚 Documentation:"
echo "   - INDEX.md - Complete project index"
echo "   - QUICKSTART.md - Quick reference"
echo "   - README_DASHBOARD.md - Full guide"
echo "   - DEPLOYMENT_COMPLETE.md - Status summary"
echo ""
echo "🛑 To stop the dashboard, press Ctrl+C"
echo ""
