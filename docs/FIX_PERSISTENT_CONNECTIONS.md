# Fix Summary: Persistent Instrument Connections

## Problem
During test execution, commands were not being sent to the power supply because the `InstrumentManager` was creating **new, unconnected driver instances** every time `mgr.ac_source` or `mgr.get_driver_instance()` was called.

## Root Cause
The `InstrumentManager.get_driver_instance()` method was creating a fresh driver instance on every call, which meant:
- Connections made in the Instrument Setup Window were lost
- Test sequences received new, unconnected drivers
- Commands were sent to unconnected instances (no effect on hardware)

## Solution
Updated `InstrumentManager` to maintain **persistent driver instances**:

### Changes Made

1. **Added persistent storage** in [manager.py](file:///d:/Vishnu/Antigravity%20Workspace/Test%20Automation%20GUI/instruments/manager.py):
   ```python
   self._driver_instances = {}  # Store persistent instances
   ```

2. **Modified `get_driver_instance()`** to cache instances:
   - First call: Creates new driver and stores it
   - Subsequent calls: Returns the same cached instance
   
3. **Implemented `connect_all()`** to connect all instruments:
   - Iterates through all configured instruments
   - Connects each one if not already connected
   - Returns success/failure status

4. **Implemented `disconnect_all()`** for cleanup:
   - Disconnects all connected instruments
   - Properly closes VISA resources

5. **Updated Instrument Setup Window** to use manager's persistent instances:
   - Removed local `driver_instances` storage
   - Now uses shared instances from manager

## Verification

Tested with `scripts/test_persistent_connection.py`:
- ✅ Connection to Chroma 62000D successful
- ✅ Same driver instance returned on multiple calls
- ✅ Connection state persists across calls
- ✅ IDN query returns: `Chroma,62060D-600,96206007000231,2.04`

## How It Works Now

### Flow 1: Connect via Instrument Setup Window
1. User clicks "Connect" for Chroma 62000D
2. Manager creates driver instance and stores it
3. Driver connects to hardware via VISA
4. Connection status: 🟢 Connected

### Flow 2: Run Test Execution
1. Test runner calls `mgr.connect_all()`
2. Manager uses **same cached instance** from Setup Window
3. If already connected, skips connection
4. Test sequences use `mgr.ac_source` → returns **same connected instance**
5. Commands are sent to the **connected hardware** ✅

## Result
- ✅ Connections persist between windows
- ✅ Commands are sent to real hardware during test execution
- ✅ No duplicate connections or instances
- ✅ Proper resource management with disconnect_all()
