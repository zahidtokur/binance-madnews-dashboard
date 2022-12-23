# To run Celery periodic tasks


### Step 1:
```
celery -A dashboard beat -l info
```

### Step 2:

In another terminal

```
celery -A dashboard worker -l info
```

if you are on windows follow the steps below:

```
pip install eventLet
```

and then run the worker again as such:

```
celery -A dashboard worker -l info -P eventlet
```