# Setup Guide - Brass Monkey Smart Home

## Pre-Arrival Setup (Do Now)

### 1. Prepare Home Assistant Integrations

```bash
# SSH into your Home Assistant server
# Navigate to Settings → Devices & Services
```

**Integrations to prepare:**
- [ ] **ZHA (Zigbee Home Automation)** - for Aqara sensors + Sonoff dongle
- [ ] **Kasa Smart** - for plugs, bulbs, and power strip
- [ ] **VeSync** - for Levoit air purifier
- [ ] **HomeKit Bridge** - optional, to expose to Apple Home

### 2. Review Current Home Assistant Setup

Check that your HA instance is healthy:
- [ ] Home Assistant version: Latest stable
- [ ] Disk space: Adequate
- [ ] Backup: Recent backup exists
- [ ] Network: Server has static IP

## Device Arrival & Setup

### Phase 1: Zigbee Foundation (Sonoff Dongle + Sensors)

**When Sonoff Zigbee Dongle arrives:**

1. **Plug in dongle** to USB port on HA server
2. **Add ZHA integration**:
   - Settings → Devices & Services → Add Integration
   - Search "ZHA"
   - Select the Sonoff dongle from device list
   - Follow prompts to complete setup

3. **Verify ZHA is running**:
   - Should see "Zigbee Home Automation" in integrations
   - Check for any errors

**When Aqara sensors arrive:**

1. **Pair door/window sensors**:
   - In HA: Devices & Services → ZHA → Add Device
   - Press reset button on sensor (hold 5 seconds until LED blinks)
   - Sensor should appear in HA within 30 seconds
   - Rename to: `binary_sensor.bedroom_window`, `binary_sensor.living_room_window`

2. **Pair temperature sensors**:
   - Same process as door sensors
   - Rename to: `sensor.bedroom_temperature`, `sensor.living_room_temperature`, etc.

3. **Test sensors**:
   - Open/close window → verify state changes in HA
   - Breathe on temp sensor → verify temperature increases

### Phase 2: WiFi Devices (Kasa)

**When Kasa devices arrive:**

1. **Set up in Kasa app first** (one-time):
   - Download "Kasa Smart" app
   - Create account or log in
   - Add each device through app
   - Connect to WiFi
   - Name devices clearly

2. **Add to Home Assistant**:
   - Settings → Devices & Services → Add Integration
   - Search "TP-Link Kasa Smart"
   - Should auto-discover all devices
   - If not, add manually by IP address

3. **Rename entities** in HA:
   - **Smart plugs**: `switch.music_gear`, `switch.bedroom_fan`, `switch.living_room_fan`
   - **Power strip outlets**: `switch.tv`, `switch.apple_tv`, `switch.ps5`, etc.
   - **Bulbs**: `light.bedroom_lamp`, `light.living_room_lamp`, etc.

4. **Test control**:
   - Toggle each device from HA dashboard
   - Verify physical device responds
   - Check energy monitoring data appears (if applicable)

### Phase 3: Air Purifier (Levoit)

**When Levoit Vital 100S arrives:**

1. **Set up in VeSync app**:
   - Download "VeSync" app
   - Create account
   - Add air purifier
   - Connect to WiFi
   - Test manual control

2. **Add to Home Assistant**:
   - Install VeSync integration (HACS or manual)
   - Settings → Devices & Services → Add Integration
   - Search "VeSync"
   - Log in with VeSync credentials
   - Air purifier should appear

3. **Rename entity**:
   - `fan.air_purifier` or `fan.levoit_vital_100s`

4. **Test modes**:
   - Auto mode
   - Sleep mode
   - Manual speed levels
   - Check air quality sensor readings

### Phase 4: NFC Tags (iPhone Shortcuts)

**When NFC tags arrive:**

1. **Open Shortcuts app** on iPhone
2. **Create "Leaving Home" automation**:
   - Automation tab → + → NFC
   - Scan NFC tag
   - Add actions:
     - Turn off all lights
     - Turn off music gear switch
     - Turn off entertainment switches
     - Set air purifier to turbo (if window closed)
   - Name: "Leaving Home"

3. **Program additional tags**:
   - **Bedside**: Sleep mode automation
   - **Desk**: Work mode automation
   - **Front door**: Arriving home automation

4. **Place tags**:
   - Front door frame (shoulder height)
   - Bedside table
   - Desk edge
   - Keep extras for experimentation

## Configuring Automations

### Update YAML Files

Once devices are paired, update entity IDs in:
- `automations/air-quality.yaml`
- `automations/lighting.yaml`
- `automations/climate-control.yaml`
- `scripts/leaving-home.yaml`

Replace placeholder entity IDs with actual IDs from your HA setup.

### Test Each Automation

**Air Quality:**
- [ ] Open window → purifier stops
- [ ] Close window → purifier resumes
- [ ] Leave home (simulate) → purifier goes to turbo

**Climate Control:**
- [ ] Temp rises above 72°F → fan turns on
- [ ] Temp drops below 65°F → fan turns off
- [ ] Window opens → fans stop

**Lighting:**
- [ ] Morning routine triggers at 7 AM
- [ ] Evening lights at sunset
- [ ] NFC tag controls work

## Troubleshooting

### Zigbee Devices Won't Pair
- Move closer to coordinator
- Replace battery (if old stock)
- Reset device (hold button 10+ seconds)
- Restart ZHA integration

### Kasa Devices Not Discovered
- Ensure on same WiFi network as HA
- Check 2.4GHz WiFi enabled (not 5GHz only)
- Verify devices have static DHCP reservations
- Manual add by IP if needed

### Air Purifier Offline
- Check VeSync app works
- Verify WiFi connection
- Restart HA VeSync integration
- Check firewall rules

### NFC Tags Not Working
- Ensure iPhone NFC is enabled
- Tag must be close to top of phone
- Phone might need to be unlocked
- Try re-programming tag

## Backup & Documentation

### Create Backup
```bash
# In HA: Settings → System → Backups → Create Backup
```

### Document Entity IDs
Create file: `devices/entity-mapping.md`

```markdown
## Entity ID Reference

### Sensors
- Bedroom window: binary_sensor.bedroom_window
- Living room window: binary_sensor.living_room_window
- Bedroom temp: sensor.bedroom_temperature
- Living room temp: sensor.living_room_temperature

### Switches
- Music gear: switch.music_gear
- Bedroom fan: switch.bedroom_fan
- Living room fan: switch.living_room_fan
- TV: switch.tv
...
```

### Update Git Repo
```bash
cd ~/brass-monkey
git add .
git commit -m "Update with actual entity IDs and working automations"
git push
```

## Next Steps After Setup

1. **Monitor for 1 week**:
   - Note any false triggers
   - Adjust temperature thresholds
   - Fine-tune timing schedules

2. **Optimize**:
   - Adjust fan temperature setpoints
   - Tweak light brightness/color
   - Refine NFC automation actions

3. **Expand** (optional):
   - Add more sensors to other areas
   - Create more advanced scenes
   - Integrate with other services

4. **Maintain**:
   - Monthly HA backups
   - Replace sensor batteries yearly
   - Update automations as needed
