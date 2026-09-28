import os

from talon import Context, actions, ui

ctx = Context()
ctx.matches = r"""
app: finder
tag: user.custom-fs
"""
@ctx.action_class("user")
class UserActions:
    
    def file_manager_open_directory(path: str):
            """opens the directory that's already visible in the view, with proper symlink handling"""
            if os.path.islink(path):
                actions.user.file_manager_select_directory(path)
                actions.sleep("50ms")
                actions.key("cmd-o")
            else:
                actions.key("cmd-shift-g")
                actions.sleep("50ms")
                actions.insert(path)
                actions.key("enter")    