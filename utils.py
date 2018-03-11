import os
import subprocess

import sublime


def get_selected_line_nos(view):
    return (
        view.rowcol(view.sel()[0].begin())[0] + 1,
        view.rowcol(view.sel()[0].end())[0] + 1,
    )


def get_line_no(view):
    return view.rowcol(view.sel()[0].begin())[0] + 1


def get_buffer(view):
    return view.substr(sublime.Region(0, view.size()))


def run(*args, **kwargs):
    output = subprocess.check_output(*args, **kwargs)
    output = output.decode('utf-8')
    output = output.strip()
    return output


def get_cwd(view):
    file_name = view.file_name()

    if not file_name:
        return ''

    return os.path.dirname(file_name)
