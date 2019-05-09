import boto3
from chalice import Chalice

app = Chalice(app_name='enram-backup-vp')

@app.on_s3_event(bucket='lw-enram', events=['s3:ObjectCreated:*'])
def handler(event):
    print("Object uploaded for bucket: %s, key: %s"
          % (event.bucket, event.key))

    TARGET_BUCKET = 'lw-enram-archive'

    print("Replicating file to archive S3 bucket...")

    s3 = boto3.resource('s3')
    copy_source = {
        'Bucket': event.bucket,
        'Key': event.key
    }
    s3.meta.client.copy(copy_source, TARGET_BUCKET, event.key)
    print("... file", event.key, "moved to archive bucket.")

    print(event.to_dict())
