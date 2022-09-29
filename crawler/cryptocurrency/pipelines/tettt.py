import asyncio
import time

async def coro():
    await asyncio.sleep(2)


async def main():
    tasks = []
    print('Tasks count: ', len(asyncio.Task.all_tasks()))
    for idx in range(100):
        task = asyncio.ensure_future(coro())
        tasks.append(task)
        print('Tasks count: ', len(asyncio.Task.all_tasks()))
    await asyncio.gather(*tasks)
    # print('Tasks count: ', len(asyncio.Task.all_tasks()))


def run():

    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
    while True:
        print(loop.is_closed())
        time.sleep(3)

run()