### About
s3kv is a key value database backed by S3 Object Storage. As such it leverages many of the inbuilt capabilities of Object Storage. Especially interesting features are those such as key access policies, legal holds and retention. 

It is primarily intended for use cases such as data flow caching, configuration management and secrets management. 

### Basic Operations
The following are the basic operations.

```
# Import the s3kv library
from s3kv import S3KV
import os

# Initialize the database with S3 credentials and bucket name
s3kv = S3KV(os.environ['S3_ENDPOINT_URL'],
             os.environ['S3_BUCKET'], 
             os.environ['AWS_ACCESS_KEY_ID'], os.environ['AWS_SECRET_ACCESS_KEY'],
             enable_local_cache=True)

# Store data in the database
s3kv.add('key1', 'value1')
s3kv.add('key2', {'name': 'John', 'age': 30})

# Retrieve data from the database
value1 = s3kv.get('key1')
data = s3kv.get('key2')

# Delete a key
s3kv.delete('key1')

# Check if a key exists
if s3kv.exists('key3'):
    print("Key 'key3' exists!")
```

### Extended Key Operations : Copy and Merge

In the copy_key method, we use the get_object method to retrieve the value of the source key from the S3 bucket. Then, we use the put_object method to store the same value under the destination key. If the source key exists in the local cache (/tmp/s3kv_cache), we also copy the cached value to the destination key in the cache.

Please note that if the source key does not exist, the method will raise an error. Ensure that the source key exists before calling this method. You can use the key_exists method to check if the source key exists.

Here’s an example of how to use the copy_key method:

```
# Import the s3kv library
from s3kv import S3KV
import os

# Initialize the database with S3 credentials and bucket name
s3kv = S3KV(os.environ['S3_ENDPOINT_URL'],
             os.environ['S3_BUCKET'], 
             os.environ['AWS_ACCESS_KEY_ID'], os.environ['AWS_SECRET_ACCESS_KEY'],
             enable_local_cache=True)

data = {"name": "john"}
s3kv.add('source_key',data)

source_key = 'source_key'
destination_key = 'destination_key'
if s3kv.key_exists(source_key):
    s3kv.copy_key(source_key, destination_key)
else:
    print(f"The source key '{source_key}' does not exist in the S3KV database.")
```

In the merge_keys method, we iterate through the list of source keys, retrieve their values, and merge them into the destination value using the update method. Then, we update the value of the destination key both in the S3 bucket and the local cache. To use this method, you can call it with a list of source keys and the destination key:

```
# Import the s3kv library
from s3kv import S3KV
import os


# Initialize the database with S3 credentials and bucket name
s3kv = S3KV(os.environ['S3_ENDPOINT_URL'],
             os.environ['S3_BUCKET'], 
             os.environ['AWS_ACCESS_KEY_ID'], os.environ['AWS_SECRET_ACCESS_KEY'],
             enable_local_cache=True)

data_a = {"data_a": "value_a"}
s3kv.add('source_key_a',data_a,None)

data_b = {"data_b": "value_b"}
s3kv.add('source_key_b',data_b,None)

source_keys = ['source_key_a', 'source_key_b']
destination_key = 'destination_key'

s3kv.merge_keys(source_keys, destination_key)

```

### Cache Operations
The following are the Cache operations.

```
# Import the s3kv library
from s3kv import S3KV
import os

# Initialize the s3kv database with local caching and key indexing
s3kv = S3KV(os.environ['S3_ENDPOINT_URL'],
             os.environ['S3_BUCKET'], 
             os.environ['AWS_ACCESS_KEY_ID'], os.environ['AWS_SECRET_ACCESS_KEY'],
             enable_local_cache=True)

# Explicitly clear the cache
s3kv.clear_cache()  # Clears the entire local cache

# Clear files older than max_days
max_days = 2
s3kv.clear_old_cache(max_days)

# Clear the cache for a specific key
s3kv.clear_cache_for_key('test')
```

### Tagging Keys

In addition to the existing features, S3KV introduces the ability to tag keys, which provides a convenient and organized way to manage hundreds of configurations or key-value pairs. Tags allow developers to associate metadata with individual keys, making it easier to categorize, search, and apply policies based on specific attributes. For example, in the context of configuration settings, keys related to a particular module or component can be tagged with the module's name, making it easier to manage and retrieve configurations for specific parts of the application.

You can add tags to new objects when you upload them, or you can add them to existing objects. Quoting the AWS S3 Docs -
* You can associate up to 10 tags with an object. Tags that are associated with an object must have unique tag keys.
* A tag key can be up to 128 Unicode characters in length, and tag values can be up to 256 Unicode characters in length. Amazon S3 object tags are internally represented in UTF-16. Note that in UTF-16, characters consume either 1 or 2 character positions.
* The key and values are case sensitive.

