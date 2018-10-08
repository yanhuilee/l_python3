pygame-飞机大战
```
验证是否安装： python -m pygame.examples.aliens
```

#### 控制台输出中文
```
import io
import sys
# 改变标准输出的默认编码
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf8')
```

venv
---
```
source venv/Scripts/activate
python -m pip install -U pip
```

#### 问题整理
Microsoft Visual C++ 14.0 is required.
手动下载whl包

