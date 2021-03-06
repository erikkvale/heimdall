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
##### Install dependencies into local virtual env (make sure you are in the repo directory)
```
pipenv install
```

##### Check python dependencies (see [detection-of-security-vulnerabilities](https://pipenv.kennethreitz.org/en/latest/advanced/#detection-of-security-vulnerabilities))
```
pipenv check

# Expected Output:
Checking PEP 508 requirements…
Passed!
Checking installed package safety…
All good!
```

##### Run unit tests
```
python -m pytest
```

##### Run test coverage
```
# Run 
coverage run --source=. -m pytest

# Report stdout
coverage report

# Report HTML then open htmlcov/index.html in working dir
coverage html
```

##### Start Zookeeper and Kafka
```
docker-compose up
```

##### Set ENV variables (see sample.env for concrete examples, `docker ps` for ip and port details)
```
KAFKA_BOOTSTRAP_SERVER=<kafka host IP><port>
KAFKA_TOPIC=<topic name>

# Expects a combined format Apache access log file path (See: https://httpd.apache.org/docs/current/logs.html#combined)
APACHE_ACCESS_LOG_FILE_PATH=<abs file path>
```


##### Run the package's relevant producer module to publish to Kafka
```
# Assuming pipenv venv is activated
python -m ddos.producer
```
##### Run the package's relevant consumer module to consume messages
```
# Assuming pipenv venv activated
python -m ddos.consumer
```

# Next Steps and Improvements
- Improving the detection algorithm and refactoring. Right now when the number of requests from a certain
IP address reach a specified integer threshold, that IP is simply written to a file in the ddos package root directory called
`suspect_ips.txt`. It's way too simple and clunky. Expanding to also check which URL endpoints are being hit and the
timeframe would be obvious next steps. I want to get what I have in at this point, but I can improve and do more research on implementing
an ML solution in the mean time.

- Improving test coverage, this goes hand in hand with refactoring some of the main code, as it currently sits at 74% coverage

- Would like to read up more on Kafka and the kafka-python library's various arguments and settings, in order
to make this more robust and scale appropriately. Definitely need to improve my understanding.