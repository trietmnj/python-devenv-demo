import h5_converter as h5c
import argparse
import os
import numpy
import time

def get_parser():
    parser = argparse.ArgumentParser(description="Discount from AssetDamageDetailFile")
    parser.add_argument(
        '-i',
        '--input_folder',
        help='Path to master folder containing h5 files')
    parser.add_argument(
        '-o', 
        '--output_folder', 
        help='Path to output folder')
    return parser

def main(input_folder: str, return_folder: str):
    start_time = time.time()
    h5_pth = []
    h5_dump = os.path.join(return_folder)
    # Loop Through Directory Tree In NACCS Data Folder
    for root, _, files in os.walk(input_folder):
        if len(files) > 0:
            for f in files:
                h5_pth = numpy.hstack((h5_pth, os.path.join(root, f)))
    # Convert h5 to CSV
    for f in h5_pth:
        h5c.h5_converter(f, return_folder)

    print("--- %s seconds ---" % (time.time() - start_time))

if __name__ == "__main__":
    args, _ = get_parser().parse_known_args()
    main(args.input_folder, args.output_folder)