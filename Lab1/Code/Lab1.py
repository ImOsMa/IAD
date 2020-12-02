import pandas as pd
from sys import argv
import os
import datetime as DT
import re
import time
from dateutil.relativedelta import relativedelta

class PhoneBook:
    def __init__(self):
        self.dict = {'name': [], 'surn': [], 'date': [], 'mphone': [], 'hphone': [], 'wphone': []}
        self.df = pd.DataFrame(self.dict)
        self.dsize = 6
        self.c = int(self.df.shape[0])

    def read_db(self, file: str) -> pd: # may be it's init
        if os.path.exists(file) and os.path.getsize(file) != 0:
            self.df = pd.read_csv(file, index_col=None)
        else:
            self.df = pd.DataFrame(self.dict)
            self.df.to_csv(file, encoding='utf-8', index=False)
        return self.df

    def add_main_record(self, name: str, surn: str, data: dict) -> int:
        if self.df.loc[(self.df['name'] == name) & (self.df['surn'] == surn)].shape[0] != 0:
            return -1
        else:
            self.df.loc[self.c + 1] = data
            self.c = self.c + 1
            self.save_data("Data.csv")
            return 1

    def change_record_val(self, name: str, surn: str, data: dict, new_name: str, new_surn: str) -> str:
        if self.df.loc[(self.df['name'] == name) & (self.df['surn'] == surn)].shape[0] != 0:
            if bool(data):
                for i, k in zip(data.keys(), data.values()):
                    if k != "":
                        self.df.loc[(self.df['name'] == name) & (self.df['surn'] == surn), i] = k
            else:
                return -1
            if new_name != "" and new_surn == "":
                print("Check1")
                self.df.loc[(self.df['name'] == name) & (self.df['surn'] == surn), 'name'] = new_name
            elif new_name == "" and new_surn != "":
                print("Check2")
                self.df.loc[(self.df['name'] == name) & (self.df['surn'] == surn), 'surn'] = new_surn
            elif new_name != "" and new_surn != "-":
                print("Check3")
                self.df.loc[(self.df['name'] == name) & (self.df['surn'] == surn), 'name'] = new_name
                self.df.loc[(self.df['name'] == new_name) & (self.df['surn'] == surn), 'surn'] = new_surn

            self.save_data("Data.csv")
            return 1
        else:
            return 0


    def delete_record_val(self, name: str, surn: str):

        if self.df.loc[(self.df['name'] == name) & (self.df['surn'] == surn)].shape[0] != 0:
            self.df = self.df.loc[(self.df['name'] != name) | (self.df['surn'] != surn)]
            self.c -= self.df.loc[(self.df['name'] == name) & (self.df['surn'] == surn)].shape[0]
            self.save_data("Data.csv")
            return 1
        else:
            return -1

    def delete_record_val_with_tag(self, dframe, data: dict):
        for i, k in zip(data.keys(), data.values()):
            kat = list()
            kat.append(k)
            dframe = dframe.loc[(dframe[i].isin(kat))]

        names = dframe['name'].to_list()
        surnames = dframe['surn'].to_list()
        for i in range(len(names)):
            nam = list()
            nam.append(names[i])
            sur = list()
            sur.append(surnames[i])
            self.df = self.df.loc[(self.df['name'] != names[i]) | (self.df['surn'] != surnames[i])]
        self.c -= dframe.shape[0]
        self.save_data("Data.csv")
        return 1

    def delete_record_val_with_phone(self, phone: str): # связана с вышестоящей функцией
        d = list()
        d.append(phone)
        if self.df.loc[self.df['mphone'].isin(d)].shape[0] != 0:
            buf = self.df.loc[self.df['mphone'].isin(d)]
            return buf
        else:
            buf = pd.DataFrame()
            return buf

    def print_data(self, data="") -> None:
        buf = self.df
        if type(data) == dict:
            for i, j in zip(list(data.values()), list(data.keys())):
                if i != "":
                    buf = buf.loc[buf[j] == i]
            return buf
        elif type(data) == str:
            return buf
        else:
            return -1

    def print_age(self, name: str, surn: str) -> int:

        if self.df.loc[(self.df['name'] == name) & (self.df['surn'] == surn)].shape[0] != 0:

            date = self.df.loc[(self.df['name'] == name ) & (self.df['surn'] == surn), "date"]
            date = date.iloc[0]
            date = DT.datetime.strptime(date, '%d.%m.%Y')
            now = DT.datetime.now()
            age = abs(relativedelta(date, now)).years
            return int(age)
        else:
            return -1

    def find_user_nearest_bith(self):
        curr_date = DT.datetime.now()
        nearest_dates = [curr_date + DT.timedelta(days=x) for x in range(0, 31)]
        dates = self.df['date'].to_list()
        dates = set(dates)
        buf = pd.DataFrame(self.dict)
        for i in dates:
            birthday = DT.datetime.strptime(i, "%d.%m.%Y")
            if birthday.month - curr_date.month > 1:
                continue
            for n_date in nearest_dates:
                if n_date.month == birthday.month and n_date.day == birthday.day:
                    buf = buf.append(self.df.loc[(self.df['date'] == i)], ignore_index = True)
        print(buf[["name", "surn"]])

    def print_data_higher_N(self, n: int, comp: str):

        dates = self.df["date"].to_list()
        dates = set(dates)
        now = DT.datetime.now()
        buf = pd.DataFrame(self.dict)

        for i in dates:
            birth = DT.datetime.strptime(i, "%d.%m.%Y")
            age = abs(relativedelta(birth, now)).years
            if comp == ">":
                if age > n:
                    buf = buf.append(self.df.loc[self.df['date'] == i])
            elif comp == "<":
                if age < n:
                    buf = buf.append(self.df.loc[self.df['date'] == i])
            elif comp == "=":
                if age == n:
                    buf = buf.append(self.df.loc[self.df['date'] == i])

        if buf.shape[0] == 0:
            print("There is not such elements!!")
        else:
            print(buf)


    def save_data(self, file: str) -> None:

        if os.path.exists(file):
            self.df.to_csv(file, index=False)

