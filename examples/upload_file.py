from for_google.drive.client import GoogleDriveClient
from for_google.drive.constants import GoogleMIMETypes

if __name__ == '__main__':
    client = GoogleDriveClient(
        credentials_file_path="../for-development-375705-f0727c7b86b9.json"
    )
    test = 10
    client.mkdir(f"Test {test}").set_permissions()
    client.upload_file(
        "report.csv",
        f"Report Test {test}",
        origin_mime_type=GoogleMIMETypes.CSV_FILE,
        transform_mime_type=GoogleMIMETypes.GOOGLE_SHEETS
    ).set_permissions()

    files = client.list_files()

    for file in files:
        print(f"Name: {file.name} | URL: {file.uri}")
        # print(f"File {file.id} deleted: {client.delete(file_id=file.id)}")