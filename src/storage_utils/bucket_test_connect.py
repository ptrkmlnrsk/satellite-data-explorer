from src.config import BUCKET_ADDRESS, LOGIN, PASSWORD
from minio import Minio
from minio.error import S3Error


def main() -> None:
    client = Minio(BUCKET_ADDRESS, access_key=LOGIN, secret_key=PASSWORD, secure=False)

    try:
        buckets = client.list_buckets()
        print("Connected to MinIO.")
        print("Buckets: ")

        for bucket in buckets:
            print(f" -{bucket.name}")

    except S3Error as error:
        print("S3 MinIO error")
        print(error)

    except Exception as error:
        print("Unknown error:")
        print(error)


if __name__ == "__main__":
    main()
