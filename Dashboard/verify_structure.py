#!/usr/bin/env python3
"""
Project Structure Verification Script
Confirms all files are properly organized after restructuring
"""

import os
import sys
from pathlib import Path

def check_structure():
    """Verify project structure"""
    project_root = Path(__file__).parent
    
    print("=" * 60)
    print("PROJECT STRUCTURE VERIFICATION")
    print("=" * 60)
    
    checks = {
        "✓ Core": [
            ("app.py", True),
            ("src/core/data_processor.py", True),
            ("src/core/loyalty_engine.py", True),
            ("src/engines/dynamic_rules_engine.py", True),
        ],
        "✓ Data": [
            ("data/input/customers_master.csv", True),
            ("data/input/products_master.csv", True),
            ("data/input/sales_header.csv", True),
            ("data/output/products_master_dynamic.csv", True),
            ("data/output/customer_recommendations_dynamic.csv", True),
            ("data/output/dashboard_suggestions_dynamic.csv", True),
        ],
        "✓ Documentation": [
            ("START_HERE.md", True),
            ("PROJECT_STRUCTURE.md", True),
            ("docs/README_DASHBOARD.md", False),
            ("docs/guides/DYNAMIC_RULES_DOCUMENTATION.md", False),
        ],
        "✓ Infrastructure": [
            ("src/__init__.py", True),
            ("src/core/__init__.py", True),
            ("src/engines/__init__.py", True),
            ("config/__init__.py", True),
            ("tests/__init__.py", True),
        ],
    }
    
    all_good = True
    for section, files in checks.items():
        print(f"\n{section}")
        print("-" * 40)
        
        for file_path, required in files:
            full_path = project_root / file_path
            exists = full_path.exists()
            status = "✓" if exists else "✗"
            req_indicator = "[REQUIRED]" if required else "[OPTIONAL]"
            
            print(f"  {status} {file_path:45} {req_indicator}")
            
            if required and not exists:
                all_good = False
    
    print("\n" + "=" * 60)
    
    # Test imports
    print("\nTESTING IMPORTS")
    print("-" * 40)
    
    try:
        sys.path.insert(0, str(project_root / "src/core"))
        sys.path.insert(0, str(project_root / "src/engines"))
        
        from data_processor import DataProcessor
        print("  ✓ data_processor imports successfully")
        
        from loyalty_engine import LoyaltyPointsEngine
        print("  ✓ loyalty_engine imports successfully")
        
        from dynamic_rules_engine import DynamicRulesEngine
        print("  ✓ dynamic_rules_engine imports successfully")
        
    except ImportError as e:
        print(f"  ✗ Import error: {e}")
        all_good = False
    
    print("\n" + "=" * 60)
    
    # Summary
    if all_good:
        print("\n✓ PROJECT STRUCTURE VERIFIED SUCCESSFULLY!")
        print("\nNext steps:")
        print("  1. Run: streamlit run app.py")
        print("  2. Dashboard will open at http://localhost:8501")
        print("  3. Review START_HERE.md for navigation guide")
    else:
        print("\n✗ SOME REQUIRED FILES ARE MISSING")
        print("Please review the structure above and address any issues.")
    
    print("\n" + "=" * 60)
    
    return all_good

if __name__ == "__main__":
    success = check_structure()
    sys.exit(0 if success else 1)
