import os
import time
import socket
import csv
import requests
import numpy as np
import matplotlib.pyplot as plt
import datetime
import pandas as pd

url = input("Enter domain URL (include http:// or https://): ")
totalTime = float(input("Please enter the total time for running the code in hours"))

max_time = totalTime * 60 * 60  # 8 hours in seconds
filename = "availability2_records.csv"

import requests

def retrieve_domain(url):
    try:
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            print(f"{url} is reachable.")
            return url
        else:
            print(f"{url} returned status code {response.status_code}.")
            return " "
    except requests.exceptions.RequestException as e:
        print(f"{url} is not a valid domain name or is not reachable.")
        return " "



def service(url):
    try:
        response = requests.get(url, timeout=5)  # sends an HTTP GET request
        return response.status_code == 200  # checks if the response status is 200 OK
    except requests.exceptions.RequestException:
        return False


def availability_measurement(ip_address,max_time):
    timestamps = []
    availability_values = []
    success_count = 0
    total_count = 0
    end_time = time.time() + max_time
    if ip_address != " ":
        with open(filename, 'w', newline='') as csvfile:
            csvwriter = csv.writer(csvfile)
            while time.time() < end_time:
                if service(ip_address):
                    success_count += 1
                    var = 1
                else:
                    var = 0
                total_count += 1
                csvwriter.writerow([str(time.time()), str(var)])
                timestamps.append(time.time())
                availability_values.append(var)
                time.sleep(1)
    if(total_count>0):
        availability = (success_count / total_count) * 100
    else:
        availability = (success_count / 1) * 100
    return availability, timestamps, availability_values

ip_address = retrieve_domain(url)
availability, timestamps, availability_values = availability_measurement(ip_address,max_time)
print(f"Server availability over {totalTime} hours: {availability}%")


timestamps = [datetime.datetime.fromtimestamp(ts).strftime('%H:%M:%S') for ts in timestamps]

# Plot the graph
plt.figure(figsize=(10,5))
plt.plot(timestamps, availability_values)
plt.title('Service Availability')
plt.xlabel('Time')
plt.ylabel('Availability')
plt.grid(True)
plt.yticks([0, 1])
plt.xticks(rotation=45)
plt.show()

