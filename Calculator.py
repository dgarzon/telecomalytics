import sys
import os
import time
import xlrd
from FCCEntry import FCCEntry


ROOT_DIR = "."
FCC = {}
WB = {}


class TrafficBilledInTheUSA(object):
    """docstring for TrafficBilledInTheUSA"""
    def __init__(self):
        super(TrafficBilledInTheUSA, self).__init__()
        self.num_of_messages = 0
        self.num_of_minutes = 0
        self.us_carrier_revenues = 0
        self.payout_to_foreign_carriers = 0
        self.retained_revenues = 0


class OriginatingOrTerminatingInTheUS(object):
    """docstring for OriginatingOrTerminatingInTheUS"""
    def __init__(self):
        super(OriginatingOrTerminatingInTheUS, self).__init__()
        self.num_of_messages = 0
        self.num_of_minutes = 0
        self.receipt_from_foreign_carriers = 0


class TransittingTheUSByCountryOfOrigin(object):
    """docstring for TransittingTheUSByCountryOfOrigin"""
    def __init__(self):
        super(TransittingTheUSByCountryOfOrigin, self).__init__()
        self.receipt_from_foreign_carriers = 0
        self.payout_to_foreign_carriers = 0
        self.retained_revenues = 0


class TrafficBilledInForeignCountries(object):
    """docstring for TrafficBilledInForeignCountries"""
    def __init__(self):
        super(TrafficBilledInForeignCountries, self).__init__()
        self.originating_or_terminating_in_the_us = {}
        self.transitting_the_us_by_country_of_origin = {}


class TotalUSCarriers(object):
    """docstring for TotalUSCarriers"""
    def __init__(self):
        super(TotalUSCarriers, self).__init__()
        self.retained_revenues = 0


def prompt():
    print "\n"
    print "------------------------------------------------------------------"
    print "--- Price Elasticity Calculator for International Traffic Data ---"
    print "------------------------------------------------------------------"
    print "\n"
    pass


def get_fcc_entry(path):
    # print path
    entries = []

    workbook = xlrd.open_workbook(path)
    worksheet = workbook.sheet_by_name(workbook.sheet_names()[0])

    num_rows = worksheet.nrows - 1
    num_cells = worksheet.ncols - 1
    curr_row = -1
    while curr_row < num_rows:
        curr_cell = -1
        curr_row += 1

        row = worksheet.row(curr_row)

        entry = FCCEntry()

        traffic_billed_in_the_us = TrafficBilledInTheUSA()

        traffic_billed_in_foreign_countries = TrafficBilledInForeignCountries()

        originating_or_terminating_in_the_us =\
            OriginatingOrTerminatingInTheUS()
        transitting_the_us_by_country_of_origin =\
            TransittingTheUSByCountryOfOrigin()

        total_us_carriers = TotalUSCarriers()

        while curr_cell < num_cells:
            curr_cell += 1
            cell_type = worksheet.cell_type(curr_row, curr_cell)
            cell_value = worksheet.cell_value(curr_row, curr_cell)

            if cell_value == "n.a.":
                cell_value = 0.0

            if curr_cell == 0:
                entry.country_name = str(cell_value)
                pass
            elif curr_cell == 1:
                traffic_billed_in_the_us.num_of_messages = float(cell_value)
                pass
            elif curr_cell == 2:
                traffic_billed_in_the_us.num_of_minutes = float(cell_value)
                pass
            elif curr_cell == 3:
                traffic_billed_in_the_us.us_carrier_revenues =\
                    float(cell_value)
                pass
            elif curr_cell == 4:
                traffic_billed_in_the_us.payout_to_foreign_carriers =\
                    float(cell_value)
                pass
            elif curr_cell == 5:
                traffic_billed_in_the_us.retained_revenues = float(cell_value)
                pass
            elif curr_cell == 6:
                originating_or_terminating_in_the_us.num_of_messages =\
                    float(cell_value)
                pass
            elif curr_cell == 7:
                originating_or_terminating_in_the_us.num_of_minutes =\
                    float(cell_value)
                pass
            elif curr_cell == 8:
                originating_or_terminating_in_the_us.receipt_from_foreign_carriers =\
                    float(cell_value)
                pass
            elif curr_cell == 9:
                transitting_the_us_by_country_of_origin.receipt_from_foreign_carriers =\
                    float(cell_value)
                pass
            elif curr_cell == 10:
                transitting_the_us_by_country_of_origin.payout_to_foreign_carriers =\
                    float(cell_value)
                pass
            elif curr_cell == 11:
                transitting_the_us_by_country_of_origin.retained_revenues =\
                    float(cell_value)
                pass
            elif curr_cell == 12:
                total_us_carriers.retained_revenues = float(cell_value)
                pass
            else:
                print "Error: Cell index out of supported range."

        entry.traffic_billed_in_usa = traffic_billed_in_the_us.__dict__

        traffic_billed_in_foreign_countries.originating_or_terminating_in_the_us =\
            originating_or_terminating_in_the_us.__dict__

        traffic_billed_in_foreign_countries.transitting_the_us_by_country_of_origin =\
            transitting_the_us_by_country_of_origin.__dict__

        entry.traffic_billed_in_foreign_countries =\
            traffic_billed_in_foreign_countries.__dict__

        entry.total_us_carriers = total_us_carriers.__dict__

        entries.append(entry)

    return entries


def parse_fcc_data():
    for subdir, dirs, files in os.walk(ROOT_DIR + "/FCC"):
        for file in files:
            if file.endswith(".xls"):
                print file
                entries = get_fcc_entry(os.path.join(subdir, file))
                FCC[str(os.path.splitext(file)[0])] = entries

    pass


def parse_world_bank_data():
    for subdir, dirs, files in os.walk(ROOT_DIR + "/WB"):
        for file in files:
            if file.endswith(".xls"):
                print os.path.join(subdir, file)
    pass


def print_fcc_data_structure():
    for key, value in FCC.iteritems():
        print str(key) + ":"
        for item in value:
            print(item)
    pass


def main():
    prompt()
    parse_fcc_data()
    # print_fcc_data_structure()
    # parse_world_bank_data()


if __name__ == "__main__":
    main()
