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

    python main.py --inputPath <<input folder>> --writePath <<Output Directory to Write To>>

eg) If you want to check the intersecting validation



    python main.py --inputPath TestData/input --writePath TestData/Output

TO DO:
- Add all the validations implemented and tested as default
- Write information about the output files. What they contain and how to use them.
- Remove file_filter from config.py
- Write better instructions about how to recreate the environment
- Separate requirements.txt into conda_reqs.txt, and pip_reqs.txt
- Recheck missing_intersections and recommended_interesections files.
- 