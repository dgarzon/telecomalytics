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
from copy import deepcopy
from FCCEntry import FCCEntry
from WBEntry import WBEntry
from ImmigrationEntry import ImmigrationEntry
from Helpers import *


ROOT_DIR = "."

FCC = {}
WB = []

COUNTRIES = []

SYMMETRIES = collections.defaultdict(lambda: collections.defaultdict(dict))
PRICES = collections.defaultdict(lambda: collections.defaultdict(dict))
QUANTITIES = collections.defaultdict(lambda: collections.defaultdict(dict))

YEARS = [1992, 1993, 1994, 1995, 1996, 1997, 1998, 1999, 2000, 2001, 2002,
         2003, 2004, 2005, 2006, 2007, 2008, 2009, 2010, 2011, 2012]
ADMISSIBLE_YEARS = [2005, 2006, 2007, 2008, 2009, 2010, 2011, 2012]

AFRICA = ["Algeria", "Angola", "Benin", "Botswana",
          "Burkina", "Burundi", "Cameroon", "Cape Verde",
          "Central African Republic", "Chad", "Comoros",
          "Congo", "Congo, Democratic Republic of", "Djibouti",
          "Egypt", "Equatorial Guinea", "Eritrea", "Ethiopia",
          "Gabon", "Gambia", "Ghana", "Guinea", "Guinea-Bissau",
          "Ivory Coast", "Kenya", "Lesotho", "Liberia", "Libya",
          "Madagascar", "Malawi", "Mali", "Mauritania", "Mauritius",
          "Morocco", "Mozambique", "Namibia", "Niger", "Nigeria", "Rwanda",
          "Sao Tome and Principe", "Senegal", "Seychelles", "Sierra Leone",
          "Somalia", "South Africa", "South Sudan", "Sudan", "Swaziland",
          "Tanzania", "Togo", "Tunisia", "Uganda", "Zambia", "Zimbabwe"]

ASIA = ["Afghanistan", "Bahrain", "Bangladesh", "Bhutan",
        "Brunei", "Burma", "Cambodia", "China", "East Timor",
        "India", "Indonesia", "Iran", "Iraq", "Israel", "Japan",
        "Jordan", "Kazakhstan", "South Korea", "Kuwait",
        "Kyrgyzstan", "Laos", "Lebanon", "Malaysia", "Maldives",
        "Mongolia", "Nepal", "Oman", "Pakistan", "Philippines",
        "Qatar", "Russian Federation", "Saudi Arabia", "Singapore",
        "Sri Lanka", "Syria", "Tajikistan", "Thailand", "Turkey",
        "Turkmenistan", "United Arab Emirates", "Uzbekistan",
        "Vietnam", "Yemen"]

EUROPE = ["Albania", "Andorra", "Armenia", "Austria",
          "Azerbaijan", "Belarus", "Belgium",
          "Bosnia and Herzegovina", "Bulgaria",
          "Croatia", "Cyprus", "Czech Republic",
          "Denmark", "Estonia", "Finland", "France",
          "Georgia", "Germany", "Greece", "Hungary",
          "Iceland", "Ireland", "Italy", "Latvia",
          "Liechtenstein", "Lithuania", "Luxembourg",
          "Macedonia", "Malta", "Moldova", "Monaco",
          "Montenegro", "Netherlands", "Norway",
          "Poland", "Portugal", "Romania", "San Marino",
          "Serbia", "Slovakia", "Slovenia", "Spain",
          "Sweden", "Switzerland", "Ukraine",
          "United Kingdom", "Vatican City"]

NORTH_AMERICA = ["Antigua and Barbuda", "Bahamas", "Barbados",
                 "Belize", "Canada", "Costa Rica", "Cuba",
                 "Dominica", "Dominican Republic", "El Salvador",
                 "Grenada", "Guatemala", "Haiti", "Honduras",
                 "Jamaica", "Mexico", "Nicaragua", "Panama",
                 "Saint Kitts and Nevis", "Saint Lucia",
                 "Saint Vincent and the Grenadines",
                 "Trinidad and Tobago",
                 "United States"]

