import google.auth
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from for_google.drive.constants import GoogleMIMETypes, Roles, FilePermissions
from for_google.drive.dataclasses import GFile


class GoogleDriveClient:
    instance = None
    default_scopes = (
        'https://www.googleapis.com/auth/drive.file',
        'https://www.googleapis.com/auth/drive',
        'https://www.googleapis.com/auth/drive.file',
        'https://www.googleapis.com/auth/drive.metadata',
        'https://www.googleapis.com/auth/drive.appdata',
    )
    __scopes: tuple
    __credentials = None
    __credentials_file_path = None
    __gdrive_service = None
    __current_parent_folder = None
    __current_file = None

    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, "instance") or cls.instance is None:
            cls.instance = super(GoogleDriveClient, cls).__new__(cls)

        return cls.instance

    def __init__(self, *args, **kwargs):
        init_scopes = kwargs.get("scopes", self.default_scopes)
        self.__scopes = tuple(init_scopes)

        self.__credentials_file_path = kwargs.get("credentials_file_path")


    def __lazy_get_credentials(self):
        if self.__credentials is None:
            credentials, _ = self.__build_credentials(auth_file_path=self.__credentials_file_path)
            self.__credentials = credentials

        return self.__credentials

    def __lazy_get_gdrive_service(self):
        if self.__gdrive_service is None:
            self.__gdrive_service = self.__get_gdrive_service()

        return self.__gdrive_service

    def __build_credentials(self, auth_file_path=None):
        if auth_file_path is None:
            return google.auth.default(scopes=self.scopes)
        else:
            return google.auth.load_credentials_from_file(auth_file_path, scopes=self.scopes)

    def __get_gdrive_service(self):
        return build('drive', 'v3', credentials=self.__lazy_get_credentials())

    @property
    def scopes(self):
        return self.__scopes

    @property
    def parent_folder(self):
        return self.__current_parent_folder

    @parent_folder.setter
    def parent_folder(self, folder):
        self.__current_parent_folder = folder

    @property
    def current_file(self):
        return self.__current_file

    @current_file.setter
    def current_file(self, file):
        self.__current_file = file

    def mkdir(self, folder_name):
        service = self.__lazy_get_gdrive_service()

        metadata = {
            "name": str(folder_name),
            "mimeType": GoogleMIMETypes.GOOGLE_DRIVE_FOLDER,
        }

        folder = service.files().create(body=metadata, fields="id").execute()
        self.parent_folder = folder
        self.current_file = folder

        return self

    def set_permissions(
            self,
            email_address=None,
            role: Roles=Roles.READER,
            p_type: FilePermissions=FilePermissions.ANYONE,
            domain=None,):
        """
        For more info see `https://developers.google.com/drive/api/v3/reference/permissions/create`
        """
        permissions_body = {
            "role": str(role),
            "type": str(p_type),
            "domain": domain if domain is not None and email_address is None else None,
            "emailAddress": email_address if email_address is not None else None,
            "transferOwnership": role == Roles.OWNER
        }

        service = self.__lazy_get_gdrive_service()
        service.permissions().create(
            fileId=self.current_file.get("id"),
            body=permissions_body,
        ).execute()

        return self

    def upload_file(
            self,
            from_file_path,
            file_name,
            origin_mime_type: GoogleMIMETypes,
            transform_mime_type: GoogleMIMETypes=None,
            parent_id = None,):
        service = self.__lazy_get_gdrive_service()

        if parent_id is not None:
            parents_list = [{"id": parent_id}]
        elif self.parent_folder is not None:
            parents_list = [{"id": self.parent_folder.get("id")}]
        else:
            parents_list = []

        metadata = {
            'name': file_name,
            'mimeType': transform_mime_type if transform_mime_type is not None else origin_mime_type,
            'parents': parents_list,
        }
        media = MediaFileUpload(from_file_path, mimetype=origin_mime_type)
        print(f"metadata: {metadata}")

        file = service.files().create(body=metadata, media_body=media, supportsAllDrives=True, fields="id").execute()

        self.current_file = file

        return self

    def list_files(self, page_size=100):
        service = self.__lazy_get_gdrive_service()

        results = service.files().list(
            pageSize=page_size,
            fields="nextPageToken, files(id, name, webViewLink)"
        ).execute()
        files = results.get('files', [])
        return tuple([
            GFile(id=file.get("id"), name=file.get("name"), uri=file.get("webViewLink"))
            for file in files
        ])

    def delete(self, file_id=None):
        if file_id is not None:
            file_id_for_deletion = file_id
        elif self.current_file is not None:
            file_id_for_deletion = self.current_file.get("id")
        else:
            raise Exception("No file provided")

        service = self.__lazy_get_gdrive_service()
        service.files().delete(fileId=file_id_for_deletion).execute()

        return True
