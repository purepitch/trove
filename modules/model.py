# -*- coding: utf-8 -*-

import ConfigParser
import subprocess
import time
from datetime import datetime

class Model():
    """
    Model for the common license management interface.
    This class handles all business logic.
    """
    def __init__(self):
        self.program    = ""
        self.author     = ""
        self.copyright  = ""
        self.email      = ""
        self.maintainer = ""
        self.status     = ""
        self.version    = ""
        self.config = None

    # XXX: this method isn't called anywhere
    # XXX: what does the config file look like?
    # XXX: what config items are we expecting here?
    # XXX: should this method raise an error if the config file doesn't exist?
    def get_config(self, file):
        config = ConfigParser.ConfigParser()
        config.read(file)
        # Fill dictionary with config information:
        section_dict = {}
        for section in config.sections():
            options = config.options(section)
            param_dict = {}
            for option in options:
                param_dict[option] = config.get(section, option)
            section_dict[section] = param_dict
        self.secdict = section_dict
        return self.secdict

    # XXX: this method isn't called anywhere
    def get_date(self):
        now = time.time()
        time_stamp = datetime.fromtimestamp(now).strftime('%Y-%m-%d %H:%M:%S')
        return time_stamp

    # XXX: this method isn't called anywhere
    # XXX: what kind of command is expected here?
    def execute(self, command):
        proc = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)
        proc.wait()
        output = proc.communicate()[0]
        return output

# vim: expandtab shiftwidth=4 softtabstop=4