OCEANIA = ["Australia", "Fiji", "Kiribati",
           "Marshall Islands", "Micronesia", "Nauru",
           "New Zealand", "Palau", "Papua New Guinea",
           "Samoa", "Solomon Islands", "Tonga",
           "Tuvalu", "Vanuatu"]

SOUTH_AMERICA = ["Argentina", "Bolivia", "Brazil",
                 "Chile", "Colombia", "Ecuador",
                 "Guyana", "Paraguay", "Peru",
                 "Suriname", "Uruguay", "Venezuela"]

QUANTITY_PRICE_REGRESSION =\
    collections.defaultdict(lambda: collections.defaultdict(dict))

RATIO_PRICE_REGRESSION =\
    collections.defaultdict(lambda: collections.defaultdict(dict))


def get_fcc_entry(path):
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


def get_immigration_entry(path):
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

        entry = ImmigrationEntry()

        while curr_cell < num_cells:
            curr_cell += 1
            cell_type = worksheet.cell_type(curr_row, curr_cell)
            cell_value = worksheet.cell_value(curr_row, curr_cell)

            if curr_cell == 0:
                entry.country_name = str(cell_value)
            else:
                data = ForeignPopulationData()
                data.year = YEARS[curr_cell + 12]
                data.population = float(cell_value)
                entry.data.append(data.__dict__)
        entries.append(entry)
    return entries


def parse_immigration_data():
    global IMMIGRATION
    for subdir, dirs, files in os.walk(ROOT_DIR + "/IMMIGRATION"):
        for file in files:
            if file.endswith(".xls"):
                print file
                entries = get_foreign_entry(os.path.join(subdir, file))
                IMMIGRATION = entries
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
    for key, value in QUANTITY_PRICE_REGRESSION.iteritems():
        print key
        print value


def prompt():
    print "\n"
    print "------------------------------------------------------------------"
    print "--- Price Elasticity Calculator for International Traffic Data ---"
    print "------------------------------------------------------------------"
    pass


def process_fcc_data():
    global QUANTITY_PRICE_REGRESSION
    global RATIO_PRICE_REGRESSION
    global SYMMETRIES
    for key in sorted(FCC):
        for value in FCC[int(key)]:
            international_quantity =\
                (value.traffic_billed_in_foreign_countries[
                 "originating_or_terminating_in_the_us"
                 ][
                    "num_of_minutes"
                    ] +
                 value.traffic_billed_in_foreign_countries[
                 "originating_or_terminating_in_the_us"
                 ][
                    "num_of_minutes"
                    ])

            national_quantity =\
                (value.traffic_billed_in_usa[
                 "num_of_minutes"
                 ] +
                 value.traffic_billed_in_usa[
                 "num_of_messages"
                 ])

            PRICES[value.country_name][key] =\
                value.traffic_billed_in_usa["us_carrier_revenues"] /\
                national_quantity

            QUANTITIES[value.country_name][key] =\
                national_quantity

            if international_quantity != 0:
                ratio = national_quantity / international_quantity
                SYMMETRIES[value.country_name][key]["ratio"] = ratio
                RATIO_PRICE_REGRESSION[value.country_name][key]["ratio"] =\
                    ratio
            else:
                ratio = 0.000001
                SYMMETRIES[value.country_name][key]["ratio"] = ratio
                RATIO_PRICE_REGRESSION[value.country_name][key]["ratio"] =\
                    ratio

            RATIO_PRICE_REGRESSION[value.country_name][key]["price"] =\
                value.traffic_billed_in_usa["us_carrier_revenues"] /\
                (value.traffic_billed_in_usa["num_of_minutes"] +
                 value.traffic_billed_in_usa["num_of_messages"])

            RATIO_PRICE_REGRESSION[value.country_name][key]["quantity"] =\
                (value.traffic_billed_in_usa["num_of_minutes"] +
                 value.traffic_billed_in_usa["num_of_messages"])

            QUANTITY_PRICE_REGRESSION[value.country_name][key]["price"] =\
                value.traffic_billed_in_usa["us_carrier_revenues"] /\
                (value.traffic_billed_in_usa["num_of_minutes"] +
                 value.traffic_billed_in_usa["num_of_messages"])

            QUANTITY_PRICE_REGRESSION[value.country_name][key]["quantity"] =\
                (value.traffic_billed_in_usa["num_of_minutes"] +
                 value.traffic_billed_in_usa["num_of_messages"])


