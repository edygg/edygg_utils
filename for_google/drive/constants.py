
class GoogleMIMETypes:
    """
    MIME types supported `https://developers.google.com/drive/api/guides/mime-types`
    Common MIME types `https://developer.mozilla.org/en-US/docs/Web/HTTP/Basics_of_HTTP/MIME_types/Common_types`
    """
    CSV_FILE = "text/csv"
    ZIP_FILE = "application/zip"

    EXCEL_FILE = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"

    AUDIO = "application/vnd.google-apps.audio"
    VIDEO = "application/vnd.google-apps.spreadsheet"
    UNKNOWN = "application/vnd.google-apps.unknown"

    GOOGLE_DOCS = "application/vnd.google-apps.document"
    GOOGLE_SHEETS = "application/vnd.google-apps.spreadsheet"
    GOOGLE_PHOTO = "application/vnd.google-apps.spreadsheet"

    GOOGLE_DRIVE_FILE = "application/vnd.google-apps.file"
    GOOGLE_DRIVE_FOLDER = "application/vnd.google-apps.folder"


class FilePermissions:
    USER = "user"
    GROUP = "group"
    DOMAIN = "domain"
    ANYONE = "anyone"


class Roles:
    OWNER = "owner"
    ORGANIZER = "Organizer"
    FILE_ORGANIZER = "fileorganizer"
    WRITER = "writer"
    COMMENTER = "commenter"
    READER = "reader"