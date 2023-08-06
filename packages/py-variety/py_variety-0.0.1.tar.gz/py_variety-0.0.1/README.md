# 项目背景
基于 Python 调用 Github 项目 [variety](https://github.com/variety/variety) 的脚本  
variety 文件夹来源于该项目拷贝  
版本：![https://img.shields.io/badge/Python-3.x-brightgreen]() ![https://img.shields.io/badge/variety-1.5.1-lightgrey]()

---

## 目前已有的功能  

### 1. 规整指定数据库集合的首层字段
```text
如： 
object1={'a':1,'b':2,'d':4}
object2={'a':1,'b':2,'c':3}
...
变更为：
object1={'a':1,'b':2,'c':'','d':4}
object2={'a':1,'b':2,'c':3,'d':''}
...
```

#### demo
```python
from py_variety import formal_fields

db_name = 'db_name'
coll_name = 'coll_name'
new_name = 'new_name'
formal_fields(host='x.x.x.x', verify={'user': 'xxx', 'passwd': 'xxxxxx', 'authdb': 'xxxx'},
              db_name=db_name, coll_name=coll_name,new_name=new_name)
```