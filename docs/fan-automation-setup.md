# Fan Automation Setup Guide

## Overview

Automatically control your bedroom fan using the temperature sensor in your HomePod mini.

## Hardware

- **HomePod mini** (Bedroom) - Temperature & humidity sensor
- **Kasa EP25 Plug** (10.0.0.200 / bc:07:1d:2c:0d:29) - Controls fan
- **Fan** - Connected to the Kasa plug

## Setup Steps

### 1. Add HomeKit Integration to Home Assistant

1. **Open Home Assistant**
   ```
   http://localhost:8123
   ```

2. **Add HomeKit Controller**
   - Settings → Devices & Services
   - Click **+ ADD INTEGRATION**
   - Search for **"HomeKit Controller"**
   - Click to add

3. **Find Your HomePod**
   - HA will scan for HomeKit devices
   - Look for your HomePod mini (in "Bedroom")
   - Select it and click **SUBMIT**

4. **Pairing Code**
   - If prompted for a pairing code:
     - Open Home app on iPhone
     - Long-press HomePod mini
     - Go to Settings
     - Scroll down to "Reset HomeKit Pairing Code"
     - Use the new code in Home Assistant

5. **Verify Sensors**
   After pairing, check that these entities exist:
   - `sensor.bedroom_temperature` (or similar name)
   - `sensor.bedroom_humidity`

   To verify:
   - Settings → Devices & Services → HomeKit Controller
   - Click on your HomePod device
   - Check the sensor entities

### 2. Add Kasa Integration

1. **Add TP-Link Kasa Smart**
   - Settings → Devices & Services
   - Click **+ ADD INTEGRATION**
   - Search for **"TP-Link Kasa Smart"**

2. **Auto-Discovery**
   - Should find all your Kasa devices including:
     - 4 bulbs
     - 3 plugs (including fan control at 10.0.0.200)

3. **Rename Fan Plug**
   - Find the plug at 10.0.0.200
   - Rename to **"Fan Control"** or **"Bedroom Fan"**
   - The entity will be `switch.fan_control` (or similar)

### 3. Install Fan Automation

1. **Copy automation file**
   ```bash
   # The automation is already in brass-monkey/automations/fan-control-homepod.yaml

   # You'll need to copy this to Home Assistant config
   # After we set up HA integration with brass-monkey repo
   ```

2. **Or create manually in HA:**
   - Settings → Automations & Scenes
   - Click **CREATE AUTOMATION**
   - Click the three dots → **Edit in YAML**
   - Copy content from `automations/fan-control-homepod.yaml`
   - Save

### 4. Customize Temperature Thresholds

Edit the automation to match your comfort level:

```yaml
# In the "Fan On" automation:
above: 72  # Change this to your preferred temperature

# In the "Fan Off" automation:
below: 70  # Should be 2-4 degrees lower than "on" temp
```

**Hysteresis Explanation:**
- Turn ON at 72°F
- Turn OFF at 70°F
- This prevents the fan from rapidly cycling on/off when temp hovers around the threshold

### 5. Adjust Time Settings

**Active Hours:**
```yaml
condition:
  - condition: time
    after: '07:00:00'  # Start automatic control at 7 AM
    before: '23:00:00'  # Stop automatic control at 11 PM
```

**Night Mode:**
```yaml
trigger:
  - platform: time
    at: '23:00:00'  # Turn off fan for quiet sleep
```

## Automation Features

### ✓ Automatic Temperature Control
- Fan turns ON when bedroom hits 72°F
- Fan turns OFF when temp drops to 70°F
- Prevents rapid on/off cycling

### ✓ Night Mode
- Automatically turns off fan at 11 PM for quiet sleep
- Unless temperature is dangerously high (>78°F)
- Resumes automatic control at 7 AM

### ✓ Smart Logic
- 2-minute delay before turning on (avoids false triggers)
- 5-minute delay before turning off (ensures it's not temporary)
- Only active during waking hours

### ✓ Optional Window Integration
- When Aqara window sensor is added
- Turns off fan when window opens (natural airflow)
- Saves energy

### ✓ Notifications (Optional)
- Alerts when fan turns on/off
- Shows current temperature
- Requires Home Assistant mobile app

## Testing

### 1. Check Entity Names

```
Developer Tools → States
Search for: "temperature"
Find your HomePod sensor (might be named differently)
```

### 2. Update Entity IDs in Automation

If your sensor is named differently, update the automation:
```yaml
# Change this:
entity_id: sensor.bedroom_temperature

# To match your actual entity, like:
entity_id: sensor.homepod_mini_temperature
```

### 3. Manual Test

Test the fan plug manually:
```
Developer Tools → Services
Service: switch.turn_on
Target: switch.fan_control
Click "CALL SERVICE"
```

Verify the fan turns on!

### 4. Monitor Temperature

Watch the temperature sensor:
```
Developer Tools → States
Find: sensor.bedroom_temperature
Watch the value update
```

### 5. Test Automation

Option A - Wait for temperature to rise naturally
Option B - Manually trigger:
```
Settings → Automations & Scenes
Find "Fan On - High Temperature"
Click three dots → "Run"
```

## Troubleshooting

### HomePod Not Found

Check possible IPs:
- 10.0.0.118
- 10.0.0.98
- 10.0.0.54

One of these is your HomePod. Try adding manually if auto-discovery fails.

### Temperature Sensor Missing

1. Check entity registry:
   - Settings → Devices & Services → HomeKit Controller
   - Click on HomePod device
   - Enable temperature sensor if disabled

2. Check entity name:
   - Developer Tools → States
   - Search for entities containing "temperature"

### Fan Not Responding

1. Verify plug is online:
   - Check in Kasa app
   - Ping 10.0.0.200

2. Check Home Assistant:
   - Settings → Devices & Services → TP-Link Kasa Smart
   - Verify plug appears and is online

### Automation Not Triggering

1. **Check automation is enabled:**
   - Settings → Automations & Scenes
   - Ensure automation has toggle ON

2. **Check trigger values:**
   - Current temp must actually cross threshold
   - Check current temp in Developer Tools → States

3. **Check conditions:**
   - Time conditions might prevent it from running
   - Remove conditions for testing

4. **Check logs:**
   - Settings → System → Logs
   - Look for automation errors

## Advanced Tweaks

### Use Humidity Too

Add humidity-based control:
```yaml
trigger:
  - platform: numeric_state
    entity_id: sensor.bedroom_humidity
    above: 65  # High humidity
condition:
  - condition: numeric_state
    entity_id: sensor.bedroom_temperature
    above: 70  # Must also be warm
```

### Multiple Sensors Average

If you add Aqara sensors, use average temperature:
```yaml
trigger:
  - platform: template
    value_template: >
      {% set temps = [
        states('sensor.bedroom_temperature') | float,
        states('sensor.aqara_bedroom_temperature') | float
      ] %}
      {{ (temps | sum / temps | length) > 72 }}
```

### Fan Speed Control

If your fan has multiple speeds (controlled by different plugs):
```yaml
# High speed for very hot
- above: 76
  action: turn on high_speed_plug

# Medium speed for warm
- above: 73
  below: 76
  action: turn on medium_speed_plug
```

## Next Steps

1. ✓ Add HomeKit Controller integration
2. ✓ Pair HomePod mini
3. ✓ Add TP-Link Kasa integration
4. ✓ Rename fan plug
5. ✓ Install fan automation
6. ✓ Test and adjust thresholds
7. Later: Add Aqara window sensor for smarter control