def write_regression_files_for_quantity_price():
    global COUNTRIES
    for k in sorted(QUANTITY_PRICE_REGRESSION):
        filename = os.path.join(ROOT_DIR + "/GLOBAL/REGRESSION/QUANTITY_PRICE",
                                str(k) + ".csv")
        COUNTRIES.append(str(k))
        with open(filename, 'wb') as fp:
            csv_writer = csv.writer(fp, delimiter=',')
            csv_writer.writerow(['', 'Price', 'Quantity'])
            for key, val in QUANTITY_PRICE_REGRESSION[k].iteritems():
                csv_writer.writerow([key,
                                    str(math.log(val["price"])),
                                    str(math.log(val["quantity"]))])


def compute_elastic_regression_for_quantity_price(country):
    fp = pd.read_csv(os.path.join(ROOT_DIR +
                     "/GLOBAL/REGRESSION/QUANTITY_PRICE",
                                  str(country) + ".csv"),
                     index_col=0)

    X = fp[['Price']]
    y = fp['Quantity']

    X = sm.add_constant(X)
    est = sm.OLS(y, X).fit()

    betas = est.params
    errors = est.bse
    t = est.tvalues
    p = est.pvalues
    conf = est.conf_int()

    return betas, errors, t, p, conf


def write_result_file_for_quantity_price_regression():
    counter = 0
    filename = os.path.join(ROOT_DIR + "/GLOBAL/RESULTS/QUANTITY_PRICE",
                            "Summary" + ".csv")
    with open(filename, 'wb') as fp:
        csv_writer = csv.writer(fp, delimiter=',')
        for country in sorted(COUNTRIES):
            if counter == 0:
                csv_writer.writerow(['Country', 'Beta0 (Coeff)',
                                     'Beta1 (Price)',
                                     'e0 (Coeff)', 'e1 (Price)',
                                     't0 (Coeff)', 't1 (Price)',
                                     '95%% Coeff. Int (Coeff)',
                                     '95%% Coeff. Int (Price)'])
                counter += 1
            betas, errors, t, p, conf =\
                compute_elastic_regression_for_quantity_price(country)
            csv_writer.writerow([str(country), str(betas[0]), str(betas[1]),
                                 str(errors[0]), str(errors[1]),
                                 str(t[0]), str(t[1]),
                                 str('[' + str(conf[0][0]) + ', '
                                     + str(conf[1][0]) + ']'),
                                 str('[' + str(conf[0][1]) + ', '
                                     + str(conf[1][1]) + ']')])


def close_prompt():
    print "------------------------------------------------------------------"
    print "                  Script Completed Successfully!                  "
    print "          Find the results summary in ./GLOBAL/RESULTS/           "
    print "------------------------------------------------------------------"
    pass


def write_prices_file():
    filename = os.path.join(ROOT_DIR + "/GLOBAL/PRICES", "Summary" + ".csv")

    with open(filename, 'wb') as fp:
        csv_writer = csv.writer(fp, delimiter=',')
        csv_writer.writerow(['Country', '1992', '1993', '1994',
                             '1995', '1996', '1997', '1998',
                             '1999', '2000', '2001', '2002',
                             '2003', '2004', '2005', '2006',
                             '2007', '2008', '2009', '2010',
                             '2011', '2012'])
        for country, values in PRICES.iteritems():
            prices = [country]
            for year, price in values.iteritems():
                prices.append(str(price))
            csv_writer.writerow(prices)
    pass


