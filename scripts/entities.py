from bs4 import BeautifulSoup
import requests
import os
import re
import pprint
import json

data_dir = os.environ["DATA_DIR"]
raw_DIR = data_dir + "/raw/"


def main():
    download_jsons()


def download_jsons():
    paragraph_dict = get_reason()
    send_to_refinitiv(paragraph_dict)


def get_reason():
    paragraph_dict = {}
    file_names = [
        file_name for file_name in os.listdir(raw_DIR) if ".html" in file_name
    ]
    for file_name in file_names:
        with open(raw_DIR + file_name, "r") as f:
            soup = BeautifulSoup(f, "html.parser")  # parsing html that is saved
        header = soup.find("h2", text=re.compile("Reason"))
        reason_paragraph = header.find_next_sibling("p").text
        recall_name = file_name.split(".")[0]
        paragraph_dict[recall_name] = reason_paragraph
    return paragraph_dict


def send_to_refinitiv(paragraph_dict):
    CALAIS_URL = "https://api-eit.refinitiv.com/permid/calais"
    API_KEY = os.environ["OPENCALAIS_API_KEY"]
    headers = {
        "X-AG-Access-Token": API_KEY,
        "Content-Type": "text/raw",
        "outputformat": "application/json",
        "x-calais-selectiveTags": "company,industry,socialtags",
    }
    for (
        name,
        paragraph,
    ) in (
        paragraph_dict.items()
    ):  # iterate over dictionary, separate between keys and values
        try:
            response = requests.post(
                CALAIS_URL, data=paragraph.encode("utf-8"), headers=headers, timeout=80
            ).json()
            with open(raw_DIR + name + ".json", "w") as f:
                json.dump(response, f)
        except:
            print(name, paragraph)


# API was giving trouble, different errors differnt times I executed, I used try and except to identify the JSons that weren't downloaded. after trying a few times, i got all of them.


if __name__ == "__main__":
    main()
