import shlex
import argparse
import exrenhlp.run


class ArgumentParser(argparse.ArgumentParser):
    def __init__(*args, **kwds):
        self, *args = args
        argparse.ArgumentParser.__init__(self, *args, **kwds)
        self.add_argument('-f', '--full', action='store_true')
        group1 = self.add_mutually_exclusive_group()
        group1.add_argument('prefix', nargs='?', default=argparse.SUPPRESS)
        group1.add_argument('-p', '--prefix')
        group2 = self.add_mutually_exclusive_group()
        group2.add_argument('suffix', nargs='?', default=argparse.SUPPRESS)
        group2.add_argument('-s', '--suffix')
        return None


def patch(location,
          items,
          *,
          parser=ArgumentParser(prog='prefix', add_help=False)):
    while True:
        argv = shlex.split(input('(prefix) '))
        try:
            options = parser.parse_args(argv)
            break
        except SystemExit:
            pass
    for item in items:
        item.rename = ''.join(
            (options.prefix or '', item.source.stem,
             item.source.suffix if options.full else options.suffix or '',
             options.suffix or '' if options.full else item.source.suffix))
    return None


if '__main__' == __name__:
    exrenhlp.run.run_error_safe(patch)
