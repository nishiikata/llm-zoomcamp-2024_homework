"""
NOTE: Scratchpad blocks are used only for experimentation and testing out code.
The code written here will not be executed as part of the pipeline.
"""


## 

from importlib.metadata import version


mage_version: str = version("mage-ai")
print("Q1 Answer: The version of mage is {}".format(mage_version))