def write_prices_file_for_north_america():
    filename = os.path.join(ROOT_DIR + "/GLOBAL/PRICES",
                            "NorthAmerica" + ".csv")

    with open(filename, 'wb') as fp:
        csv_writer = csv.writer(fp, delimiter=',')
        csv_writer.writerow(['Country', '1992', '1993', '1994',
                             '1995', '1996', '1997', '1998',
                             '1999', '2000', '2001', '2002',
                             '2003', '2004', '2005', '2006',
                             '2007', '2008', '2009', '2010',
                             '2011', '2012'])
        for country, values in PRICES.iteritems():
            if country in NORTH_AMERICA:
                prices = [country]
                for year, price in values.iteritems():
                    prices.append(str(price))
                csv_writer.writerow(prices)
    pass


def write_prices_file_for_south_america():
    filename = os.path.join(ROOT_DIR + "/GLOBAL/PRICES",
                            "SouthAmerica" + ".csv")

    with open(filename, 'wb') as fp:
        csv_writer = csv.writer(fp, delimiter=',')
        csv_writer.writerow(['Country', '1992', '1993', '1994',
                             '1995', '1996', '1997', '1998',
                             '1999', '2000', '2001', '2002',
                             '2003', '2004', '2005', '2006',
                             '2007', '2008', '2009', '2010',
                             '2011', '2012'])
        for country, values in PRICES.iteritems():
            if country in SOUTH_AMERICA:
                prices = [country]
                for year, price in values.iteritems():
                    prices.append(str(price))
                csv_writer.writerow(prices)
    pass


def write_prices_file_for_europe():
    filename = os.path.join(ROOT_DIR + "/GLOBAL/PRICES", "Europe" + ".csv")

    with open(filename, 'wb') as fp:
        csv_writer = csv.writer(fp, delimiter=',')
        csv_writer.writerow(['Country', '1992', '1993', '1994',
                             '1995', '1996', '1997', '1998',
                             '1999', '2000', '2001', '2002',
                             '2003', '2004', '2005', '2006',
                             '2007', '2008', '2009', '2010',
                             '2011', '2012'])
        for country, values in PRICES.iteritems():
            if country in EUROPE:
                prices = [country]
                for year, price in values.iteritems():
                    prices.append(str(price))
                csv_writer.writerow(prices)
    pass


def write_prices_file_for_africa():
    filename = os.path.join(ROOT_DIR + "/GLOBAL/PRICES", "Africa" + ".csv")

    with open(filename, 'wb') as fp:
        csv_writer = csv.writer(fp, delimiter=',')
        csv_writer.writerow(['Country', '1992', '1993', '1994',
                             '1995', '1996', '1997', '1998',
                             '1999', '2000', '2001', '2002',
                             '2003', '2004', '2005', '2006',
                             '2007', '2008', '2009', '2010',
                             '2011', '2012'])
        for country, values in PRICES.iteritems():
            if country in AFRICA:
                prices = [country]
                for year, price in values.iteritems():
                    prices.append(str(price))
                csv_writer.writerow(prices)
    pass


def write_prices_file_for_asia():
    filename = os.path.join(ROOT_DIR + "/GLOBAL/PRICES", "Asia" + ".csv")

    with open(filename, 'wb') as fp:
        csv_writer = csv.writer(fp, delimiter=',')
        csv_writer.writerow(['Country', '1992', '1993', '1994',
                             '1995', '1996', '1997', '1998',
                             '1999', '2000', '2001', '2002',
                             '2003', '2004', '2005', '2006',
                             '2007', '2008', '2009', '2010',
                             '2011', '2012'])
        for country, values in PRICES.iteritems():
            if country in ASIA:
                prices = [country]
                for year, price in values.iteritems():
                    prices.append(str(price))
                csv_writer.writerow(prices)
    pass


