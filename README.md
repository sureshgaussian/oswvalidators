# OpenSidewalks data schema, and its validators
This repository contains information about OpenSidewalks (OSW), its data schema, and validators.

Running in Linux

Inside the Root of the project:

1) Creation of Virtual environment :
   virtualenv env1 -p /usr/bin/python3.6

2) Activate virtual environment:
   source env1/bin/activate

3) pip3 install -r requirements.txt


eg) If you want to check the intersecting validation

    python main.py --GeoJSON OSW/TestData/redmond.geojson --validation intersectingvalidation --writePath OSW/TestData/