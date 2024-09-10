import argparse
import os

parser = argparse.ArgumentParser(
    prog="rename_preservation_tiffs.py",
    description='Rename tiffs under preservation directory')
parser.add_argument('directory', type=str, help='Directory to search for files')
parser.add_argument('--dry-run', action='store_true', 
                    help='Dry run, do not move files', dest='dry_run')
args = parser.parse_args()

dirs = os.listdir(args.directory)

for dir in dirs:
    folders = os.listdir(os.path.join(args.directory, dir))
    for folder in sorted(folders):
        print ('\nIn folder: {}'.format(folder))
        if folder == 'access':
            access_filename = os.listdir(os.path.join(args.directory, dir, folder))
            print("access_filename: {}".format(access_filename[0]))
        if folder == 'preservation':
            preserv_filename = os.listdir(os.path.join(args.directory, dir, folder))
            print("preserv_filename: {}".format(preserv_filename[0]))
            if not args.dry_run:
                os.rename(os.path.join(args.directory, dir, folder, preserv_filename[0]), os.path.join(args.directory, dir, folder, access_filename[0]))
            print("Renamed {} to {}".format(os.path.join(args.directory, dir, folder, preserv_filename[0]), access_filename[0]))
