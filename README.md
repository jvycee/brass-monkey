# Brass Monkey - Home Assistant Configuration

Smart home setup for a 1-bedroom apartment focused on practical quality-of-life automations.

## Overview

**Living Situation:**
- 1 bedroom apartment, older building
- No smart thermostat possible
- Good natural light (morning sun, afternoon shade)
- Windows provide airflow 6+ months/year
- Living alone

**Goals:**
- Smart air quality management (purifier + window awareness)
- Entertainment center power management
- Music gear automation (amp/pedals never left on)
- Ambient lighting for daily routines
- Low maintenance, high impact

## Devices (Ordered Dec 2025)

### Air Quality & Monitoring
- [x] **Levoit Vital 100S** Air Purifier ($114)
- [x] **Aqara Door/Window Sensor** x2 ($29)
- [x] **Aqara Temp/Humidity Sensor** 3-pack ($44)

### Control & Automation
- [x] **Sonoff Zigbee 3.0 USB Dongle Plus-E** ($25)
- [x] **Kasa EP25P4** Smart Plugs 4-pack ($37)
- [x] **Kasa HS300** Power Strip 6-outlet ($40)
- [x] **Kasa KL125P4** RGB Smart Bulbs 4-pack ($24)
- [x] **NFC Tags NTAG215** 50-pack ($10)

**Total: ~$323**

See [actual-purchases.md](docs/actual-purchases.md) for full details.

## Key Automations

### Air Quality Intelligence
- **Window Open**: Purifier stops automatically
- **Window Closed**: Purifier resumes auto mode
- **Away Mode**: Purifier runs on HIGH (aggressive cleaning)
- **Home Mode**: Purifier returns to AUTO/LOW

### Daily Routines
- **Morning**: Bedroom lamp gradual wake-up, work setup powers on
- **Evening**: Living room lamp at sunset
- **Leaving**: All lights off, entertainment off, purifier HIGH
- **Arriving**: Purifier to LOW, lights on if dark

### Entertainment Center
- Power strip controls: TV, Apple TV, PS5, Switch, Pi
- Standby power cut when not in use
- Quick "Gaming Mode" scene

### Music Studio
- Guitar amp + pedal power on single smart plug
- Auto-off timer (never left on overnight)
- "Practice Mode" scene

### Climate Control
- **Above 72°F**: Room fans turn on automatically
- **Below 65°F**: Fans turn off (hysteresis prevents rapid cycling)
- **Window Open**: Fans pause (natural airflow priority)
- **Night Mode**: Bedroom fan off for quiet sleep (if >70°F)

## NFC Tag Locations
1. **Front Door**: Leaving/arriving home automation
2. **Bedside**: Sleep mode (all off, purifier low)
3. **Desk**: Work mode toggle
4. **Optional Car**: "Heading home" prep

## Repository Structure

```
brass-monkey/
├── automations/          # Home Assistant automation configs
├── scripts/              # Reusable scripts
├── devices/              # Device-specific configs and docs
├── docs/                 # Additional documentation
└── README.md            # This file
```

## Setup Instructions

Coming soon...

## Notes

- All devices chosen for **local control** (no cloud dependency)
- Focus on **practical automations** that improve daily life
- No gimmicks - only things that actually matter

---

*Named after the Cold Chisel song, because good vibes matter*
