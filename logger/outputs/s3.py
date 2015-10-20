#! /usr/bin/env python3

import asyncio
import aiobotocore
from datetime import datetime
import io
import umsgpack

_records = []
_max_qlen = 0
_ev_flush = None

def init(loop, opts):
    global _max_qlen, _ev_flush
    assert opts['codec'] in ('msgpack', 'text')
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
    buffer = io.BytesIO()
    part_count = 1
    while True:
        await ev.wait()
        ev.clear()
        print('s3: flushing {} entries...'.format(len(_records)))
        if opts['codec'] == 'msgpack':
            packer = umsgpack.Packer()
            for rec in _records:
                buffer.write(packer.pack(rec.data))
        elif opts['codec'] == 'text':
            for rec in _records:
                print(str(rec).encode('utf8'), file=buffer)
        _records.clear()  # must be cleared before any await
        session = aiobotocore.get_session(loop=loop)
        client = session.create_client('s3', region_name=opts['region'],
                                       aws_secret_access_key=opts['secret_key'],
                                       aws_access_key_id=opts['access_key'])
        ts = datetime.now().strftime('%Y-%m-%dT%H.%M.%S')
        key = '{}.{}.part{}.msgpack'.format(opts['key_prefix'], ts, part_count)
        resp = await client.put_object(Bucket=opts['bucket'],
                                       Key=key,
                                       Body=buffer.getvalue(),
                                       ACL='private')
        buffer.seek(0, io.SEEK_SET)
        buffer.truncate(0)
        part_count += 1

def enqueue(records):
    global _records, _max_qlen
    _records.extend(records)
    if _max_qlen == 0 or (_max_qlen > 0 and len(_records) >= _max_qlen):
        _ev_flush.set()
