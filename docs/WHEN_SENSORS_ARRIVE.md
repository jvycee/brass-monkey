# When Your Aqara Sensors Arrive - Quick Start Guide

## What You Have Ready

✅ **Home Assistant** - Fully configured
✅ **Kasa devices** - All 7 working (4 bulbs + 3 plugs)
✅ **Zigbee (ZHA)** - Dongle configured and ready
✅ **Fan plug** - 10.0.0.200, named "Fan" in Kasa app
✅ **Fan automation** - Already written, just needs sensor

## Step 1: Pair Aqara Temperature Sensor (5 minutes)

### In Home Assistant:

1. **Go to:** Settings → Devices & Services
2. **Find:** Zigbee Home Automation (ZHA)
3. **Click:** "ADD DEVICE" or "Configure" → "Add Device"
4. **You'll see:** "Searching for devices..."

### On the Aqara Sensor:

1. **Remove the battery tab** (if brand new)
2. **Hold the button** on the sensor for 5+ seconds
3. **Watch for:** LED to blink (pairing mode)
4. **Wait:** 10-30 seconds for it to appear in HA

### What You'll See:

- Device name like: "lumi.weather" or "Temperature/Humidity Sensor"
- Entities created:
  - `sensor.bedroom_temperature` (or similar name)
  - `sensor.bedroom_humidity`
  - `sensor.bedroom_battery` (battery level)

### Verify It Works:

1. **Go to:** Developer Tools → States
2. **Search for:** "temperature"
3. **Find:** Your new sensor (e.g., `sensor.bedroom_temperature`)
4. **Check:** It shows current temperature in °C or °F

## Step 2: Place Sensor in Bedroom

**Best location:**
- Near where you sleep (bedside table is good)
- Away from windows (avoid direct sun/cold spots)
- Not directly under air vents
- Not on top of electronics (they generate heat)

**Quick test:**
- Place sensor
- Wait 5 minutes for reading to stabilize
- Check temperature in HA Developer Tools → States

## Step 3: Install Fan Automation (10 minutes)

### Option A: Via File Editor (if you have it)

1. **In Home Assistant:** Settings → Add-ons → File Editor (install if needed)
2. **Navigate to:** `/config/automations.yaml`
3. **Copy the automation** from `/home/jvycee/brass-monkey/automations/fan-control-homepod.yaml`
4. **Update entity names** to match your sensor:
   - Change `sensor.bedroom_temperature` to your actual entity name
   - Change `switch.fan_control` to match your Fan plug entity

### Option B: Via UI (easier)

1. **Settings → Automations & Scenes**
2. **Click:** "CREATE AUTOMATION" (blue button, bottom right)
3. **Click:** Three dots (⋮) → "Edit in YAML"
4. **Copy/paste** the automation from `brass-monkey/automations/fan-control-homepod.yaml`
5. **Update** entity names to match your devices
6. **Save**

### Important Entity Names to Update:

Find your actual entity names in **Developer Tools → States**:

```yaml
# Temperature sensor - find yours and update:
entity_id: sensor.bedroom_temperature  # ← Update this

# Fan plug - find yours and update:
entity_id: switch.fan_control  # ← Update this (might be switch.fan)
```

### Temperature Thresholds (adjust to your preference):

```yaml
# Fan turns ON when temp exceeds:
above: 72  # °F - Change if you want different temp

# Fan turns OFF when temp drops below:
below: 70  # °F - Should be 2-4° lower than "on" temp
```

## Step 4: Connect Physical Fan (Tomorrow)

