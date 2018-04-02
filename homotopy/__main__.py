import argparse
import homotopy.parser

from homotopy.compiler import Compiler


def main():
    parser = argparse.ArgumentParser(description="Compile a snippet.")
    parser.add_argument('snippet', nargs=1, type=str, help='a snippet to be compiled')

    snippet = parser.parse_args().snippet[0]

    print(Compiler().compile(homotopy.parser.parser.parse(snippet)), end='')


if __name__ == "__main__":
    main()