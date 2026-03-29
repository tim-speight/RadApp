from caproto.server import pvproperty, PVGroup, ioc_arg_parser, run
import requests
import time

class RadAppIOC(PVGroup):
    box1_remaining = pvproperty(value=0)
    box1_colour = pvproperty(value="green")

    async def update(self):
        while True:
            data = requests.get("http://<pi-ip>:8080/status").json()
            box1 = data[0]

            await self.box1_remaining.write(box1["remaining"])
            await self.box1_colour.write(box1["colour"])

            await asyncio.sleep(1)

if __name__ == "__main__":
    ioc_options, run_options = ioc_arg_parser(default_prefix="RADAPP:")
    ioc = RadAppIOC(**ioc_options)
    run(ioc.pvdb, **run_options)