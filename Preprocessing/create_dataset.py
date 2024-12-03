import pandas as pd
import os
from tqdm import tqdm
from xml_parser import parse_report
reports_path = "/Users/aayush/Downloads/ecgen-radiology/"
labels_path = "/Users/aayush/PycharmProjects/CapstoneJSONGeneration/Labels/"
df = pd.DataFrame(columns=["labels","reports","report_number"])
for i in tqdm(range(0, 4000)):
    if os.path.exists(reports_path+f"{i}.xml") and os.path.exists(labels_path+f"{i}.txt"):
        report = parse_report(f"{i}.xml")
        with open(labels_path+f"{i}.txt","r") as labels:
            df = pd.concat([df,pd.DataFrame({"labels":labels.read(),"reports":report,"report_number":i},index = [i])])
print(df)
df.to_json("dataset.json",orient="index")