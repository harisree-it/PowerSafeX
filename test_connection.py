import pyvisa

# VISA address for Chroma 62000D
VISA_ADDRESS = "USB0::0x0A69::0x0884::96206007000231::INSTR"

print("=" * 60)
print("Testing Connection to Chroma 62000D Power Supply")
print("=" * 60)

try:
    # Create resource manager
    rm = pyvisa.ResourceManager()
    
    print("\n1. Listing all available VISA resources...")
    resources = rm.list_resources()
    print(f"   Found {len(resources)} resource(s):")
    for res in resources:
        print(f"   - {res}")
    
    print(f"\n2. Attempting to connect to: {VISA_ADDRESS}")
    
    # Open the instrument
    psu = rm.open_resource(VISA_ADDRESS)
    
    # Configure VISA settings
    psu.timeout = 5000  # 5 seconds
    psu.write_termination = '\n'
    psu.read_termination = '\n'
    
    print("   [OK] Connection opened successfully")
    
    # Query identification
    print("\n3. Querying instrument identification (*IDN?)...")
    idn = psu.query("*IDN?")
    print(f"   [OK] IDN Response: {idn.strip()}")
    
    # Close connection
    psu.close()
    rm.close()
    
    print("\n" + "=" * 60)
    print("[SUCCESS] CONNECTION TEST SUCCESSFUL!")
    print("=" * 60)
    print("\nThe Chroma 62000D is connected and responding properly.")
    
except pyvisa.errors.VisaIOError as e:
    print(f"\n[ERROR] VISA Error: {e}")
    print("\nPossible issues:")
    print("  - Instrument not powered on")
    print("  - USB cable not connected")
    print("  - Wrong VISA address")
    print("  - NI-VISA not installed or configured properly")
    
except Exception as e:
    print(f"\n[ERROR] Unexpected Error: {e}")
    print(f"   Error Type: {type(e).__name__}")

print("\n")
