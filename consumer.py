import asyncio
import time

from ndn.app import NDNApp
from ndn.encoding import Name
from ndn.types import InterestNack, InterestTimeout, InterestCanceled, ValidationFailure

app = NDNApp()


async def main():
    async def express_interest():
        try:
            data_name, meta_info, content = await app.express_interest(
                '/hello/test',
                must_be_fresh=True,
                can_be_prefix=False,
                lifetime=6000)
            print(f'Received Data Name: {Name.to_str(data_name)}')
            print(meta_info)
            print(bytes(content) if content else None)
        except InterestNack as e:
            print(f'Nacked with reason={e.reason}')
        except InterestTimeout:
            print(f'Timeout')
        except InterestCanceled:
            print(f'Canceled')
        except ValidationFailure:
            print(f'Data failed to validate')

    jobs = [express_interest() for _ in range(50)]
    await asyncio.gather(*jobs)


async def looper():
    starttime = time.time()
    while True:
        await main()
        time.sleep(1.0 - ((time.time() - starttime) % 1.0))  # Call every second. Lock time loop to system clock.


app.run_forever(after_start=looper())
