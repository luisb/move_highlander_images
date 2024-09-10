import argparse
import os
import shutil
import re


parser = argparse.ArgumentParser(
    prog="move_pdfs_into_preservation.py",
    description='Move highlander pdfs into its perservation directory')

parser.add_argument('directory', type=str, help='Directory to search for files')
parser.add_argument('--dry-run', action='store_true', 
                    help='Dry run, do not move files', dest='dry_run')
args = parser.parse_args()

print("Searching in {}".format(args.directory))

for file in os.listdir(args.directory):
    if file.endswith('.pdf'):
        print("\nFound pdf: {}".format(file))
        basename = os.path.splitext(file)[0]
        if os.path.isdir(os.path.join(args.directory, basename)):
            print("Found folder: {}. Deeper checks needed...".format(basename))
            if os.path.isdir(os.path.join(args.directory, basename, 'preservation')):
                print("Found preservation folder in {}".format(basename))
                if not args.dry_run:
                    shutil.move(os.path.join(args.directory, file), os.path.join(args.directory, basename, 'preservation'))
                print("Moved {} to {}".format(os.path.join(args.directory, file), os.path.join(args.directory, basename, 'preservation')))
 