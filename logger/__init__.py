#! /usr/bin/env python3

import argparse
import asyncio
import toml
from .server import ServerLoop

def main():
    argparser = argparse.ArgumentParser()
    argparser.add_argument('-f', '--config', type=str, help='The path to configuration file.')
    args = argparser.parse_args()

    with open(args.config, 'r') as fin:
        config = toml.loads(fin.read())

    loop = asyncio.get_event_loop()
    server = ServerLoop(loop, config['inputs'], config['filters'], config['outputs'])
    asyncio.async(server.serve(), loop=loop)
    try:
        loop.run_forever()
    except (KeyboardInterrupt, SystemExit):
        for t in asyncio.Task.all_tasks():
            t.cancel()
        try:
            loop.run_until_complete(asyncio.sleep(0))
        except asyncio.CancelledError:
            pass
    finally:
        loop.close()
        print('exit.')
