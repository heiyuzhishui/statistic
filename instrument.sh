Agent pid 103485
(labelimg_env) depth@depth:~/statistic$ ssh-add ~/.ssh/id_ed25519
Enter passphrase for /home/depth/.ssh/id_ed25519: 
(labelimg_env) depth@depth:~/statistic$ ssh-add -l
The agent has no identities.
(labelimg_env) depth@depth:~/statistic$ eval "$(ssh-agent -s)"
Agent pid 103504
(labelimg_env) depth@depth:~/statistic$ ssh-add ~/.ssh/id_ed25519.pub
@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
@         WARNING: UNPROTECTED PRIVATE KEY FILE!          @
@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
Permissions 0644 for '/home/depth/.ssh/id_ed25519.pub' are too open.
It is required that your private key files are NOT accessible by others.
This private key will be ignored.
(labelimg_env) depth@depth:~/statistic$ ssh-add -l
The agent has no identities.
(labelimg_env) depth@depth:~/statistic$ ssh-add -l
The agent has no identities.
(labelimg_env) depth@depth:~/statistic$ ssh-add ~/.ssh/id_ed25519
Enter passphrase for /home/depth/.ssh/id_ed25519: 
(labelimg_env) depth@depth:~/statistic$ ssh-add -l
The agent has no identities.
(labelimg_env) depth@depth:~/statistic$ ssh-add ~/.ssh/id_ed25519
Enter passphrase for /home/depth/.ssh/id_ed25519: 
(labelimg_env) depth@depth:~/statistic$ ssh-add -l
The agent has no identities.
(labelimg_env) depth@depth:~/statistic$ cat ~/.ssh/id_ed25519 
-----BEGIN OPENSSH PRIVATE KEY-----
b3BlbnNzaC1rZXktdjEAAAAACmFlczI1Ni1jdHIAAAAGYmNyeXB0AAAAGAAAABD8Vh9Nas
coQbpxsBeyudSBAAAAGAAAAAEAAAAzAAAAC3NzaC1lZDI1NTE5AAAAIHo2s/5iNXvSyHop
890PGQv0xbE+gu9uDacHEa5ofCf2AAAAoBkR6c3TKNZJFVysmkC3+BmqUDasPpjjNVp99C
ME7AbYgqMr80FOq/H/zH5DuyQViDydHyiHPfzftOb5xA7mfFSDgD+2Gi+RPxFLk57t++RY
A20/1k5NFvs3IJbCOUFXLHaZdBOMWTnqRr36LMvXoqu/p0FVY1bfON5y2FFZGZniMJcWWQ
o8+zuuX7Nq/PYpDEijDkubcrLo/3bJ7PbIvHA=
-----END OPENSSH PRIVATE KEY-----
(labelimg_env) depth@depth:~/statistic$ ssh-keygen -t ed25519 -C "baiyuzhishui@gmail.com"
Generating public/private ed25519 key pair.
Enter file in which to save the key (/home/depth/.ssh/id_ed25519): 
/home/depth/.ssh/id_ed25519 already exists.
Overwrite (y/n)? y
Enter passphrase (empty for no passphrase): 
Enter same passphrase again: 
Your identification has been saved in /home/depth/.ssh/id_ed25519
Your public key has been saved in /home/depth/.ssh/id_ed25519.pub
The key fingerprint is:
SHA256:4W3H5+w3xggbrC0h5AC1Ib2vj/kwzhMCQoliit/xr/U baiyuzhishui@gmail.com
The key's randomart image is:
+--[ED25519 256]--+
|. ..oo           |
|o+ ...o          |
|*   ... .        |
|+.  .o o o .     |
|.... o= S + o .  |
|  .....+ o = +   |
|    .oo.o + + =  |
|    oo=..+ o o +.|
|     ==+  E   o..|
+----[SHA256]-----+
(labelimg_env) depth@depth:~/statistic$ ssh-add ~/.ssh/id_ed25519
Identity added: /home/depth/.ssh/id_ed25519 (baiyuzhishui@gmail.com)
(labelimg_env) depth@depth:~/statistic$ ssh-add -l
256 SHA256:4W3H5+w3xggbrC0h5AC1Ib2vj/kwzhMCQoliit/xr/U baiyuzhishui@gmail.com (ED25519)
(labelimg_env) depth@depth:~/statistic$ ssh -T git@github.com
git@github.com: Permission denied (publickey).
(labelimg_env) depth@depth:~/statistic$ cat ~/.ssh/id_ed25519.pub 
ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIDAq20USAc5/bU77pSxirqcCG7TkoQReoCu7IreRoFbC baiyuzhishui@gmail.com
(labelimg_env) depth@depth:~/statistic$ ssh -T git@github.com
Hi heiyuzhishui! You've successfully authenticated, but GitHub does not provide shell access.
(labelimg_env) depth@depth:~/statistic$ git push origin master
枚举对象中: 40, 完成.
对象计数中: 100% (40/40), 完成.
使用 20 个线程进行压缩
压缩对象中: 100% (37/37), 完成.
写入对象中: 100% (40/40), 9.09 KiB | 9.09 MiB/s, 完成.
总共 40（差异 12），复用 0（差异 0），包复用 0
remote: Resolving deltas: 100% (12/12), done.
remote: 
remote: Create a pull request for 'master' on GitHub by visiting:
remote:      https://github.com/heiyuzhishui/statistic/pull/new/master
remote: 
To github.com:heiyuzhishui/statistic.git
 * [new branch]      master -> master
