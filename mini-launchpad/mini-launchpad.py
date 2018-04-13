#!/usr/bin/env python

import sys
import time
import logging
import os
import shutil
import tempfile
import argparse
import subprocess

from watchdog.observers import Observer
from watchdog.events import LoggingEventHandler
from watchdog.events import FileSystemEventHandler

class cd:
    """Context manager for changing the current working directory"""
    def __init__(self, newPath):
        self.newPath = os.path.expanduser(newPath)

    def __enter__(self):
        self.savedPath = os.getcwd()
        os.chdir(self.newPath)

    def __exit__(self, etype, value, traceback):
        os.chdir(self.savedPath)


class MiniLaunchpad (FileSystemEventHandler):
    def __init__(self):
        # TODO : use argparse to get arguments
        #parser = argparse.ArgumentParser(description='SCRIMMAGE Plotter')
        #add = parser.add_argument
        #add('-c', '--csv_filename', help='CSV filename. (e.g., trajectory.csv)', required=True)
        #args = parser.parse_args()

        self.file_list = []

        self.watch('/home/ftp') # TODO use argument

    def on_any_event(self, event):
        if event.event_type == 'created':
            self.file_list.append(event.src_path)

        if event.event_type == 'created' and event.src_path.endswith('.changes'):
            self.process_upload()

    def watch(self, path):
        self.event_handler = self
        self.observer = Observer()
        self.observer.schedule(self.event_handler, path, recursive=True)
        self.observer.start()

    def process_upload(self):
        print('Waiting 2 seconds...')
        time.sleep(2)
        print('Processing upload')

        # move the input files out of the incoming ftp directory
        input_files_tmp_dir = tempfile.mkdtemp()
        print('Input files tmp dir: %s' % input_files_tmp_dir)
        for f in self.file_list:
            shutil.move(f, input_files_tmp_dir + "/")
        self.file_list = []

        # TODO use arguments to specify distribution and architectures to build
        self.build_package(input_files_tmp_dir, "xenial", "amd64")
        self.build_package(input_files_tmp_dir, "xenial", "armhf")
        self.build_package(input_files_tmp_dir, "xenial", "arm64")
        self.build_package(input_files_tmp_dir, "xenial", "i386")

        shutil.rmtree(input_files_tmp_dir)

    def build_package(self, input_files_tmp_dir, dist, arch):
        # TODO for each build, write output to different log file

        # create a temporary directory for this build
        tmp_dir = tempfile.mkdtemp()
        print('Temp dir (%s, %s): %s' % (dist, arch, tmp_dir))

        for f in os.listdir(input_files_tmp_dir):
            shutil.copy(os.path.join(input_files_tmp_dir, f), tmp_dir + "/")

        with cd(tmp_dir):
            dsc_file = None
            for file in os.listdir(tmp_dir):
                if file.endswith(".dsc"):
                    dsc_file = file

            if dsc_file is None:
                print('Cannot find dsc file')
                return

            config_file= "/home/syllogismrxs/.pbuilderrc" # TODO configurable

            cmd = "DIST="+dist+" ARCH="+arch+" pbuilder --build " \
                  "--configfile "+config_file+" " \
                  "--distribution "+dist+" " \
                  "--architecture "+arch+" --basetgz " \
                  "/var/cache/pbuilder/"+dist+"-"+arch+"-base.tgz " \
                  "--buildresult ./ " + dsc_file

            print('Command: %s', cmd)
            subprocess.call(cmd, shell=True)

            dput_success = False
            for file in os.listdir(tmp_dir):
                if file.endswith(arch + ".changes"):
                    # TODO make --config argument configurable
                    dput_cmd = "dput --config /home/syllogismrxs/.dput.cf " + \
                               "gtri-binary " + file
                    print("dput command: %s" % dput_cmd)
                    subprocess.call(dput_cmd, shell=True)
                    dput_success = True
                    #shutil.move(file, "/home/syllogismrxs/python/temp/")

            if not dput_success:
                print('Failed to dput')
                subprocess.call("ls")

        print('Removing tmp dir: %s' % tmp_dir)
        shutil.rmtree(tmp_dir)

    def run(self):
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            self.observer.stop()
        self.observer.join()

if __name__ == "__main__":
    ml = MiniLaunchpad()
    ml.run()
