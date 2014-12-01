import sys
import os
import time
import xlrd
import collections
import csv
import pandas as pd
import numpy as np
import statsmodels.api as sm
import math
import pprint as pp
from itertools import izip
from FCCEntry import FCCEntry
from WBEntry import WBEntry
from Helpers import *


ROOT_DIR = "."
FCC = {}
WB = []
REG = collections.defaultdict(lambda: collections.defaultdict(dict))
COUNTRIES = []
YEARS = [1992, 1993, 1994, 1995, 1996, 1997, 1998, 1999, 2000, 2001, 2002,
         2003, 2004, 2005, 2006, 2007, 2008, 2009, 2010, 2011, 2012]


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
                data.year = YEARS[curr_cell - 1]
                data.gdp = float(cell_value)
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
    global COUNTRIES
    for k in sorted(REG):
        filename = os.path.join(ROOT_DIR + "/REG", str(k) + ".csv")
        COUNTRIES.append(str(k))
        with open(filename, 'wb') as fp:
            csv_writer = csv.writer(fp, delimiter=',')
            csv_writer.writerow(['', 'GDP', 'Price', 'Quantity'])
            for key, val in REG[k].iteritems():
                csv_writer.writerow([key, str(math.log(val["GDP"])),
                                    str(math.log(val["price"])),
                                    str(math.log(val["quantity"]))])


def compute_elastic_regression(country):
    fp = pd.read_csv(os.path.join(ROOT_DIR + "/REG", str(country) + ".csv"),
                     index_col=0)

    X = fp[['GDP', 'Price']]
    y = fp['Quantity']

    X = sm.add_constant(X)
    est = sm.OLS(y, X).fit()

    betas = est.params
    errors = est.bse
    t = est.tvalues
    p = est.pvalues
    conf = est.conf_int()

    return betas, errors, t, p, conf


def write_result_files():
    counter = 0
    filename = os.path.join(ROOT_DIR + "/RESULTS", "Summary" + ".csv")
    with open(filename, 'wb') as fp:
        csv_writer = csv.writer(fp, delimiter=',')
        for country in sorted(COUNTRIES):
            if counter == 0:
                csv_writer.writerow(['Country', 'Beta0 (Coeff)',
                                     'Beta1 (GDP)', 'Beta2 (Price)',
                                     'e0 (Coeff)', 'e1 (GDP)', 'e2 (Price)',
                                     't0 (Coeff)', 't1 (GDP)', 't2 (Price)',
                                     '95%% Coeff. Int (Coeff)',
                                     '95%% Coeff. Int (GDP)',
                                     '95%% Coeff. Int (Price)'])
                counter += 1
            betas, errors, t, p, conf = compute_elastic_regression(country)
            csv_writer.writerow([str(country), str(betas[0]), str(betas[1]),
                                 str(betas[2]), str(errors[0]), str(errors[1]),
                                 str(errors[2]), str(t[0]), str(t[1]),
                                 str(t[2]),
                                 str('[' + str(conf[0][0]) + ', '
                                     + str(conf[1][0]) + ']'),
                                 str('[' + str(conf[0][1]) + ', '
                                     + str(conf[1][1]) + ']'),
                                 str('[' + str(conf[0][2]) + ', '
                                     + str(conf[1][2]) + ']')])


def close_prompt():
    print "------------------------------------------------------------------"
    print "                  Script Completed Successfully!                  "
    print "         Find the result summary in ./RESULTS/Summary.csv         "
    print "------------------------------------------------------------------"
    pass


def main():
    prompt()
    write_regression_files()
    write_result_files()
    close_prompt()


if __name__ == "__main__":
    main()
