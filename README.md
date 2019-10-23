# rfm69-pocsag-python
transmits POCSAG Messages with an RFM69 Module
### Infrastructure:
![](doc/rabbitmq-users.jpg?raw=true)
  Producer(s) => rabbitMQ => Gateway(s)
  
  rabbitMQ Format (address, message):
   `["3D", "Text"]`
   
### config.ini:
```ini
[main]
amqpuri = amqp://user:pas@host:port
```
