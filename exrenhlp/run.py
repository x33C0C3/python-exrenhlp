import pathlib
from . import Browser


def get_from_ex():
    browser = Browser.get()
    return (pathlib.WindowsPath(browser.location()),
            tuple(browser.selected_items()))


class Item(object):
    def __str__(self):
        return str(self.source)

    def __init__(self, source):
        object.__init__(self)
        self.source = source
        self.rename = None
        return None


def run(callback, items=None, location=None, *, browser=None):
    if None is items and None is location:
        if None is browser:
            browser = Browser.get()
        location =pathlib.WindowsPath(browser.location())
        items = tuple(browser.selected_items())
    elif None is location:
        location = pathlib.Path.cwd()
    location = pathlib.Path(location)
    if any(
            location.joinpath(item).resolve().parent != location
            for item in items):
        raise ValueError
    items = tuple(map(pathlib.PurePath, items))
    while True:
        forces = tuple(map(Item, items))
        callback(location, forces)
        count = 0
        for before, after in zip(items, (item.rename for item in forces)):
            if None is after:
                continue
            before = str(before)
            after = str(after)
            if before == after:
                continue
            print('{!r} => {!r}'.format(before, after))
            count += 1
        print('@count    {!s}/{!s}'.format(count, len(items)))
        print('@location {!s}'.format(location))
        if 0 >= count:
            input('There is no change.')
            continue
        if input("yes or no? ") in ('y', 'Y', 'yes', 'Yes', 'YES'):
            for before, after in zip(items, (item.rename for item in forces)):
                if None is after:
                    continue
                item = pathlib.Path(location, before)
                item.rename(item.with_name(str(after)))
            break
        if None is not browser:
            browser._webbrowser_.Refresh()
    return None

def run_error_safe(*args, **kwds):
    try:
        run(*args, **kwds)
    except:
        import traceback
        traceback.print_exc()
        input('Press Return to close this window...')
    return None
