# This file is part of pyrasite.
#
# pyrasite is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# pyrasite is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with pyrasite.  If not, see <http://www.gnu.org/licenses/>.
#
# Copyright (C) 2011-2013 Red Hat, Inc., Luke Macken <lmacken@redhat.com>

import os
import sys
import argparse

import pyrasite


def shell(args):
    """Open a Python shell in a running process"""
    ipc = pyrasite.PyrasiteIPC(args.pid, 'ReversePythonShell',
                               timeout=os.getenv('PYRASITE_IPC_TIMEOUT') or 5)
    ipc.connect()

    print("Pyrasite Shell %s" % pyrasite.__version__)
    print("Connected to '%s'" % ipc.title)

    prompt, payload = ipc.recv().split('\n', 1)
    print(payload)

    try:
        import readline
    except ImportError:
        pass

    if args.cmd:
        try:
            ipc.send(cmd)
            payload = ipc.recv()
            if payload is None:
                ipc.close()
                return
            prompt, payload = payload.split('\n', 1)
            if payload != '':
                print(payload)
        except:
            print('')
            raise
        finally:
            ipc.close()

    # py3k compat
    try:
        input_ = raw_input
    except NameError:
        input_ = input

    try:
        while True:
            try:
                input_line = input_(prompt)
            except EOFError:
                input_line = 'exit()'
                print('')
            except KeyboardInterrupt:
                input_line = 'None'
                print('')

            ipc.send(input_line)
            payload = ipc.recv()
            if payload is None:
                break
            prompt, payload = payload.split('\n', 1)
            if payload != '':
                print(payload)
    except:
        print('')
        raise
    finally:
        ipc.close()


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("PID", dest="pid", type=int)
    parser.add_argument(
        "-c",
        "--cmd",
        dest="cmd",
        type=str
    )
    return parser.parse_args()


if __name__ == '__main__':
    args = parse_args()
    shell(args)
