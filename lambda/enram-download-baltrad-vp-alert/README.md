
# Replication of the bucket to an archive bucket

## AWS resources

The functionality depends on a (hard-coded) S3 bucket and a SNS topic to which subscribers can be added.

    - `BUCKET` = 'lw-enram'
    - `SNS_TOPIC_ARN` = 'arn:aws:sns:eu-west-1:226308051916:lw-enram-alerts'

The current check of the coverage file update is 2 days, as defined by the `DAYS_BUFFER` parameter.

## Deployment

To deploy the lambda app, deploy with:

```
chalice deploy
```

## Chalice

Info:

* https://github.com/aws/chalice
* https://github.com/aws/chalice/blob/master/docs/source/topics/configfile.rst
