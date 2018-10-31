#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/9/29 下午11:58
# @Author  : Komi
# @File    : scanv2.py
# @Ver:    : 0.1

import uvloop
import asyncio
import argparse
from tqdm import tqdm

#MAX_SEMAPHORE_NUM = 2048
MAX_SEMAPHORE_NUM = 200


# check port
async def check_port(target_ip, port, semaphore,timeout=1,loopm=None):
    try:
        async with semaphore:

            con = await asyncio.open_connection(target_ip, port)

            try:
                reader, writer = await asyncio.wait_for(con,timeout,loop=loopm)
                tqdm.write("%s is open " % str(port))
            except Exception as e:
                # If this is reach -> port closed
                pass
            tqdm.write("%s is open " % str(port))
    except Exception as e:
        pass

async def wait_with_progress(coroutines):
    for f in tqdm(asyncio.as_completed(coroutines),total=len(coroutines)):
        await f

def main(target_ip):
    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
    loop = asyncio.get_event_loop()

    print('[+] Setting up max semaphore number',MAX_SEMAPHORE_NUM)
    semaphore = asyncio.Semaphore(MAX_SEMAPHORE_NUM)
    tasks = []

    print('[+] Starting brute %s ports...'%target_ip)

    for p in range(1, 65535):
        tasks.append(asyncio.ensure_future(
            check_port(target_ip, p, semaphore, timeout=1, loopm=loop)))
    try:
        loop.run_until_complete(wait_with_progress(tasks))
    except KeyboardInterrupt as e:
        print('[-] Cancel task...')
        for task in asyncio.Task.all_tasks():
            task.cancel()
        loop.stop()
        loop.run_forever()
    finally:
        loop.close()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Port Scan Program', usage='python3 %(prog)s <option> <domain>', prog='subDomainsCollect.py'
    )
    parser.add_argument('-i', '--ip', dest='target_ip', help='the target ip.',
                        action='store',default='127.0.0.1')

    parser.add_argument('-v','--version', action='version', version='%(prog)s 1.0')
    args = parser.parse_args()
    if not args.target_ip:
        parser.parse_args(['-h'])
    main(args.target_ip)
