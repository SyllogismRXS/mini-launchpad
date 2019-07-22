#!/usr/bin/env python

import os
import time
import argparse
import subprocess
import tempfile
import shutil
from argparse import ArgumentDefaultsHelpFormatter
from threading import Thread

from watchdog.observers import Observer
from watchdog.events import LoggingEventHandler
from watchdog.events import FileSystemEventHandler

def get_package_details(changes_file):
    name = 'INVALID'
    filenames = [changes_file]
    storing_filenames = False

    with open(changes_file, 'r') as f:
        for line in f:
            if "Binary:" in line:
                tokens = line.strip().split(' ')
                name = tokens[1]

            if storing_filenames:
                tokens = line.strip().split(' ')
                filenames.append(tokens[4])

            if line.strip() == 'Files:':
                storing_filenames = True

    details = {}
    details['name'] = name
    details['filenames'] = filenames

    return details

def binary_deb_arch(deb_file):
    cmd = 'dpkg-deb --field ' + deb_file + ' Architecture'
    try:
        arch = subprocess.check_output(cmd.split()).strip()
        return arch
    except Exception as e:
        print(e)
    return "INVALID"

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
        add('-n', '--no-changes-file', default=False, action='store_true')
        add('-v', '--allow-same-version', default=False, action='store_true')

        self.args = parser.parse_args()

        # Create the required directories if they don't exist
        if not os.path.exists(self.args.base_repository):
            os.makedirs(self.args.base_repository)
        if not os.path.exists(self.args.incoming_dir):
            print('WARNING: Incoming directory does not exist: %s' % self.args.incoming_dir)

        self.remove_oninit(self.args.incoming_dir)

        self.watch(self.args.incoming_dir)

    def watch(self, path):
        self.event_handler = self
        self.observer = Observer()
        self.observer.schedule(self.event_handler, path, recursive=True)
        self.observer.start()

    def on_any_event(self, event):
        if not self.args.no_changes_file and event.event_type == 'created' and event.src_path.endswith('.changes'):
            thread = Thread(target = self.process_changes_upload, args = (event.src_path,))
            thread.start()

        elif self.args.no_changes_file and event.event_type == 'created' and event.src_path.endswith('.deb'):
            thread = Thread(target = self.process_binary_upload, args = (event.src_path,))
            thread.start()

    def process_binary_upload(self, debian_file):
        print('Debian binary file uploaded: waiting 3 seconds...')
        time.sleep(3)

        # Get the package name from the .deb file
        cmd = 'dpkg-deb --field ' + debian_file + ' Package'
        package_name = subprocess.check_output(cmd.split()).strip()

        # Move the uploaded debian file into a temporary directory
        input_files_tmp_dir = tempfile.mkdtemp()
        shutil.move(debian_file, input_files_tmp_dir + "/")

        self.process_deb(input_files_tmp_dir, package_name)
        shutil.rmtree(input_files_tmp_dir)

    def process_changes_upload(self, changes_file):
        print('Changes file uploaded: waiting 3 seconds...')
        time.sleep(3)

        input_files_tmp_dir = tempfile.mkdtemp()

        # Move the changes file and package related files to temp dir
        details = get_package_details(changes_file)
        for f in details['filenames']:
            shutil.move(os.path.join(self.args.incoming_dir, f), input_files_tmp_dir + "/")

        self.process_deb(input_files_tmp_dir, details['name'])
        shutil.rmtree(input_files_tmp_dir)

    def process_deb(self, dir_path, package_name):
        deb_filename = 'INVALID'
        for file in os.listdir(dir_path):
            if file.endswith(".deb"):
                deb_filename = os.path.join(dir_path, file)

        arch = binary_deb_arch(deb_filename)

        if self.package_exists(package_name, arch):
            if self.args.allow_same_version:
                print('Removing package that already exists: %s' % package_name)
                self.remove_package(package_name, arch)
            else:
                print('Package already exists, but not removing: %s' % package_name)

        cmd = 'reprepro -b ' + self.args.base_repository + ' includedeb ' \
            + self.args.distribution + ' ' + deb_filename
        print(cmd)

        try:
            subprocess.check_call(cmd.split())
        except Exception as e:
            print(e)

    def package_exists(self, package_name, arch):
        cmd = 'reprepro -b ' + self.args.base_repository \
            + ' --architecture ' + arch + ' ls ' + package_name
        try:
            result = subprocess.check_output(cmd.split()).strip()
            if result == "":
                return False
        except Exception as e:
            print(e)

        return True

    def remove_package(self, package_name, arch):
        cmd = 'reprepro -b ' + self.args.base_repository \
            + ' --architecture ' + arch + ' remove ' \
            + self.args.distribution + ' ' + package_name
        print(cmd)

        try:
            subprocess.check_call(cmd.split())
        except Exception as e:
            print(e)

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
