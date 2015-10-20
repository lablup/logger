#! /usr/bin/env python3

import asyncio
import enum
import zmq, aiozmq
from ..record import Record

_records = []

class Topologies(enum.Enum):
    pubsub = zmq.SUB
    reqrep = zmq.REQ
    routerdealer = zmq.ROUTER

def init(loop, opts, rec_avail_ev):
    topo = Topologies[opts['topology']].value
    server = loop.run_until_complete(
            aiozmq.create_zmq_stream(topo, bind=opts['endpoint'], loop=loop))
    if topo == zmq.SUB:
        server.transport.setsockopt(zmq.SUBSCRIBE, b'')
    asyncio.ensure_future(zmq_fetcher(loop, server, rec_avail_ev), loop=loop)

async def zmq_fetcher(loop, server, rec_avail_ev):
    global _records
    while True:
        try:
            recv_data = await server.read()
        except aiozmq.stream.ZmqStreamClosed:
            break
        rec = Record.parse(recv_data[0])
        _records.append(rec)

        # Notify the logger loop to proceed.
        rec_avail_ev.set()

    server.close()

def fetch():
    global _records
    while _records:
        yield _records.pop(0)
