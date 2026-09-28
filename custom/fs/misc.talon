os: mac
app: finder
tag: user.file_manager
and tag: user.custom-fs
-
copy (directory | deer | dir | folder) path:
    user.copy_here_to_clipboard()