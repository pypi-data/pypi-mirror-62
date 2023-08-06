"""Somewhat useful 'python -m gd' implementation"""

import argparse
import sys
import pkg_resources
import platform

import gd

con_v = '0.3.0'  # gd_console version


def show_version() -> None:
    # do imports here because we don't use them
    import aiohttp

    entries = []

    entries.append('- Python v{0.major}.{0.minor}.{0.micro}-{0.releaselevel}'.format(sys.version_info))

    version_info = gd.version_info
    entries.append('- gd.py v{0.major}.{0.minor}.{0.micro}-{0.releaselevel}'.format(version_info))

    if version_info.releaselevel != 'final':
        pkg = pkg_resources.get_distribution('gd.py')
        if pkg:
            entries.append('    - gd.py pkg_resources: v{0}'.format(pkg.version))

    entries.append('- [gd_console] v{0}'.format(con_v))

    entries.append('- aiohttp v{0.__version__}'.format(aiohttp))

    uname = platform.uname()
    entries.append('- System Info: {0.system} {0.release} {0.version}'.format(uname))

    print('\n'.join(entries))


def show_docs() -> None:
    _docs = 'https://gdpy.readthedocs.io/en/latest'

    print('- gd.py docs: [{}]'.format(_docs))


def main() -> None:
    # make parser
    parser = argparse.ArgumentParser(description='gd.py console commands', prog='gd')
    # add --console
    parser.add_argument(
        '-c', '--console', help='start async repl session',
        action='store_true', default=False)
    # add --version
    parser.add_argument(
        '-v', '--version', help='show versions (gd.py, python, etc.)',
        action='store_true', default=False)
    # add --docs
    parser.add_argument(
        '-d', '--docs', help='show links to gd.py docs',
        action='store_true', default=False)
    # parse args
    args = parser.parse_args()
    # run functions
    if args.console:

        try:
            import aioconsole
            aioconsole.run_apython(list())

        except ImportError:
            print(
                'Failed to import aioconsole. You can install it manually',
                'or via "pip install gd.py[console]".'
            )
            exit()

    if args.version:
        show_version()
        exit()

    if args.docs:
        show_docs()
        exit()


# run main
if __name__ == '__main__':
    main()
