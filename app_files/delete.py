from google.cloud import storage
import os
import time
start_time=time.time()
print('Credentials from environ: {}'.format(os.environ.get('GOOGLE_APPLICATION_CREDENTIALS')))

def list_bucket_contents():
    storage_client = storage.Client()
    buckets_list = storage_client.list_buckets()

    def list_blobs(bucket_name):
        blobs = storage_client.list_blobs(bucket_name)
        files_list=[]
        for blob in blobs:
            files_list.append(blob.name)
        return files_list

    bucket_contents={}
    for bucket in buckets_list:
        if ".appspot.com" not in bucket.name:
            bucket_contents[bucket.name]=list_blobs(bucket.name)
    return bucket_contents
print(list_bucket_contents())
print(time.time() - start_time)
