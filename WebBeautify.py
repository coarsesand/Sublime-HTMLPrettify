import commands
import os
import re
import sublime
import sublime_plugin
from .lib import *


class WebBeautifyCommand(sublime_plugin.TextCommand):

    def run(self, edit):
        self.save()
        self.beautify(edit)

    def save(self):
        self.view.run_command("save")

    def prettify(self, edit):
        pass
