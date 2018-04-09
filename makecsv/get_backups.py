import paramiko
import scp
import pathlib
from datetime import datetime
import sys

class GetBackups():
    # ローカルパス
    backup_dir = str(datetime.now().strftime('backup_%Y%m%d_%H%M%S'))
    pathlib.Path('./backups/'+backup_dir).resolve().mkdir()
    
    def __init__(self,ip='192.168.1.254',remote_path='/home/conprosys/bacnet/', local_path=str(pathlib.Path('./backups/').resolve().joinpath(backup_dir))):
        # リモートパス
        self.ip=ip
        self.remote_path = remote_path
        self.local_path  = local_path
        print("local_path:", self.local_path)
        
        # monitored_object_data.sqlite3のパスをファイル出力
        with open('backup_path.txt','w') as f:
            f.write(str(pathlib.Path(self.local_path)))
            
        self.stop_service_cmds = [
            # serviceの停止
            'sudo killall systemserviced',
            'sudo killall bacnetd',
            'sudo chown -R conprosys:conprosys /home/conprosys/bacnet/'
        ]
        
        self.restart_service_cmds = [
            # serviceの再開
            'sudo systemserviced',
            'sudo bacnetd',
            'exit'
        ]


    def check_result(self, stdin, stdout, stderr):
        result = True
        for o in stdout:
            if o:
                print("    " + o.strip())
        for e in stderr:
            if e:
                print("    " + e.strip())
                result = False
        return result

    def exec_command(self, ssh, cmds):
        result = True
        for cmd in cmds:
            print("  " + cmd)
            stdin, stdout, stderr = ssh.exec_command(cmd)
        if self.check_result(stdin, stdout, stderr):
            pass
        else:
            print("ERROR -- " + cmd)
            result = False
        return result
    
    
    def get(self):
        # ssh clientオブジェクト(ssh)を作る・・・
        with paramiko.SSHClient() as ssh:
            # どうやってhostname & keyを登録するのかわからないので、AutoAddPolicy()としておく
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            # ssh接続する
            ssh.connect(hostname=self.ip, port=22, username='conprosys', password='contec')
            
            # serviceの停止
            print("start -- stop_service")
            if self.exec_command(ssh, self.stop_service_cmds):
                print("done -- stop_service")
            #else:
            #    sys.exit()
            
            # sftp接続
            with ssh.open_sftp() as sftp:
                # 任意のディレクトリの下に移動
                sftp.chdir('/home/conprosys/bacnet')
                for _file in sftp.listdir():
                    sftp.get(self.remote_path+_file,self.local_path+'/'+_file)
                    
            # serviceの再開
            print("start -- restart_service")
            if self.exec_command(ssh, self.restart_service_cmds):
                print("done  -- restart_service")
            else:
                print("ERROR -- restart_service")
                sys.exit()


# In[4]:


if __name__ == '__main__':
    #gb = GetBackups(ip='172.168.200.183',local_path=str(pathlib.Path('./DB').resolve()))
    gb = GetBackups()
    gb.get()