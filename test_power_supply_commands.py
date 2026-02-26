"""
Test to verify power supply commands are sent correctly during execution
"""
from instruments.manager import InstrumentManager

print("=" * 60)
print("Testing Power Supply Command Execution")
print("=" * 60)

# Create manager
mgr = InstrumentManager()

print(f"\nSimulation Mode: {mgr.simulation_mode}")

# Test 1: Check if ac_source can be found
print("\n1. Testing mgr.ac_source property...")
try:
    source = mgr.ac_source
    print(f"   [OK] Found source: {source}")
    print(f"   Resource: {source.resource_name}")
    print(f"   Connected: {source.connected}")
except Exception as e:
    print(f"   [ERROR] Failed to get source: {e}")
    exit(1)

# Test 2: Connect to the source
print("\n2. Connecting to power supply...")
try:
    if not source.connected:
        source.connect()
    print(f"   [OK] Connected: {source.connected}")
    print(f"   IDN: {source.query_idn()}")
except Exception as e:
    print(f"   [ERROR] Connection failed: {e}")
    exit(1)

# Test 3: Set voltage
print("\n3. Setting voltage to 48V...")
try:
    source.set_voltage(48.0)
    print("   [OK] Voltage command sent")
except Exception as e:
    print(f"   [ERROR] Failed: {e}")

# Test 4: Set current limit
print("\n4. Setting current limit to 10A...")
try:
    source.set_current_limit(10.0)
    print("   [OK] Current limit command sent")
except Exception as e:
    print(f"   [ERROR] Failed: {e}")

# Test 5: Turn output ON
print("\n5. Turning output ON...")
try:
    source.output_on()
    print("   [OK] Output ON command sent")
    print("\n   >>> CHECK YOUR POWER SUPPLY DISPLAY <<<")
    print("   >>> Output should be ON with 48V, 10A limit <<<")
except Exception as e:
    print(f"   [ERROR] Failed: {e}")

# Wait for user to check
input("\nPress Enter after checking the power supply...")

# Test 6: Turn output OFF
print("\n6. Turning output OFF...")
try:
    source.output_off()
    print("   [OK] Output OFF command sent")
except Exception as e:
    print(f"   [ERROR] Failed: {e}")

# Cleanup
print("\n7. Disconnecting...")
source.disconnect()

print("\n" + "=" * 60)
print("Test Complete")
print("=" * 60)