**IMPORTANT**
If a key is overwritten any tags added prior will be deleted.

```
# Import the s3kv library
from s3kv import S3KV
import os

# Initialize the s3kv database with local caching and key indexing
s3kv = S3KV(os.environ['S3_ENDPOINT_URL'],
             os.environ['S3_BUCKET'], 
             os.environ['AWS_ACCESS_KEY_ID'], os.environ['AWS_SECRET_ACCESS_KEY'],
             enable_local_cache=True)

# Store data in the database with tags
s3kv.tag_key('test_c',  tags={'module': 'user_management', 'environment': 'production'})

# Get tags assigned to a specific key
tags = s3kv.get_tags('s3kv/test_c.json')
print(tags)

# Find all keys with a tag key set to a specific value
keys = s3kv.find_keys_by_tag_value('environment','production')
print(keys)

# Tag multiple keys which share a prefix
s3kv.tag_keys_with_prefix('s3kv/test', {'module': 'user_management', 'environment': 'production'})

# Delete a key by tag (delete all keys where the "module" tag == "user_management")
s3kv.delete_by_tag('module', 'user_management')
```

### Listing Keys

The following are the list operations.

```
# Import the s3kv library
from s3kv import S3KV
import os

# Initialize the database with S3 credentials and bucket name
s3kv = S3KV(os.environ['S3_ENDPOINT_URL'],
             os.environ['S3_BUCKET'], 
             os.environ['AWS_ACCESS_KEY_ID'], os.environ['AWS_SECRET_ACCESS_KEY'],
             enable_local_cache=True)

# List all keys
keys = s3kv.list_keys()

# List all keys with a specific prefix
s3kv.list_keys_with_prefix('s3kv/test')

# Find all keys with a tag set to a specific value
keys = s3kv.find_keys_by_tag_value('environment','production')
print(keys)
```

### Locking Keys - Retention and Legal Hold

Introducing the ability to apply locks to keys offers enhanced data governance and compliance capabilities. These locks come in two types - retention and legal hold - each serving a specific purpose in ensuring data immutability and compliance with regulations or internal policies.

1. Retention Lock: A retention lock allows users to enforce a specified period during which a key cannot be modified or deleted. This feature is particularly useful for maintaining data integrity and ensuring that critical data remains unchanged for regulatory or compliance reasons. *Once a retention lock is applied to a key, it cannot be altered or deleted until the specified retention period expires.*
2. Legal Hold: On the other hand, a legal hold lock is a more flexible form of locking. *When a legal hold is applied to a key, it prevents the key from being deleted, but allows it to be modified.* The lock remains in effect until explicitly removed, providing a higher level of control over the data lifecycle while still allowing for data updates as needed.

**IMPORTANT**
Key locks require bucket versioning to be enabled on bucket creation. 

```
# Import the s3kv library
from s3kv import S3KV
import os

# Initialize the database with S3 credentials and bucket name
s3kv = S3KV(os.environ['S3_ENDPOINT_URL'],
             os.environ['S3_BUCKET'], 
             os.environ['AWS_ACCESS_KEY_ID'], os.environ['AWS_SECRET_ACCESS_KEY'],
             enable_local_cache=True)


data = {'name': 'fat_boy_slim'}
s3kv.add('test_retention', data)

# Place a retention lock on a key (object cannot be deleted or 
# changed for 365 days)
s3kv.place_retention_lock('test_retention', 365)

# Remove a retention lock
s3kv.remove_retention_lock('test_retention')

# Apply legal hold to a key (object cannot be deleted but can be modified)
s3kv.apply_legal_hold('test_retention')

# Check if a key is under legal hold
if s3kv.is_legal_hold_applied('test_retention'):
    print("Key 'test_retention' is under legal hold.")


# Release legal hold on a key
s3kv.release_legal_hold('test_retention')

# Check if a key is under legal hold
if s3kv.is_legal_hold_applied('test_retention'):
    print("Key 'test_retention' is under legal hold.")

```

### Utility functions
The following are utility functions

```
# Import the s3kv library
from s3kv import S3KV
import os

# Initialize the database with S3 credentials and bucket name
s3kv = S3KV(os.environ['S3_ENDPOINT_URL'],
             os.environ['S3_BUCKET'], 
             os.environ['AWS_ACCESS_KEY_ID'], os.environ['AWS_SECRET_ACCESS_KEY'],
             enable_local_cache=True)

data = {"dj": "fatboy slim"}
s3kv.add('test', data)

# Get the key size (file size)
size = s3kv.get_key_size('test')
print(size)

# Get the last updated time of the key
last_updated_date = s3kv.get_key_last_updated_time('test')
print(last_updated_date)
```
