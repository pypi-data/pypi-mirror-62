gd_kafka
---
**For internal ```Greendeck``` use only.**

![Greendeck](./images/gd_transparent_blue_bg.png)  ![kafka](./images/kafka.png)
### Install from pip
https://pypi.org/project/gd-kafka/

```pip install gd-kafka```


### How to use ?
##### import the library
```python
import gd_kafka
```

##### import ```kafka``` class
```python
from gd_kafka import GDKafka

```

##### initialize ```Kafka``` client connection
```python
# declare variables
IP_PORT = KAFKA_IP_PORT
# Here default values is IP_PORT=''

gdk = GDKafka(IP_PORT="12.12.12.12:9092")

#Here, 12.12.12.12 is example host ip.
```

---
How to build your pip package

* open an account here https://pypi.org/

In the parent directory
* ```python setup.py sdist bdist_wheel```
* ```twine upload dist/*```

references
* https://medium.com/small-things-about-python/lets-talk-about-python-packaging-6d84b81f1bb5

# Thank You
