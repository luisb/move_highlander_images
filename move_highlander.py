import argparse
import os
import shutil
import re


parser = argparse.ArgumentParser(
    prog="move_highlander.py",
    description='Move highlander files into directories by year')

parser.add_argument('directory', type=str, help='Directory to search for files')
parser.add_argument('--dry-run', action='store_true', 
                    help='Dry run, do not move files', dest='dry_run')
args = parser.parse_args()

print("Searching in {}".format(args.directory))

for folder in os.listdir(args.directory):
    print ('\nIn folder: {}'.format(folder))
    regex = r'(?<=highlander_)([0-9]{4})[0-9]{4}'
    match = re.search(regex, folder)
    if match:
        year = match.group(1)
        print ('year: {}'.format(year))

        new_folder = os.path.join(args.directory, year)
        print("new_folder: {}".format(new_folder))
        if not os.path.exists(new_folder):
            if not args.dry_run:
                os.makedirs(new_folder)
            print('Created {}...'.format(new_folder))
        else:
            print('Folder {} already exists...'.format(new_folder))
        
        file_names = os.listdir(os.path.join(args.directory, folder))
        for file in file_names:
            if os.path.isdir(os.path.join(args.directory, folder, file)):
                print("Found folder: {}. Deeper checks needed...".format(file))
                if file == 'access':
                    print("Skipping folder: {}".format(file))
                    continue
                elif file == 'preservation' or file == 'pdfs' or file == 'tiffs':
                    deeper_filenames = os.listdir(os.path.join(args.directory, folder, file))
                    for deeper_file in deeper_filenames:
                        dupe_counter = 0
                        print("(deeper) Checking if {} already exists in {}".format(os.path.join(new_folder, deeper_file), new_folder))
                        if os.path.exists(os.path.join(new_folder, deeper_file)):
                            print("(deeper) File {} already exists in {}".format(os.path.join(new_folder, deeper_file), new_folder))
                            dupe_counter += 1
                            deeper_file_name, deeper_file_extension = os.path.splitext(deeper_file)
                            new_filename = "{}_{}".format(deeper_file_name, dupe_counter)
                            new_filename += deeper_file_extension
                            print("New filename: {}".format(new_filename))
                            while os.path.exists(os.path.join(new_folder, new_filename)):
                                dupe_counter += 1
                                deeper_file_name, deeper_file_extension = os.path.splitext(deeper_file)
                                new_filename = "{}_{}".format(deeper_file_name, dupe_counter)
                                new_filename += deeper_file_extension
                                print("New filename: {}".format(new_filename))
                            if new_filename:
                                print("(deeper) Moving {} to {}".format(os.path.join(args.directory, folder, file, deeper_file), os.path.join(new_folder, new_filename)))
                                if not args.dry_run:
                                    shutil.move(os.path.join(args.directory, folder, file, deeper_file),  new_folder)
                        print("(deeper) Moving {} to {}".format(os.path.join(args.directory, folder, file, deeper_file), new_folder))
                        if not args.dry_run:
                            shutil.move(os.path.join(args.directory, folder, file, deeper_file),  new_folder)
                        
            else:
                dupe_counter = 0
                print("Checking if {} already exists in {}".format(os.path.join(new_folder, file), new_folder))
                if os.path.exists(os.path.join(new_folder, file)):
                    print("File {} already exists in {}".format(file, new_folder))
                    dupe_counter += 1
                    file_name, file_extension = os.path.splitext(file)
                    new_filename = "{}_{}".format(file_name, dupe_counter)
                    new_filename += file_extension
                    print("New filename: {}".format(new_filename))
                    while os.path.exists(os.path.join(new_folder, new_filename)):
                        dupe_counter += 1
                        file_name, file_extension = os.path.splitext(file)
                        new_filename = "{}_{}".format(file_name, dupe_counter)
                        new_filename += file_extension
                    if new_filename:
                        print("Moving {} to {}".format(os.path.join(args.directory, folder, file), os.path.join(new_folder, new_filename)))
                        if not args.dry_run:
                            shutil.move(os.path.join(args.directory, folder, file), os.path.join(new_folder, new_filename))
                else:
                    print("Moving {} to {}".format(os.path.join(args.directory, folder, file), new_folder))
                    if not args.dry_run:
                        shutil.move(os.path.join(args.directory, folder, file), new_folder)
