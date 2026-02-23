from src.queries.metadata_queries import upload_metadata_to_db
import json

if __name__ == "__main__":
    with open("D:\\repos\\sentinel_data_downloader\\data\\s2_metadata.json", "r") as f:
        mtd_f = json.loads(f.read())

    upload_metadata_to_db(metadata=mtd_f)
