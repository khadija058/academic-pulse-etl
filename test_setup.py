import os
import sys
from pathlib import Path

print("🔍 DIAGNOSTIC CHECK")
print("=" * 30)

# Check current directory
print(f"Current directory: {os.getcwd()}")

# Check Python path
print(f"Python path: {sys.path}")

# Check if directories exist
dirs_to_check = [
    "src",
    "src/extract", 
    "src/transform",
    "data",
    "data/raw",
    "data/processed",
    "scripts"
]

print(f"\n📁 Directory Check:")
for dir_name in dirs_to_check:
    exists = "✅" if Path(dir_name).exists() else "❌"
    print(f"  {exists} {dir_name}")

# Check if Python files exist
files_to_check = [
    "src/extract/data_extractor.py",
    "src/transform/data_transformer.py"
]

print(f"\n📄 File Check:")
for file_name in files_to_check:
    exists = "✅" if Path(file_name).exists() else "❌"
    print(f"  {exists} {file_name}")

# Test basic import
print(f"\n🐍 Testing Python imports:")
try:
    import csv
    print("  ✅ csv module")
except ImportError:
    print("  ❌ csv module")

try:
    import json
    print("  ✅ json module")
except ImportError:
    print("  ❌ json module")

try:
    from pathlib import Path
    print("  ✅ pathlib module")
except ImportError:
    print("  ❌ pathlib module")

print(f"\n🚀 Ready to proceed!")
