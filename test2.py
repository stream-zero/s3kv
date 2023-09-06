# Import the s3kv library
from s3kv import S3KV
import os

# Initialize the database with S3 credentials and bucket name
s3kv = S3KV(os.environ['S3_ENDPOINT_URL'],
             os.environ['S3_BUCKET'], 
             os.environ['AWS_ACCESS_KEY_ID'], os.environ['AWS_SECRET_ACCESS_KEY'],
             enable_local_cache=True)

data = {"dj": "fat boy slim"}
s3kv.add('test', data)

# Get the key size (file size)
size = s3kv.get_key_size('test')
print(size)

# Get the last updated time of the key
last_updated_date = s3kv.get_key_last_updated_time('test')
print(last_updated_date)