def write_prices_file_for_oceania():
    filename = os.path.join(ROOT_DIR + "/GLOBAL/PRICES", "Oceania" + ".csv")

    with open(filename, 'wb') as fp:
        csv_writer = csv.writer(fp, delimiter=',')
        csv_writer.writerow(['Country', '1992', '1993', '1994',
                             '1995', '1996', '1997', '1998',
                             '1999', '2000', '2001', '2002',
                             '2003', '2004', '2005', '2006',
                             '2007', '2008', '2009', '2010',
                             '2011', '2012'])
        for country, values in PRICES.iteritems():
            if country in OCEANIA:
                prices = [country]
                for year, price in values.iteritems():
                    prices.append(str(price))
                csv_writer.writerow(prices)
    pass


def write_quatities_file():
    filename = os.path.join(ROOT_DIR + "/GLOBAL/QUANTITIES",
                            "Summary" + ".csv")

    with open(filename, 'wb') as fp:
        csv_writer = csv.writer(fp, delimiter=',')
        csv_writer.writerow(['Country', '1992', '1993', '1994',
                             '1995', '1996', '1997', '1998',
                             '1999', '2000', '2001', '2002',
                             '2003', '2004', '2005', '2006',
                             '2007', '2008', '2009', '2010',
                             '2011', '2012'])
        for country, values in QUANTITIES.iteritems():
            quantities = [country]
            for year, quantity in values.iteritems():
                quantities.append(str(quantity))
            csv_writer.writerow(quantities)
    pass


def write_quantities_file_for_north_america():
    filename = os.path.join(ROOT_DIR + "/GLOBAL/QUANTITIES",
                            "NorthAmerica" + ".csv")

    with open(filename, 'wb') as fp:
        csv_writer = csv.writer(fp, delimiter=',')
        csv_writer.writerow(['Country', '1992', '1993', '1994',
                             '1995', '1996', '1997', '1998',
                             '1999', '2000', '2001', '2002',
                             '2003', '2004', '2005', '2006',
                             '2007', '2008', '2009', '2010',
                             '2011', '2012'])
        for country, values in QUANTITIES.iteritems():
            if country in NORTH_AMERICA:
                quantities = [country]
                for year, quantity in values.iteritems():
                    quantities.append(str(quantity))
                csv_writer.writerow(quantities)
    pass


def write_quantities_file_for_south_america():
    filename = os.path.join(ROOT_DIR + "/GLOBAL/QUANTITIES",
                            "SouthAmerica" + ".csv")

    with open(filename, 'wb') as fp:
        csv_writer = csv.writer(fp, delimiter=',')
        csv_writer.writerow(['Country', '1992', '1993', '1994',
                             '1995', '1996', '1997', '1998',
                             '1999', '2000', '2001', '2002',
                             '2003', '2004', '2005', '2006',
                             '2007', '2008', '2009', '2010',
                             '2011', '2012'])
        for country, values in QUANTITIES.iteritems():
            if country in SOUTH_AMERICA:
                quantities = [country]
                for year, quantity in values.iteritems():
                    quantities.append(str(quantity))
                csv_writer.writerow(quantities)
    pass


def write_quantities_file_for_europe():
    filename = os.path.join(ROOT_DIR + "/GLOBAL/QUANTITIES", "Europe" + ".csv")

    with open(filename, 'wb') as fp:
        csv_writer = csv.writer(fp, delimiter=',')
        csv_writer.writerow(['Country', '1992', '1993', '1994',
                             '1995', '1996', '1997', '1998',
                             '1999', '2000', '2001', '2002',
                             '2003', '2004', '2005', '2006',
                             '2007', '2008', '2009', '2010',
                             '2011', '2012'])
        for country, values in QUANTITIES.iteritems():
            if country in EUROPE:
                quantities = [country]
                for year, quantity in values.iteritems():
                    quantities.append(str(quantity))
                csv_writer.writerow(quantities)
    pass


