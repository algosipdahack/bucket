import boto3
import uuid

region = 'ap-northeast-2'
expires_in = 3600

def main():
    session = boto3.Session(profile_name='lecture')
    s3 = session.client(service_name='s3',region_name=region)
    location = {'LocationConstraint': region}
    
    s3.create_bucket(Bucket='bob10-5460-hw3',CreateBucketConfiguration=location)
    rid = 'bob10-5460-{}'.format(uuid.uuid1())
    bucket_name='bob10-5460-hw3'
    object_key='HW3-5460'
    object_key2='HW3-5460_2'
    s3.put_object(Bucket=bucket_name,Key = object_key,Body=rid)
    s3.put_object(Bucket=bucket_name,Key = object_key2,Body=rid)
    presigned_url = s3.generate_presigned_url(
        ClientMethod='get_object',
        Params={
            'Bucket': bucket_name,
            'Key': object_key
        },
        ExpiresIn = expires_in,
        HttpMethod='GET'
    )
    print('----------\n{}\n---------'.format(presigned_url))
    print('\n===================<list_objects>===============\n')
    response = s3.list_objects(Bucket = bucket_name)
    for content in response['Contents']:
        print(content['Key'])

    print('\n===================<delete_objects>===============\n')
    response = s3.delete_objects(Bucket = bucket_name,
            Delete = {
                'Objects' : [
                    {'Key': object_key},
                    {'Key': object_key2}
                ]
            }
    )
    print(response)
    
    print('\n===================<list_object_versions>===============\n')
    response = s3.list_object_versions(Bucket = bucket_name)
    print(response)
    
    print('\n===================<object_versions.delete>===============\n')
    response = boto3.resource('s3').Bucket(bucket_name).object_versions.delete()
    print(response)
    
    print('\n===================<delete_bucket>===============\n')
    response = s3.delete_bucket(Bucket = bucket_name)
    print(response)
	
if __name__ == '__main__':
    main()