(labelimg_env) depth@depth:~/statistic$ git add .
(labelimg_env) depth@depth:~/statistic$ git status
位于分支 master
要提交的变更：
  （使用 "git restore --staged <文件>..." 以取消暂存）
        修改：     .idea/vcs.xml
        修改：     .idea/workspace.xml

(labelimg_env) depth@depth:~/statistic$ git commit -m "success"
[master 7979dc2] success
 2 files changed, 15 insertions(+), 4 deletions(-)
(labelimg_env) depth@depth:~/statistic$ git log
commit 7979dc241b942e91b6af99a85042072f1c114258 (HEAD -> master)
Author: depth <baiyuzhishui@gmail.com>
Date:   Fri Dec 27 14:17:36 2024 +0800

    success

commit a055112f9a6bf345f4e0b4f1da36cc00330f45bc (origin/master)
Author: depth <baiyuzhishui@gmail.com>
Date:   Fri Dec 27 12:04:13 2024 +0800


[4]+  已停止               git log
(labelimg_env) depth@depth:~/statistic$ git push origin master
枚举对象中: 9, 完成.
对象计数中: 100% (9/9), 完成.
使用 20 个线程进行压缩
压缩对象中: 100% (5/5), 完成.
写入对象中: 100% (5/5), 610 字节 | 610.00 KiB/s, 完成.
总共 5（差异 3），复用 0（差异 0），包复用 0
remote: Resolving deltas: 100% (3/3), completed with 3 local objects.
To github.com:heiyuzhishui/statistic.git
   a055112..7979dc2  master -> master
(labelimg_env) depth@depth:~/statistic$ git push origin main
error: 源引用规格 main 没有匹配
error: 无法推送一些引用到 'github.com:heiyuzhishui/statistic.git'
(labelimg_env) depth@depth:~/statistic$ git push --set-upstream origin main         
error: 源引用规格 main 没有匹配
error: 无法推送一些引用到 'github.com:heiyuzhishui/statistic.git'
(labelimg_env) depth@depth:~/statistic$ git add .
(labelimg_env) depth@depth:~/statistic$ git commit -m "again"
位于分支 master
无文件要提交，干净的工作区
(labelimg_env) depth@depth:~/statistic$ git add .
(labelimg_env) depth@depth:~/statistic$ git commit -m "again"
[master 0a87c09] again
 1 file changed, 2 insertions(+)
(labelimg_env) depth@depth:~/statistic$ git push origin main
error: 源引用规格 main 没有匹配
error: 无法推送一些引用到 'github.com:heiyuzhishui/statistic.git'
(labelimg_env) depth@depth:~/statistic$ git status
位于分支 master
无文件要提交，干净的工作区
(labelimg_env) depth@depth:~/statistic$ git push origin main
error: 源引用规格 main 没有匹配
