import boto3
import os

class AwsEc2(object):
    # methods for spawning and destroying ssh capable aws instances
    ami = os.environ.get('AWS_AMI')

    def deploy_aws_instance(self,publickey):
        i = self.ec2.create_instances(
            ImageId=self.ami,
            MinCount=1,
            MaxCount=2,
            InstanceType='t2.micro'
        )
        i.start()

    def destroy_aws_instance(self,ip):
        for ins in self.ec2.instances.all():
            if ins.public_ip_address == ip:
                ins.terminate()

    def __init__(self):
        try:
            self.ec2 = boto3.resource('ec2')
        except:
            raise()
