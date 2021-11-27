""" azure-blob-storage/main.py
This scipt upload file to Azure blob storage.
"""
import logging
import os
import sys

from azure.common import AzureHttpError, AzureMissingResourceHttpError
from azure.core.exceptions import ResourceExistsError
from azure.storage.blob import BlockBlobService

if __name__ == "__main__":
    # USER DEFINE VARIABLES: Container Name
    container_name = 'pytraining'
    blob_name = 'sample.blob'

    # Load logger config & Set Logger
    logging.basicConfig(level='INFO', format='%(asctime)s [%(levelname)s] %(message)s')
    logger = logging.getLogger()

    # Create the client
    # https://docs.microsoft.com/en-us/python/api/azure-storage-blob/azure.storage.blob.blockblobservice.blockblobservice?view=azure-python-previous
    try:
        account = os.environ['STORAGE_ACCOUNT']
        key = os.environ['STORAGE_KEY1']
        service = BlockBlobService(account_name=account, account_key=key)
    except KeyError:
        logger.error('There is no expected environment variables.')
        sys.exit('Error')

    # Create Container
    try:
        service.create_container(container_name)
        logger.info('Create Container is successfully finished: ' + container_name)
    except AzureHttpError:
        logger.error('The container_name should be contain lower letters: ' + container_name)
        sys.exit('Error')
    except ResourceExistsError:
        logger.info(container_name + ' is already exists.')
        pass

    # Upload blob data to Azure blob storage
    # If there is same name file on storage, the function overwrite it.
    data = 'Hello Azure Blob Storage'
    service.create_blob_from_bytes(container_name, blob_name, data.encode())
    # service.create_blob_from_file(container_name, file_name, file_path)
    logger.info('Upload file is successfully finished: ' + blob_name)

    # Get blob data from Azure blob storage
    blob = service.get_blob_to_bytes(container_name, blob_name)
    logger.info('Download file is successfully finished: ' + blob.content.decode())

    # Delete file
    try:
        service.delete_blob(container_name, blob_name)
        logger.info('Delete file is successfully finished: ' + blob_name)
    except AzureMissingResourceHttpError:
        logger.warning('There is no target file: ' + blob_name)
        pass

    # Delete container
    service.delete_container(container_name)
    logger.info('Delete container is successfully finished: ' + container_name)
