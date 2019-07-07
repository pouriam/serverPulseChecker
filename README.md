# Server Pulse Checker
A python project to constantly monitor services for availability and send email if services are down. Basically it checks
if a service on a specified host is running.

## Requirements
Python 3 (tested with python 3.6 but should be fine with any version of python 3)

## Run
There are two options to run the application:

1- In the root of the application run following command:
`python src/main.py`

**Note**: Make proper changes to the `config/config.cfg` file.

2- In the root of the application run following command:
`python src/main.py {PATH_TO_CONFIG_FILE}`.

which `{PATH_TO_CONFIG_FILE}` is absolute path to the configuration file (explained below)

## Configuration file (config.cfg)
It follows the rules of configuration files in python.
For more info see: https://docs.python.org/3/library/configparser.html

Note that for the application to properly function,
`general` section MUST be present. Here is the template.
Use this template and modify parameters:

```
[general]

logging.format= [%(asctime)-15s] %(section)s %(message)s
interval=60
smtp.host=smtp.gmail.com
smtp.port=587
smtp.login.email=your@email.com
smtp.login.password=your_password
from.email=from@email.com
to.email=to@email.com
email.subject=Serve Pulse Checker Critical Alert
```

`logging.format` is the format of the message being logged.

`interval` is the time between each round of checking availability. Default is 60 seconds.

`smtp.host` is the email smtp server host. By default it set to gmail smtp server.

`smtp.port` is the email smtp server port. By default it set to gmail smtp server port which is 587

`smtp.login.email` and `smtp.login.password` are email and password to login to smtp server.

`from.email` is the email of the sender.

`to.email` is the email of the receiver.

`email.subject` is the subject of email.

### Add more services to monitor
Simply follow the convensions of python cfg file (https://docs.python.org/3/library/configparser.html).

for example if need to check SQL Server availability, just add a meaningful section name
(for exmaple sqlServer) and enter host and port. Section name is just used in logging.

```
[sqlServer]
host=localhost
port=1433
```
