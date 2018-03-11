import os
import re
import webbrowser

import sublime_plugin

from .utils import run, get_cwd, get_selected_line_nos


class GitHubBlobCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        open_in_github(self.view, 'blob')


class GitHubBlameCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        open_in_github(self.view, 'blame')


class GitHubHistoryCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        # TODO refactor to remove line number fragment
        open_in_github(self.view, 'commits')


def open_in_github(view, action):
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
