from bs4 import BeautifulSoup as Soup
import os
def parse_report(path):
    base_path = "/Users/aayush/Downloads/ecgen-radiology/"
    if os.path.exists(base_path+path):
        with open(base_path+path,"r") as f:
            text = f.read()
            soup = Soup(text,"lxml-xml").find(Label = "FINDINGS").text
            return soup
    else:
        return ""

def parse_report_for_impression(path):
    base_path = "/Users/aayush/Downloads/ecgen-radiology/"
    if os.path.exists(base_path+path):
        with open(base_path+path,"r") as f:
            text = f.read()
            soup = Soup(text,"lxml-xml").find(Label = "IMPRESSION").text
            return soup
    else:
        return ""

def parse_report_for_image_tag(path):
    base_path = "/Users/aayush/Downloads/ecgen-radiology/"
    if os.path.exists(base_path+path):
        with open(base_path+path,"r") as f:
            text = f.read()
            soup = Soup(text,"lxml-xml").find_all("parentImage")
            return [tag['id'] for tag in soup]


if __name__ == "__main__":
    images = parse_report_for_image_tag("1.xml")
    print(images)