class Corrector:

    @staticmethod
    def name_surn_correct(name="") -> str:

        if name.isalpha():
            name = name.lower()
            return name[0].upper() + name[1:]
        return ""

    @staticmethod
    def mob_corrector(mphone: str) -> str:
        if bool(re.match(r'^((8|\+7)[\- ]?)?(\(?\d{3}\)?[\- ]?)?[\d\- ]{7,10}$', mphone)) and (len(mphone) == 11 or len(mphone) == 12):

            if mphone[0] == '+':
                mphone = mphone.replace("+", "")
            mphone = list(mphone)
            if int(mphone[0]) != 8:
                mphone[0] = '8'
            mphone = "".join(mphone)

            return mphone
        return ""

    @staticmethod
    def phone_corrector(phone: str) -> str:
        if bool(re.match(r'^((\+8|\+7|\+1|\+2|\+3|\+4|\+5|\+6|\+9)[\- ]?)?(\(?\d{3}\)?[\- ]?)?[\d\- ]{7,10}$', phone)) and len(phone) < 14:
            return phone
        else:
            return ""

    @staticmethod
    def date_corrector(date: str) -> int:

        try:
            valid_date = time.strptime(date, '%d.%m.%Y')
        except ValueError:
            return -1
        return str(valid_date.tm_mday) + "." + str(valid_date.tm_mon) + "." + str(valid_date.tm_year)


