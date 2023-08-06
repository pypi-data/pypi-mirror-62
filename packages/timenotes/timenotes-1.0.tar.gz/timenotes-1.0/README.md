# TimeNotes Readme

an easy-use tool for time researching

### 安装

```powershell
pip install timenotes
```

### 引用

```python
import timenotes
```

### 声明一个笔记本

```python
timenote = timenotes.Timenote(words=None, intimeshow=False)
```

words参数为自定义输出形式，不填时默认为`"阶段[{}]：{}时间花费 {} 秒"`

例如，需要输入这种形式的字符串：`words="区块{}：{}时间 {} 喵"`



intimeshow参数为True时，每结束一个时间段的记录(具体为end)就会自动输出

为False时，不输出，需要在结尾专门输出，同时这种输出可以保持格式的对齐

默认为False

### 使用

```python
timenote.start("示例一")
......
timenote.note("示例二")
......
timenote.pause()
......
timenote.start()
......
timenote.end()
......
timenote.show()
timenote.sleep(1)
```

`timenote.start()`可以输入一个字符串类型的参数并作为这个阶段的名称

如果无输入参数则自动以当前阶段的序数为名称

`timenote.end()`用于结束一个阶段的记录

`timenote.note()`和同时执行end和start的效果相同

`timenote.show()`用于输出记录，这里建议名字长度不同时使用纯中文`

`timenote.sleep()`用于使程序休眠一定时间，单位为秒