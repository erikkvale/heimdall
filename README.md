# Heimdall
![alt text](static/Heimdall.jpg)
Image courtesy of Marvel Studios

### Overview
Heimdall consists of Python packages containing various Kafka producer and consumer implementations
pertaining to application monitoring and related workflows/tasks.

### Package(s)
* ddos
  * A DDOS (Distributed Denial of Service) monitor where an Apache access log is ingested, parsed then
    evaluated by a set of algorithms to determine if any IP addresses should be flagged for further
    investigation as part of a DDOS attack. Suspect IP addresses will be written to a local file directory.
    
### Quickstart & Features
In order to speed up creating the Kafka and Zookeeper environments that any producer and consumer components are 
dependent on, I have opted to use some open-source Docker images with some decent support:

- Kafka: [wurstmeister/kafka](https://hub.docker.com/r/wurstmeister/kafka/)
- Zookeeper: [wurstmeister/zookeeper](https://hub.docker.com/r/wurstmeister/zookeeper)

These images are "bundled" and referenced in the `docker-compose.yml` file in the repo directory root, along
with some common environment variable settings for the images. Most notably for this configuration is the `KAFKA_ADVERTISED_HOST_NAME`
which is currently set to the Docker Machine IP on the host machine. Which is also the value (along with the port)
that the Kafka producer and consumer components use to connect to the broker, this is a multi-broker `docker-compose` file, see 
the helpful wiki for more on the details of the Docker networking acrobatics for the image [here](https://github.com/wurstmeister/kafka-docker/wiki/Connectivity).
and any image pre-reqs. Otherwise...

#### Pre-requisites
- docker
- docker-compose
- pipenv (in absence of app docker container)
__________________________________________________
##### Clone the respository
```
git clone https://github.com/erikkvale/heimdall.git
```
##### Install dependencies into local virtual env
```
pipenv install
```

##### Run unit tests
```
python -m pytest
```

##### Set ENV variables (see sample.env for concrete examples)
```
KAFKA_BOOTSTRAP_SERVER=<kafka host IP><port>
KAFKA_TOPIC=<topic name>
APACHE_ACCESS_LOG_FILE_PATH=<abs file path>
```

##### Start Zookeeper and Kafka
```
docker-compose up
```

##### Run the package's relevant producer.py script to publish to Kafka
```
# Assuming pipenv venv is activated
python ddos/producer.py
```
##### Run the package's relevant consumer.py script to consume messages
```
# Assuming pipenv venv activated
python ddos/consumer.py
```
