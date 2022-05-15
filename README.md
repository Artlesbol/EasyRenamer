# README

一个简单的Windows文件重命名批处理工具。
一个……简陋的控制台程序

## 安装

下载程序，然后把它加入环境变量（[不会加入环境变量？](https://blog.csdn.net/weixin_29701553/article/details/119199452)）

## 使用


加入环境变量后你可以在控制台呼出这个程序

```
easyrenamer
```

### help information

输入``easyrenamer``或者``easyrenamer -h``可以打印帮助信息:
```
usage: easyrenamer [-h] [-v] {replace,insert,delate} ...

一个简单的Windows重命名批处理工具

positional arguments:
  {replace,insert,delate}
    replace             替换模式
    insert              插入模式
    delate              删除模式

optional arguments:
  -h, --help            show this help message and exit
  -v, --version         关于我
```

具体模式的帮助信息可以使用``easyrenamer {replace,insert,delate} -h``来查看

所有模式下默认【大小写敏感】、【不处理后缀名】、【不使用正则表达式】

如果需要以上操作，可以使用如下选项：``--case``,``--withsuffix``,``--regular``

替换帮助
```
usage: easyrenamer replace [-h] -s SOURCE -d DESTINATION [-S [suffix ...]] [--case] [--withsuffix] [--regular]
                           directory

positional arguments:
  directory             文件目录

optional arguments:
  -h, --help            show this help message and exit
  -s SOURCE, --source SOURCE
                        替换源
  -d DESTINATION, --destination DESTINATION
                        替换字段
  -S [suffix ...]       指定后缀集
  --case                忽略大小写
  --withsuffix          处理后缀名
  --regular             正则匹配
```

插入帮助
```
usage: easyrenamer insert [-h] (-s SOURCE | -b | -f) [-S [suffix ...]] [--case] [--withsuffix] [--regular] -d
                          DESTINATION
                          directory

positional arguments:
  directory             文件目录

optional arguments:
  -h, --help            show this help message and exit
  -s SOURCE, --source SOURCE
                        插入处
  -b, --back            在最前方插入
  -f, --front           在最后方插入
  -S [suffix ...]       指定后缀集
  --case                忽略大小写
  --withsuffix          处理后缀名
  --regular             正则匹配
  -d DESTINATION, --destination DESTINATION
                        插入字段
```

删除帮助
```
usage: easyrenamer delate [-h] -s SOURCE [-S [suffix ...]] [--case] [--withsuffix] [--regular] directory

positional arguments:
  directory             文件目录

optional arguments:
  -h, --help            show this help message and exit
  -s SOURCE, --source SOURCE
                        删除字段
  -S [suffix ...]       指定后缀集
  --case                忽略大小写
  --withsuffix          处理后缀名
  --regular             正则匹配
```


### example

一个样例文件夹
```
test
├─北京科技大学-小明-2班.docx
├─北京科技大学-小李-2班.docx
├─北京科技大学-小王-3班.docx
├─北京科技大学-小红-5班.docx
└─北京科技大学-小赵-2班.docx
```

**替换**

```北京科技大学 to USTB```

command:
```
easyrenamer replace -s 北京科技大学 -d USTB test
```

log:
```
北京科技大学-小明-2班.docx -> USTB-小明-2班.docx 
北京科技大学-小李-2班.docx -> USTB-小李-2班.docx 
北京科技大学-小王-3班.docx -> USTB-小王-3班.docx 
北京科技大学-小红-5班.docx -> USTB-小红-5班.docx 
北京科技大学-小赵-2班.docx -> USTB-小赵-2班.docx 
```

results:
```
test
├─USTB-小明-2班.docx
├─USTB-小李-2班.docx
├─USTB-小王-3班.docx
├─USTB-小红-5班.docx
└─USTB-小赵-2班.docx
```

**删除**

```delate -x班```

这里使用了正则模式启用命令为``--regular``
并且由于windows CMD和python解析的问题需要对``-``进行转义，写做``\-``，说明它是一个减号字符而不是选项。

command:
```
easyrenamer delate -s \-[0-9]班 --regular test
```

log:
```
USTB-小明-2班.docx -> USTB-小明.docx
USTB-小李-2班.docx -> USTB-小李.docx
USTB-小王-3班.docx -> USTB-小王.docx
USTB-小红-5班.docx -> USTB-小红.docx
USTB-小赵-2班.docx -> USTB-小赵.docx
```

results:
```
test
├─USTB-小明.docx
├─USTB-小李.docx
├─USTB-小王.docx
├─USTB-小红.docx
└─USTB-小赵.docx
```

**插入**

插入有多个模式，这里演示在最后方插入``-CS``

这里由于``-CS``第一个字符为``-``，会被误判，可以采用``=``的方法告诉程序这是一个参数而非选项
command:
```
easyrenamer insert -b -d="-CS" test
```

log:
```
USTB-小明.docx -> USTB-小明-CS.docx
USTB-小李.docx -> USTB-小李-CS.docx
USTB-小王.docx -> USTB-小王-CS.docx
USTB-小红.docx -> USTB-小红-CS.docx
USTB-小赵.docx -> USTB-小赵-CS.docx
```

results:
```
test
├─USTB-小明-CS.docx
├─USTB-小李-CS.docx
├─USTB-小王-CS.docx
├─USTB-小红-CS.docx
└─USTB-小赵-CS.docx
```