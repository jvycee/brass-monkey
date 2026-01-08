#!/usr/bin/env python3
"""
Control TP-Link Kasa devices from command line.

Examples:
    ./kasa_control.py --list
    ./kasa_control.py --on "Paper lamp - low"
    ./kasa_control.py --off all
    ./kasa_control.py --brightness 50 "Bedside lamp - 1"
    ./kasa_control.py --blink "Egg lamp"
"""
import asyncio
import argparse
from kasa import Discover, SmartDevice

async def discover_devices():
    """Discover all Kasa devices on network."""
    devices = await Discover.discover(timeout=5)
    device_dict = {}
    for addr, dev in devices.items():
        await dev.update()
        device_dict[dev.alias] = dev
    return device_dict

async def list_devices():
    """List all devices."""
    devices = await discover_devices()
    print(f"\nFound {len(devices)} device(s):\n")
    for alias, dev in devices.items():
        state = "ON" if dev.is_on else "OFF"
        device_type = "Bulb" if dev.is_bulb else "Plug"
        print(f"  [{state}] {alias} ({device_type}) - {dev.host}")

async def turn_on(target):
    """Turn on device(s)."""
    devices = await discover_devices()

    if target.lower() == "all":
        for dev in devices.values():
            await dev.turn_on()
            print(f"✓ Turned on {dev.alias}")
    else:
        if target in devices:
            await devices[target].turn_on()
            print(f"✓ Turned on {target}")
        else:
            print(f"❌ Device '{target}' not found")

async def turn_off(target):
    """Turn off device(s)."""
    devices = await discover_devices()

    if target.lower() == "all":
        for dev in devices.values():
            await dev.turn_off()
            print(f"✓ Turned off {dev.alias}")
    else:
        if target in devices:
            await devices[target].turn_off()
            print(f"✓ Turned off {target}")
        else:
            print(f"❌ Device '{target}' not found")

async def set_brightness(target, brightness):
    """Set brightness for bulb(s)."""
    devices = await discover_devices()

    if target.lower() == "all":
        for dev in devices.values():
            if dev.is_bulb:
                await dev.set_brightness(brightness)
                print(f"✓ Set {dev.alias} brightness to {brightness}%")
    else:
        if target in devices:
            dev = devices[target]
            if dev.is_bulb:
                await dev.set_brightness(brightness)
                print(f"✓ Set {target} brightness to {brightness}%")
            else:
                print(f"❌ {target} is not a bulb")
        else:
            print(f"❌ Device '{target}' not found")

async def blink_device(target):
    """Blink device(s) to identify them."""
    devices = await discover_devices()

    async def blink(dev):
        """Blink a single device."""
        original_state = dev.is_on
        print(f"Blinking {dev.alias}...")

        for _ in range(3):
            await dev.turn_off()
            await asyncio.sleep(0.5)
            await dev.turn_on()
            await asyncio.sleep(0.5)

        # Restore original state
        if original_state:
            await dev.turn_on()
        else:
            await dev.turn_off()

        print(f"✓ Blinked {dev.alias}")

    if target.lower() == "all":
        for dev in devices.values():
            await blink(dev)
    else:
        if target in devices:
            await blink(devices[target])
        else:
            print(f"❌ Device '{target}' not found")

def main():
    parser = argparse.ArgumentParser(description="Control TP-Link Kasa devices")
    parser.add_argument("--list", action="store_true", help="List all devices")
    parser.add_argument("--on", metavar="DEVICE", help="Turn on device (use 'all' for all devices)")
    parser.add_argument("--off", metavar="DEVICE", help="Turn off device (use 'all' for all devices)")
    parser.add_argument("--brightness", type=int, metavar="LEVEL", help="Set brightness (0-100)")
    parser.add_argument("--blink", metavar="DEVICE", help="Blink device to identify (use 'all' for all devices)")
    parser.add_argument("device", nargs="?", help="Device name (for brightness)")

    args = parser.parse_args()

    if args.list:
        asyncio.run(list_devices())
    elif args.on:
        asyncio.run(turn_on(args.on))
    elif args.off:
        asyncio.run(turn_off(args.off))
    elif args.blink:
        asyncio.run(blink_device(args.blink))
    elif args.brightness is not None:
        if not args.device:
            print("❌ Please specify a device name or 'all'")
        else:
            asyncio.run(set_brightness(args.device, args.brightness))
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
