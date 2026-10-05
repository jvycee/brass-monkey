# Brass Monkey Setup Status

**Updated:** 2026-01-08

## ✅ Discovered & Working

### TP-Link Kasa Smart Bulbs (4)
All verified working - successfully blinked each one!

| Device | IP | MAC | Status |
|--------|-----|-----|--------|
| Paper lamp - low | 10.0.0.103 | 8c:86:dd:48:f9:f9 | ✓ Working |
| Paper lamp - upper | 10.0.0.177 | 8c:86:dd:48:f6:38 | ✓ Working |
| Bedside lamp - 1 | 10.0.0.224 | e0:d3:62:4d:cf:f7 | ✓ Working |
| Egg lamp | 10.0.0.244 | e0:d3:62:4d:ce:5e | ✓ Working |

### TP-Link Kasa Smart Plugs (3 active)
Identified on network - require Home Assistant integration for control.

| Device | IP | MAC | Status |
|--------|-----|-----|--------|
| String lights | 10.0.0.165 | bc:07:1d:2c:4d:f2 | ✓ On network |
| (Rename me) | 10.0.0.201 | bc:07:1d:2b:f1:6f | ✓ On network |
| Fan | 10.0.0.200 | bc:07:1d:2c:0d:29 | ✓ Configured (Bedroom) |

**Note:** EP25 plugs use newer KLAP protocol - use Home Assistant integration instead of CLI.

### Zigbee Coordinator
| Device | Path | Status |
|--------|------|--------|
| Sonoff Zigbee 3.0 USB Dongle Plus-E | /dev/ttyUSB0 | ✓ Detected |

## 📋 Configured in Home Assistant

### Home Assistant Integrations
- [x] **TP-Link Kasa Smart** - All 7 devices configured! ✓
  - 4 bulbs working
  - 3 plugs working (including Fan plug at 10.0.0.200)
- [x] **Zigbee Home Automation (ZHA)** - Sonoff dongle configured! ✓
  - Radio type: EZSP
  - Device: /dev/ttyUSB0
  - Network created and ready for device pairing

### Apple HomeKit Devices
| Device | Model | IP | MAC | Status |
|--------|-------|-----|-----|--------|
| HomePod mini | MY5G2LL/A | 10.0.0.118 | 74:6d:fa:f3:d6:5c | ✓ Identified |

**Features:**
- Temperature sensor (for fan automation)
- Humidity sensor
- AirPlay 2
- Siri
- HomeKit Hub

**Serial:** HG5JK5g9PQ1H (Space Gray model)

### Zigbee Devices (Waiting to arrive)
- [ ] Aqara Door/Window Sensor x2 - **Not ordered yet**
- [ ] Aqara Temperature/Humidity Sensor x3 - **Not ordered yet**
  - One will be used for bedroom fan automation

### Physical Hardware (In Transit)
- [ ] Non-digital fan - **Arrives tomorrow** ✓ Smart choice for plug control!

## 📝 Scripts Created

All in `/home/jvycee/projects/brass-monkey/scripts/`:

| Script | Purpose |
|--------|---------|
| `discover_kasa.py` | Find all Kasa devices and output YAML config |
| `kasa_control.py` | Control devices via CLI (on/off/brightness/blink) |
| `device_status.py` | Get status summary of all devices |
| `setup_zigbee_zha.sh` | Guide for Zigbee dongle setup in HA |

## 🤖 Automations Created

All in `/home/jvycee/projects/brass-monkey/automations/`:

| Automation | Purpose |
|------------|---------|
| `fan-control-homepod.yaml` | Temperature-based fan control using HomePod mini sensor |
| `air-quality.yaml` | Purifier control based on window state |
| `climate-control.yaml` | Temperature-based climate management |
| `lighting.yaml` | Daily lighting routines |
| `presence-detection.yaml` | Geofencing + door sensor presence |
| `bathroom-lighting.yaml` | Motion-activated bathroom lights |

## 📄 Documentation Created

| File | Contents |
|------|----------|
| `devices/kasa_devices.yaml` | Full inventory of all Kasa devices |
| `docs/kasa-setup-guide.md` | Step-by-step HA integration guide |
| `scripts/README.md` | Script usage documentation |

## 🎯 Next Steps

### ✅ Completed Today (2026-01-08)
1. ✓ **Discovered all devices** - 4 bulbs, 3 plugs, HomePod, Zigbee dongle
2. ✓ **Added Kasa to Home Assistant** - All 7 devices working
3. ✓ **Configured Zigbee (ZHA)** - Sonoff dongle ready for sensors
4. ✓ **Created fan automation** - Ready to install when sensors arrive

### 📦 Waiting On
1. **Fan arrives tomorrow** - Non-digital model for easy plug control
2. **Order Aqara sensors** - Temperature/humidity for fan automation
3. **Order Aqara door/window sensors** (optional) - For presence detection

### 🔜 When Sensors Arrive
1. **Pair Aqara temperature sensor to ZHA**
   - In HA: ZHA integration → Add Device
   - Hold sensor button for 5 seconds
   - Sensor will appear in HA

2. **Install fan automation**
   - Copy `automations/fan-control-homepod.yaml` to HA
   - Update to use Aqara sensor instead of HomePod
   - Entity: `sensor.bedroom_temperature` (or similar)

3. **Test with real fan**
   - Plug fan into Kasa plug (10.0.0.200)
   - Verify automation turns fan on/off based on temp
   - Adjust temperature thresholds if needed

### 🔧 Optional Later
- Set up static IPs in router for all devices
- Configure NFC tags for manual overrides
- Add bathroom motion sensor
- Set up door sensors for presence detection
- Migrate other automations from brass-monkey repo

## 🛠 System Info

- Home Assistant: Running on port 8123 (Docker)
- MQTT Broker: Mosquitto on port 1883
- Zigbee Path: `/dev/ttyUSB0`
- Network: 10.0.0.0/24