1. **Plug fan into** Kasa EP25 plug (the one named "Fan")
2. **Set fan to HIGH speed** (since we'll control on/off via plug)
3. **Turn plug ON** in Home Assistant to test fan works
4. **Turn plug OFF**

**Why non-digital fan is perfect:**
- Digital fans with touch controls often reset to OFF when power cycles
- Your non-digital fan will resume at its set speed when power comes back
- This means the smart plug can simply turn power on/off

## Step 5: Test Automation

### Manual Test First:

1. **Developer Tools → Services**
2. **Service:** `switch.turn_on`
3. **Target:** Your fan plug (e.g., `switch.fan_control`)
4. **Click:** "CALL SERVICE"
5. **Verify:** Fan turns on

Then test OFF the same way.

### Test Temperature Automation:

**Option A - Wait for natural temperature change:**
- Monitor temp in HA throughout the day
- When it crosses 72°F, fan should turn on
- When it drops to 70°F, fan should turn off

**Option B - Manually trigger (for testing):**
1. **Settings → Automations & Scenes**
2. **Find:** "Fan On - High Temperature"
3. **Click:** Three dots (⋮) → "Run"
4. **Fan should turn on**

### Check Automation Logs:

**Settings → System → Logs**
- Search for your automation name
- Verify no errors
- Should see triggers firing

## Troubleshooting

### Sensor Won't Pair

**Try:**
1. Get closer to the Zigbee dongle (within 6 feet)
2. Remove battery for 10 seconds, reinsert
3. Hold button longer (10+ seconds)
4. In ZHA, click "Add Device" again

### Wrong Temperature Units

If sensor shows Celsius but you want Fahrenheit:

1. **Settings → System → General**
2. **Unit system:** Select "Imperial"
3. **Restart Home Assistant**

Or convert in automation:
```yaml
# Celsius to Fahrenheit
{{ (states('sensor.bedroom_temperature') | float * 9/5 + 32) | round(1) }}
```

### Fan Not Responding

1. **Check plug is online:**
   - Settings → Devices & Services → TP-Link Kasa Smart
   - Verify Fan plug shows as "Available"

2. **Test plug manually:**
   - Developer Tools → Services → `switch.turn_on`
   - If plug doesn't respond, check WiFi/power

3. **Check entity name:**
   - Developer Tools → States
   - Search for "fan"
   - Use exact entity name in automation

### Automation Not Triggering

1. **Verify automation is enabled:**
   - Settings → Automations & Scenes
   - Toggle should be ON (blue)

2. **Check temperature actually crosses threshold:**
   - Current temp must go from below 72° to above 72° (or vice versa)
   - Just being at 73° won't trigger if it's been there a while

3. **Check time conditions:**
   - Automation only runs 7 AM - 11 PM
   - Remove time conditions for testing

4. **Check logs:**
   - Settings → System → Logs
   - Look for automation errors

## After Everything Works

### Fine-tune Temperature Thresholds:

Start conservative, adjust based on comfort:
- Too hot at night? Lower the ON threshold (68°F instead of 72°F)
- Fan cycling too much? Increase hysteresis gap (ON: 72°F, OFF: 68°F)
- Want it cooler? Raise the ON threshold (75°F)

### Optional Enhancements:

1. **Add notification when fan turns on:**
   ```yaml
   - service: notify.mobile_app_iphone
     data:
       message: "Fan on - room is {{ states('sensor.bedroom_temperature') }}°F"
   ```

2. **Different thresholds for night:**
   ```yaml
   # Lower threshold at night for quieter sleep
   condition:
     - condition: time
       after: '22:00:00'
       before: '07:00:00'
   action:
     # Turn off unless extremely hot (>80°F)
   ```

3. **Use multiple sensors for average:**
   If you place sensors in different spots, average them for better control.

## Quick Reference

**Pair sensor:** ZHA → Add Device → Hold sensor button 5sec
**Check entities:** Developer Tools → States
**Test fan:** Developer Tools → Services → `switch.turn_on`
**View logs:** Settings → System → Logs
**Edit automation:** Settings → Automations → Click automation → Edit

---

**Need help?** Check the detailed guides:
- `docs/fan-automation-setup.md` - Full automation guide
- `docs/kasa-setup-guide.md` - Kasa device guide
- `SETUP_STATUS.md` - Current setup status
