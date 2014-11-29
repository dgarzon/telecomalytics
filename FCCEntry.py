class FCCEntry(object):
    """docstring for FCCEntry"""
    def __init__(self):
        super(FCCEntry, self).__init__()
        self.country_name = ""
        self.traffic_billed_in_usa = {}
        self.traffic_billed_in_foreign_countries = {}
        self.total_us_carriers = {}

    def __str__(self):
        obj = ""
        obj += "\tcountry_name: " + self.country_name + "\n"
        obj += "\ttraffic_billed_in_usa: \n"
        for key in self.traffic_billed_in_usa:
            obj += str("\t\t" + key + ": " +
                       str(self.traffic_billed_in_usa[key])
                       + "\n")

        obj += "\ttraffic_billed_in_foreign_countries: \n"
        for k in self.traffic_billed_in_foreign_countries:
            obj += str("\t\t" + k + ": " + "\n")

            for key, value in\
                    self.traffic_billed_in_foreign_countries[k].iteritems():
                obj += "\t\t\t" + str(key) + ": " + str(value) + "\n"

        obj += "\ttotal_us_carriers: \n"
        for key in self.total_us_carriers:
            obj += str("\t\t" + key + ": " +
                       str(self.total_us_carriers[key])
                       + "\n")
        return obj
