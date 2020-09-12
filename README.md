# OpenSidewalks data schema, and its validators

This repository is created to perform validations on the geojson files provided against OpenSideWalks Schema.

### Steps to run:

1. Create a Virtual environment in Python
2. Activate virtual environment
3. Install the required packages to run the code

 
#### Using Pip
1.  `virtualenv opensidewalk -p /usr/bin/python3.6`
2.  `source opensidewalk/bin/activate`
3.  `pip3 install -r pip_reqs.txt`
  
#### Using Conda Distribution
1.  `conda create -n opensidewalk python=3.8`
2.  `conda activate opensidewalk`
3.  `conda install --file conda_reqs.txt`
4. `pip install -r conda_pip_reqs.txt`

  
##### How to run the code:

  `python main.py --inputPath <<input folder>> --writePath <<Output Directory to Write To>>`

Example:

`python main.py --inputPath TestData/input --writePath TestData/Output`

#####  Expected Input:
Input folder should contain nodes, and ways files belonging to a region with the same prefix.   For example:
|FileName  | Data it should contain |
|--|--|
|1. Redmond_nodes.geojson  | Contains all the points in that region |
|2. Redmond_ways.geojson   | Contains all the ways in that region |

##### Output:
The program writes the following files in the output folder
|FileName  | Data it contains |
|--|--|
|1. Redmond_nodes_valid.geojson  | All the points in the region that adhere to OSW Schema |
|2. Redmond_ways_valid.geojson   | All the ways in the region that are in accordance with OSW schema |
|3. Redmond_nodes_invalid.geojson | All the points in the region that do **NOT** adhere to OSW schema|
|4. Redmond_ways_invalid.geojson | All the ways in the region that do **NOT** adhere to OSW schema |

For the *invalid* files, please look at the tag "fixme" in them to know what the possible reason is for the point or the way declared invalid and take the necessary action to fix them.


TO DO:
- Recheck missing_intersections and recommended_interesections files.
- Qualify subgraph connectivity code better

### How to file issues:
Please open a GitHub issue for any for any bugs/requested features. For each issue, please provide:
    - Branch commit your code is based on. This could be done in a couple of ways:
    -- pick the 'commit' tag from the first line of the command 'git log'
    -- If the code you're working on is based on a release tag, provide the release tag
    - Provide potential test input files you used while running the code