def write_quantities_file_for_africa():
    filename = os.path.join(ROOT_DIR + "/GLOBAL/QUANTITIES", "Africa" + ".csv")

    with open(filename, 'wb') as fp:
        csv_writer = csv.writer(fp, delimiter=',')
        csv_writer.writerow(['Country', '1992', '1993', '1994',
                             '1995', '1996', '1997', '1998',
                             '1999', '2000', '2001', '2002',
                             '2003', '2004', '2005', '2006',
                             '2007', '2008', '2009', '2010',
                             '2011', '2012'])
        for country, values in QUANTITIES.iteritems():
            if country in AFRICA:
                quantities = [country]
                for year, quantity in values.iteritems():
                    quantities.append(str(quantity))
                csv_writer.writerow(quantities)
    pass


def write_quantities_file_for_asia():
    filename = os.path.join(ROOT_DIR + "/GLOBAL/QUANTITIES", "Asia" + ".csv")

    with open(filename, 'wb') as fp:
        csv_writer = csv.writer(fp, delimiter=',')
        csv_writer.writerow(['Country', '1992', '1993', '1994',
                             '1995', '1996', '1997', '1998',
                             '1999', '2000', '2001', '2002',
                             '2003', '2004', '2005', '2006',
                             '2007', '2008', '2009', '2010',
                             '2011', '2012'])
        for country, values in QUANTITIES.iteritems():
            if country in ASIA:
                quantities = [country]
                for year, quantity in values.iteritems():
                    quantities.append(str(quantity))
                csv_writer.writerow(quantities)
    pass


def write_quantities_file_for_oceania():
    filename = os.path.join(ROOT_DIR + "/GLOBAL/QUANTITIES",
                            "Oceania" + ".csv")

    with open(filename, 'wb') as fp:
        csv_writer = csv.writer(fp, delimiter=',')
        csv_writer.writerow(['Country', '1992', '1993', '1994',
                             '1995', '1996', '1997', '1998',
                             '1999', '2000', '2001', '2002',
                             '2003', '2004', '2005', '2006',
                             '2007', '2008', '2009', '2010',
                             '2011', '2012'])
        for country, values in QUANTITIES.iteritems():
            if country in OCEANIA:
                quantities = [country]
                for year, quantity in values.iteritems():
                    quantities.append(str(quantity))
                csv_writer.writerow(quantities)
    pass


def print_symmetries_data_structure():
    for key, val in SYMMETRIES.iteritems():
        print key, val


def write_symmetries_file():
    filename = os.path.join(ROOT_DIR + "/GLOBAL/SYMMETRIES",
                            "Summary" + ".csv")

    with open(filename, 'wb') as fp:
        csv_writer = csv.writer(fp, delimiter=',')
        csv_writer.writerow(['Country', '1992', '1993', '1994',
                             '1995', '1996', '1997', '1998',
                             '1999', '2000', '2001', '2002',
                             '2003', '2004', '2005', '2006',
                             '2007', '2008', '2009', '2010',
                             '2011', '2012'])
        for country, values in SYMMETRIES.iteritems():
            symmetries = [country]
            for year, value in values.iteritems():
                symmetries.append(str(value["ratio"]))
            csv_writer.writerow(symmetries)
    pass


def write_symmetries_file_for_north_america():
    filename = os.path.join(ROOT_DIR + "/GLOBAL/SYMMETRIES",
                            "NorthAmerica" + ".csv")

    with open(filename, 'wb') as fp:
        csv_writer = csv.writer(fp, delimiter=',')
        csv_writer.writerow(['Country', '1992', '1993', '1994',
                             '1995', '1996', '1997', '1998',
                             '1999', '2000', '2001', '2002',
                             '2003', '2004', '2005', '2006',
                             '2007', '2008', '2009', '2010',
                             '2011', '2012'])
        for country, values in SYMMETRIES.iteritems():
            if country in NORTH_AMERICA:
                symmetries = [country]
                for year, value in values.iteritems():
                    symmetries.append(str(value["ratio"]))
                csv_writer.writerow(symmetries)
    pass


