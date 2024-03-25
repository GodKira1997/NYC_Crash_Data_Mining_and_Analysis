"""
file: setup.py
prerequisites: Read readme.md
description: This program installs all the packages required for the main
program
language: python3
Author: Anurag Kallurwar, ak6491
Author: Vishal Panchidi, vp8760
"""


import pip


def install_and_import_packages(package: str):
    try:
        __import__(package)
    except ImportError:
        pip.main(['install', package])
    finally:
        return __import__(package)


warnings = install_and_import_packages('warnings')
print(warnings)
numpy = install_and_import_packages('numpy')
print(numpy)
pandas = install_and_import_packages('pandas')
print(pandas)
matplotlib = install_and_import_packages('matplotlib')
print(matplotlib)
seaborn = install_and_import_packages('seaborn')
print(seaborn)
folium = install_and_import_packages('folium')
print(folium)
