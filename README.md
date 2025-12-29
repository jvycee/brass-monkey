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

### Optional (Add Later)
- [ ] **Aqara Motion Sensor P1** (~$18) - Bathroom hands-free lighting

**Total: ~$323** (or ~$340 with motion sensor)

See [actual-purchases.md](docs/actual-purchases.md) for full details.

## Key Automations

### Presence Detection (Multi-Layered)
- **Primary: Geofencing** - Phone location triggers away/home modes automatically
- **Backup: Front Door Sensor** - Catches cases where geofencing fails
- **Manual: NFC Tag** - Direct override when needed
- **Smart State Tracking** - Prevents duplicate triggers from multiple methods

### Air Quality Intelligence
- **Window Open**: Purifier stops automatically
- **Window Closed**: Purifier resumes auto mode
- **Away Mode**: Purifier runs on HIGH (aggressive cleaning while you're gone)
- **Home Mode**: Purifier returns to AUTO/LOW (quiet operation)

### Daily Routines
- **Morning**: Bedroom lamp gradual wake-up, work setup powers on
- **Evening**: Living room lamp at sunset
- **Leaving Home**: All lights off, entertainment off, purifier HIGH, music gear off
- **Arriving Home**: Purifier to LOW, lights on if dark, welcome notification

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

### Bathroom Lighting (Optional)
- **Night (10 PM - 7 AM)**: Motion → 20% dim warm light
- **Day (7 AM - 10 PM)**: Motion → 100% full brightness
- **Auto-off**: 30s-60s after motion clears
- **Manual override**: Temporarily disables motion automation

## Automation Triggers

### Automatic (Preferred)
- **Geofencing**: Phone location (100m radius)
- **Door Sensor**: Front door activity patterns
- **Time-based**: Morning/evening routines, schedules
- **Temperature**: Fan control based on room temp
- **Window State**: Air quality optimization

### Manual Override
1. **NFC Tag - Front Door**: Force leaving/arriving mode
2. **NFC Tag - Bedside**: Sleep mode (all off, purifier low)
3. **NFC Tag - Desk**: Work mode toggle
4. **iPhone Shortcuts**: Siri voice commands

## Repository Structure

```
brass-monkey/
├── automations/
│   ├── air-quality.yaml           # Purifier + window logic
│   ├── climate-control.yaml       # Temperature-based fans
│   ├── lighting.yaml              # Daily lighting routines
│   └── presence-detection.yaml    # Geofencing + door sensor
├── scripts/
│   ├── leaving-home.yaml          # Away mode actions
│   └── arriving-home.yaml         # Home mode actions
├── devices/                       # Device configs (to be added)
├── docs/
│   ├── actual-purchases.md        # Complete order ($323)
│   ├── setup-guide.md             # Device setup instructions
│   ├── presence-detection-setup.md # Geofencing configuration
│   └── shopping-list.md           # Original research
└── README.md                      # This file
```

## Setup Instructions

See detailed guides in `/docs`:
- **[setup-guide.md](docs/setup-guide.md)** - Device pairing and initial setup
- **[presence-detection-setup.md](docs/presence-detection-setup.md)** - Geofencing configuration
- **[actual-purchases.md](docs/actual-purchases.md)** - What was ordered and why

## Notes

- All devices chosen for **local control** (no cloud dependency)
- Focus on **practical automations** that improve daily life
- No gimmicks - only things that actually matter

---

*Named after the Cold Chisel song, because good vibes matter*
