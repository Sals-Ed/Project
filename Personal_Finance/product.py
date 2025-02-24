import pandas
import IPython

class Product:
    init_data = { # parameter of Product
        "Time_Stamp": "未知",
        "Product_Name": "未知",
        "Product_Code": "未知",
        "Reoduct_Type": "未知",
        "Bid_Price": 0,
        "Quantity": 0,
        "Bid_Value": 0,
        "Current_Price": 0,
        "Current_Value": 0,
        "Current_ROI": 0.0
    }

    def __init__(self, **entry): # Product initialization
        self.__dict__.update(self.init_data)
        for key, value in entry.items(): # support Product info imported from initialization
            if key in self.__dict__:
                self.__dict__[key] = value