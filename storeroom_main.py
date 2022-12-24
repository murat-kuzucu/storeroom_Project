"""
To run this code, you will have to install some libraries. You can install using pip:

pip install sqlite3 # SQL
pip install opencv-python # Opencv
pip install tkinter # Tkinter
pip install xlwt # Excel

"""

import cv2
import sqlite3
from tkinter import *
from tkinter import ttk
from abc import ABC, abstractmethod
from collections.abc import MutableMapping

class Visualize:
    def __init__(self):
        self.root = Tk()
        self.root.title("Storeroom Software")
        self.frame = ttk.Frame(self.root, padding=10)
        self.frame.grid()

        self.capture_button = ttk.Button(self.frame, text="Capture", command=self.capture_video)
        self.capture_button.grid(column=0, row=0)

        self.image_button = ttk.Button(self.frame, text="Image", command=self.show_image)
        self.image_button.grid(column=1, row=0)

        self.report_button = ttk.Button(self.frame, text="Report Generation", command=self.generate_report)
        self.report_button.grid(column=2, row=0)

        self.root.mainloop()

    def capture_video(self):
        self.cap = cv2.VideoCapture(0)
        while True:
            ret, frame = self.cap.read()
            cv2.imshow("Storeroom", frame)
            if cv2.waitKey(1) == 27:
                break
        self.cap.release()
        cv2.destroyAllWindows()

    def show_image(self):
        pass  # TODO: Add code to show image of selected raw material/product photo

    def generate_report(self):
        pass  # TODO: Add code to generate report for raw materials and products considering their expiration and statistical information

class RawMaterials(MutableMapping):
    def __init__(self, *args, **kwargs):
        self.store = dict()
        self.update(dict(*args, **kwargs))  # use the free update to set keys

    def __getitem__(self, key):
        return self.store[self.__keytransform__(key)]

    def __setitem__(self, key, value):
        self.store[self.__keytransform__(key)] = value

    def __delitem__(self, key):
        del self.store[self.__keytransform__(key)]

    def __iter__(self):
        return iter(self.store)

    def __len__(self):
        return len(self.store)

    def __keytransform__(self, key):
        return key

    def save_to_database(self, conn):
        c = conn.cursor()
        c.execute("CREATE TABLE IF NOT EXISTS raw_materials (name text, date_of_purchase text, supplier text, storage_expiration_date text, storage_code text, description text)")
        for key, value in self.items():
            c.execute("INSERT INTO raw_materials VALUES (?, ?, ?, ?, ?, ?)", value)
        conn.commit()

    def load_from_database(self, conn):
        c = conn.cursor()
        c.execute("SELECT * FROM raw_materials")
        rows = c.fetchall()
        for row in rows:
            self[row[0]] = row[1:]

class Products(RawMaterials):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def __keytransform__(self, key):
        return key.lower()

    def save_to_database(self, conn):
        c = conn.cursor()
        c.execute("CREATE TABLE IF NOT EXISTS products (name text, date_of_production text, customer text, product_expiration_date text, storage_code text, raw_material_codes text, description text)")
        for key, value in self.items():
            c.execute("INSERT INTO products VALUES (?, ?, ?, ?, ?, ?, ?)", value)
        conn.commit()

    def load_from_database(self, conn):
        c = conn.cursor()
        c.execute("SELECT * FROM products")
        rows = c.fetchall()
        for row in rows:
            self[row[0]] = row[1:]

visualize = Visualize()

conn = sqlite3.connect("storeroom.db")

raw_materials = RawMaterials()
raw_materials["RM1"] = ("Name", "Date of Purchase", "Name of Supplier", "Storage Expiration Date", "Storage Code", "Description")
raw_materials["RM2"] = ("Name", "Date of Purchase", "Name of Supplier", "Storage Expiration Date", "Storage Code", "Description")
raw_materials["RM3"] = ("Name", "Date of Purchase", "Name of Supplier", "Storage Expiration Date", "Storage Code", "Description")
raw_materials["RM4"] = ("Name", "Date of Purchase", "Name of Supplier", "Storage Expiration Date", "Storage Code", "Description")
raw_materials["RM5"] = ("Name", "Date of Purchase", "Name of Supplier", "Storage Expiration Date", "Storage Code", "Description")

raw_materials.save_to_database(conn)

products = Products()
products["Product1"] = ("Name", "Date of Production", "Name of Customer", "Product Expiration Date", "Storage Code", "List of Raw Material Codes", "Description")
products["Product2"] = ("Name", "Date of Production", "Name of Customer", "Product Expiration Date", "Storage Code", "List of Raw Material Codes", "Description")
products["Product3"] = ("Name", "Date of Production", "Name of Customer", "Product Expiration Date", "Storage Code", "List of Raw Material Codes", "Description")
products["Product4"] = ("Name", "Date of Production", "Name of Customer", "Product Expiration Date", "Storage Code", "List of Raw Material Codes", "Description")
products["Product5"] = ("Name", "Date of Production", "Name of Customer", "Product Expiration Date", "Storage Code", "List of Raw Material Codes", "Description")

products.save_to_database(conn)

conn.close()
