import os
import re
import webbrowser

import sublime_plugin

from .utils import run, get_cwd, get_selected_line_nos


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
    cwd = get_cwd()
    repo = get_github_repo(cwd)
    commit = get_git_commit(cwd)
    url = 'https://github.com/{repo}/tree/{commit}'.format(  # noqa
        repo=repo, commit=commit,
    )
    webbrowser.open(url)


def open_history(view):
    file_name = view.file_name()

    if not file_name:
        return

    path = os.path.relpath(file_name, git_root)
    repo = get_github_repo(cwd)
    commit = get_git_commit(cwd)

    url = 'https://github.com/{repo}/commits/{commit}/{path}'.format(  # noqa
        repo=repo, commit=commit, path=path,
    )

    webbrowser.open(url)


def open_blame(view):
    open_file(view, 'blame')


def open_blob(view):
    open_file(view, 'blob')


def open_file(view, action):
    file_name = view.file_name()

    if not file_name:
        return

    cwd = get_cwd()

    git_root = get_git_root(cwd)

    path = os.path.relpath(file_name, git_root)

    line_no_begin, line_no_end = get_selected_line_nos(view)

    if line_no_begin == line_no_end:
        line_no = 'L{begin}'.format(begin=line_no_begin)
    else:
        line_no = 'L{begin}-L{end}'.format(
            begin=line_no_begin, end=line_no_end,
        )

    repo = get_github_repo(cwd)
    commit = get_git_commit(cwd)

    url = 'https://github.com/{repo}/{action}/{commit}/{path}#{line_no}'.format(  # noqa
        repo=repo, commit=commit, path=path, line_no=line_no, action=action,
    )

    webbrowser.open(url)


def get_git_root(cwd):
    return run(['git', 'rev-parse', '--show-toplevel'], cwd=cwd)


def get_git_commit(cwd):
    return run(['git', 'rev-parse', '--verify', 'HEAD'], cwd=cwd)


def get_github_repo(cwd):
    url = run(['git', 'config', '--get', 'remote.origin.url'], cwd=cwd)
    match = re.search('github.com/([^/]+/[^/]+)', url)
    return match.group(1)
