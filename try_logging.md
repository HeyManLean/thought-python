## logging


### 1. 格式化参数

参数|用法|说明|
---|---|---|
asctime|%(asctime)s|时间
created|%(created)f|时间戳
filename|%(filename)s|文件名
funcName|%(funcName)s|函数名
levelname|%(levelname)s|日志级别名
levelno|%(levelno)s|日志级别序号
lineno|%(lineno)d|日志信息所在行数
message|%(message)s|日志内容
module|%(module)s|模块名
name|%(name)s|logger名字
pathname|%(pathname)s|文件绝对路径(如果可以获取)
process|%(process)d|进程id
processName|%(processName)s|进程名字
thread|%(thread)d|线程id
threadName|%(threadName)s|线程名字


### 2. basicConfig

- 默认是控制台输出
- 配置写到文件中

```python
logging.basicConfig(
    level=logging.DEBUG,
    filename='app.log',
    filemode='w',
    datefmt='%b %d-%Y %H:%M:%S',  # 时间格式
    format=(
        '%(asctime)s %(levelname)s -'
        '%(filename)s/%(lineno)d - %(message)s'
    )
)
```

### 3. ERROR

- 捕捉异常, 可打印异常信息到日志里
- `exc_info=True`
- 或`logging.exception`

```python
try:
    d = 1 / 0
except:
    logging.error('Oops! Something went wrong!', exc_info=True)
    # logging.exception('Oops! Something went wrong!')
```

输出

```
Jan 24-2019 11:26:58 ERROR -tryLogging.py/26 - Oops! Something went wrong!
Traceback (most recent call last):
  File "tryLogging.py", line 24, in <module>
    d = 1 / 0
ZeroDivisionError: division by zero
```


### 4. 配置

- logger
- handler
- formatter


```
logger --(1:n)--> handler --(1:1)--> formatter
```

- 基本配置

```python
logging.basicConfig(
    level=logging.DEBUG,
    filename='app.log',
    filemode='w',
    datefmt='%b %d-%Y %H:%M:%S',
    format=(
        '%(levelname)8s %(asctime)s '
        '%(filename)s/%(lineno)d - %(message)s'
    )
)
```

- 复杂配置

```python
c_formatter = logging.Formatter(
    fmt='%(name)s - %(levelname)s - %(message)s',
    datefmt='%b %d-%Y')
f_formatter = logging.Formatter(
    fmt='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S')

# --- 初始化handler ---
c_handler = logging.StreamHandler()
f_handler = logging.FileHandler(
    filename='app.log',
    mode='a',
    encoding='utf-8'
)
# 设置level
c_handler.setLevel(logging.WARNING)
f_handler.setLevel(logging.ERROR)
# 设置formatter
c_handler.setFormatter(c_formatter)
f_handler.setFormatter(f_formatter)

# --- 初始化logger ---
logger = logging.getLogger(__name__)
# 设置handler
logger.addHandler(c_handler)
logger.addHandler(f_handler)

logger.warning('This is a warning!')
logger.error('This is an error!')
```

- 文件或对象复杂配置

```python
LOGGING_CONF = {
    'version': 1,  # 版本必须为1
    'disable_existing_loggers': False,  # True 重新配置会使之前 logger 无效
    # formatter
    'formatters': {
        'simple': {
            'format': '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            'datefmt': '%Y-%m-%d %H:%M:%S'
        }
    },
    # handler
    'handlers': {
        'default': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'simple',
            'stream': 'ext://sys.stdout'
        },
        'info_file_handler': {
            'class': 'logging.handlers.RotatingFileHandler',  # 自动切割
            'level': 'INFO',
            'formatter': 'simple',
            'filename': 'info.log',
            'maxBytes': 10485760,
            'backupCount': 20,
            'encoding': 'utf8'
        },
        'error_file_handler': {
            'class': 'logging.FileHandler',
            'level': 'ERROR',
            'formatter': 'simple',
            'filename': 'error.log'
        }
    },
    # logger
    'loggers': {
        'test': {
            'level': 'DEBUG',
            'handlers': ['default', 'info_file_handler'],
            'propagate': False
        },
        'error': {
            'level': 'ERROR',
            'handlers': ['error_file_handler'],
            'propagate': False
        }
    }

}
logging.config.dictConfig(LOGGING_CONF)

# test
test_logger = logging.getLogger('test')
# error
error_logger = logging.getLogger('error')
```
