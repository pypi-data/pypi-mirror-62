"""
Class for starting and stopping named timers.

This class is based on a similar java class in cyberaide, and java cog kit.

"""
from pathlib import Path
import multiprocessing
import os
import time
import sys
import platform
import humanize
import psutil
from pprint import pprint
from cloudmesh_installer.install.util import banner


def readfile(filename, mode='r'):
    """
    returns the content of a file
    :param filename: the filename
    :return:
    """
    if mode != 'r' and mode != 'rb':
        print(f"incorrect mode : expected \'r\' or \'rb\' given {mode}\n")
    else:
        with open(filename, mode)as f:
            content = f.read()
            f.close()
        return content


def systeminfo():
    data = {
        'machine': platform.machine(),
        'version': platform.version(),
        'platform': platform.platform(),
        'system': platform.system(),
        'processors': platform.system(),
        'sys': sys.platform,
        'mac_version': "",
        'win_version': "",
        'python': sys.version
    }
    try:
        data['node'] = platform.uname().node,
    except:
        data['node'] = 'unkown'
    try:
        data['release'] = platform.uname().release,
    except:
        data['release'] = ''
    try:
        data['machine'] = platform.uname().machine,
    except:
        data['machine'] = ''
    try:
        data['processor'] = platform.uname().processor,
    except:
        data['processor'] = ''

    try:
        data['user'] = os.environ['USER']
    except:
        data['user'] = ''
    try:
        data['mac_version'] = platform.mac_ver()[0]
        if data['mac_version'] == ('', '', '', ''):
            data['mac_version'] = ""
    except:
        pass
    try:
        data['win_version'] = platform.win32_ver()
        if data['win_version'] == ('', '', '', ''):
            data['win_version'] = ""
    except:
        pass

    try:
        release_files = Path("/etc").glob("*release")
        for filename in release_files:
            content = readfile(filename.resolve()).splitlines()
            for line in content:
                if "=" in line:
                    attribute, value = line.split("=", 1)
                    attribute = attribute.replace(" ", "")
                    data[attribute] = value
    except:
        pass

    return dict(data)


class StopWatch(object):
    """
    A class to measure times between events.
    """
    debug = False
    verbose = True
    # Timer start dict
    timer_start = {}
    # Timer end dict
    timer_end = {}
    # Timer diff
    timer_elapsed = {}

    @classmethod
    def keys(cls):
        """returns the names of the timers"""
        return list(cls.timer_end.keys())

    @classmethod
    def start(cls, name):
        """
        starts a timer with the given name.

        :param name: the name of the timer
        :type name: string
        """
        if cls.debug:
            print("Timer", name, "started ...")
        cls.timer_start[name] = time.time()

    @classmethod
    def stop(cls, name):
        """
        stops the timer with a given name.

        :param name: the name of the timer
        :type name: string
        """
        cls.timer_end[name] = time.time()
        if cls.debug:
            print("Timer", name, "stopped ...")

    @classmethod
    def get(cls, name):
        """
        returns the time of the timer.

        :param name: the name of the timer
        :type name: string
        :rtype: the elapsed time
        """
        if name in cls.timer_end:
            cls.timer_elapsed[name] = cls.timer_end[name] - \
                                      cls.timer_start[name]
            return cls.timer_elapsed[name]
        else:
            return "undefined"

    @classmethod
    def clear(cls):
        """
        clear start and end timer_start
        """
        cls.timer_start.clear()
        cls.timer_end.clear()

    @classmethod
    def print(cls, *args):
        """
        prints a timer. The first argument is the label if it exists, the last is the timer
        :param args: label, name 
        :return: 
        """
        if cls.verbose:
            if len(args) == 2:
                print(args[0], str("{0:.2f}".format(cls.get(args[1]))), "s")
            else:
                raise Exception("StopWatch: wrong number of arguments")

    @classmethod
    def __str__(cls):
        s = ""
        for t in cls.timer_end:
            data = {"label": t,
                    "start": str(cls.timer_start[t]),
                    "end": str(cls.timer_end[t]),
                    "elapsed": str(cls.get(t)),
                    "newline": os.linesep}
            s += "{label} {start} {end} {elapsed} {newline}".format(**data)
        return s

    @classmethod
    def benchmark(cls, sysinfo=True):
        """
        prints out all timers in a convenient benchmark table
        :return:
        :rtype:
        """

        #
        # PRINT PLATFORM
        #

        print()
        data_platform = systeminfo()

        data_platform['cpu_count'] = multiprocessing.cpu_count()
        mem = psutil.virtual_memory()
        try:
            data_platform['mem_total'] = humanize.naturalsize(mem.total, \
                                                              binary=True)
        except:
            pass
        try:
            data_platform['mem_available'] = humanize.naturalsize(
                mem.available, binary=True)
        except:
            pass
        try:
            data_platform['mem_percent'] = str(mem.percent) + "%"
        except:
            pass
        try:
            data_platform['mem_used'] = humanize.naturalsize(mem.used,
                                                             binary=True)
        except:
            pass
        try:
            data_platform['mem_free'] = humanize.naturalsize(mem.free,
                                                             binary=True)
        except:
            pass
        try:
            data_platform['mem_active'] = humanize.naturalsize(mem.active,
                                                               binary=True)
        except:
            pass
        try:
            data_platform['mem_inactive'] = humanize.naturalsize(mem.inactive,
                                                                 binary=True)
        except:
            pass
        try:
            data_platform['mem_wired'] = humanize.naturalsize(mem.wired,
                                                              binary=True)
        except:
            pass
        # svmem(total=17179869184, available=6552825856, percent=61.9,

        banner("Platform")
        pprint(data_platform)

        #
        # PRINT TIMERS
        #
        timers = StopWatch.keys()

        if len(timers) > 0:
            banner("Timers")

            data_timers = {}
            for timer in timers:
                data_timers[timer] = {
                    'time': round(StopWatch.get(timer), 2),
                    'timer': timer
                }
                for attribute in ["node",
                                  "user",
                                  "system",
                                  "machine",
                                  "mac_version",
                                  "win_version"]:
                    data_timers[timer][attribute] = data_platform[attribute]

            for timer in data_timers:
                element = data_timers[timer]

                print(timer, element["time"])

        else:

            print("ERROR: No timers found")
