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


class ImmigrationPopulationData(object):
    """docstring for ImmigrationPopulationData"""
    def __init__(self):
        super(ImmigrationPopulationData, self).__init__()
        self.year = 0
        self.population = 0
