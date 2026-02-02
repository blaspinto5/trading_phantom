import os
import sys

print("CWD:", os.getcwd())
print("sys.path[0]:", sys.path[0])
print("Listing:", os.listdir())
try:
    import trading_phantom

    print("import trading_phantom OK")
except Exception as e:
    print("Import failed:", e)
    raise
