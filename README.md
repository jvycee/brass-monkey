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

## Planned Devices

### Phase 1: Air Quality & Basics
- [ ] Levoit Core 300S/400S Air Purifier
- [ ] Aqara Door/Window Sensor (for window-open detection)
- [ ] 2x Kasa Smart Bulbs (lamps)
- [ ] 1x Kasa Smart Plug (music gear)

### Phase 2: Entertainment & Work
- [ ] Kasa Smart Power Strip (entertainment center)
- [ ] Additional smart plugs as needed
- [ ] NFC tags for automations

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
