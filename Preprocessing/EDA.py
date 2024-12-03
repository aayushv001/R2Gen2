from openai import OpenAI
from pydantic import BaseModel
from xml_parser import parse_report_for_impression
from tqdm import tqdm
import time
import json
import pickle
client = OpenAI(
    organization="",
    project="",
    api_key = "")
class report_classification(BaseModel):
    report_class: int

def get_json(report):
    completion = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system",
             "content": """You are an Expert Radiologist.
                            Your only task is to look at the Impression of a Radiology Report and classify if it is normal or not.
                            Stick to the given JSON format at all times.
                            Here are the given classes:
                            Abnormal:- 1
                            Normal:- 0
                            Examples:
                            1. REPORT:- Normal Chest Xray. Mediastinum Normal.
                            Response:-{"classification":0}
                            2.REPORT:- Patchy opacities. costophrenic angles blunted. Abnormal Chest.
                            Response:-{"classification":1}
                            """},
            {
                "role": "user",
                "content": f"""Can you please tell me if this report is normal or not?
                REPORT:-{report}"""
            }
        ]
    )
    return completion.choices[0].message.content
if __name__ == "__main__":
    res = []
    for i in tqdm(range(0,4000)):
        if (i+1)%100 == 0:
            time.sleep(61)
        report = parse_report_for_impression(f"{i}.xml")
        if report.strip() != "":
            try:
                res.append(json.loads(get_json(report))["classification"])
            except Exception as e:
                print(e)
                pass
    with open("report_eda.pkl","wb") as f:
        pickle.dump(res,f)