def write_symmetries_file_for_south_america():
    filename = os.path.join(ROOT_DIR + "/GLOBAL/SYMMETRIES",
                            "SouthAmerica" + ".csv")

    with open(filename, 'wb') as fp:
        csv_writer = csv.writer(fp, delimiter=',')
        csv_writer.writerow(['Country', '1992', '1993', '1994',
                             '1995', '1996', '1997', '1998',
                             '1999', '2000', '2001', '2002',
                             '2003', '2004', '2005', '2006',
                             '2007', '2008', '2009', '2010',
                             '2011', '2012'])
        for country, values in SYMMETRIES.iteritems():
            if country in SOUTH_AMERICA:
                symmetries = [country]
                for year, value in values.iteritems():
                    symmetries.append(str(value["ratio"]))
                csv_writer.writerow(symmetries)
    pass


def write_symmetries_file_for_europe():
    filename = os.path.join(ROOT_DIR + "/GLOBAL/SYMMETRIES",
                            "Europe" + ".csv")

    with open(filename, 'wb') as fp:
        csv_writer = csv.writer(fp, delimiter=',')
        csv_writer.writerow(['Country', '1992', '1993', '1994',
                             '1995', '1996', '1997', '1998',
                             '1999', '2000', '2001', '2002',
                             '2003', '2004', '2005', '2006',
                             '2007', '2008', '2009', '2010',
                             '2011', '2012'])
        for country, values in SYMMETRIES.iteritems():
            if country in EUROPE:
                symmetries = [country]
                for year, value in values.iteritems():
                    symmetries.append(str(value["ratio"]))
                csv_writer.writerow(symmetries)
    pass


def write_symmetries_file_for_africa():
    filename = os.path.join(ROOT_DIR + "/GLOBAL/SYMMETRIES", "Africa" + ".csv")

    with open(filename, 'wb') as fp:
        csv_writer = csv.writer(fp, delimiter=',')
        csv_writer.writerow(['Country', '1992', '1993', '1994',
                             '1995', '1996', '1997', '1998',
                             '1999', '2000', '2001', '2002',
                             '2003', '2004', '2005', '2006',
                             '2007', '2008', '2009', '2010',
                             '2011', '2012'])
        for country, values in SYMMETRIES.iteritems():
            if country in AFRICA:
                symmetries = [country]
                for year, value in values.iteritems():
                    symmetries.append(str(value["ratio"]))
                csv_writer.writerow(symmetries)
    pass


def write_symmetries_file_for_asia():
    filename = os.path.join(ROOT_DIR + "/GLOBAL/SYMMETRIES", "Asia" + ".csv")

    with open(filename, 'wb') as fp:
        csv_writer = csv.writer(fp, delimiter=',')
        csv_writer.writerow(['Country', '1992', '1993', '1994',
                             '1995', '1996', '1997', '1998',
                             '1999', '2000', '2001', '2002',
                             '2003', '2004', '2005', '2006',
                             '2007', '2008', '2009', '2010',
                             '2011', '2012'])
        for country, values in SYMMETRIES.iteritems():
            if country in ASIA:
                symmetries = [country]
                for year, value in values.iteritems():
                    symmetries.append(str(value["ratio"]))
                csv_writer.writerow(symmetries)
    pass


