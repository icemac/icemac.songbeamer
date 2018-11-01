import argparse
import dataclasses
import icemac.songbeamer
import logging
import os
import sys


log = logging.getLogger(__name__)


def get_xlwt():
    """Get the `xlwt` module or exit with an error message."""
    try:
        import xlwt
        return xlwt
    except ImportError:
        print('You have to install the `xls` extra for this feature.')
        print('e. g. call `pip install icemac.songbeamer[xls]`.')
        sys.exit(-1)


@dataclasses.dataclass
class Exporter:
    """Export from file full of beamer files to XLS."""

    src_dir: str
    dest_file: open

    def __call__(self):
        songs = [
            icemac.songbeamer.open(os.path.join(dirpath, x))
            for dirpath, dirnames, filenames in os.walk(self.src_dir)
            for x in filenames]
        songs = sorted([x for x in songs if x is not None],
                       key=lambda x: x.get('Title', ''))
        xlwt = get_xlwt()
        workbook = xlwt.Workbook()
        sheet = workbook.add_sheet('SongBeamer songs')
        for row, song in enumerate(songs):
            title = song.get('Title')
            if not title:
                log.warning('Missing Title in %r', song.filename)
            sheet.write(row, 0, title)
            sheet.write(row, 1, song.get('ChurchSongID'))
            sheet.write(row, 2, song.get('Songbook'))
        workbook.save(self.dest_file)


class readable_dir(argparse.Action):
    """Argparse action which requires a readable directory.

    Based on https://stackoverflow.com/a/11415816
    """

    def __call__(self, parser, namespace, candidate, option_string=None):
        if not os.path.isdir(candidate):
            raise argparse.ArgumentError(
                self, "{!r} is not a valid path.".format(candidate))
        if os.access(candidate, os.R_OK):
            setattr(namespace, self.dest, candidate)
        else:
            raise argparse.ArgumentError(
                self, "{!r} is not a readable dir.".format(candidate))


def main(args=None):
    """Export titles and numbers from Songbeamer files to Excel.

    The export file contains the following columns:

    * #Title
    * #ChurchSongID
    * #Songbook

    """
    parser = argparse.ArgumentParser(description=main.__doc__)
    parser.add_argument(
        'src_dir', action=readable_dir,
        help='Directory containing the Songbeamer song files.')
    parser.add_argument(
        'dest_file', type=argparse.FileType('wb'),
        help='Destination XLS for storing the export data')

    args = parser.parse_args(args)
    Exporter(args.src_dir, args.dest_file)()
