import pyvisa
import time

rm = pyvisa.ResourceManager()

print("Scanning for instruments (Press Ctrl+C to stop)...")
print("-" * 60)

while True:
    try:
        resources = rm.list_resources()
        print(f"[{time.strftime('%H:%M:%S')}] Found {len(resources)} instruments:")
        for res in resources:
            if "0x0699" in res:
                print(f"  -> TEKTRONIX SCOPE FOUND: {res} <--- COMMAND SHOULD WORK NOW")
            else:
                print(f"  - {res}")
        print("-" * 60)
    except Exception as e:
        print(f"Error scanning: {e}")
    
    time.sleep(2)
