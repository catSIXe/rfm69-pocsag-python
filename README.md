# rfm69-pocsag-python
transmits POCSAG Messages with an RFM69 Module

# Libraries
https://github.com/Gadgetoid/py-spidev
# Install
## SPI-Dev Lib
```bash
git clone https://github.com/Gadgetoid/py-spidev
cd py-spidev
sudo make install
```
## Python Libraries(Pika for rabbitMQ)
```bash
pip install pika
```

## Pin Configuration
| RFM pin | Pi pin  
| ------- |-------
| DIO0    | 18 (GPIO24)  
| MOSI    | 19  
| MISO    | 21  
| CLK     | 23  
| NSS     | 24  
| Ground  | 25  
| RESET   | 29

## Infrastructure:
![](doc/rabbitmq-users.jpg?raw=true)

Producer(s) => rabbitMQ => Gateway(s)

rabbitMQ Format (address, message): 
`["3D", "Text"]`
   
## config.ini:
```ini
[main]
amqpuri = amqp://user:pas@host:port
```
