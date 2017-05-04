"""
    This program updates the given source  zip file to the AWS Lambda for given Lambda function ARN.
"""
import boto3
import os
import shutil


class LambdaUpdater(object):
    def __init__(self, config):
        self.__config = config  # Place holder for lambda configuration
        self.__client = boto3.client('lambda')
        folder = self.__config['folder']
        self.__absoluteFolderPath = self.__getAbsolutePath(folder)
        self.__file_location = self.__zipFile(self.__absoluteFolderPath)

    def __getAbsolutePath(self, folder):
        # print "Current Dir: %s" % os.getcwd()
        return os.path.join(os.getcwd(), folder)

    def __zipFile(self, folder):
        zipFileName = self.__config['serviceName'] + '.zip'
        shutil.make_archive(self.__config['serviceName'], 'zip', folder)
        return zipFileName

    def upload_lambda_fuction(self):
        file_bytes_read = open(self.__file_location, "rb").read()
        response = self.__client.update_function_code(
            FunctionName=self.__config['arn'],
            ZipFile=file_bytes_read,
            Publish=True
        )

        if response['ResponseMetadata']['HTTPStatusCode'] == 200:
            return True
        return False