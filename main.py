import argparse as ag
import os
from datetime import datetime

from intersectingValidation import intersectLineStringInValidFormat
from glob import glob
from node_connectivity import plot_nodes_vs_ways, subgraph_eda, get_invalidNodes
from config import DefaultConfigs
from util_data import UtilData
import ntpath
import logging
from logging.config import fileConfig
import shutil

if __name__ == '__main__':
    filename1 = datetime.now().strftime("%Y%m%d-%H%M%S")
    shutil.copy2('log/logfile.log', 'log/logfile.old.' + filename1 + '.log')
    open('log/logfile.log', "w+").truncate(0)

    fileConfig('logging_config.ini')
    mainLogger = logging.getLogger("main")
    parser = ag.ArgumentParser()
    parser.add_argument("--inputPath", help="Relative input path to GeoJSON files",
                        default=os.path.join(os.getcwd(), "OSW\TestData\input"))
    parser.add_argument("--validation", help="Type of validation", default='intersectingvalidation')
    parser.add_argument("--writePath", help="Relative output path to write the validation errors",
                        default=os.path.join(os.getcwd(), "OSW\TestData\Output"))
    args = parser.parse_args()
    cf = DefaultConfigs(args)
    inputPath = args.inputPath
    writePath = args.writePath

    json_files = glob(os.path.join(inputPath, "*.geojson"))
    if cf.file_filter:
        json_files = sorted([i for i in json_files if cf.file_filter in i])
    print("Number of geojson files read :", len(json_files))
    mainLogger.info(
        "function:main, step 0, 0 calls, 0 seconds, 0.000 seconds per call, Number of geojson files read : %s",
        len(json_files))
    nodes_files = sorted([x for x in json_files if 'node' in x])
    ways_files = sorted([x for x in json_files if 'node' not in x])

    for ind, (nodes_file, ways_file) in enumerate(zip(nodes_files, ways_files)):
        print('Processing File : {} , {}'.format(ntpath.basename(nodes_file), ntpath.basename(ways_file)))
        mainLogger.info(
            'function:main, step 0, 0 calls, 0 seconds, 0.000 seconds per call,Processing File : {}  {}'.format(
                ntpath.basename(nodes_file), ntpath.basename(ways_file)))
        utild = UtilData(nodes_file, ways_file, cf)
        if cf.validation == 'intersectingvalidation':
            print("--" * 10)
            print(
                "Running intersectingvalidation to check if any ways which are intersecting have a missing intersection node")
            mainLogger.info(
                "function:main, step 0, 0 calls, 0 seconds, 0.000 seconds per call, Running intersectingvalidation to see if any ways which are intersecting have a missing intersecting node")

            print("--" * 10)
            intersectLineStringInValidFormat(utild.ways_json, "brunnel", cf)

        if cf.do_eda:
            print("--" * 10)
            print("Performing Exploratory Data Analysis")
            mainLogger.info(
                "function:main, step 1,  1 calls, 0 seconds, 0.000 seconds per call, Performing Exploratory Data Analysis")
            print("--" * 10)
            plot_nodes_vs_ways(utild, cf)
            subgraph_eda(utild, cf)

        if cf.do_all_validations:
            print("--" * 10)
            print("Performing Exploratory Data Analysis")
            mainLogger.info(
                "function:main, step 1, 1 calls, 0 seconds, 0.000 seconds per call, Performing all validations")
            print("--" * 10)
            get_invalidNodes(utild, cf)
