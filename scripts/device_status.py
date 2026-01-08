#!/usr/bin/env python3
"""
Get status of all Kasa devices and generate a summary.
"""
import asyncio
import json
from datetime import datetime
from kasa import Discover

async def main():
    print(f"Device Status Report - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 70)
    print()

    devices = await Discover.discover(timeout=5)

    if not devices:
        print("⚠️  No Kasa devices found on network")
        print("   - Check WiFi connection")
        print("   - Ensure devices are powered on")
        print("   - Verify they're on same network as this server")
        return

    total_power = 0
    online_count = len(devices)

    # Separate devices by type
    bulbs = []
    plugs = []

    for addr, dev in devices.items():
        await dev.update()

        if dev.is_bulb:
            bulbs.append((addr, dev))
        elif dev.is_plug:
            plugs.append((addr, dev))

    # Display bulbs
    if bulbs:
        print("💡 SMART BULBS")
        print("-" * 70)
        for addr, dev in bulbs:
            status = "🟢 ON " if dev.is_on else "⚫ OFF"
            print(f"\n{status} {dev.alias}")
            print(f"       IP: {addr}")
            print(f"       Model: {dev.model}")

            if dev.is_on and dev.is_variable_color_temp:
                print(f"       Brightness: {dev.brightness}%")
                print(f"       Color Temp: {dev.color_temp}K")

                if hasattr(dev, 'current_consumption'):
                    power = dev.current_consumption
                    total_power += power
                    print(f"       Power: {power:.1f}W")

        print()

    # Display plugs
    if plugs:
        print("🔌 SMART PLUGS")
        print("-" * 70)
        for addr, dev in plugs:
            status = "🟢 ON " if dev.is_on else "⚫ OFF"
            print(f"\n{status} {dev.alias}")
            print(f"       IP: {addr}")
            print(f"       Model: {dev.model}")

            if hasattr(dev, 'current_consumption'):
                power = dev.current_consumption
                total_power += power
                if dev.is_on:
                    print(f"       Power: {power:.1f}W")

        print()

    # Summary
    print("=" * 70)
    print(f"📊 SUMMARY")
    print(f"   Devices Online: {online_count}")
    print(f"   Bulbs: {len(bulbs)}")
    print(f"   Plugs: {len(plugs)}")
    if total_power > 0:
        print(f"   Total Power Consumption: {total_power:.1f}W")
    print()

if __name__ == "__main__":
    asyncio.run(main())
