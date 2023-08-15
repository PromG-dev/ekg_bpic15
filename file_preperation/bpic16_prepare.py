# -*- coding: utf-8 -*-
"""
Created on Mon Jun 17 16:51:36 2019

@author: 20175070
"""

# website click data, labour services process
import pandas as pd
import time
import os

# config
input_path = os.path.join(os.getcwd(), "..", "data", "BPIC16")
output_path = os.path.join(input_path, "prepared")  # where prepared files will be stored
file_name = 'BPIC16'


################## data prep ##################

def create_bpic16():
    clicks_log = pd.read_csv(os.path.join(input_path, 'BPI2016_Clicks_Logged_In.csv'), keep_default_na=True,
                             sep=';', encoding='latin1',
                             dtype={"PAGE_NAME": "str", "REF_URL_category": "str", "page_action_detail": "str",
                                    "tip": "str", "service_detail": "str", "xps_info": "str",
                                    "page_action_detail_EN": "str",
                                    "service_detail_EN": "str", "tip_EN": "str"})
    # find ids to ensure that the other data sets only contain these customer ids
    ids = clicks_log['CustomerID'].unique().tolist()
    clicks_log.loc[~clicks_log['TIMESTAMP'].str.contains("\."), 'TIMESTAMP'] = clicks_log['TIMESTAMP'] + ".00"
    clicks_log['TIMESTAMP'] = pd.to_datetime(clicks_log['TIMESTAMP']).dt.strftime("%Y-%m-%d %H:%M:%S.%f")
    clicks_log.to_csv(os.path.join(output_path, f"{file_name}Clicks.csv"))

    complaints = pd.read_csv(os.path.join(input_path, 'BPI2016_Complaints.csv'), keep_default_na=True, sep=';',
                             encoding='latin1')
    complaints = complaints[complaints['CustomerID'].isin(ids)]
    complaints.to_csv(os.path.join(output_path, f"{file_name}Complaints.csv"), na_rep="Unknown")

    questions = pd.read_csv(os.path.join(input_path, 'BPI2016_Questions.csv'), keep_default_na=True, sep=';',
                            encoding='latin1')
    questions = questions[questions['CustomerID'].isin(ids)]
    questions.to_csv(os.path.join(output_path, f"{file_name}Questions.csv"), na_rep="Unknown")

    messages = pd.read_csv(os.path.join(input_path, 'BPI2016_Werkmap_Messages.csv'), keep_default_na=True, sep=';',
                           encoding='latin1')
    messages = messages[messages['CustomerID'].isin(ids)]
    messages.to_csv(os.path.join(output_path, f"{file_name}Messages.csv"), index=True, index_label="idx")


start = time.time()
create_bpic16()
end = time.time()
print("Prepared data for import in: " + str((end - start)) + " seconds.")
