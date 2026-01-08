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

## 📋 Ready to Configure

### Home Assistant Integrations
- [ ] TP-Link Kasa Smart (for all 6 devices)
- [ ] Zigbee Home Automation (ZHA) for Sonoff dongle

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

### Zigbee Devices (Not yet paired)
- [ ] Aqara Door/Window Sensor x2
- [ ] Aqara Temperature/Humidity Sensor x3

## 📝 Scripts Created

All in `/home/jvycee/brass-monkey/scripts/`:

| Script | Purpose |
|--------|---------|
| `discover_kasa.py` | Find all Kasa devices and output YAML config |
| `kasa_control.py` | Control devices via CLI (on/off/brightness/blink) |
| `device_status.py` | Get status summary of all devices |
| `setup_zigbee_zha.sh` | Guide for Zigbee dongle setup in HA |

## 🤖 Automations Created

All in `/home/jvycee/brass-monkey/automations/`:

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

1. **Add Kasa to Home Assistant**
   - Follow `docs/kasa-setup-guide.md`
   - Should auto-discover all 6 devices

2. **Configure Zigbee**
   - Run: `./scripts/setup_zigbee_zha.sh`
   - Add dongle to docker-compose.yml
   - Set up ZHA integration

3. **Pair Aqara Sensors**
   - Door/window sensors for presence detection
   - Temperature sensors for climate control

4. **Test Automations**
   - Migrate automations from brass-monkey to HA
   - Test presence detection with door sensor
   - Configure air quality logic

5. **Optional Enhancements**
   - Set up static IPs in router
   - Configure NFC tags
   - Add motion sensor for bathroom lighting

## 🛠 System Info

- Home Assistant: Running on port 8123 (Docker)
- MQTT Broker: Mosquitto on port 1883
- Zigbee Path: `/dev/ttyUSB0`
- Network: 10.0.0.0/24
