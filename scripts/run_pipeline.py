from fda import download_recall_pages
from entities import download_jsons
from report import download_csv


def main():
    print("Downloading the recall pages from FDA.gov...")
    download_recall_pages()
    print("Sending to Refinitiv API and downloading jsons...")
    download_jsons()
    print("Finding social tag names and compiling in CSV...")
    download_csv()
    print(
        "Donezo, but if anything was printed after the send to Refinitiv API call, that means that JSON wasnt downloaded, so try again."
    )


if __name__ == "__main__":
    main()
