from s3kv import S3KV
import os
import time
from datetime import datetime


s3kv = S3KV(os.environ['S3_ENDPOINT_URL'],
             os.environ['S3_BUCKET'], 
             os.environ['AWS_ACCESS_KEY_ID'], os.environ['AWS_SECRET_ACCESS_KEY'])


s3kv.add('key1', 'value1')

keys = s3kv.list_keys()
print(keys)

data = {"test":"test"}

'''
for key in ['test.streamzero.01', 'test.streamzero.02', 'test.streamzero.03', 'test.streamzero.04']:
    s3kv.add(key,data,None)
'''

keys = s3kv.list_keys()
print(keys)


s3kv.delete('test')
s3kv.clear_old_cache(1)

config = s3kv.get('test')
print(config)

s3kv.get('test')

#s3kv.clear_cache()

s3kv.get('test')

s3kv.add('test',data,None)

s3kv.key_exists('test')


s3kv.add('test',data,None)
print(s3kv.get_key_last_updated_time('test'))


data_a = {"data_a": "value_a"}
s3kv.add('test_a',data_a,None)

data_b = {"data_b": "value_b"}
s3kv.add('test_b',data_b,None)

s3kv.merge_keys(['test_a','test_b'], 'test_c')

print(s3kv.get('test_c'))

s3kv.tag_key('test_c',  tags={'module': 'user_management', 'environment': 'production'})


keys = s3kv.find_keys_by_tag_value('environment','production')
print(f"keys with tag environment:production - {keys}")

tags = s3kv.get_tags('s3kv/test_c.json')
print(tags)

s3kv.tag_keys_with_prefix('s3kv/test', {'module': 'user_management', 'environment': 'production'})
# Place a retention lock on a key
s3kv.place_retention_lock('test_c', 1)

# Remove a retention lock
s3kv.remove_retention_lock('test_c')
