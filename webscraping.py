from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
import pandas as pd
import time
import requests
import csv
from selenium.webdriver.support.ui import WebDriverWait

START_URL = "https://en.wikipedia.org/wiki/Lists_of_stars"
headings = ["Name", "Distance (ly)", "Mass (M☉)", "Radius (R☉)"]
browser = webdriver.Chrome()
data = []

response = requests.get (START_URL, headers = headings, verify = False)

if response.status_code == 200:
    print("Page fetched successfully")
    soup = BeautifulSoup(response.text, "html.parser")
    table = soup.find ("table", {"class": "wikitable"})
    headers = [headings.text.strip () for headings in table.find_all ("th")]
    rows = table.find_all ("tr")

else:
    print (f"Failed to fetch the page. Status code: {response.status_code}")

soup = BeautifulSoup (response.content, "html.parser")

table = soup.find ("table", {"class": "wikitable"})

if not table:
    print ("Could not find the target table on the page")
    exit ()

rows = table.find_all ("tr")

for row in rows [1:]:
    cols = row.find_all ("td")
    if len (cols) >= 4:
        name = cols[1].text.strip ()
        distance = cols[3].text.strip ()
        mass = cols[5].text.strip ()
        radius = cols[6].text.strip ()

        data.append ([name, distance, mass, radius])

csv_filename = "brightest_stars.csv"

with open (csv_filename, "w", newline = "", encoding = "utf-8") as csvfile:
            writer = csv.writer (csvfile)
            writer.writerow (headers)
            writer.writerow (data)

print (f"Data sucessfully saved to {csv_filename}")