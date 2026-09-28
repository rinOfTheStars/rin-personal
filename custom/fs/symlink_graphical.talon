os: mac
app: finder
tag: user.file_manager
and tag: user.custom-fs
-
(sim link | sym link | linkle) from here to clipboard:
    user.symlink_active_to_clipboard(true, "")

(sim link | sym link | linkle) from clipboard to here:
    user.symlink_active_to_clipboard(false, "")

(sim link | sym link | linkle) from here to clipboard with name <user.text>:
    user.symlink_active_to_clipboard(true, user.text)

(sim link | sym link | linkle) from clipboard to here with name <user.text>:
    user.symlink_active_to_clipboard(false, user.text)
