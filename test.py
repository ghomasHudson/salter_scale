import asyncio
from bleak import BleakScanner, BleakClient

weight_service_uuid = "0000ffe0-0000-1000-8000-00805f9b34fb"
weight_char_uuid = "0000ffe1-0000-1000-8000-00805f9b34fb"
weight_map = ["g", "oz", "ml", "fl. oz"]

async def main():
    devices = await BleakScanner.discover()
    for d in devices:
        if d.name == "KG2362BT":
            async with BleakClient(d.address) as client:
                svcs = await client.get_services()
                def callback(sender,data):
                    weight = data[-2]
                    if data[-3] != 0:
                        weight = weight * -1
                    print(f"Weight: {weight}{weight_map[data[-1]]}")
                await client.start_notify(weight_char_uuid, callback)
                await asyncio.sleep(30.0)
                await client.stop_notify(weight_char_uuid)

asyncio.run(main())
