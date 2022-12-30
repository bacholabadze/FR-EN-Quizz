from PyQt5 import QtWidgets
import sys
import threading
from myapp import Ui_MainWindow
import pandas
import matplotlib.pyplot as plt

from wordTypes import DetailedWord, Word

import time
from pymongo import MongoClient

cluster = MongoClient("mongodb+srv://adminfr:adminen@fr-en-dictionary.jc0716q.mongodb.net/?retryWrites=true&w=majority")


class myApp(QtWidgets.QMainWindow):
    def __init__(self):
        super(myApp, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.pushButton.clicked.connect(self.check_input)  # Enter Button

        # ----------- Database ----------------
        self.FILENAME = "French_word_lists.xlsx"
        self.__conn = cluster
        self.myBase = self.__conn["DictionaryDB"]
        self.mycoll = self.myBase["DictionaryCol"]
        # --------------------------------------

    """ Check if visualisation is closed, with using Threads"""
    def is_closed(self):
        while True:
            print(f"Checking with threads! {plt.get_fignums()} GUI Window is open")
            time.sleep(2)
            if not plt.get_fignums():
                self.close()
                sys.exit()

    # Update database from file
    def update_data_base(self):
        df = pandas.read_excel(self.FILENAME)
        for i in df.index:
            try:
                curWord = DetailedWord(df['Word'][i], df['Translation'][i], df["Word class"][i],
                                       df["Frequency ranking"][i])
                print(curWord.__dict__)
            except KeyError:
                try:
                    curWord = Word(df['Word'][i], df['Translation'][i])
                    print(f"Haha {curWord}")
                except KeyError:
                    print("[!] Invalid Word.")
                    continue
            # self.ui.label_2.setText(f"{curWord['fr_word']}")
            # შევამოწმოთ ესეთი სიტყვა ბაზაში თუ არსებობს უკვე
            print(f"--------------------{curWord['en_word']}")
            word_en = curWord["en_word"]
            result = self.mycoll.find({"en_word": word_en})
            check = True
            for x in result:
                if word_en in x["en_word"]:
                    check = False  # არსებობს და აღარ დავამატოთ
                    print(f"{word_en} - Is already in Database")
            if check:
                print(f"Ready to add {curWord['fr_word']}")
                # print(f"{curWord.__dict__}=========================================")
                self.mycoll.insert_one(curWord.__dict__)

    """ ღილაკზე კლიკისას ამოწმებს შეყვანილ ინფუთს, 
        ინფუთში ბრძანებები:
        
        [!] update > ანახლებს ბაზას
        მონაცემთა ბაზის განახლება ხორციელდება French_word_list.xlsx ფაილიდან.
        ერთიდაიგივე ინგლისური სიტყვა ბაზაში არ დაემატება.
        ბაზის განახლების დასრულების შემდეგ კი ეკრანზე გამოვა პირველი ფრანგული სიტყვა,
        რომელიც უნდა ვთარგმნოთ ინგლისურად. 
        
        [!] start > თამაშის დაწყება
        სწორი პასუხი გიმატებს Correct ქულას +1
        არასწორი პასუხი გიმატებს Wrong ქულას +1
        
        [!] exit > თამაშის დასრულება
        თამაშის დასრულების შემდეგ გამოდის ვიზუალიზაცია სწორი/არასწორი პასუხების
        """

    def start(self):
        random_data = self.mycoll.aggregate([{'$sample': {'size': 1}}])
        for document in random_data:
            print(document)
            self.ui.label_2.setText(document["fr_word"])
            self.ui.plainTextEdit.setPlainText("")

    def check_input(self):
        inp = str(self.ui.plainTextEdit.toPlainText()).strip().lower()
        if inp == "start":
            self.start()

        elif inp == "exit":
            plt.bar(["Wrong", "Correct"], [int(self.ui.label_6.text()), int(self.ui.label_4.text())])
            plt.show()

            # Threading
            t = threading.Thread(target=self.is_closed)
            t.start()

        elif inp == "update":
            self.ui.label.setText("Updating...")
            print("[+] დავიწყოთ ბაზის განახლება")
            t = threading.Thread(target=self.update_data_base)
            t.start()
            if threading.active_count() == 0:
                self.ui.label.setText("Guess The Word")
        else:
            if inp == "":
                print("[!] Empty Input")
            else:
                word = self.mycoll.find_one({"fr_word": self.ui.label_2.text()})
                if word and inp in word["en_word"]:
                    correct_score = int(self.ui.label_4.text()) + 1
                    self.ui.label_4.setText(str(correct_score))
                    self.start()
                elif word:
                    wrong_score = int(self.ui.label_6.text()) + 1
                    self.ui.label_6.setText(str(wrong_score))
                    self.start()


app = QtWidgets.QApplication([])
application = myApp()
application.show()
sys.exit(app.exec())