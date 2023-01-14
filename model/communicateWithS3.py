import boto3
import os
from dotenv import load_dotenv

class communicateWithS3():
    '''
    AWS_ACCESS_KEY_ID: '存取金鑰 ID'
    AWS_SECRET_ACCESS_KEY: '私密存取金鑰'
    S3_BUCKET_NAME: '儲存庫名稱'
    '''
    load_dotenv()
    AWS_ACCESS_KEY_ID=os.getenv("AWS_ACCESS_KEY_ID")
    AWS_SECRET_ACCESS_KEY=os.getenv("AWS_SECRET_ACCESS_KEY")
    S3_BUCKET_NAME=os.getenv("S3_BUCKET_NAME")

    def __init__(self):
        # 建立 S3 资源
        self.s3 = boto3.resource('s3',
                    aws_access_key_id=communicateWithS3.AWS_ACCESS_KEY_ID,
                    aws_secret_access_key=communicateWithS3.AWS_SECRET_ACCESS_KEY)

    def uploadImage(self,imageName,imageBody):
        self.s3.Bucket(communicateWithS3.S3_BUCKET_NAME).upload_fileobj(imageBody, imageName,ExtraArgs={'ContentType': 'image/jpeg','ACL':'public-read'})
    
    def showAllObjectInS3(self):
        # 回傳在S3的所有物件名字
        AllObjectInS3=[]  
        for obj in boto3.resource('s3').Bucket(communicateWithS3.S3_BUCKET_NAME).objects.all():
            AllObjectInS3.append(obj.key)
        return AllObjectInS3
        