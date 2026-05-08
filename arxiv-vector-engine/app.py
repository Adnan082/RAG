import os
import sys

print("[OK] STEP 1: Python is alive!")
print(f"Current Directory: {os.getcwd()}")
print(f"Python Version: {sys.version}")

try:
    import pandas
    print("[OK] STEP 2: Pandas is installed!")
except Exception as e:
    print(f"[MISSING] STEP 2: Pandas NOT FOUND! ({type(e).__name__}: {e})")

try:
    import chromadb
    print("[OK] STEP 3: ChromaDB is installed!")
except ImportError:
    print("[MISSING] STEP 3: ChromaDB NOT FOUND!")

print("[DONE] End of Pulse Test.")