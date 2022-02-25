import json
import csv
import os

data_dir = os.environ["DATA_DIR"]
raw_DIR = data_dir + "/raw/"
processed_DIR = data_dir + "/processed/"


def main():
    download_csv()


def download_csv():
    file_names = [
        file_name for file_name in os.listdir(raw_DIR) if ".json" in file_name
    ]
    rows = make_rows(file_names)
    create_csv(rows)


def make_rows(file_names):
    rows = [["entity", "source_file"]]
    for file_name in file_names:
        with open(raw_DIR + file_name, "r") as f:
            data = json.load(f)
        keys = [key for key in data.keys() if "SocialTag" in key]
        for key in keys:
            social_tag_name = data[key]["name"]
            row = [social_tag_name, file_name]
            rows.append(row)
    return rows


def create_csv(rows):
    with open(processed_DIR + "fda_tags.csv", "w") as f:
        writer = csv.writer(f)
        for row in rows:
            writer.writerow(row)


if __name__ == "__main__":
    main()
