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

        # TODO: reload support using imp.reload()
        self.input_mods = []
        self.filter_mods = []
        self.output_mods = []

        for name, opts in self.inputs.items():
            try:
                mod = importlib.import_module('..inputs.{}'.format(name), __name__)
                mod.init(opts)
                self.input_mods.append(mod)
            except ImportError:
                print('Could not load inputs.{} module.'.format(name),
                      file=sys.stderr)

        for name, opts in self.filters.items():
            try:
                mod = importlib.import_module('..filters.{}'.format(name), __name__)
                mod.init(opts)
                self.filter_mods.append(mod)
            except ImportError:
                print('Could not load filters.{} module.'.format(name),
                      file=sys.stderr)

        for name, opts in self.outputs.items():
            try:
                mod = importlib.import_module('..outputs.{}'.format(name), __name__)
                mod.init(opts)
                self.output_mods.append(mod)
            except ImportError:
                print('Could not load outputs.{} module.'.format(name),
                      file=sys.stderr)

    async def serve(self):
        print('begin')
        await asyncio.sleep(1)
        print('end')
