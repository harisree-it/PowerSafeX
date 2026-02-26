"""
Quick test to verify InstrumentManager maintains persistent connections
"""
from instruments.manager import InstrumentManager

print("=" * 60)
print("Testing InstrumentManager Persistent Connections")
print("=" * 60)

# Create manager instance
mgr = InstrumentManager()

print(f"\nSimulation Mode: {mgr.simulation_mode}")
print(f"Number of instruments configured: {len(mgr.instruments)}")

# Get the Chroma 62000D instance
print("\n1. Getting Chroma 62000D driver instance (first call)...")
driver1 = mgr.get_driver_instance("Chroma 62000D")
print(f"   Driver instance ID: {id(driver1)}")
print(f"   Connected: {driver1.connected}")

# Connect to it
print("\n2. Connecting to Chroma 62000D...")
try:
    driver1.connect()
    print(f"   Connection successful!")
    print(f"   Connected: {driver1.connected}")
    print(f"   IDN: {driver1.query_idn()}")
except Exception as e:
    print(f"   Connection failed: {e}")

# Get the same instance again (should be the SAME object)
print("\n3. Getting Chroma 62000D driver instance (second call)...")
driver2 = mgr.get_driver_instance("Chroma 62000D")
print(f"   Driver instance ID: {id(driver2)}")
print(f"   Connected: {driver2.connected}")

# Verify they are the same object
print("\n4. Verification:")
if driver1 is driver2:
    print("   ✓ SUCCESS: Both calls returned the SAME driver instance")
    print("   ✓ The connection is persistent!")
else:
    print("   ✗ FAIL: Different instances returned")

# Test using the property accessor
print("\n5. Testing property accessor (mgr.ac_source)...")
source1 = mgr.ac_source
print(f"   Source instance ID: {id(source1)}")
print(f"   Connected: {source1.connected}")

source2 = mgr.ac_source
print(f"   Source instance ID (2nd call): {id(source2)}")

if source1 is source2:
    print("   ✓ SUCCESS: Property accessor also returns persistent instance")
else:
    print("   ✗ FAIL: Property accessor creates new instances")

print("\n" + "=" * 60)
print("Test Complete")
print("=" * 60)
