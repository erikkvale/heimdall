# Heimdall
![alt text](static/Heimdall.jpg)
Image courtesy of Marvel Studios

### Overview
Heimdall consists of Python packages containing various Kafka producer and consumer implementations
pertaining to application monitoring and related workflows/tasks.

### Package(s)
* ddos
  * A DDOS (Distributed Denial of Service) monitor where an Apache access log is ingested, parsed then
    evaluated by a set of algorithms to determine if any ip addresses should be flagged for further
    investigation as part of a DDOS attack.
    
### Quickstart & Features
In order to speed up creating the Kafka and Zookeeper environments that any producer and consumer components are 
dependent on, I have opted to use some open-source, well supported images:

- Kafka: [wurstmeister/kafka](https://hub.docker.com/r/wurstmeister/kafka/)
- Zookeeper: [wurstmeister/zookeeper](https://hub.docker.com/r/wurstmeister/zookeeper)

These images are "bundled" and referenced in the `docker-compose.yml` file in the repo directory root, along
with some common environment variable settings for the images. Most notably for this configuration is the `KAFKA_ADVERTISED_HOST_NAME`
which is currently set to the Docker Machine IP on the host machine. Which is also the value that the Kafka
producer and consumer components use to connect to the broker.

