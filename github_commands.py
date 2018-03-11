import os
import re
import webbrowser

import sublime_plugin

from .utils import run, get_selected_line_nos


class GitHubTreeCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        open_tree(self.view)


class GitHubBlobCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        open_blob(self.view)


class GitHubBlameCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        open_blame(self.view)


class GitHubHistoryCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        open_history(self.view)


def open_tree(view):
    repo = get_github_repo()
    commit = get_git_commit()
    url = 'https://github.com/{repo}/tree/{commit}'.format(  # noqa
        repo=repo, commit=commit,
    )
    webbrowser.open(url)


def open_history(view):
    file_name = get_file_name(view)

    if not file_name:
        return

    repo = get_github_repo()
    commit = get_git_commit()

    url = 'https://github.com/{repo}/commits/{commit}/{file_name}'.format(
        repo=repo, commit=commit, file_name=file_name,
    )
    webbrowser.open(url)


def open_blame(view):
    open_file(view, 'blame')


def open_blob(view):
    open_file(view, 'blob')


def open_file(view, action):
    file_name = get_file_name(view)

    if not file_name:
        return

    repo = get_github_repo()
    commit = get_git_commit()
    line_no = get_line_no_fragment(view)

    url = 'https://github.com/{repo}/{action}/{commit}/{file_name}#{line_no}'.format(  # noqa
        repo=repo, commit=commit, file_name=file_name, line_no=line_no,
        action=action,
    )
    webbrowser.open(url)


def get_git_root():
    return run(['git', 'rev-parse', '--show-toplevel'])


def get_git_commit():
    return run(['git', 'rev-parse', '--verify', 'HEAD'])


def get_github_repo():
    url = run(['git', 'config', '--get', 'remote.origin.url'])
    match = re.search('github.com/([^/]+/[^/]+)', url)  # TODO remove .git
    return match.group(1)


def get_file_name(view):
    file_name = view.file_name()

    if not file_name:
        return None

    git_root = get_git_root()
    return os.path.relpath(file_name, git_root)


def get_line_no_fragment(view):
    line_no_begin, line_no_end = get_selected_line_nos(view)

    if line_no_begin == line_no_end:
        fragment = 'L{begin}'.format(begin=line_no_begin)
    else:
        fragment = 'L{begin}-L{end}'.format(
            begin=line_no_begin, end=line_no_end,
        )

    return fragment
