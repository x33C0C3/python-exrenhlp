import shlex
import string
import functools
import argparse
import exrenhlp.run


def i2a(value, base=10, *, numbers=string.digits + string.ascii_lowercase):
    if not isinstance(value, int):
        raise ValueError
    s = list()
    q = value
    while base <= q:
        q, r = divmod(q, base)
        s.append(numbers[r])
    s.append(numbers[q])
    return ''.join(reversed(s))


def number(value, base=10):
    value = str(value)
    return sum(n * base**d for d, n in enumerate(
        map(functools.partial(int, base=base), reversed(value))))


class ArgumentParser(argparse.ArgumentParser):
    def __init__(*args, **kwds):
        self, *args = args
        argparse.ArgumentParser.__init__(self, *args, **kwds)
        self.add_argument('-f', '--full', action='store_true')
        self.add_argument('start')
        self.add_argument('base', type=int, nargs='?', default=10)
        return None


def patch(location,
          items,
          *,
          callback=None,
          parser=ArgumentParser(prog='num', add_help=False)):
    while True:
        argv = shlex.split(input('(num) '))
        try:
            args = parser.parse_args(argv)
            break
        except SystemExit:
            pass
    num = number(args.start, base=args.base)
    for item in sorted(items, key=str):
        if callable(callback):
            incr = callback(location / item.source)
            if not isinstance(incr, int) or 1 > incr:
                raise ValueError
        else:
            incr = 1
        chunks = list()
        chunks.append(i2a(num, base=args.base).zfill(len(args.start)))
        if 1 < incr:
            chunks.append('-')
            chunks.append(
                i2a(incr - 1 + num, base=args.base).zfill(len(args.start)))
        num += incr
        if not args.full:
            chunks.append(item.source.suffix)
        item.rename = ''.join(chunks)
    return None


if '__main__' == __name__:
    exrenhlp.run.run_error_safe(patch)
