import pandas
import IPython

class Bank:
    init_data = { # parameter of Bank
        "Account_list": pandas.DataFrame(),
        "Balance": 0,
        "Value": 0,
        "Event_list": pandas.DataFrame()
    }

    def __init__(self, **entry): # Bank initialization
        self.__dict__.update(self.init_data)
        for key, value in entry.items(): # support Event info imported from initialization
            if key in self.__dict__:
                self.__dict__[key] = value

    def update(self, event): # renew Bank info from the new transaction
        self.Event_list = pandas.concat([self.Event_list, event], ignore_index=True) # Link old and new transaction together
        self.Event_list = self.Event_list.sort_values(by=["Time_Stamp"], ascending=True) # sort them by Time_stamp
        self.Balance = self.Balance + event.Credit.sum() - event.Debit.sum() # calculate related Bank info
        self.Value
        IPython.display.display(self.Event_list)