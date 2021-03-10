import helpers

class Ticker(object):

    def __init__(self, values_dict) -> None:
        helpers.set_class_property(self, "high", values_dict, True)
        helpers.set_class_property(self, "low", values_dict, True)
        helpers.set_class_property(self, "vol", values_dict, True)
        helpers.set_class_property(self, "last", values_dict, True)
        helpers.set_class_property(self, "buy", values_dict, True)
        helpers.set_class_property(self, "sell", values_dict, True)
        helpers.set_class_property(self, "open", values_dict, True)
        helpers.set_class_property(self, "date", values_dict, True)
