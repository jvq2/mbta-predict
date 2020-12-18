import os
import sys

# Change the working directory to be the project root so the modules are
# available. This would not be necessary if it were setup as an installable
dirname = os.path.join(os.path.dirname(__file__), '..')
sys.path.append(dirname)
