# Presence Detection Setup Guide

## Overview

Your brass-monkey system uses **three layers** of presence detection for maximum reliability:

1. **Primary: Geofencing** - Automatic, based on phone location
2. **Backup: Front Door Sensor** - Catches cases where geofence fails
3. **Manual Override: NFC Tag** - Direct control when needed

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     PRESENCE DETECTION                       │
└─────────────────────────────────────────────────────────────┘
                              │
        ┌─────────────────────┼─────────────────────┐
        │                     │                     │
        ▼                     ▼                     ▼
   GEOFENCING            DOOR SENSOR            NFC TAG
   (Primary)              (Backup)             (Manual)
        │                     │                     │
        │                     │                     │
        └─────────────────────┴─────────────────────┘
                              │
                              ▼
                    input_boolean.away_mode
                    (Tracks current state)
                              │
                ┌─────────────┴─────────────┐
                │                           │
                ▼                           ▼
        script.leaving_home       script.arriving_home
```

## Setup Steps

### Step 1: Create Away Mode Helper

**In Home Assistant:**

1. Go to **Settings** → **Devices & Services** → **Helpers**
2. Click **Create Helper** → **Toggle**
3. Name: `Away Mode`
4. Entity ID should be: `input_boolean.away_mode`
5. Icon: `mdi:home-export-outline`
6. Click **Create**

**What it does:**
- Tracks whether you're currently home or away
- Prevents duplicate triggers (e.g., both geofence AND door sensor firing)
- All automations check this state before triggering

### Step 2: Set Up Person Entity

**In Home Assistant:**

1. Go to **Settings** → **People**
2. Click on your name
3. Link to **device_tracker** entities from your phone
4. Entity ID should be: `person.you` (or your name)

**What it does:**
- Combines multiple device trackers (HA app, router, etc.)
- Provides unified "home" or "not_home" state
- Used by geofencing automation

### Step 3: Install Home Assistant Companion App

**On your iPhone:**

1. Download **Home Assistant** app from App Store
2. Log in to your HA instance
3. Go to **Settings** → **Companion App** → **Location**
4. Enable **Location Tracking**
5. Set update interval: **Every update** (most accurate)
6. Allow **Always** location access in iOS Settings

**Important settings:**
- ✅ Background App Refresh: ON
- ✅ Precise Location: ON
- ✅ Location Services: Always
- ✅ Low Power Mode compatible: ON

### Step 4: Configure Home Zone

**In Home Assistant:**

1. Go to **Settings** → **Areas & Zones**
2. Edit **Home** zone
3. Set radius: **100-150 meters** (start with 100m)
4. Verify map shows accurate home location
5. Save

**Tuning tips:**
- Too small (50m): May trigger while still in apartment
- Too large (500m): Won't trigger until you're far away
- Start at 100m, adjust based on false positives

### Step 5: Add Presence Automations

**Copy automations from repo:**

1. Copy contents of `automations/presence-detection.yaml`
2. Paste into **Home Assistant** → **Settings** → **Automations & Scenes**
3. Or add to your `automations.yaml` file
4. Reload automations

**Update entity IDs:**
- `person.you` → your actual person entity
- `binary_sensor.front_door` → your actual door sensor
- `fan.air_purifier` → your actual purifier entity
- `binary_sensor.window_sensor` → your window sensor

### Step 6: Add Scripts

**Copy scripts from repo:**

1. Copy `scripts/leaving-home.yaml` content
2. Copy `scripts/arriving-home.yaml` content
3. Add to HA scripts configuration
4. Reload scripts

**Update entity IDs** in scripts to match your actual devices.

### Step 7: Test Each Layer

#### Test Geofencing:

1. **Leaving test**:
   - Check current state: `input_boolean.away_mode` should be OFF
   - Walk 150m away from home with phone
   - Wait 2 minutes (geofence delay)
   - Check automation triggered
   - Verify notification received
   - Check `input_boolean.away_mode` is now ON

2. **Arriving test**:
   - Walk back toward home
   - As soon as you cross zone boundary, automation should trigger
   - Check notification
   - Verify `input_boolean.away_mode` is now OFF

#### Test Door Sensor Backup:

1. **Simulate geofence failure**:
   - Turn off phone location OR airplane mode
   - Manually set `input_boolean.away_mode` to OFF
   - Open front door, walk out, close door
   - Wait 30 seconds
   - Check automation triggered
   - Verify away mode activated

2. **Arriving via door**:
   - Manually set `input_boolean.away_mode` to ON
   - Open front door, walk in, close door
   - Wait 10 seconds
   - Check automation triggered

#### Test NFC Manual Override:

1. **Create iPhone Shortcut**:
   - Open Shortcuts app
   - Create new Automation → NFC
   - Scan your NFC tag
   - Add action: **Call Service**
     - Service: `script.leaving_home` or `script.arriving_home`
   - Or toggle `input_boolean.away_mode`

2. **Test**:
   - Tap NFC tag
   - Verify script runs
   - Check lights, purifier, etc. respond

## Tuning & Optimization

### Reduce False Positives

**If triggering too often:**

- **Increase geofence delay**: Change `for: minutes: 2` to `3` or `5`
- **Increase zone radius**: Make home zone larger
- **Increase door delay**: Change `delay: seconds: 30` to `60`

**If not triggering when it should:**

- **Decrease geofence delay**: Change to `1` minute
- **Decrease zone radius**: Make home zone smaller
- **Check phone battery saver**: Might limit location updates

### Monitor Which Method Triggers

Check your notifications:
- "geofence" = Primary working ✅
- "door sensor backup" = Geofence missed, backup working ✅
- Manual NFC often = Automation not triggering, needs tuning ⚠️

**Ideal state:** 80%+ geofence, 10-20% door backup, rarely NFC

## Troubleshooting

### Geofencing Not Working

**Phone location not updating:**
- Check HA Companion app has location permission
- Verify "Always" location access in iOS Settings
- Restart HA Companion app
- Check `person.you` entity shows current location

**Geofence too sensitive:**
- Increase zone radius to 150m
- Increase delay to 3-5 minutes
- Check for GPS drift (location bouncing)

**Battery drain concerns:**
- HA app uses minimal battery (< 2% per day)
- iOS optimizes background location
- Can disable if concerned, rely on door sensor

### Door Sensor Not Working

**Sensor not responding:**
- Check battery level
- Verify paired to Zigbee coordinator
- Check signal strength (may need repeater)
- Test sensor manually in HA dashboard

**False triggers:**
- Increase delay from 30s to 60s
- Add condition to check time of day
- Disable if geofencing works well

### Duplicate Triggers

**Both geofence AND door fire:**
- This is normal occasionally
- `input_boolean.away_mode` prevents duplicate actions
- Scripts run only once
- Check notifications to see which triggered first

## Advanced: Conditional Behaviors

### Different modes for different times

```yaml
# Night mode - quieter arriving home
- if:
    - condition: time
      after: "22:00:00"
      before: "07:00:00"
  then:
    # Dim lights, quiet purifier
    - service: light.turn_on
      data:
        brightness_pct: 30
