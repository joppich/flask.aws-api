import boto3
import os

class AwsEc2(object):
    # methods for spawning and destroying ssh capable aws instances

    def deploy_aws_instance(self,publickey):
        ins = self.ec2.create_instances(
                ImageId=self.ami,
                MinCount=1,
                MaxCount=1,
                InstanceType='t2.micro'
            )
        return ins[0].id

    def destroy_aws_instance(self,ip):
        for ins in self.ec2.instances.all():
            if ins.public_ip_address == ip:
                ins.terminate()
                return ins.id

    def __init__(self):
        self.ami = os.environ.get('AWS_AMI', 'ami-060cde69')
        self.ec2 = boto3.resource('ec2')
