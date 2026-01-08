#!/bin/bash
# Setup Sonoff Zigbee dongle with Home Assistant using ZHA (Zigbee Home Automation)

set -e

echo "=== Sonoff Zigbee Dongle Setup (ZHA) ==="
echo ""

# Check if dongle is detected
if [ ! -e /dev/ttyUSB0 ]; then
    echo "❌ Zigbee dongle not found at /dev/ttyUSB0"
    echo "   Please check USB connection"
    exit 1
fi

echo "✓ Zigbee dongle detected at /dev/ttyUSB0"
echo ""

# Get dongle info
DONGLE_PATH=$(readlink -f /dev/serial/by-id/usb-Itead_Sonoff_Zigbee_3.0_USB_Dongle_Plus_V2_* 2>/dev/null || echo "/dev/ttyUSB0")
echo "Device path: $DONGLE_PATH"
echo ""

# Check if HomeAssistant container exists
if ! docker ps -a | grep -q homeassistant; then
    echo "❌ Home Assistant container not found"
    echo "   Please set up Home Assistant first"
    exit 1
fi

echo "✓ Home Assistant container found"
echo ""

# Check if device is already mounted
if docker inspect homeassistant | grep -q "$DONGLE_PATH"; then
    echo "✓ Zigbee dongle already mounted in Home Assistant"
else
    echo "📝 Adding Zigbee dongle to Home Assistant..."
    echo ""
    echo "You need to add this to your docker-compose.yml:"
    echo ""
    echo "  homeassistant:"
    echo "    devices:"
    echo "      - $DONGLE_PATH:/dev/ttyUSB0"
    echo ""
    echo "Then restart Home Assistant:"
    echo "  docker-compose restart homeassistant"
    echo ""
fi

echo "=== Next Steps ==="
echo ""
echo "1. Go to Home Assistant: http://localhost:8123"
echo "2. Navigate to: Settings → Devices & Services"
echo "3. Click '+ ADD INTEGRATION'"
echo "4. Search for 'Zigbee Home Automation' (ZHA)"
echo "5. Select device path: $DONGLE_PATH"
echo "6. Choose 'EZSP' as radio type (for Sonoff dongle)"
echo "7. Leave other settings as default"
echo "8. Click Submit"
echo ""
echo "Once ZHA is set up, you can pair devices:"
echo "- Click 'ADD DEVICE' in ZHA integration"
echo "- Put your Aqara sensor in pairing mode (hold button for 5s)"
echo "- Wait for device to be discovered"
echo ""
