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