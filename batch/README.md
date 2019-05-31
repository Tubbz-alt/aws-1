# AWS Batch setup

## Cluster setup

The cluster is the set of spot engines (autoscaled) where the batch jobs are running. The `oscibio-cluster.yaml` provides the cloudformation template to setup the cluster and the queue. By describing the parameters in a file for each environment (dev versus prd) and collecting the tags in a json file as well, the setup can be done with the following command.

```
aws cloudformation create-stack --stack-name oscibio-cluster --template-body file://oscibio-cluster.yaml --capabilities CAPABILITY_NAMED_IAM --parameters file://oscibio-cluster-parameters-dev.json --tags file://oscibio-cluster-tags.json
```

__Note:__ This will just create the compute environment as well as the job queue to receive the batch jobs. No engines will start until jobs are added, as the cluster scales down to zero.

To remove the cluster, use `aws cloudformation delete-stack --stack-name oscibio-cluster`.

## Docker setup

As AWS Batch uses Docker containers to run jobs, the code need to be able to run inside a Docker container.

### Docker creation locally

The setup of a Dockerfile can be tested locally. Starting from a `Dockerfile`, building the container:

```
docker build -t CONTAINERNAME .
```

with `CONTAINERNAME` the name of the container you want to deploy.

Some elements to take into account to run/test the container locally:

- To run the container locally, make sure you have the required AWS permissions yourself, most likely (on linux) stored in the `.aws/credentials` file of your home directory. You can pass this file read-only to your Docker on runtime.
- Credentials, e.g. FTP username/password should not be hardcoded in the Python code or Dockerfile. You can pass these as environmental variables using the `-e` argument.

```
docker run -it -v ${HOME}/.aws/credentials:/root/.aws/credentials:ro -e LOGIN="YOUR_USERNAME" -e PASSWORD="YOUR_PASSWORD" CONTAINERNAME
```

with `YOUR_USERNAME` and `YOUR_PASSWORD` the username an password and `CONTAINERNAME` the name of the container build in the previous step.

### Docker Registration on AWS ECR

The registration to the AWS ECR (Docker regitry within AWS) of the Docker image is explained in the [AWS documentation](https://docs.aws.amazon.com/AmazonECR/latest/userguide/docker-basics.html#use-ecr).

- Create a repository: `aws ecr create-repository --repository-name CONTAINERNAME --region eu-west-1` and remember the output (with `CONTAINERNAME` here `enram`):

```
{
    "repository": {
        "repositoryArn": "arn:aws:ecr:eu-west-1:226308051916:repository/enram",
        "registryId": "226308051916",
        "repositoryName": "enram",
        "repositoryUri": "226308051916.dkr.ecr.eu-west-1.amazonaws.com/enram",
        "createdAt": 1559330323.0
    }
}
```

- Tag your Docker image with the repository: `docker tag CONTAINERNAME 226308051916.dkr.ecr.eu-west-1.amazonaws.com/CONTAINERNAME`

- Get the Docker login: `aws ecr get-login --no-include-email --region eu-west-1` and run the login command you just received as stdout.

- Push the Docker image: `docker push 226308051916.dkr.ecr.eu-west-1.amazonaws.com/CONTAINERNAME`

__Note:__ To overcome the login step with the manual copy paste, consider using the [ecr credentials helper](https://github.com/awslabs/amazon-ecr-credential-helper). After repository creation, push/pull commands are supported directly and the login is managed for you.

### Using the Docker container in cloudformation

When setting up the stack, the `Repository-URI` will be used as an input parameter, so the stack knows which Docker image to use.

-> TO CHECK: Hence, to update the code, one can just push a new container to the registry, while keeping the stack as such (or vice versa).

## Scheduled job setup

```
aws cloudformation create-stack --stack-name oscibio-enram-getvp --template-body file://job.yaml --capabilities CAPABILITY_NAMED_IAM --parameters file://job-parameters-dev.json --tags file://job-tags.json
```

A crucial element is the link between the job definition/submission and the compute environment (cluster) created with the first template. This is done by [importing](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/intrinsic-function-reference-importvalue.html) the JobQueue value from the first cloudformation stack in the latter one.

__Note:__ Make sure the cluster stack is running before running the scheduled job stack, as otherwise the exported value will not yet be available.

To remove the cluster, use `aws cloudformation delete-stack --stack-name oscibio-enram-getvp`.

# TODO

TODO: ADD S3 bucket for the credentials!
    - add S3 bucket to template + permissions,...
    - provide instructions on how to put credentials in S3
    - add download of creds into python routine

TODO: make BidPercentage and max CPU a parameter of cluster setup

TODO: current python script has bucket name harcoded, should be os.environ[]