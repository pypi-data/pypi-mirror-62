from . import directory
from . import manpages
from . import pages
from . import reader
from . import summary
from ..program import PROGRAM


def main():
    help = reader.read()
    directory.main(help)
    pages.main(help)
    summary.main(help)
    manpages.main(help)


if __name__ == '__main__':
    PROGRAM.start()
    main()
