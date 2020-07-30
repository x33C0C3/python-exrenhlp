import shlex
import argparse
import exrenhlp.run


class ArgumentParser(argparse.ArgumentParser):
    def __init__(*args, **kwds):
        self, *args = args
        argparse.ArgumentParser.__init__(self, *args, **kwds)
        self.add_argument('-f', '--full', action='store_true')
        self.add_argument('start', type=int)
        self.add_argument('length', type=int, nargs='?')


def patch(location,
          items,
          *,
          parser=ArgumentParser(prog='sub', add_help=False)):
    while True:
        argv = shlex.split(input('(sub) '))
        try:
            args = parser.parse_args(argv)
            break
        except SystemExit:
            pass
    stop = args.length
    if None is not stop:
        if 0 == stop:
            stop = None
        if 0 < stop:
            stop += args.start
    slice_obj = slice(args.start, stop)
    for item in items:
        if args.full:
            item.rename = item.source.name[slice_obj]
        else:
            item.rename = item.source.stem[slice_obj] + item.source.suffix
    return None


if '__main__' == __name__:
    exrenhlp.run.run_error_safe(patch)
