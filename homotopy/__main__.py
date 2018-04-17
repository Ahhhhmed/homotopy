import argparse

from homotopy.homotopy import Homotopy


def main():
    parser = argparse.ArgumentParser(description="Compile a snippet.")
    parser.add_argument('language', type=str,
                        help='Language for the snippet to be compiled to')
    parser.add_argument('snippet', type=str,
                        help='A snippet to be compiled')
    parser.add_argument('-t', '--tabsize', type=int, metavar="N",
                        help='Number of spaces in one tab. Tabs remain tabs if absent')
    parser.add_argument('-c', '--cursor', action='store_true',
                        help='Indicate cursor marker in compiled snippet')
    parser.add_argument('-p', '--path', type=str, metavar="PATH",
                        help='Path to snippet library folders separated by :')

    args = parser.parse_args()

    homotopy = Homotopy(args.language)

    if args.tabsize:
        homotopy.set_indent(" "*args.tabsize)

    if args.cursor:
        homotopy.enable_cursor_marker()

    if args.path:
        for item in args.path.split(':'):
            homotopy.add_lib_folder(item)

    print(homotopy.compile(args.snippet), end='')


def init():
    if __name__ == "__main__":
        main()


init()
