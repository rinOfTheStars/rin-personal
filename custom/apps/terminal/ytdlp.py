import os
import subprocess

from talon import Context, Module, actions, app, clip

ctx = Context()
mod = Module()

ctx.matches = r"""
os: mac
tag: terminal
"""

def validate_and_clean_link(link: str) -> str | None:
    if "https://youtu.be" not in link:
        return None
    else:
        return link.split("?")[0]

@mod.action_class
class Actions:
    
    def ytdlp_from_clipboard():
        """WIP; currently only supports -f m4a"""
        clipboard = clip.get()
        clean = validate_and_clean_link(clipboard)
        if clean is None:
            app.notify(
                "String parse failure",
                f"{clipboard} is not a youtu.be link"
            )
        else:
            to_paste = "yt-dlp -f m4a " + clean
            clip.set(to_paste)
            actions.sleep("50ms")
            actions.key("cmd-v") # We don't press enter for the user in case they made a mistake
            clip.set(clean) # Will probs make this a configurable feature in the future?
