# TP-Link Kasa Integration Setup Guide

## Current Devices

### Smart Bulbs (KL125) - 4 devices
All bulbs are working and controllable via command line tools.

- **Paper lamp - low** (10.0.0.103) - 8c:86:dd:48:f9:f9
- **Paper lamp - upper** (10.0.0.177) - 8c:86:dd:48:f6:38
- **Bedside lamp - 1** (10.0.0.224) - e0:d3:62:4d:cf:f7
- **Egg lamp** (10.0.0.244) - e0:d3:62:4d:ce:5e

### Smart Plugs (EP25) - 2 active
These use newer KLAP protocol and work best through Home Assistant.

- **String lights** (10.0.0.165) - bc:07:1d:2c:4d:f2
- **(Rename me)** (10.0.0.201) - bc:07:1d:2b:f1:6f

## Adding to Home Assistant

### Option 1: TP-Link Kasa Integration (Recommended)

1. **Open Home Assistant**
   - Go to http://localhost:8123 (or your Home Assistant URL)

2. **Add Integration**
   - Navigate to: **Settings** → **Devices & Services**
   - Click the **+ ADD INTEGRATION** button (bottom right)

3. **Search for Kasa**
   - Type "TP-Link Kasa Smart" in the search box
   - Click on **TP-Link Kasa Smart** when it appears

4. **Discovery**
   - Home Assistant will automatically discover devices on your network
   - You should see all 6 devices (4 bulbs + 2 plugs)
   - Click **SUBMIT** to add them all

5. **Verify**
   - Go to **Settings** → **Devices & Services** → **TP-Link Kasa Smart**
   - You should see all your devices listed
   - Click on each to verify and customize

### Option 2: Manual Device Addition

If auto-discovery doesn't work:

1. Add each device by IP address:
   - In TP-Link Kasa Smart integration settings
   - Click **+ ADD DEVICE**
   - Enter IP address manually

2. Bulbs:
   - 10.0.0.103 (Paper lamp - low)
   - 10.0.0.177 (Paper lamp - upper)
   - 10.0.0.224 (Bedside lamp - 1)
   - 10.0.0.244 (Egg lamp)

3. Plugs:
   - 10.0.0.165 (String lights)
   - 10.0.0.201 ((Rename me))

## Post-Setup Configuration

### 1. Rename Devices
- Go to each device page
- Click the device name to edit
- Give descriptive names

### 2. Assign Areas
Organize devices by room:
- Living Room: Paper lamps
- Bedroom: Bedside lamp
- etc.

### 3. Create Groups
Group related devices:
- **All Lights**: All 4 bulbs
- **Living Room Lamps**: Both paper lamps
- **Entertainment**: String lights + other devices

### 4. Test Automations
Your brass-monkey automations reference these devices:
- `lighting.yaml` - Daily lighting routines
- `leaving-home.yaml` - Turn off all devices when away
- `arriving-home.yaml` - Welcome home lighting

## Troubleshooting

### Devices Not Discovered
1. Ensure all devices are powered on
2. Check they're on the same network as Home Assistant
3. Try restarting Home Assistant: `docker restart homeassistant`
4. Use manual IP addition instead

### Authentication Errors (EP25 Plugs)
- EP25 uses KLAP protocol
- Ensure latest Home Assistant version (2024.1+)
- If issues persist, update python-kasa in Home Assistant

### Command Line Control
Bulbs (KL125) work with command line tools:
```bash
cd /home/jvycee/projects/brass-monkey/scripts
./kasa_control.py --list
./kasa_control.py --blink all
```

Plugs (EP25) require Home Assistant integration for reliable control.

## Static IP Recommendations

To prevent IP addresses from changing:

1. **Router DHCP Reservation** (Recommended)
   - Access your router settings
   - Find DHCP/LAN settings
   - Create reservations using MAC addresses
   - This ensures devices always get the same IP

2. **Device Static IP** (Alternative)
   - Configure in Kasa app (less reliable)
   - Or use router reservations instead

## Next Steps

After adding Kasa devices:
1. ✓ Set up Zigbee dongle (run `scripts/setup_zigbee_zha.sh`)
2. ✓ Pair Aqara sensors (door/window, temperature)
3. ✓ Configure automations from brass-monkey repo
4. ✓ Test presence detection
5. ✓ Set up NFC tags for manual overrides
