class WBEntry(object):
    """docstring for WBEntry"""
    def __init__(self):
        super(WBEntry, self).__init__()
        self.country_name = ""
        self.data = []

    def __str__(self):
        obj = ""
        obj += "\tcountry_name: " + self.country_name + "\n"
        obj += "\tdata: \n"
        for item in self.data:
            obj += "\t\t" + "year: " + str(item["year"]) + "\n"
            obj += "\t\t" + "gdp: " + str(item["gdp"]) + "\n"

        return obj
