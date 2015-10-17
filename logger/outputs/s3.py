#! /usr/bin/env python3

import asyncio
import boto3
from io import BytesIO

_records = []
_max_qlen = 0
_ev_flush = None

def init(loop, opts):
    global _max_qlen, _ev_flush
    ev = asyncio.Event(loop=loop)
    _ev_flush = ev
    interval = opts.get('flush_interval', 30)
    if interval > 0:
        asyncio.ensure_future(s3_flush_timer(loop, interval, ev), loop=loop)
    _max_qlen = opts.get('max_queue_length', 0)
    asyncio.ensure_future(s3_flusher(loop, opts, ev), loop=loop)

async def s3_flush_timer(loop, interval, ev):
    global _records, _max_qlen
    while True:
        await asyncio.sleep(interval)
        if len(_records) > 0:
            ev.set()

async def s3_flusher(loop, opts, ev):
    global _records
    # TODO: replace this with asyncio-enabled version in the future
    #       (e.g., https://github.com/jettify/aiobotocore)
    # TODO: support for different codecs
    buffer = BytesIO()
    while True:
        await ev.wait()
        ev.clear()
        #print('flushed {} records'.format(len(_records)))
        #for r in _records:
        #    print(r)
        packer = umsgpack.Packer()
        for rec in _records:
            buffer.write(packer.pack(rec))
        _records.clear()
        # TODO: apply credentials
        s3 = boto3.resource('s3')
        bucket = s3.Bucket(opts['bucket'])
        resp = bucket.put_object(Key='<mangled_logname>', Body=buffer.getvalue())

def enqueue(records):
    global _records, _max_qlen
    _records.extend(records)
    if _max_qlen == 0 or (_max_qlen > 0 and len(_records) >= _max_qlen):
        _ev_flush.set()
