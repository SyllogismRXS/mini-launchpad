#!/usr/bin/env python

import os
import time
import argparse
import subprocess
from argparse import ArgumentDefaultsHelpFormatter

from watchdog.observers import Observer
from watchdog.events import LoggingEventHandler
from watchdog.events import FileSystemEventHandler

class ProcessIncoming(FileSystemEventHandler):
    def __init__(self):
        parser = argparse.ArgumentParser(description='Watch incoming debs and call reprepro',
                                         formatter_class=ArgumentDefaultsHelpFormatter)
        add = parser.add_argument
        add('-b', '--base-repository', default='/var/repositories',
            help='Base repository directory')
        add('-d', '--distribution', default='xenial',
            help='default distribution name')
        add('-i', '--incoming-dir', default='.',
            help='Incoming directory to watch')

        self.args = parser.parse_args()

        # Create the required directories if they don't exist
        if not os.path.exists(self.args.base_repository):
            os.makedirs(self.args.base_repository)
        if not os.path.exists(self.args.incoming_dir):
            os.makedirs(self.args.incoming_dir)

        self.remove_oninit(self.args.incoming_dir)

        self.watch(self.args.incoming_dir)

    def watch(self, path):
        self.event_handler = self
        self.observer = Observer()
        self.observer.schedule(self.event_handler, path, recursive=True)
        self.observer.start()

    def on_any_event(self, event):
        if event.event_type == 'created' and event.src_path.endswith('.deb'):
            print('waiting...')
            time.sleep(3)
            print('running...')
            cmd = 'reprepro -b ' + self.args.base_repository + ' includedeb ' \
                + self.args.distribution + ' ' + event.src_path
            print(cmd)
            subprocess.check_call(cmd.split())
            os.remove(event.src_path)

    def remove_oninit(self, path):
	# If our directory has something within. Purge!
	if not len(os.listdir(path)) == 0:
	    for file in os.listdir(path):
		try:
		    full_path = os.path.join(path, file)
		    os.remove(full_path)
		except:
		    print("Error removing the current file: %s" % full_path)

    def run(self):
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            self.observer.stop()
        self.observer.join()

if __name__ == "__main__":
    pi = ProcessIncoming()
    pi.run()
