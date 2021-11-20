import argparse
import datetime
from pathlib import Path

import exifread

import fileutils

DATETIME_FORMAT = "%Y:%m:%d %H:%M:%S"
OUTPUT_DATETIME_FORMAT = "%Y-%b-%d"

parser = argparse.ArgumentParser(description='Organise photos into directories based on their exif data')
parser.add_argument('directories', metavar='directories', type=str, nargs='+',
                    help='Directories to organise')
parser.add_argument('--dryRun', '-d', dest="dryRun", action="store_true",
                    help="Print what this script would do, but don't actually do anything.")
parser.add_argument('--displayAll', '-a', dest="displayAll", action="store_true",
                    help="Display output for all files, not just images")
# parser.add_argument('--directory_format', '-f', dest="tag", action="store",
#                     default="<datetime#yyyy-MM-dd>",
#                     help="Format to create directories to organise within. Should take the format \"<tagname>_dir\""
#                          "where anything within angle brackets is looked up in the image's exif tags."
#                          "Formatting can also be applied for certain tags, datetime for example allows formatting:"
#                          "<datetime#yyyy-MM-dd> will be parsed to the given format")

# Parse arguments
args = parser.parse_args()

# For each directory
for dir in args.directories:
    print(f"Processing {dir}")
    # For each file
    files = fileutils.get_files(dir)

    for file in files:
        # Check they are image files (have exif data)
        with open(file.full_filename(), 'rb') as image_file:
            image = exifread.process_file(image_file)

        if image.keys():
            # If they are, extract the tag from the exif data
            tag_value = image["EXIF DateTimeOriginal"]

            # and create a dir with the VALUE of the tag
            output = datetime.datetime.strptime(tag_value.printable, DATETIME_FORMAT).strftime(OUTPUT_DATETIME_FORMAT)

            output_path = Path(dir, output)

            print(f"{file.name} has date time value of {tag_value}, and output dir of {output_path}")

            output_path.mkdir(exist_ok=True)

            new_location = Path(output_path, file.name)

            # Move file to that dir
            Path(file.full_filename()).rename(new_location)
        else:
            if args.displayAll:
                print(f"{file.name} is not a photo (no exif data found)")
