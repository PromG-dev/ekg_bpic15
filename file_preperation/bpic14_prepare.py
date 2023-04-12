# -*- coding: utf-8 -*-
"""
Created on Mon Jul  1 14:02:29 2019

@author: 20175070
"""

import pandas as pd
import time
import os

# config
input_path = os.path.join(os.getcwd(), "..", "data", "BPIC14")
output_path = os.path.join(input_path, "prepared")  # where prepared files will be stored

start = time.time()

incident = pd.read_csv(os.path.join(input_path, 'Detail_Incident.csv'), keep_default_na=True, sep=';', decimal=",",
                       dtype={"Urgency": "str"})
# only keep numeric values for urgency column and convert to Int64
incident["Urgency"] = incident["Urgency"].str.replace('(\D+)', '', regex=True)
incident["Urgency"] = incident["Urgency"].astype('Int64')
incident.to_csv(os.path.join(output_path, "BPIC14Incident.csv"))

interaction = pd.read_csv(os.path.join(input_path, 'Detail_Interaction.csv'), keep_default_na=True, sep=';',
                          dtype={"Urgency": "str"})
# only keep numeric values for urgency column and convert to Int64
interaction["Urgency"] = interaction["Urgency"].str.replace('(\D+)', '', regex=True)
interaction["Urgency"] = interaction["Urgency"].astype('Int64')
interaction.to_csv(os.path.join(output_path, "BPIC14Interaction.csv"))

end = time.time()
print("Prepared data for import in: " + str((end - start)) + " seconds.")