```

### Guest mode

Create `input_boolean.guest_mode`:
- When enabled, disable away automations
- Allows guest to come/go without triggering

### Vacation mode

Create `input_boolean.vacation_mode`:
- Overrides away mode
- Keeps some lights on schedule
- Ignores door sensor
- Security monitoring only

## Privacy Considerations

**What's tracked:**
- Phone location (local to HA, not cloud)
- Home/not_home state
- Door open/close events

**What's NOT tracked:**
- Specific locations outside home
- Movement patterns (unless you enable)
- Shared with third parties

**To disable location:**
- Turn off HA Companion app location
- Rely only on door sensor
- Manual NFC control

## Monitoring & Maintenance

### Weekly Check:
- Review automation traces in HA
- Check battery levels on sensors
- Verify notifications working

### Monthly:
- Review which detection method is most reliable
- Adjust delays/zones if needed
- Update automations based on patterns

### Yearly:
- Replace sensor batteries
- Review and clean up unused automations
- Update HA Companion app

## Summary

**You have 3 ways to detect leaving/arriving:**

1. **Automatic** (Geofencing) - Works 80%+ of the time
2. **Backup** (Door sensor) - Catches the 20% geofence misses
3. **Manual** (NFC tag) - When you want direct control

**All three can work together** - whichever triggers first wins, others are ignored until state changes.

This gives you the most reliable presence detection possible for a smart home!
