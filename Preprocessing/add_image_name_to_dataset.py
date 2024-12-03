import pandas as pd
import os
from tqdm import tqdm
from xml_parser import parse_report_for_image_tag
def add_image_for_row(ex):
    report_num = str(ex["report_number"]) + ".xml"
    return parse_report_for_image_tag(report_num)
if __name__ == "__main__":
    df = pd.read_json("dataset.json",orient="index")
    df["image"] = df.apply(add_image_for_row,axis = 1)
    df = df.explode(["image"]).reset_index(drop = True)
    df.to_json("image_added_dataset.json",orient = "index")