def write_symmetries_file_for_oceania():
    filename = os.path.join(ROOT_DIR + "/GLOBAL/SYMMETRIES",
                            "Oceania" + ".csv")

    with open(filename, 'wb') as fp:
        csv_writer = csv.writer(fp, delimiter=',')
        csv_writer.writerow(['Country', '1992', '1993', '1994',
                             '1995', '1996', '1997', '1998',
                             '1999', '2000', '2001', '2002',
                             '2003', '2004', '2005', '2006',
                             '2007', '2008', '2009', '2010',
                             '2011', '2012'])
        for country, values in SYMMETRIES.iteritems():
            if country in OCEANIA:
                symmetries = [country]
                for year, value in values.iteritems():
                    symmetries.append(str(value["ratio"]))
                csv_writer.writerow(symmetries)
    pass


def write_regression_files_for_symmetry_price():
    for k in sorted(QUANTITY_PRICE_REGRESSION):
        filename = os.path.join(ROOT_DIR + "/GLOBAL/REGRESSION/RATIO_PRICE",
                                str(k) + ".csv")
        with open(filename, 'wb') as fp:
            csv_writer = csv.writer(fp, delimiter=',')
            csv_writer.writerow(['', 'Ratio', 'Price', 'Quantity'])
            for key, val in RATIO_PRICE_REGRESSION[k].iteritems():
                csv_writer.writerow([key,
                                    str(math.log(val["price"])),
                                    str(math.log(val["ratio"])),
                                    str(math.log(val["quantity"]))])


def compute_elastic_regression_for_symmetry_price(country):
    fp = pd.read_csv(os.path.join(ROOT_DIR + "/GLOBAL/REGRESSION/RATIO_PRICE",
                     str(country) + ".csv"),
                     index_col=0)

    X = fp[['Ratio', 'Price']]
    y = fp['Quantity']

    X = sm.add_constant(X)
    est = sm.OLS(y, X).fit()

    betas = est.params
    errors = est.bse
    t = est.tvalues
    p = est.pvalues
    conf = est.conf_int()

    return betas, errors, t, p, conf


def write_result_file_for_symmetry_price_regression():
    counter = 0
    filename = os.path.join(ROOT_DIR + "/GLOBAL/RESULTS/RATIO_PRICE",
                            "Summary" + ".csv")
    with open(filename, 'wb') as fp:
        csv_writer = csv.writer(fp, delimiter=',')
        for country in sorted(COUNTRIES):
            if counter == 0:
                csv_writer.writerow(['Country', 'Beta0 (Coeff)',
                                     'Beta1 (Ratio)', 'Beta2 (Price)',
                                     'e0 (Coeff)', 'e1 (Ratio)', 'e2 (Price)',
                                     't0 (Coeff)', 't1 (Ratio)', 't2 (Price)',
                                     '95%% Coeff. Int (Coeff)',
                                     '95%% Coeff. Int (Ratio)',
                                     '95%% Coeff. Int (Price)'])
                counter += 1
            betas, errors, t, p, conf =\
                compute_elastic_regression_for_symmetry_price(country)
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


def run():
    parse_fcc_data()
    parse_world_bank_data()
    process_fcc_data()

    write_regression_files_for_quantity_price()
    write_regression_files_for_symmetry_price()

    write_result_file_for_quantity_price_regression()
    write_result_file_for_symmetry_price_regression()

    write_prices_file()
    write_prices_file_for_north_america()
    write_prices_file_for_south_america()
    write_prices_file_for_europe()
    write_prices_file_for_asia()
    write_prices_file_for_africa()
    write_prices_file_for_oceania()

    write_quatities_file()
    write_quantities_file_for_north_america()
    write_quantities_file_for_south_america()
    write_quantities_file_for_europe()
    write_quantities_file_for_asia()
    write_quantities_file_for_africa()
    write_quantities_file_for_oceania()

    write_symmetries_file()
    write_symmetries_file_for_africa()
    write_symmetries_file_for_asia()
    write_symmetries_file_for_oceania()
    write_symmetries_file_for_north_america()
    write_symmetries_file_for_south_america()
    write_symmetries_file_for_europe()


def main():
    prompt()
    run()
    close_prompt()


if __name__ == "__main__":
    main()
