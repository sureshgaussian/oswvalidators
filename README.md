# OpenSidewalks data schema, and its validators
This repository contains information about OpenSidewalks (OSW), its data schema, and validators.  

General steps to run:
1. Create a Virtual environment in Python
2. Activate virtual environment
3. Install the required packages to run the code

#### Running in Linux
1. `virtualenv env1 -p /usr/bin/python3.6`
2.  `source env1/bin/activate`
3. `pip3 install -r requirements.txt`

#### Running in Windows (Anaconda distribution)
1. `conda create -n opensidewalk python=3.8`
2. `conda activate opensidewalk`
3. `conda install --file requirements.txt`

##### How to run the code:

    python main.py --GeoJSON <<input file>> --validation <<Validation to Perform> --writePath <<Output Directory to Write To>>

eg) If you want to check the intersecting validation



    python main.py --GeoJSON OSW/TestData/redmond.geojson --validation intersectingvalidation --writePath OSW/TestData/
