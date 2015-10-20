#! /usr/bin/env python3

import asyncio
import importlib
import sys

class ServerLoop:

    def __init__(self, loop, inputs, filters, outputs):
        self.loop = loop
        self.inputs = inputs
        self.filters = filters
        self.outputs = outputs
        self.records_available = asyncio.Event(loop=loop)

        # TODO: reload support using imp.reload()
        self.input_mods = []
        self.filter_mods = []
        self.output_mods = []

        for name, opts in self.inputs.items():
            print('loading input module {}...'.format(name))
            mod = importlib.import_module('..inputs.{}'.format(name), __name__)
            mod.init(self.loop, opts, self.records_available)
            self.input_mods.append(mod)

        for name, opts in self.filters.items():
            print('loading filter module {}...'.format(name))
            mod = importlib.import_module('..filters.{}'.format(name), __name__)
            mod.init(self.loop, opts)
            self.filter_mods.append(mod)

        for name, opts in self.outputs.items():
            print('loading output module {}...'.format(name))
            mod = importlib.import_module('..outputs.{}'.format(name), __name__)
            mod.init(self.loop, opts)
            self.output_mods.append(mod)

    async def serve(self):
        print('started.')
        while True:
            # Wait until if any input module notifies me.
            # Via this notification scheme, we can avoid busy-waiting.
            await self.records_available.wait()
            self.records_available.clear()
            records = []
            for mod in self.input_mods:
                records.extend(mod.fetch())
            if records:
                # TODO: apply filters
                for mod in self.output_mods:
                    mod.enqueue(records)
