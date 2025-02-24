import pandas as pd # DataFrame imported
import tkinter as tk # GUI imported

class Event:
    init_data = { # parameter of Event
        "Time_Stamp": "未知",
        "Institution": "其他",
        "Title": "無標題",
        "Category": "其他",
        "Debit": 0,
        "Credit": 0,
        "Remark": "無"
    }

    def __init__(self, **entry): # Event initialization
        self.__dict__.update(self.init_data)
        for key, value in entry.items(): # support Event info imported from initialization
            if key in self.__dict__:
                self.__dict__[key] = value
        
        self.InputWindow = tk.Tk() # create a window
        self.InputWindow.title("輸入資訊")
        self.InputWindow.geometry("800x400")
        self.InputWindow.resizable(False, False)
        self.InputWindow.withdraw()

    def get_TimeStamp(self):
        try:
            data = input("Time_Stamp ").strip()
            if data != "": self.Time_Stamp = data
        except KeyboardInterrupt:
            print("輸入中斷存檔失敗")
        except:
            print("發生未知錯誤")

    def get_Institution(self):
        try:
            data = input("Institution ").strip()
            if data != "": self.Institution = data
        except KeyboardInterrupt:
            print("輸入中斷存檔失敗")
        except:
            print("發生未知錯誤")

    def get_Title(self):
        try:
            data = input("Title ").strip()
            if data != "": self.Title = data
        except KeyboardInterrupt:
            print("輸入中斷存檔失敗")
        except:
            print("發生未知錯誤")

    def get_Category(self):
        try:
            data = input("Category ").strip()
            if data != "": self.Category = data
        except KeyboardInterrupt:
            print("輸入中斷存檔失敗")
        except:
            print("發生未知錯誤")

    def get_Debit(self):
        try:
            data = input("Debit ").strip()
            if data != "": self.Debit = int(data)
        except KeyboardInterrupt:
            print("輸入中斷存檔失敗")
        except:
            print("發生未知錯誤")

    def get_Credit(self):
        try:
            data = input("Credit ").strip()
            if data != "": self.Credit = (data)
        except KeyboardInterrupt:
            print("輸入中斷存檔失敗")
        except:
            print("發生未知錯誤")

    def get_Remark(self):
        try:
            data = input(f"Remark ").strip()
            if data != "": self.Remark = data
        except KeyboardInterrupt:
            print("輸入中斷存檔失敗")
        except:
            print("發生未知錯誤")

    def create(self): # manual input Event info and make it DataFrame
        self.get_TimeStamp()
        self.get_Institution()
        self.get_Title()
        self.get_Category()
        self.get_Debit()
        self.get_Credit()
        self.get_Remark()
        data = pd.DataFrame([self.__dict__]) # turn the Event attributes into a single row of DataFrame
        print(data)
        return data
    
sample = Event()
sample.create()
sample.recall()