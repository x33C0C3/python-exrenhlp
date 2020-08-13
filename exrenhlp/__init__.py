import operator
import functools
import pathlib
import urllib.parse
import win32com.client
import fgwnd


def file_uri_to_path(uri, *, encoding='unicode-escape'):
    if None is encoding:
        import locale
        encoding = locale.getpreferredencoding()
    parsed = urllib.parse.urlparse(uri)
    if 'file' != parsed.scheme:
        raise ValueError
    path = urllib.parse.unquote(parsed.path, encoding=encoding)
    if parsed.netloc:
        path = ''.join((r'//', parsed.netloc, path))
    elif path.startswith('/'):
        path = path[1:]
    return path


class Browser(object):
    @classmethod
    def get(cls,
            hwnd=None,
            *,
            ex_path=pathlib.WindowsPath(r'C:\WINDOWS\Explorer.EXE'),
            shell_obj=None):
        if None is shell_obj:
            shell_obj = win32com.client.Dispatch('Shell.Application')
        iterable = filter(
            fgwnd.txn((operator.attrgetter('FullName'), ex_path.samefile)),
            iter(shell_obj.WIndows()))
        if hwnd:
            wnd_obj = next(
                filter(
                    fgwnd.txn((operator.attrgetter('HWND'),
                               functools.partial(operator.eq, hwnd))),
                    iterable), None)
        else:
            wnd_tab = dict((wnd.HWND, wnd) for wnd in iterable)
            hwnd = next(fgwnd.iterwindow(wnd_tab.__contains__), None)
            if not hwnd:
                raise IndexError
            wnd_obj = wnd_tab[hwnd]
        return cls(wnd_obj)

    def location_url(self):
        return self._webbrowser_.LocationURL or None

    def location(self):
        url = self.location_url()
        if not url:
            return None
        return file_uri_to_path(url)

    def selected_items(self):
        yield from (item.Name
                    for item in self._webbrowser_.Document.SelectedItems())
        return None

    def __init__(self, webbrowser):
        self._webbrowser_ = webbrowser
        return None