class Menu:
    def __init__(self):
        self.user = PhoneBook()
        self.user.read_db("Data.csv")

    def greeting(self, yname: str) -> None:
        print("Hi, user, smart phonebook greets you!!!")
        time.sleep(2)
        os.system("cls")
        Menu.commands()

    @staticmethod
    def commands() -> int:
        print("Please choose the number of desired operation:")
        print("1. Add new record to the phonebook")
        print("2. Change the record")
        print("3. Delete the record")
        print("4. Show persons with the nearest birthdays")
        print("5. Search the record")
        print("6. Search people > ot < or = N years old")
        print("7. How old is the user")
        print("8. Exit")

    def adding(self) -> None:
        data = {'name': "", 'surn': "", 'date': "", 'mphone': "", 'hphone': [], 'wphone': []}

        def hello() -> None:
            os.system("cls")
            print("       ADDING RECODRD IN PHONEBOOK")
            print("Enter the values in the next cell (cells with * is necessarily")
        com_list = ['Name*', 'Surname*', 'Date of birthday', 'Mob Phone*', "Home Phone", "Work Phone"]
        example_list = ['Islam', 'Osmanov', '14.12.2001 (with dots)', '89167591927', "+5414861231", "+45678932120"]

        hello()

        for i in range(len(com_list)): #com_list, example_list, data.values()

            val = str(input(com_list[i] + " (example: " + example_list[i] + "): "))

            if list(list(data.keys()))[i] == 'name' or list(list(data.keys()))[i] == 'surn':
                while Corrector.name_surn_correct(name=val) == "":
                    print("Please enter correct value!!!")
                    val = str(input(com_list[i] + " (example: " + example_list[i] + "): "))
                val = Corrector.name_surn_correct(name=val)
                data[list(data.keys())[i]] = val

            elif list(data.keys())[i] == 'date':

                if val == "-":
                    data[list(data.keys())[i]] = ""
                    continue

                while Corrector.date_corrector(date=val) == -1 and val != "-":
                    print("Please enter correct value or don't enter value!!!")
                    val = str(input(com_list[i] + " (example: " + example_list[i] + "): "))
                    if val == "-":
                        data[list(data.keys())[i]] = ""
                        continue

                val = Corrector.date_corrector(date=val)
                if val != -1:
                    data[list(data.keys())[i]] = val
                else:
                    data[list(data.keys())[i]] = ""

            elif list(data.keys())[i] == 'mphone':
                while Corrector.mob_corrector(val) == "":
                    print("Please enter correct value!!!")
                    val = str(input(com_list[i] + " (example: " + example_list[i] + "): "))
                val = Corrector.mob_corrector(mphone=val)
                data[list(data.keys())[i]] = val

            elif list(data.keys())[i] == 'hphone' or list(data.keys())[i] == 'wphone':
                if val == "-":
                    data[list(data.keys())[i]] = ""
                    continue
                while Corrector.phone_corrector(val) == "" and val != "-":
                    print("Please enter correct value or don't enter value!!!")
                    val = str(input(com_list[i] + " (example: " + example_list[i] + "): "))
                    if val == "-":
                        data[list(data.keys())[i]] = ""
                        continue
                val = Corrector.phone_corrector(phone=val)
                data[list(data.keys())[i]] = val

        os.system("cls")
        if self.user.add_main_record(name=data['name'], surn=data['surn'], data=data) == 1:
            print("You successfully over adding new record. We are going in Main Menu ")
            time.sleep(2)
            os.system("cls")
            Menu.commands()
        else:
            print("This record has already exist.")
            print("If you want go to menu and cancel adding, enter the 1")
            print("If you want change the record with these keys, enter the 2")
            print("If you want re-fill in the data, enter the 3")
            a = str(input("Enter the number: "))

            while not a.isdigit():
                if not a.isdigit():
                    print("Please, enter the correct variant!!!")
                    a = input("Please, enter the number [1..3]: ")
                elif int(a) > 3 and int(a) <= 0:
                    print("Please, enter the correct variant!!!")
                    a = input("Please, enter the number [1..3]: ")
                else:
                    continue

            if int(a) == 1:
                Menu.commands()
            elif int(a) == 2:
                Client.changing_record()
            elif int(a) == 3:
                Client.adding()

    def changing_record(self):
        print("       CHANGING DATA")
        print("Enter 1, if you want to see list of records")
        print("Enter 2, if you want to search records with certain qualities")
        print("Enter 3, if you want to change record")
        print("Enter 4, to back to menu")
        a = str(input("Enter the number: "))
        while not a.isdigit():
            if not a.isdigit():
                print("Please, enter the correct value!!!")
                a = input("Please, enter the number [1..4]: ")
            elif int(a) > 4 and int(a) <= 0:
              print("Please, enter the correct variant!!!")
              a = input("Please, enter the number [1..4]: ")


        data = {'name': "", 'surn': "", 'date': "", 'mphone': "", 'hphone': [], 'wphone': []}
        com_list = ['Name', 'Surname', 'Date of birthday', 'Mob Phone', "Home Phone", "Work Phone"]
        example_list = ['Islam', 'Osmanov', '14.12.2001 (with dots)', '89167591927', "+5414861231", "+45678932120"]

        if int(a) == 1:
            os.system("cls")
            print(self.user.print_data())
            Client.changing_record()
        if int(a) == 2:
            os.system("cls")
            print("       ADDING DATA FOR SEARCHING")
            print("Enter the values in the next cell, You don't have to fill in the data")

            for i in range(len(com_list)):  # com_list, example_list, data.values()

                val = str(input(com_list[i] + " (example: " + example_list[i] + "): "))

                if list(data.keys())[i] == 'name' or list(data.keys())[i] == 'surn':
                    if val == "-":
                        data[list(data.keys())[i]] = ""
                        continue

                    while Corrector.name_surn_correct(name=val) == "" and val != "-":
                        print("Please enter correct value!!!")
                        val = str(input(com_list[i] + " (example: " + example_list[i] + "): "))
                        if val == "-":
                            data[list(data.keys())[i]] = ""
                            continue

                    val = Corrector.name_surn_correct(name=val)
                    data[list(data.keys())[i]] = val

                elif list(data.keys())[i] == 'date':
                    if val == "-":
                        data[list(data.keys())[i]] = ""
                        continue

                    while Corrector.date_corrector(date=val) == -1 and val != "-":
                        print("Please enter correct value or don't enter value!!!")
                        val = str(input(com_list[i] + " (example: " + example_list[i] + "): "))
                        if val == "-":
                            data[list(data.keys())[i]] = ""
                            continue

                    val = Corrector.date_corrector(date=val)
                    if val != -1:
                        data[list(data.keys())[i]] = val
                    else:
                        data[list(data.keys())[i]] = ""

                elif list(data.keys())[i] == 'mphone':
                    if val == "-":
                        data[list(data.keys())[i]] = ""
                        continue

                    while Corrector.mob_corrector(val) == "" and val != "-":
                        print("Please enter correct value!!!")
                        val = str(input(com_list[i] + " (example: " + example_list[i] + "): "))
                        if val == "-":
                            data[list(data.keys())[i]] = ""
                            continue
                    val = Corrector.mob_corrector(mphone=val)
                    data[list(data.keys())[i]] = val

                elif list(data.keys())[i] == 'hphone' or list(data.keys())[i] == 'wphone':
                    if val == "-":
                        data[list(data.keys())[i]] = ""
                        continue
                    while Corrector.phone_corrector(val) == "" and val != "-":
                        print("Please enter correct value or don't enter value!!!")
                        val = str(input(com_list[i] + " (example: " + example_list[i] + "): "))
                        if val == "-":
                            data[list(data.keys())[i]] = ""
                            continue
                    val = Corrector.phone_corrector(phone=val)
                    data[list(data.keys())[i]] = val

            print("---------------")
            print(self.user.print_data(data=data))
            Client.changing_record()
        if int(a) == 3:
            os.system("cls")
            print("       ADDING DATA FOR CHANGING")
            print("Enter the values in the next cell, You don't have to fill in the data")
            print("Values with * must be filled (name, surname) ")
            com_list = ['Name*', 'Surname*', 'Date of birthday', 'Mob Phone', "Home Phone", "Work Phone"]
            for i in range(len(com_list)):  # com_list, example_list, data.values()

                val = str(input(com_list[i] + " (example: " + example_list[i] + "): "))

                if list(data.keys())[i] == 'name' or list(data.keys())[i] == 'surn':
                    while Corrector.name_surn_correct(name=val) == "":
                        print("Please enter correct value!!!")
                        val = str(input(com_list[i] + "*" + " (example: " + example_list[i] + "): "))

                    val = Corrector.name_surn_correct(name=val)
                    print(val)
                    data[list(data.keys())[i]] = val

                if list(data.keys())[i] == 'date':
                    if val == "-":
                        data[list(data.keys())[i]] = ""
                        continue

                    while Corrector.date_corrector(date=val) == -1 and val != "-":
                        print("Please enter correct value or don't enter value!!!")
                        val = str(input(com_list[i] + " (example: " + example_list[i] + "): "))
                        if val == "-":
                            data[list(data.keys())[i]] = ""
                            continue

                    val = Corrector.date_corrector(date=val)
                    if val != -1:
                        data[list(data.keys())[i]] = val
                    else:
                        data[list(data.keys())[i]] = ""

                if list(data.keys())[i] == 'mphone':
                    if val == "-":
                        data[list(data.keys())[i]] = ""
                        continue

                    while Corrector.mob_corrector(val) and val != "-":
                        print("Please enter correct value!!!")
                        val = str(input(com_list[i] + " (example: " + example_list[i] + "): "))
                        if val == "-":
                            data[list(data.keys())[i]] = ""
                            continue


                    val = Corrector.mob_corrector(mphone=val)
                    data[list(data.keys())[i]] = val

                if list(data.keys())[i] == 'hphone' or list(data.keys())[i] == 'wphone':
                    if val == "-":
                        data[list(data.keys())[i]] = ""
                        continue
                    while Corrector.phone_corrector(val) == "" and val != "-":
                        print("Please enter correct value or don't enter value!!!")
                        val = str(input(com_list[i] + " (example: " + example_list[i] + "): "))
                        if val == "-":
                            data[list(data.keys())[i]] = ""
                            continue
                    val = Corrector.phone_corrector(phone=val)
                    data[list(data.keys())[i]] = val

            for i in range(2):

                if i == 0:
                    new_name = str(input("New Name" + " (example: " + "Islam" + "): "))
                    if new_name == "-":
                        new_name = ""
                        continue
                    while Corrector.name_surn_correct(name=new_name) == "" and val != "-":
                        print("Please enter correct value!!!")
                        new_name = str(input("New Name" + " (example: " + "Islam" + "): "))
                        if new_name == "-":
                            new_name = ""
                            continue

                if i == 1:
                    new_surname = str(input("New Surname" + " (example: " + "Osmanov" + "): "))
                    if new_surname == "-":
                        new_surname = ""
                        continue
                    while Corrector.name_surn_correct(name=new_surname) == "" and val != "-":
                        print("Please enter correct value!!!")
                        new_surname = str(input("New Surname" + " (example: " + "Osmanov" + "): "))
                        if new_surname == "-":
                            new_surname = ""
                            continue

            if self.user.change_record_val(name=data['name'], surn=data['surn'], new_name=new_name, data=data, new_surn=new_surname) == 1:
                print("Changing data was successful")
                time.sleep(2)
                Menu.commands()
            elif self.user.change_record_val(name=data['name'], surn=data['surn'], new_name=new_name, data=data, new_surn=new_surname) == 0:
                print("Such record doesn't exist")
                time.sleep(2)
                Client.changing_record()

            elif self.user.change_record_val(name=data['name'], surn=data['surn'], new_name=new_name, data=data, new_surn=new_surname) == -1:
                print("Mistake in data filling")
                time.sleep(2)
                Client.changing_record()
        if int(a) == 4:
            Menu.commands()

    def delete_record(self):
        print("       REMOVING DATA")
        print("Enter 1, if you want to see list of records")
        print("Enter 2, if you want to remove record, finding with name and surname")
        print("Enter 3, if you want to remove record, finding with Mobile Phone")
        print("Enter 4, to back to menu")
        a = input("Enter the number: ")
        while not a.isdigit():
            if not a.isdigit():
                print("Please, enter the correct variant!!!")
                a = input("Please, enter the number [1..4]: ")
            elif int(a) > 8 and int(a) <= 0:
                print("Please, enter the correct variant!!!")
                a = input("Please, enter the number [1..4]: ")
            else:
                continue

        a = int(a)
        if a == 1:
            os.system("cls")
            print(self.user.print_data())
            Client.delete_record()
        if a == 2:
            print("ENTER NAME AND SURNAME")
            name = str(input("Name" + " (example: " + "Islam" + "): "))
            while Corrector.name_surn_correct(name=name) == "":
                print("Please enter correct value!!!")
                name = str(input("Name" + " (example: " + "Islam" + "): "))
                name = Corrector.name_surn_correct(name=name)

            surname = str(input("Surname" + " (example: " + "Osmanov" + "): "))
            while Corrector.name_surn_correct(name=surname) == "":
                print("Please enter correct value!!!")
                surname = str(input("Name" + " (example: " + "Islam" + "): "))
                surname = Corrector.name_surn_correct(name=surname)

            if self.user.delete_record_val(name, surname) == 1:
                print("DELETING WAS SUCCESSFUL")
                Menu.commands()
            else:
                print("Record with these values doesn't exist")
                Client.delete_record()

        if a == 3:
            print("ENTER MOBILE PHONE")
            mob = str(input("Mobile Phone" + " (example: " + "89087591907" + "): "))

            while Corrector.mob_corrector(mob) == "":
                print("Please enter correct value!!!")
                mob = str(input("Mobile Phone" + " (example: " + "89087591907" + "): "))

            mob = Corrector.mob_corrector(mphone=mob)
            if self.user.delete_record_val_with_phone(mob).shape[0] == 0:
                print("Record with such mobile phone doesn't exist")
                Client.delete_record()
            else:
                print(self.user.delete_record_val_with_phone(mob))
                print("If you want to delete certain record, enter 1")
                print("If you want to delete all these records, enter 2")
                a = input("Enter the number: ")
                while not a.isdigit() and (int(a) != 1 or int(a) !=2 ):
                    a = input("Enter the number: ")
                if int(a) == 1:
                  for i in range(2):
                      if i == 0:
                          new_name = str(input("Name" + " (example: " + "Islam" + "): "))
                          while Corrector.name_surn_correct(name=new_name) == "":
                              print("Please enter correct value!!!")
                              new_name = str(input("Name" + " (example: " + "Islam" + "): "))

                      if i == 1:
                          new_surname = str(input("Surname" + " (example: " + "Osmanov" + "): "))
                          while Corrector.name_surn_correct(name=new_surname) == "":
                              print("Please enter correct value!!!")
                              new_surname = str(input("Surname" + " (example: " + "Osmanov" + "): "))

                  self.user.delete_record_val_with_tag(dframe=self.user.delete_record_val_with_phone(mob), data={'name':new_name, 'surn':new_surname})
                  print("Deleting was successful!")
                  time.sleep(2)
                  Menu.commands()

                else:
                    self.user.delete_record_val_with_tag(dframe=self.user.delete_record_val_with_phone(mob), data={'mphone': mob})
                    print("Deleting was successful!")
                    time.sleep(2)
                    Menu.commands()

        if a == 4:
            print("We are going to menu")
            Menu.commands()

    def nearest_bith(self):
        os.system("cls")
        print("This the list of people with the nearest birthdays(IT CAN BE EMPTY:")
        self.user.find_user_nearest_bith()
        a = str(input("Please enter 1 for going the main menu: "))
        while a != "1":
            print("Enter correct value")
            a = str(input("Please enter 1 for going the main menu: "))

        Menu.commands()

    def search_persons_with_birthday(self):
        os.system("cls")
        print("ENTER THE DATE")
        date = str(input("DATE" + " (example: " + "14.12.2001" + "): "))
        while Corrector.date_corrector(date=date) == -1:
            print("Please enter correct value or don't enter value!!!")
            date = str(input("DATE" + " (example: " + "14.12.2001" + "): "))
        date = Corrector.date_corrector(date=date)
        if self.user.print_data(data={'date': date}) == -1:
            print("The record with these date doesn't exist!")
            Menu.commands()
        else:
            print(self.user.print_data(data={'date': date}))
            Menu.commands()

    def print_person_N_years_old(self):
        os.system("cls")
        print("SEARCH RECORD WITH AGE")
        age = input("Enter the Age (example: 18): ")
        while not age.isdigit():
            print("Enter correct value!")
            age = input("Age (example: 18): ")

        val = str(input("Enter the < or > or = : "))
        while val not in [">", "<", "="]:
            print("Enter correct value!")
            val = str(input("Enter the < or > or = : "))

        self.user.print_data_higher_N(int(age), val)
        a = str(input("Please enter 1 for going the main menu: "))
        while a != "1":
            print("Enter correct value")
            a = str(input("Please enter 1 for going the main menu: "))
        Menu.commands()

    def search_record(self):
        data = {'name': "", 'surn': "", 'date': "", 'mphone': "", 'hphone': [], 'wphone': []}
        com_list = ['Name', 'Surname', 'Date of birthday', 'Mob Phone', "Home Phone", "Work Phone"]
        example_list = ['Islam', 'Osmanov', '14.12.2001 (with dots)', '89167591927', "+5414861231", "+45678932120"]

        os.system("cls")
        print("       ADDING DATA FOR SEARCHING")
        print("Enter the values in the next cell, You don't have to fill in the data")

        for i in range(len(com_list)):  # com_list, example_list, data.values()

            val = str(input(com_list[i] + " (example: " + example_list[i] + "): "))

            if list(data.keys())[i] == 'name' or list(data.keys())[i] == 'surn':
                if val == "-":
                    data[list(data.keys())[i]] = ""
                    continue

                while Corrector.name_surn_correct(name=val) == "" and val != "-":
                    print("Please enter correct value!!!")
                    val = str(input(com_list[i] + " (example: " + example_list[i] + "): "))
                    if val == "-":
                        data[list(data.keys())[i]] = ""
                        continue

                val = Corrector.name_surn_correct(name=val)
                data[list(data.keys())[i]] = val

            elif list(data.keys())[i] == 'date':
                if val == "-":
                    data[list(data.keys())[i]] = ""
                    continue

                while Corrector.date_corrector(date=val) == -1 and val != "-":
                    print("Please enter correct value or don't enter value!!!")
                    val = str(input(com_list[i] + " (example: " + example_list[i] + "): "))
                    if val == "-":
                        data[list(data.keys())[i]] = ""
                        continue
                val = Corrector.date_corrector(date=val)
                if val != -1:
                    data[list(data.keys())[i]] = val
                else:
                    data[list(data.keys())[i]] = ""

            elif list(data.keys())[i] == 'mphone':
                if val == "-":
                    data[list(data.keys())[i]] = ""
                    continue

                while Corrector.mob_corrector(val) == "" and val != "-":
                    print("Please enter correct value!!!")
                    val = str(input(com_list[i] + " (example: " + example_list[i] + "): "))
                    if val == "-":
                        data[list(data.keys())[i]] = ""
                        continue
                val = Corrector.mob_corrector(mphone=val)
                data[list(data.keys())[i]] = val

            elif list(data.keys())[i] == 'hphone' or list(data.keys())[i] == 'wphone':
                if val == "-":
                    data[list(data.keys())[i]] = ""
                    continue
                while Corrector.phone_corrector(val) == "" and val != "-":
                    print("Please enter correct value or don't enter value!!!")
                    val = str(input(com_list[i] + " (example: " + example_list[i] + "): "))
                    if val == "-":
                        data[list(data.keys())[i]] = ""
                        continue
                val = Corrector.phone_corrector(phone=val)
                data[list(data.keys())[i]] = val

        print("---------------")
        print(self.user.print_data(data=data))
        print("---------------")
        a = str(input("Please enter 1 for going the main menu: "))
        while a != "1":
            print("Enter correct value")
            a = str(input("Please enter 1 for going the main menu: "))
        Menu.commands()

    def print_age_man(self):
        print("AGE OF PEOPLE")
        print("ENTER NAME AND SURNAME")
        name = str(input("Name" + " (example: " + "Islam" + "): "))
        while Corrector.name_surn_correct(name=name) == "":
            print("Please enter correct value!!!")
            name = str(input("Name" + " (example: " + "Islam" + "): "))
            name = Corrector.name_surn_correct(name=name)

        surname = str(input("Surname" + " (example: " + "Osmanov" + "): "))
        while Corrector.name_surn_correct(name=surname) == "":
            print("Please enter correct value!!!")
            surname = str(input("Name" + " (example: " + "Islam" + "): "))
            surname = Corrector.name_surn_correct(name=surname)

        if self.user.print_age(name=name, surn=surname) != -1:
            print(name + " " + surname + " is " + str(self.user.print_age(name=name, surn=surname)) + " years old")
            time.sleep(2)
            Menu.commands()
        else:
            print("Record with these values doesn't exist")
            print(" ")
            Menu.commands()




    #@staticmethod
   # def che






if __name__ == "__main__":

    Client = Menu()
    Client.greeting("Islam")
    while True:
        a = input("Please, enter the number [1..8]: ")
        while not a.isdigit():
            if not a.isdigit():
                print("Please, enter the correct variant!!!")
                a = input("Please, enter the number [1..8]: ")
            elif int(a) > 8 and int(a) <= 0:
              print("Please, enter the correct variant!!!")
              a = input("Please, enter the number [1..8]: ")
            else:
                continue

        a = int(a)
        if a == 1:
            Client.adding()
        elif a == 2:
            Client.changing_record()
        elif a == 3:
            Client.delete_record()
        elif a == 4:
            Client.nearest_bith()
        elif a == 5:
            Client.search_record()
        elif a == 6:
            Client.print_person_N_years_old()
        elif a == 7:
            Client.print_age_man()
        elif a == 8:
            break;




