# Python Logging模块使用指南

## logging基本概念

* 日志级别：

|   日志级别  | 数字等级 | 级别描述 |
| ---------- | -------| --------------------- |
|   DEBUG    |  10  |  调试日志                 |
|   INFO     |  20  |  正常业务日志              |
|   WARNING  |  30  |  业务警告日志，不影响功能     |
|   ERROR    |  40  |  业务错误日志，已经影响部分功能|
|   CRITICAL |  50  |  崩溃日志记录               |

* 核心组件

```text
1, Logger 核心对象
    setLevel()
    addHandler()
    removeHandler()
    addFilter()
    removeFilter()
```

```text
2, Handler 记录器
    logging.StreamHandler(IO) :控制台输出handler,默认是sys.error,IO可接受一个文件
    logging.FileHandler(file [, mode='a']) : 文件输出，和StreamHandler差不多，但是FileHandle会通过mode方式打开file。
    logging.handlers.RotatingFileHandler(filename，mode，maxBytes, backupCount, encoding): 按照大小自动分割日志文件，是FileHandler的子类。
        filename是文件名，必填参数
        mode默认是‘a’追加模式，可选参数
        maxBytes=0默认无限不分割，可选参数
        backupCount=2.表示最大生成2个日志文件，log.log, log1.log.可选参数
        encoding: 'utf-8', 不配置可能导致日志乱码
    logging.TimedRotatingFileHandler(filename, when, interval, backupCount, encoding): 按照时间格式分割日志。是FileHandler的子类。
        filename:日志文件名，必填参数
        interval: 时间间隔。配合shen使用
        when: 时间间隔单位，不区分大小
            'S': 秒。 如果interval配置30，表示30秒生成一个日志文件
            'M': 分。
            'H': 时
            'D': 天
            'W': 周（interval=0表示周一）
            'MidNight': 每天凌晨
        backupCount:3 最大生成3个日志文件，其余的删除
        encoding： 防止日志中文乱码
    setLevel(level): 用于给每一个handler单独设置级别
    setFormatter(Formatter): 用于给每一个handler单独设置日志记录样式。
    addFilter(Filter): 用于给每一个handler单独设置过滤器
    removeFilter(Filter): 用于给每一个handler单独移除过滤器
```

```text
3, Filter  控制精度
```

```text
4, Formatter    样式，这里是比较复杂的，用于调整日志的打印样式。
```

| 表达式    |  解释    |
| -------- | ---- |
| %(name)s     | Logger的名字     |
| %(levelno)s      | 数字形式记录日志级别：50     |
| %(levelname)s      | 文本形式记录日志级别：DEBUG     |
| %(pathname)s      | 调用函数的模块的完成路径。可能没有     |
| %(filename)s      | 输出函数的文件名。     |
| %(module)s        | 输出函数的模块名字          |
| %(funcName)s      | 输出函数的函数名字     |
| %(lineno)d      | 输出语句所在的代码行     |
| %(created)f      | 使用UNIX的标准时间格式显示当前时间     |
| %(relativeCreated)d      | 相对Logger创建点的相对运行时间。     |
| %(asctime)s      | 字符串形式显示当前时间： '2022-02-12 17:12:34, 779'    |
| %(thread)d      | 线程ID，可能不存在     |
| %(threadName)s      | 线程Name，可能不存在     |
| %(process)d      | 进程ID，可能不存在     |
| %(message)s      | log信息     |

## logging最简单使用

* 直接使用logging打印

```python
import logging

logging.debug('debug')
logging.error('error')
```

* 使用basicConfig配置全局logging，可配置控制台打印和日志记录

```python
# 配置控制台打印
import logging

fmt = '%(asctime) - %(levelname)s - %(module)s - %(message)s'
logging.basicConfig(format=fmt, level=logging.DEBUG)
logging.error('error')
```

```python
# 配置日志记录
import logging

fmt = '%(asctime) - %(levelname)s - %(module)s - %(message)s'
logging.basicConfig(filename='log.log', level=logging.DEBUG, filemode='a', format=fmt)
# filemode = 'w': 表示覆盖写日志，'a'：表示每次都会追加日志
```

```python
# demo
import logging
from logging import Formatter, StreamHandler
from logging.handlers import TimedRotatingFileHandler as FileHandler


def fmt_logger(file: str):
    logger = logging.getLogger(file)
    logger.setLevel(level=logging.DEBUG)
    formatter: Formatter = f'%(asctime)s - %(levelname)s - ThreadId:%(thread)d - %(filename)s:%(funcName)s:%(lineno)d - %(message)s'

    stream_handler: StreamHandler = StreamHandler()
    stream_handler.setLevel(level=logging.INFO)
    stream_handler.setFormatter(fmt=formatter)

    time_handler: FileHandler = FileHandler(filename='log.log', when='MidNight', backupCount=7, encoding='utf-8')
    time_handler.setLevel(level=logging.DEBUG)
    time_handler.setFormatter(fmt=formatter)

    logger.addHandler(stream_handler)
    logger.addHandler(time_handler)
    return logger
```

基本实现了一个多线程下单例模式的logger，原生打印 更好的实现，可以采用loguru库去打印日志。