################################################################################################################
# The purpose of this file is to generate the fixtures for loading. It is anticipated
# that the size of the fixtures will be prohibitive for storing and also the fixture
# data will change over time, so having the ability to dynamically generate is desired.
################################################################################################################

#!/usr/bin/env python
import os
import sys
from lungmap_sparql_client.lungmap_sparql_client import LMClient
from lap.settings import BASE_DIR as PROJECT_DIR

if __name__ == "__main__":
    fixture_dir = os.path.join(PROJECT_DIR,'analytics','fixtures')
    if not os.path.exists(fixture_dir):
        print("Creating directory: ", fixture_dir)
        os.makedirs(fixture_dir)

    myclient = LMClient()
    myclient.generate_repository_fixtures(location = fixture_dir)

