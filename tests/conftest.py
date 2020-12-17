import os
import sys

# Change the working directory to be the project root so `app` is available
dirname = os.path.join(os.path.dirname(__file__), '..')
sys.path.append(dirname)
