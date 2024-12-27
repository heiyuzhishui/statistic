(labelimg_env) depth@depth:~/statistic$ git pull origin main
remote: Enumerating objects: 3, done.
remote: Counting objects: 100% (3/3), done.
remote: Total 3 (delta 0), reused 0 (delta 0), pack-reused 0 (from 0)
展开对象中: 100% (3/3), 863 字节 | 863.00 KiB/s, 完成.
来自 github.com:heiyuzhishui/statistic
 * branch            main       -> FETCH_HEAD
 * [新分支]          main       -> origin/main
提示：您有偏离的分支，需要指定如何调和它们。您可以在执行下一次
提示：pull 操作之前执行下面一条命令来抑制本消息：
提示：
提示：  git config pull.rebase false  # 合并
提示：  git config pull.rebase true   # 变基
提示：  git config pull.ff only       # 仅快进
提示：
提示：您可以将 "git config" 替换为 "git config --global" 以便为所有仓库设置
提示：缺省的配置项。您也可以在每次执行 pull 命令时添加 --rebase、--no-rebase，
提示：或者 --ff-only 参数覆盖缺省设置。
fatal: 需要指定如何调和偏离的分支。
(labelimg_env) depth@depth:~/statistic$ git push origin main
To github.com:heiyuzhishui/statistic.git
 ! [rejected]        main -> main (non-fast-forward)
error: 无法推送一些引用到 'github.com:heiyuzhishui/statistic.git'
提示：Updates were rejected because the tip of your current branch is behind
提示：its remote counterpart. If you want to integrate the remote changes,
提示：use 'git pull' before pushing again.
提示：See the 'Note about fast-forwards' in 'git push --help' for details.
(labelimg_env) depth@depth:~/statistic$ git push origin main --force
枚举对象中: 16, 完成.
对象计数中: 100% (16/16), 完成.
使用 20 个线程进行压缩
压缩对象中: 100% (11/11), 完成.
写入对象中: 100% (11/11), 1000 字节 | 1000.00 KiB/s, 完成.
总共 11（差异 6），复用 0（差异 0），包复用 0
remote: Resolving deltas: 100% (6/6), completed with 4 local objects.
To github.com:heiyuzhishui/statistic.git
 + 97e9e8b...68b2234 main -> main (forced update)
(labelimg_env) depth@depth:~/statistic$
