### SSH连接Linux超时自动断开

```shell
vim /etc/ssh/sshd_config
ClientAliveInterval 60
ClientAliveCountMax 3/
service sshd reload
```


### 修改mac同时打开最大文件数

```shell
sudo sysctl -w kern.maxfiles=1048600
sudo sysctl -w kern.maxfilesperproc=1048576
ulimit -n 1048576
```

### 修改 mac hosts 文件

```
vim /private/etc/hosts
122.152.206.106 whoami.haoyu526.cn
dscacheutil -flushcache
```


### linux 解压 xxx.tar.xz

```shell
xz -d ***.tar.xz
tar -xvf  ***.tar
```

### scp 文件

```shell
# 本地到远程
scp local_file remote_username@remote_ip:remote_folder

# 远程到本地
scp remote_username@remote_ip:remote_file local_folder
```

du -sh *，显示当前目录下所有的文件及其大小

解压

```
tar -zcvf /home/xahot.tar.gz /xahot
tar -xzf apollodb.tar.gz
sudo tar -zcvf /volume1/docker/gitlab/tar/logs.tar.gz /volume1/docker/gitlab/logs
```

```
# 后台输出
nohup node_exporter &
```


### linux 免密登录

```
ssh-keygen -t rsa
ssh-copy-id -i ~/.ssh/id_rsa.pub user@IP
```




### 定时同步时间

```shell
# 安装crontab
yum -y install crontab
# 创建crontab任务
crontab -e
# 添加定时任务
*/20 * * * * /usr/sbin/ntpdate ntp.api.bz > /dev/null 2>&1
# 重启crontab
service crond reload
```

