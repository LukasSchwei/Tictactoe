import sys
import os

# Add the BACKEND_NAME_PLACEHOLDER directory to sys.path so modules like 'crud' and 'model' can be found
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../BACKEND_NAME_PLACEHOLDER')))
