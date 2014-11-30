import sys
import os
import time
import xlrd
import collections
import csv
from itertools import izip
from FCCEntry import FCCEntry
from WBEntry import WBEntry


ROOT_DIR = "."
FCC = {}
WB = []
REG = collections.defaultdict(lambda: collections.defaultdict(dict))


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


class WorldBankData(object):
    """docstring for WorldBankData"""
    def __init__(self):
        super(WorldBankData, self).__init__()
        self.year = 0
        self.gdp = 0


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
                entry.country_name = str(cell_value).rstrip()
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
    global FCC
    for subdir, dirs, files in os.walk(ROOT_DIR + "/FCC"):
        for file in files:
            if file.endswith(".xls"):
                print file
                entries = get_fcc_entry(os.path.join(subdir, file))
                FCC[int(os.path.splitext(file)[0])] = entries

    pass


def get_world_bank_entry(path):
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

        entry = WBEntry()

        while curr_cell < num_cells:
            curr_cell += 1
            cell_type = worksheet.cell_type(curr_row, curr_cell)
            cell_value = worksheet.cell_value(curr_row, curr_cell)

            if curr_cell == 0:
                entry.country_name = str(cell_value)
            else:
                data = WorldBankData()

                if curr_cell == 1:
                    data.year = 1992
                    data.gdp = float(cell_value)
                    pass
                elif curr_cell == 2:
                    data.year = 1993
                    data.gdp = float(cell_value)
                    pass
                elif curr_cell == 3:
                    data.year = 1994
                    data.gdp = float(cell_value)
                    pass
                elif curr_cell == 4:
                    data.year = 1995
                    data.gdp = float(cell_value)
                    pass
                elif curr_cell == 5:
                    data.year = 1996
                    data.gdp = float(cell_value)
                    pass
                elif curr_cell == 6:
                    data.year = 1997
                    data.gdp = float(cell_value)
                    pass
                elif curr_cell == 7:
                    data.year = 1998
                    data.gdp = float(cell_value)
                    pass
                elif curr_cell == 8:
                    data.year = 1999
                    data.gdp = float(cell_value)
                    pass
                elif curr_cell == 9:
                    data.year = 2000
                    data.gdp = float(cell_value)
                    pass
                elif curr_cell == 10:
                    data.year = 2001
                    data.gdp = float(cell_value)
                    pass
                elif curr_cell == 11:
                    data.year = 2002
                    data.gdp = float(cell_value)
                    pass
                elif curr_cell == 12:
                    data.year = 2003
                    data.gdp = float(cell_value)
                    pass
                elif curr_cell == 13:
                    data.year = 2004
                    data.gdp = float(cell_value)
                    pass
                elif curr_cell == 14:
                    data.year = 2005
                    data.gdp = float(cell_value)
                    pass
                elif curr_cell == 15:
                    data.year = 2006
                    data.gdp = float(cell_value)
                    pass
                elif curr_cell == 16:
                    data.year = 2007
                    data.gdp = float(cell_value)
                    pass
                elif curr_cell == 17:
                    data.year = 2008
                    data.gdp = float(cell_value)
                    pass
                elif curr_cell == 18:
                    data.year = 2009
                    data.gdp = float(cell_value)
                    pass
                elif curr_cell == 19:
                    data.year = 2010
                    data.gdp = float(cell_value)
                    pass
                elif curr_cell == 20:
                    data.year = 2011
                    data.gdp = float(cell_value)
                    pass
                elif curr_cell == 21:
                    data.year = 2012
                    data.gdp = float(cell_value)
                    pass
                else:
                    print "Error: Cell index out of supported range."

                entry.data.append(data.__dict__)
        entries.append(entry)

    return entries


def parse_world_bank_data():
    global WB
    for subdir, dirs, files in os.walk(ROOT_DIR + "/WB"):
        for file in files:
            if file.endswith(".xls"):
                print file
                entries = get_world_bank_entry(os.path.join(subdir, file))
                WB = entries
    pass


def print_fcc_data_structure():
    for key, value in FCC.iteritems():
        print str(key) + ":"
        for item in value:
            print(item)
    pass


def print_world_bank_data_structure():
    for item in WB:
        print item


def print_regression_structure():
    for key, value in REG.iteritems():
        print key
        print value


def prompt():
    print "\n"
    print "------------------------------------------------------------------"
    print "--- Price Elasticity Calculator for International Traffic Data ---"
    print "------------------------------------------------------------------"
    parse_fcc_data()
    parse_world_bank_data()
    process_fcc_data()
    print "------------------------------------------------------------------"
    pass


def process_fcc_data():
    global REG
    for key in sorted(FCC):
        for value in FCC[int(key)]:
            wb_item = [item for item in WB
                       if item.country_name == value.country_name][0]
            for wb_value in wb_item.data:
                if wb_value["year"] == key:
                    REG[value.country_name][key]["GDP"] = wb_value["gdp"]

            REG[value.country_name][key]["price"] =\
                value.traffic_billed_in_usa["us_carrier_revenues"] /\
                value.traffic_billed_in_usa["num_of_minutes"]

            REG[value.country_name][key]["quantity"] =\
                value.traffic_billed_in_usa["num_of_minutes"]


def write_regression_files():
    for k in sorted(REG):
        filename = os.path.join(ROOT_DIR + "/REG", str(k) + ".csv")
        with open(filename, 'wb') as fp:
            csv_writer = csv.writer(fp, delimiter=',')
            csv_writer.writerow(['', 'GDP', 'Price', 'Quantity'])
            for key, val in REG[k].iteritems():
                csv_writer.writerow([key, str(val["GDP"]),
                                    str(val["price"]),
                                    str(val["quantity"])])


def main():
    prompt()
    write_regression_files()


if __name__ == "__main__":
    main()
