import os
import boto3
import ftplib
import tempfile


class Sync:
    def __init__(self):
        self.ftp = ftplib.FTP(os.environ['SERVER'])
        self.ftp.login(os.environ['USER'], os.environ['PASSWORD'])
        self.s3 = boto3.client('s3')

    def run(self, dirname):
        names = self.ftp.nlst(dirname)
        for name in names:
            if self.__is_file(name):
                if not self.__s3_has_key(name):
                    with tempfile.TemporaryFile() as file:
                        self.ftp.retrbinary('RETR ' + name, file.write)
                        file.seek(0)
                        self.s3.upload_fileobj(file, os.environ['BUCKET'],
                                               name)
                        print(name)
            else:
                self.run(name)

    def __is_file(self, name):
        try:
            self.ftp.size(name)
            return True
        except ftplib.error_perm:
            return False

    def __s3_has_key(self, key):
        try:
            self.s3.head_object(Bucket=os.environ['BUCKET'], Key=key)
            return True
        except self.s3.exceptions.ClientError as e:
            if e.response['Error']['Code'] == '404':
                return False
            else:
                raise


def lambda_handler(event, context):
    Sync().run('.')
