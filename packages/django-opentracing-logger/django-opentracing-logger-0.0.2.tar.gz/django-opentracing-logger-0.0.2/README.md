# opentracing python SDK

# 0. TODO
django-opentracing-logger is a django opentracing SDK based on logger which focus on ease to use.
This project mainly works now, but we need to do a little work to let it works with official
opentracing since it was built for a dialect of opentracing schema(90% of the schema were the same).

## 1. install
```bash
# current 0.0.1
pip install django-opentracing-logger
```

## 2. config opentracing logger
```python
# settings.py
from django_opentracing_logger.opentracing.tracer import set_log_tracer

# add request middleware
MIDDLEWARE = [
    'django_opentracing_logger.opentracing.middleware.DDTracerMiddleware',
]

# add logger
LOGGING = {
    'filters': {
        'trace_id': {
            '()': 'django_opentracing_logger.opentracing.logging.TraceIDFilter',
        }
    },
    'formatters': {
        # ...,
        'trace': {
            '()': 'pythonjsonlogger.jsonlogger.JsonFormatter',
            'fmt': '%(message)s',
        }
    },
    'handlers': {
        # ...,
        'trace': {
            'level': 'INFO',
            'class': 'django_opentracing_logger.opentracing.logging.TraceHandler',
            'filename': '%s/trace.log' % '/data/logs/trace',
            'backupCount': 10,
            'when': 'D',
            'interval': 1,
            'formatter': 'trace'
        }
    },
    'loggers': {
        'tracer': {'handlers': ['trace'], 'propagate': True, 'level': 'DEBUG'},
    }
}

# init tracer
APM_ENABLE = True 
if APM_ENABLE:
    set_log_tracer("PROJECT_NAME") # TODO replace PROJECT_NAME with your real project name
```

## 3. collect
collect logs in `/data/logs/trace` 

## 4. view
use any viewer which Compatible with opentracing.
