import os
import subprocess
from typing import Optional

from talon import Context, Module, actions, app

ctx = Context()
mod = Module()

ctx.matches = r"""
os: mac
app: finder
"""

@mod.action_class
class Actions:
    def copy_here_to_clipboard():
        """
        Copies the current directory to the clipboard. 
        Effectively the same as `\"copy path\"` w.o any file highlighted 
        """
        here = actions.user.file_manager_current_path()
        process = subprocess.Popen(
            "/usr/bin/pbcopy", stdin=subprocess.PIPE, text=True)
        process.communicate(here)
        code = process.returncode
        print(code)