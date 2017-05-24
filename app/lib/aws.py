import os
import boto3
from uuid import uuid4

from .provision import configure_sshd, add_user, run_command

ip_permissions = [{
    'IpProtocol': 'tcp',
    'FromPort': 22,
    'ToPort': 22,
    'IpRanges': [{'CidrIp': '0.0.0.0/0'}]
}]


class AwsEc2(object):
    # methods for spawning and destroying ssh capable ec2 instances

    def deploy_aws_instance(self, username, password):
        ins = self.ec2.create_instances(
                ImageId=self.ami,
                MinCount=1,
                MaxCount=1,
                InstanceType='t2.micro',
                KeyName=self.create_keypair(),
                SecurityGroups = [self.security_group()]
            )[0]
        while True:
            i = self.ec2.Instance(id=ins.id)
            if i.state['Name'] != 'running':
                pass
            else:
                run_command(configure_sshd,
                            i.keyname,
                            i.public_ip_address)
                run_command(add_user(username,password),
                            i.keyname,
                            i.public_ip_address)
                return dict(ip=i.public_ip_address)
        return -1

    def delete_keypair(self, keyname):
        self.ec2_cli.delete_key_pair(KeyName=keyname)
        try:
            os.chmod(os.path.abspath('.'+keyname+'.pem'), 0o600)
            os.remove(os.path.abspath('.'+keyname+'.pem'))
        except:
            pass

    def create_keypair(self):
        keyname = uuid4().hex[-8:]
        kp = self.ec2.create_key_pair(KeyName=keyname)
        with open('.'+keyname+'.pem', 'w') as f:
            f.write(kp.key_material)
        os.chmod(os.path.abspath('.'+keyname+'.pem'), 0o400)
        return keyname

    def destroy_aws_instance(self,ip):
        for ins in self.ec2.instances.all():
            if ins.public_ip_address == ip:
                self.delete_keypair(ins.key_name)
                ins.terminate()
                return ins.id

    def security_group(self):
        try:
            self.ec2_cli.describe_security_groups(GroupNames=['SSH'])
        except ClientError:
            sg = self.ec2_cli.create_security_group(GroupName='SSH',
                                                    Description='Open port 22')
            sg_id = sg['GroupId']
            self.ec2_cli.authorize_security_group_ingress(GroupId=sg_id,
                                                     IpPermissions=ip_permissions)
        return 'SSH'

    def __init__(self):
        self.ami = 'ami-060cde69'
        self.ec2 = boto3.resource('ec2')
        self.ec2_cli = boto3.client('ec2')
