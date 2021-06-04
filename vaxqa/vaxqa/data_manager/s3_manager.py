import json, os
from os import listdir
from os.path import isfile, join

import pandas as pd
from pathlib import Path

from vaxqa.settings import settings

# if settings['env'] == 'local':
#     import localstack_client.session as boto3_session
# elif settings['env'] == 'dev':
#     import boto3.session as boto3_session

if os.environ.get("DASH_ENV") == "prod":
    import boto3.session as boto3_session
else:
    import localstack_client.session as boto3_session


class S3Manager:

    bucket_name = 'vaxqa-data'

    def __init__(self):
        my_session = boto3_session.Session()

        self.s3_client = my_session.resource(
                                service_name='s3',
                                region_name='ap-southeast-1',
                                )

        self.bucket = self.s3_client.Bucket(self.bucket_name)
        # print(self.bucket.name, self.bucket.creation_date)
        if self.bucket.creation_date is None:
            try:
                self.bucket.create(
                            ACL='private',
                            CreateBucketConfiguration={
                                'LocationConstraint': 'ap-southeast-1'
                            },
                        )
            except Exception as e:
                print(e)
                # raise(e)

    # def get_client(self):
    #     return self.s3_client
    def get_bucket(self):
        return self.bucket


    def upload_scenario_data(self, scenario):
        '''
        Split into smaller files by Arrival rate and Percentile
        '''
        dir_path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__)))))
        folder = f'{dir_path}/data/{scenario}'

        file_list = [f for f in listdir(folder) if isfile(join(folder, f))]

        for filename in file_list:
            self.bucket.upload_file(join(folder, filename), f'{scenario}/{filename}')

            # break

if __name__ == "__main__":

    s3_manager = S3Manager()
    s3_manager.upload_scenario_data('results_cleaned_20210527')

    object_summary_iterator = s3_manager.bucket.objects.all()

    for item in object_summary_iterator:
        print(item)


