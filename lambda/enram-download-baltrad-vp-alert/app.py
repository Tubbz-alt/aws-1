from datetime import datetime, timedelta

import boto3
from chalice import Chalice, Rate

# Setup chalice APP
app = Chalice(app_name=' enram-download-baltrad-vp-alert')

# Automatically runs every...
@app.schedule(Rate(1, unit=Rate.DAYS))
def periodic_task(event):
    """Check on latest modified date of coverage file

    When not updated in the last two days, send mail.
    """

    BUCKET = 'lw-enram'
    SNS_TOPIC_ARN = 'arn:aws:sns:eu-west-1:226308051916:lw-enram-alerts'
    DAYS_BUFFER = 2

    # in enram-bucket:
    print("Loading enram s3 bucket coverage file...")
    s3_bucket = boto3.client('s3', region_name='us-west-1')
    response = s3_bucket.list_objects_v2(Bucket=BUCKET,
                                         Prefix='coverage.csv')

    last_modified = response['Contents'][0]['LastModified']
    print("Last modified date is {}".format(last_modified))
    if last_modified.date() <= (datetime.today() - timedelta(days=DAYS_BUFFER)).date():
        print("Files are older than defined time buffer, sending alert...")
        sns_alert = boto3.client('sns')
        sns_alert.publish(
                TopicArn=SNS_TOPIC_ARN,
                Message='Enram data pipeline not updated since {} days. Please check server ~/log_file_transfer and ~/data-repository/file_transfer/cronlog_enram for potential errors!'.format(DAYS_BUFFER),
                Subject='ENRAM data pipeline not updated'
                )
        print("Alert pushed to SNS.")
    else:
        print("Coverage file is up to date, nothing to report.")
    print(event.to_dict())