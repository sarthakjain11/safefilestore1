from azure.storage.blob import ContainerClient
from typing import List


class AzureBlobManager():
    '''
    Class which handles files with Azure

    Parameters
    -----------
    conn_str: str
        connection string to the storage account

    container_name: str
        Name of the container

    overwrite: bool, default=True
        Wheter uploaded files should be overwritten
    '''
    conn_str = 'DefaultEndpointsProtocol=https;AccountName=grp2ccproject;AccountKey=IsXNMGKSYADQ339guvpmOeNMgUfC6CJkEZpJy98Rn6UFVqpiIrSfyrbp0eRoJ+dYmqztWLzgRt9K+AStqb4MQQ==;EndpointSuffix=core.windows.net'
    container_name = 'filecontainer'
    overwrite = True

    def __init__(self, conn_str: str, container_name: str,
                 overwrite: bool = True):
        self.conn_str = conn_str
        self.container_name = container_name
        self.overwrite = overwrite

        self.container_client = ContainerClient.from_connection_string(
                    conn_str=conn_str,
                    container_name=container_name)

    def upload(self, flsk_file):
        '''
        Function which uploads file to a storage container

        Parameters
        ----------
        pth_to_file: str
            path where a file is downloaded

        flsk_file: MultiDict object containing all uploaded files
            File from the request
            https://flask.palletsprojects.com/en/1.1.x/api/#flask.Request.files

        Output
        ------
        None
        '''
        blob_client = self.container_client.get_blob_client(
                blob=flsk_file.filename)
        blob_client.upload_blob(flsk_file.stream.read(), blob_type="BlockBlob")

    def listBlobs(self) -> List[str]:
        '''
        Function lists all blobs in a container

        Parameters
        ----------
        None

        Output
        ------
        List[str] with blob names
        '''
        return [blob.name for blob in self.container_client.list_blobs()]

    def containerSize(self) -> float:
        '''
        Calculates size of blobs in container in bytes
        (1 byte = 1e-6 MB)

        Parameters
        ----------
        None

        Output
        ------
        Flot with size
        '''
        blobs_size = sum(blob.size for blob in
                         self.container_client.list_blobs())
        return blobs_size


def allowedFileExtension(filename: str, allowed_ext: List[str]) -> bool:
    '''
    Function tests if file extension is allowed

    Parameters
    -----------
    filename: str
        name of the file

    allowed_ext: List[str]
        list of allowed extensions

    Output
    -----
    Bool whether extension allowed or not
    '''
    file_ext = filename.rsplit('.', 1)[1].lower()

    return filename and file_ext in allowed_ext
