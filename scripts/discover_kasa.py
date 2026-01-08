#!/usr/bin/env python3
"""
Discover and list all TP-Link Kasa devices on the network.
"""
import asyncio
import json
from kasa import Discover

async def main():
    print("Scanning network for Kasa devices...\n")

    devices = await Discover.discover(timeout=5)

    if not devices:
        print("No Kasa devices found!")
        return

    bulbs = []
    plugs = []

    for addr, dev in devices.items():
        await dev.update()

        device_info = {
            'ip': addr,
            'alias': dev.alias,
            'model': dev.model,
            'mac': dev.mac,
            'is_on': dev.is_on,
        }

        if dev.is_bulb:
            if dev.is_variable_color_temp:
                device_info['brightness'] = dev.brightness
                device_info['color_temp'] = dev.color_temp
            bulbs.append(device_info)
        elif dev.is_plug:
            device_info['current_consumption'] = getattr(dev, 'current_consumption', 'N/A')
            plugs.append(device_info)

    print(f"Found {len(bulbs)} bulb(s) and {len(plugs)} plug(s)\n")

    if bulbs:
        print("=== BULBS ===")
        for bulb in bulbs:
            print(f"\n  {bulb['alias']}")
            print(f"    IP: {bulb['ip']}")
            print(f"    Model: {bulb['model']}")
            print(f"    MAC: {bulb['mac']}")
            print(f"    State: {'ON' if bulb['is_on'] else 'OFF'}")
            if 'brightness' in bulb:
                print(f"    Brightness: {bulb['brightness']}%")
            if 'color_temp' in bulb:
                print(f"    Color Temp: {bulb['color_temp']}K")

    if plugs:
        print("\n=== PLUGS ===")
        for plug in plugs:
            print(f"\n  {plug['alias']}")
            print(f"    IP: {plug['ip']}")
            print(f"    Model: {plug['model']}")
            print(f"    MAC: {plug['mac']}")
            print(f"    State: {'ON' if plug['is_on'] else 'OFF'}")
            if plug['current_consumption'] != 'N/A':
                print(f"    Power: {plug['current_consumption']}W")

    # Save to YAML format for device documentation
    print("\n\n=== Device YAML (for devices/ directory) ===\n")

    if bulbs:
        print("# Kasa Smart Bulbs")
        print("bulbs:")
        for bulb in bulbs:
            print(f"  - alias: {bulb['alias']}")
            print(f"    ip: {bulb['ip']}")
            print(f"    model: {bulb['model']}")
            print(f"    mac: {bulb['mac']}")

    if plugs:
        print("\n# Kasa Smart Plugs")
        print("plugs:")
        for plug in plugs:
            print(f"  - alias: {plug['alias']}")
            print(f"    ip: {plug['ip']}")
            print(f"    model: {plug['model']}")
            print(f"    mac: {plug['mac']}")

if __name__ == "__main__":
    asyncio.run(main())
