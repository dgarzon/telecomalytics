import sys
import os
import xlrd


ROOT_DIR = "."


def prompt():
    print "\n"
    print "------------------------------------------------------------------"
    print "--- Price Elasticity Calculator for International Traffic Data ---"
    print "------------------------------------------------------------------"
    print "\n"
    pass


def parse_fcc_data():
    for subdir, dirs, files in os.walk(ROOT_DIR + "/FCC"):
        for file in files:
            if file.endswith(".xls"):
                print file
    pass


def parse_world_bank_data():
    for subdir, dirs, files in os.walk(ROOT_DIR + "/WB"):
        for file in files:
            if file.endswith(".xls"):
                print file
    pass


def main():
    prompt()
    parse_fcc_data()
    # parse_world_bank_data()


if __name__ == "__main__":
    main()
