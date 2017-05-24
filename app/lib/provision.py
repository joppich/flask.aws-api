# as we only need to execute two commands on the target
# system, we will do this by ssh; as the requirements grow
# we can integrate a proper provisioning tool here

import paramiko
import crypt


configure_sshd = "sudo sed -i s/'PasswordAuthentication no'/'PasswordAuthentication yes'/g /etc/ssh/sshd_config"

def add_user(username,password):
    s = "sudo useradd -m -p {pw} {uname}"
    pwd = crypt.crypt(password, crypt.mksalt(crypt.METHOD_SHA512))
    return s.format(pw=pwd,uname=username)


def run_command(command,keyname,ip):
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    key = paramiko.RSAKey.from_private_key_file(os.path.abspath('.'+keyname+'.pem'))
    client.connect(hostname=ip,username='ubuntu',pkey=key)
    stdin, stdout, stderr = client.exec_command(command)
    client.close()

