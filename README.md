#Stream Cloud个人信息平台

##如何安装？

编辑 stream/key.py，修改 PUBLIC\_KEY 和 PRIVATE\_KEY 两个变量为你喜欢或者能记得的话。

保存后，执行 python stream/key.py 生成 PUBLIC\_KEY 和 SECRET 两个哈希值，把 SECRET 回填到
key.py 里面，记下PUBLIC\_KEY，这个是用来登录后台用的。

修改app.yaml的application: stream-cloud这一行，把stream-cloud修改你申请到应用名。

##演示站

http://stream-cloud.ciiaii.com/

