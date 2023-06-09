import boto3

def upload_video_to_s3(file, bucket_name, video_key): 
    s3 = boto3.client('s3', aws_access_key_id='', 
                        aws_secret_access_key='') 
    s3.put_object(Bucket=bucket_name, Body=file, Key=video_key, ContentType='video/mp4', ACL='public-read') 

def upload_task_submit_to_s3(file, bucket_name, video_key, file_type): 
    s3 = boto3.client('s3', aws_access_key_id='', 
                        aws_secret_access_key='') 
    s3.put_object(Bucket=bucket_name, Body=file, Key=video_key, ContentType=file_type, ACL='public-read') 
