from openai import OpenAI
from pydantic import BaseModel
from xml_parser import parse_report
from tqdm import tqdm
import time
client = OpenAI(
    organization="",
    project="",
    api_key = "")

class clinical_finding(BaseModel):
    clinical_finding: str
    existence: str
    descriptive_term:str
    observation: str
class Sentence_labels(BaseModel):
    anatomical_entity:list[str]
    location_descriptor:str
    procedure:list[str]
    clinical_findings: list[clinical_finding]

class Radiology_Labels(BaseModel):
    Sentences: list[Sentence_labels]

def get_json(report):
    completion = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": """You are an expert radiologist.
                                          Your only task is to convert the given report sentence by sentence into JSON Labels.
                                          Here is some more information about the labels:-
                                          Sentences:- List of Sentence Labels sentence by sentence.
                                          anatomical_entity:- List of body parts mentioned in the sentence.
                                          location_descriptor:- any location descriptor provided otherwise eg [Right,left,upper,lower,up,down,etc]
                                          procedure: List of medical descriptions mentioned in the sentence
                                          clinical_findings: List of clinical_finding schemas
                                          clinical_finding: The clinical finding in the sentence
                                          existence:existence of the clinical finding can be Positive,Negative or Unclear NOTE:{Positive:pos_dx,Negative:neg_dx,Unclear:unc_dx}
                                          EXAMPLE:
                                          Report:Retrocardiac opacity which may represent atelectasis and or or small effusion is stable. Right Lung is otherwise clear. No pneumothorax. NG tube tip below the diaphragm.
                                          JSON:{Sentences:[{"anatomical entity":null,
                                                            "location_descriptor":null,
                                                            "procedure":[null,]
                                                            "clinical findings":[{
                                                                    "clinical finding":"retrocardiac opacity",
                                                                    "existence":"pos_dx",
                                                                    "descriptive_term":"retrocardiac",
                                                                    "observation":"opacity"
                                                                    },
                                                                    {
                                                                    "clinical finding":"atelectasis",
                                                                    "existence":"unc_dx",
                                                                    "observation":"atelectasis"
                                                                    },
                                                                    {
                                                                    "clinical finding":"or small effusion",
                                                                    "existence":"unc_dx",
                                                                    "descriptive_term":"or small",
                                                                    "observation":"effusion",
                                                                    }
                                                                ]
                                                            },
                                                            {
                                                            "anatomical entity":"lungs"
                                                            "location_descriptor":Right,
                                                            "procedure":[null] 
                                                           "clinical findings":[{
                                                                    "clinical finding":"clear",
                                                                    "existence":"neg_dx",
                                                                    "observation":"clear"
                                                                    }
                                                                ]
                                                            },
                                                            {"anatomical entity":null,
                                                            "location_descriptor":null,
                                                            "procedure":[null] 
                                                            "clinical findings":[{
                                                                    "clinical finding":"pneumothorax",
                                                                    "existence":"neg_dx",
                                                                    "observation":"pneumothorax"
                                                                }]
                                                            },
                                                            {
                                                            "anatomical entity":"diaphragm",
                                                            "location_descriptor":null,
                                                            "procedure":[null] 
                                                            "clinical findings":[null]
                                                            }]}"""},
            {
                "role": "user",
                "content": f"""Can i get JSON labels for the following report?
                REPORT:-{report}"""
            }
        ]
    )
    return completion.choices[0].message.content
if __name__ == "__main__":
    for i in tqdm(range(200,4000)):
        if i%100 == 0:
            time.sleep(61)
        report = parse_report(f"{i}.xml")
        if report.strip() != "":
            with open(f"Labels/{i}.txt","w") as f:
                f.write(get_json(report))
