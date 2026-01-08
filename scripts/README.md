# Brass Monkey Scripts

Utility scripts for managing your smart home devices.

## Device Discovery & Control

### `discover_kasa.py`
Discover all TP-Link Kasa devices on your network and output their details.

```bash
python3 discover_kasa.py
```

Outputs:
- List of all bulbs and plugs
- IP addresses, models, MAC addresses
- Current state (on/off)
- YAML format for device documentation

### `kasa_control.py`
Control Kasa devices from command line.

```bash
# List all devices
./kasa_control.py --list

# Turn devices on/off
./kasa_control.py --on "Paper lamp - low"
./kasa_control.py --off "String lights"
./kasa_control.py --on all
./kasa_control.py --off all

# Set brightness (bulbs only)
./kasa_control.py --brightness 50 "Bedside lamp - 1"
./kasa_control.py --brightness 75 all

# Blink to identify
./kasa_control.py --blink "Egg lamp"
./kasa_control.py --blink all
```

### `device_status.py`
Get a summary status of all devices.

```bash
./device_status.py
```

Shows:
- Online/offline status
- Current power consumption
- Brightness/color settings
- Summary statistics

## Zigbee Setup

### `setup_zigbee_zha.sh`
Guide for setting up the Sonoff Zigbee dongle with Home Assistant.

```bash
./setup_zigbee_zha.sh
```

Checks:
- Dongle detection
- Home Assistant container status
- Provides step-by-step setup instructions

## Home Assistant Integration

### `arriving-home.yaml`
Script for actions when arriving home:
- Turn on lights if dark
- Set purifier to LOW/AUTO
- Send welcome notification

### `leaving-home.yaml`
Script for actions when leaving home:
- Turn off all lights
- Turn off entertainment center
- Set purifier to HIGH
- Turn off music gear

## Installation

Most scripts require `python-kasa` library:

```bash
pip3 install python-kasa
```

Or use a virtual environment:

```bash
python3 -m venv venv
source venv/bin/activate
pip install python-kasa
```

## Tips

1. **Find your plugs**: If `discover_kasa.py` doesn't find your EP25 plugs, check the Kasa app for their IP addresses and query directly:
   ```bash
   kasa --host 10.0.0.XXX state
   ```

2. **Blink for identification**: Use `--blink all` to identify all devices at once when setting up

3. **Device naming**: Use descriptive names in the Kasa app - they'll show up in all scripts and Home Assistant

4. **Static IPs**: Consider setting static IP addresses for your devices in your router to prevent addresses from changing
