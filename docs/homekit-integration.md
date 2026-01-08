# HomeKit Integration for HomePod mini Temperature/Humidity

## Overview

Your HomePod mini has built-in temperature and humidity sensors that can be used to control your Kasa smart plugs (like a fan) through Home Assistant.

## Discovered Apple Devices

Devices with HomeKit/AirPlay ports open:
- **10.0.0.118** (MAC: 74:6d:fa:f3:d6:5c)
- **10.0.0.98** (MAC: a4:cf:99:aa:2e:ca)
- **10.0.0.54** (MAC: 4c:22:f3:9c:98:61)

One of these is your HomePod mini. Check your Home app to identify which one.

## Setup Steps

### 1. Enable HomeKit on HomePod mini

Your HomePod should already be set up in your Home app. Verify:
1. Open **Home app** on your iPhone/Mac
2. Find your **HomePod mini**
3. Long press/tap for details
4. Check that it's in the same home
5. Note the room assignment

### 2. Add HomeKit Integration to Home Assistant

**Option A: HomeKit Controller (Recommended)**

1. **Open Home Assistant**
   - Go to http://localhost:8123

2. **Add Integration**
   - Settings → Devices & Services
   - Click **+ ADD INTEGRATION**
   - Search for **"HomeKit Controller"**

3. **Discover Devices**
   - Home Assistant will scan for HomeKit accessories
   - Your HomePod mini should appear
   - Click **SUBMIT** to add it

4. **Pairing**
   - You'll need the HomeKit pairing code
   - This is usually on the device or in the Home app
   - For HomePod: Settings → [Your HomePod] → Reset HomeKit Pairing Code

5. **Verify Sensors**
   - After pairing, check:
     - `sensor.homepod_mini_temperature`
     - `sensor.homepod_mini_humidity`

**Option B: HomeKit Bridge (if Controller doesn't work)**

If HomeKit Controller doesn't work, you can expose HA devices TO HomeKit instead and use automation within the Home app.

### 3. Create Fan Automation Based on Temperature

Once the HomePod sensors are in Home Assistant, create an automation:

**Example: Turn on fan when temp > 72°F**

```yaml
# brass-monkey/automations/fan-control-homepod.yaml

- alias: "Fan On - High Temperature"
  trigger:
    - platform: numeric_state
      entity_id: sensor.homepod_mini_temperature
      above: 72  # Adjust to your preference
  condition:
    - condition: state
      entity_id: binary_sensor.window_sensor  # Optional: only if window closed
      state: 'off'
  action:
    - service: switch.turn_on
      target:
        entity_id: switch.fan_plug  # Your Kasa plug for fan
    - service: notify.mobile_app_iphone
      data:
        message: "Fan turned on - temperature is {{ states('sensor.homepod_mini_temperature') }}°F"

- alias: "Fan Off - Normal Temperature"
  trigger:
    - platform: numeric_state
      entity_id: sensor.homepod_mini_temperature
      below: 70  # Hysteresis - turn off at lower temp to avoid cycling
  action:
    - service: switch.turn_off
      target:
        entity_id: switch.fan_plug
    - service: notify.mobile_app_iphone
      data:
        message: "Fan turned off - temperature is {{ states('sensor.homepod_mini_temperature') }}°F"
```

### 4. Advanced: Multi-Sensor Climate Control

Combine HomePod sensors with Aqara sensors for better control:

```yaml
# Use average temperature from multiple sensors
- alias: "Smart Fan Control - Average Temperature"
  trigger:
    - platform: time_pattern
      minutes: "/5"  # Check every 5 minutes
  action:
    - variables:
        avg_temp: >
          {% set temps = [
            states('sensor.homepod_mini_temperature') | float,
            states('sensor.aqara_living_room_temperature') | float,
            states('sensor.aqara_bedroom_temperature') | float
          ] %}
          {{ (temps | sum / temps | length) | round(1) }}
    - choose:
        - conditions:
            - condition: template
              value_template: "{{ avg_temp > 72 }}"
          sequence:
            - service: switch.turn_on
              target:
                entity_id: switch.fan_plug
        - conditions:
            - condition: template
              value_template: "{{ avg_temp < 70 }}"
          sequence:
            - service: switch.turn_off
              target:
                entity_id: switch.fan_plug
```

## Troubleshooting

### HomePod Not Discovered

1. **Check Network**
   - Ensure HomePod and HA are on same network/VLAN
   - Check firewall rules aren't blocking mDNS/Bonjour

2. **Reset HomeKit Pairing**
   - In Home app: [HomePod] → Settings → Reset
   - Or say "Hey Siri, reset my HomeKit pairing code"

3. **Use IP Address Directly**
   - If you know the HomePod IP (from the list above)
   - Add it manually in HomeKit Controller integration

### Sensors Not Showing

1. **Check Entity Registry**
   - Settings → Devices & Services → HomeKit Controller
   - Click on HomePod device
   - Verify temperature/humidity entities are enabled

2. **Check Units**
   - HomePod may report in Celsius
   - Convert in automation if needed:
     ```yaml
     {{ (states('sensor.homepod_mini_temperature') | float * 9/5 + 32) | round(1) }}
     ```

### Automation Not Triggering

1. **Check Current Values**
   - Developer Tools → States
   - Search for `sensor.homepod_mini_temperature`
   - Verify it's updating

2. **Test Manually**
   - Developer Tools → Services
   - Call `switch.turn_on` for your fan plug
   - Verify the plug responds

## Which Kasa Plug for Your Fan?

You have 2 EP25 plugs available:
- **String lights** (10.0.0.165) - Currently in use
- **(Rename me)** (10.0.0.201) - Available for fan

Plus 2 spare EP25 plugs not yet configured.

**Recommendation:**
1. Rename "(Rename me)" plug to "Bedroom Fan" or "Living Room Fan" in Kasa app
2. Use it for fan control
3. Keep string lights separate

## Benefits

✓ **Automated comfort** - Fan turns on/off based on real-time temperature
✓ **Energy saving** - No fan running when not needed
✓ **Smart logic** - Can factor in window state, time of day, etc.
✓ **Multi-room awareness** - Use sensors from different rooms
✓ **No additional hardware** - Using sensors you already have

## Next Steps

1. Identify which IP is your HomePod mini
2. Add HomeKit Controller integration to Home Assistant
3. Pair the HomePod
4. Verify temperature/humidity sensors appear
5. Create fan automation
6. Test and adjust temperature thresholds
