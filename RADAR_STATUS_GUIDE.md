# Radar Status Guide

## Normal Behavior

### When Radar is Running Properly:

1. **Startup Messages:**
   ```
   ✓ Serial ports connected successfully
   Sending 45 configuration commands...
   ✓ Configuration sent successfully
   Starting radar data acquisition...
   ```

2. **When Objects are Detected:**
   ```
   [14:23:45.123] Frame #1 - 2 objects detected:
   --------------------------------------------------------------------------------
   Obj  X(m)    Y(m)    Z(m)    V(m/s)  Range(m) Az(°)  El(°)
   --------------------------------------------------------------------------------
   0    1.234   2.456   0.123   -0.456  2.789    45.6   12.3
   ```

3. **When No Objects are Present:**
   - **Quiet operation** - no spam messages
   - **Occasional status**: `[14:23:45.123] Frame #50 - No objects detected` (every 50 frames)
   - **Activity dots**: `.` printed every 10 seconds to show the system is running

## What's Normal vs. What's an Error

### ✅ NORMAL (Don't worry about these):
- **No output for long periods** - means no objects detected
- **Occasional "No objects detected"** - radar is working, just nothing to see
- **Activity dots (...)** - shows radar is running and waiting for data

### ❌ ACTUAL ERRORS (These need attention):
- **"Serial ports not found"** - Check USB connections
- **"Configuration file not found"** - Make sure .cfg file is in the same directory
- **"Frame Fail, cannot find magic words"** - Data corruption, check connections
- **"Frame Fail, incomplete packet"** - Possible connection issue
- **"Parser error"** - Data parsing problem

## Tips for Testing

1. **To see object detection:**
   - Wave your hand in front of the radar
   - Walk around in the detection zone
   - Move objects (like a book or water bottle)

2. **Detection Range:**
   - **Maximum range**: ~9 meters (based on config)
   - **Minimum range**: ~0.1 meters
   - **Best detection**: Moving objects work better than stationary ones

3. **If you see too many dots:**
   - This means radar is running but not getting data frames
   - Check if radar is properly powered
   - Try moving something in front of it

## Radar Coverage

```
        Radar View (Top Down)
             90°
              |
    ±45°   ---|---   ±45°
         /    |    \
        /     |     \
    180°      |      0°
              |
            Radar
```

The radar detects objects in a roughly 180° field of view in front of it. 