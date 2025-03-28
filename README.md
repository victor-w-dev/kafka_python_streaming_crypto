# kakfa-python Azure VM Ubuntu cryptocurrency streaming
- A demo to demonstrate how to set up a remote Kafka-based data streaming workflow for collecting and processing cryptocurrency data (e.g. Bitcoin USDT perpetual contract data) using Python kafka-python package and Bybit API.
- A Kafka producer collects the data and publishes to the Kafka Broker in the same remote Azure VM with a topic (e.g. 'BTCUSDT-1min').
- A consumer in local computer receives the data and then can have further transformation for triggering a trading strategy.
<img src="https://github.com/victor-w-dev/kafka_streaming_crypto/blob/main/img/flow_chart.PNG" width="100%" height="100%"><br>

Table of contents
=================

<!--ts-->
[1. Setting up a remote Kafka Linux server](#Setting-up-a-remote-Kafka-Linux-server)<br>
[2. Install Kafka on the VM](#Install-Kafka-on-the-VM)<br>
[3. Accessing the VM via Visual Studio Code using private key from Azure VM](#Accessing-the-VM-via-Visual-Studio-Code-using-private-key-from-Azure-VM)<br>
[4. Install Python and kafka-python package in VM via VS code](#Install-Python-and-kafka-python-package-in-VM-via-VS-code)<br>
[5. Configuration in server properties in the remote Kafka broker](#Configuration-in-server-properties-in-the-remote-Kafka-broker)<br>
[6. Set up Inbound Port Rule in remote VM Network settings](#Set-up-Inbound-Port-Rule-in-remote-VM-Network-settings)<br>
[7. Remote kafka-python producer Setup](#Remote-kafka-python-producer-Setup)<br>
[8. Local Consumer Setup](#Local-Consumer-Setup)<br>
[9. Running the Demo](#Running-the-Demo)<br>
<!--te-->

Setting up a remote Kafka Linux server
============
- Create an Azure Virtual Machine (VM) with Ubuntu Linux.<br>
  Use Linux (ubuntu 22.04) and Standard B2s (2 vcpus, 4 GiB memory)<br>
  <img src="https://github.com/victor-w-dev/kafka_streaming_crypto/blob/main/img/1_VM.PNG" width="75%" height="75%"><br>
- Connect from local machine (Windows) PowerShell using SSH Private Key file provided by Azure
  <img src="https://github.com/victor-w-dev/kafka_streaming_crypto/blob/main/img/1_access_vm.png" width="75%" height="75%"><br>
  <img src="https://github.com/victor-w-dev/kafka_streaming_crypto/blob/main/img/1_powershell.png" width="75%" height="75%"><br>
  
Install Kafka on the VM
============
- Update the package in Linux and install Java Development Kit OpenJDK 11<br>
```bash
$ sudo apt-get update
$ sudo apt install openjdk-11-jdk
```
  <img src="https://github.com/victor-w-dev/kafka_streaming_crypto/blob/main/img/2_install_java.PNG" width="75%" height="75%"><br>
- Download and Install Kafka 2.4.0<br>
```bash
$ mkdir Downloads
$ curl https://archive.apache.org/dist/kafka/2.4.0/kafka_2.13-2.4.0.tgz -o Downloads/kafka.tgz
$ mkdir kafka
$ cd kafka
$ tar -xvzf ~/Downloads/kafka.tgz --strip 1
```
  <img src="https://github.com/victor-w-dev/kafka_streaming_crypto/blob/main/img/2_download_kafka.PNG" width="75%" height="75%"><br>
  <img src="https://github.com/victor-w-dev/kafka_streaming_crypto/blob/main/img/2_unzip_kafka.PNG" width="75%" height="75%"><br>
  <img src="https://github.com/victor-w-dev/kafka_streaming_crypto/blob/main/img/2_install_kafka_completed.PNG" width="75%" height="75%"><br>

Accessing the VM via Visual Studio Code using private key from Azure VM
============
- Open VS Code on local machine.
- Install the “Remote - SSH” extension.<br>
  <img src="https://github.com/victor-w-dev/kafka_streaming_crypto/blob/main/img/4_extension_ssh.PNG" width="60%" height="60%"><br>
- Use the SSH configuration to connect the Azure VM from VS Code.<br>
  - Press F1 to search "Remote-SSH: Open SSH Configuration File..."<br>
  <img src="https://github.com/victor-w-dev/kafka_streaming_crypto/blob/main/img/4_search_box.PNG" width="60%" height="60%"><br>
  - Edit SSH configuration (can get information from Azure VM Overview Page for Host: VM name, User name, HostName: VM IP address, Port, IdentityFile: Private Key location)<br>
  <img src="https://github.com/victor-w-dev/kafka_streaming_crypto/blob/main/img/4_config2.PNG" width="60%" height="60%"><br>
- Connect the VM via VS Code<br>
  <img src="https://github.com/victor-w-dev/kafka_streaming_crypto/blob/main/img/4_vm_connect.PNG" width="60%" height="60%"><br>
- After successful connection, can access and manipulate files in VM via VS code Explorer<br>
  <img src="https://github.com/victor-w-dev/kafka_streaming_crypto/blob/main/img/4_connected_explorer.PNG" width="60%" height="60%"><br>

Install Python and kafka-python package in VM via VS code
============
- In VS code terminal: 
```bash
$ sudo apt install python3
$ pip install kafka-python
```

Configuration in server properties in the remote Kafka broker
============
- Go to 'config' folder of kafka location
- In the server.properties configuration file for each broker, need to adjust `listeners`, `advertised.listeners` and set it either to DNS name or public IP address of the server where broker is hosted.<br>
Examples<br>
```listeners=PLAINTEXT://localhost:9092,EXTERNAL://0.0.0.0:9093```<br>
```advertised.listeners=PLAINTEXT://localhost:9092,EXTERNAL://public IP address of the server:9093```<br>
```listener.security.protocol.map=PLAINTEXT:PLAINTEXT,EXTERNAL:PLAINTEXT```<br>
- This setup enables a producer on the VM to send data to localhost:9092 and a consumer on a separate machine to fetch data from the public IP address of the server:9093, with an Azure Network Security Group rule allowing inbound traffic to port 9093 from the consumer’s IP.
- Here, just a single broker to demo<br>
  <img src="https://github.com/victor-w-dev/kafka_streaming_crypto/blob/main/img/6_server_properties2.PNG" width="75%" height="75%"><br>

Set up Inbound Port Rule in remote VM Network settings
============
- Allow local consumer to interact with remote VM Kafka broker (single broker default port: 9093), consuming the crypto data
- Make sure to include the local consumer IP for Source IP addresses in the Inbound Port Rule<br>
  <img src="https://github.com/victor-w-dev/kafka_streaming_crypto/blob/main/img/7_inbound_rule2.PNG" width="75%" height="75%"><br>
  
Remote kafka-python producer Setup
============
- Make sure Python package pybit (for Bybit API) installed
- Write a Python script that interacts with the Bybit API to retrieve crypto data.
- This script will also act as Kafka producer, publishing crypto data to a Kafka topic, i.e. 'BTCUSDT-1min'.<br>
[producer_kline.py](https://github.com/victor-w-dev/kafka_streaming_crypto/blob/main/producer_kline.py)<br>

Local Consumer Setup
============
- Install the kafka-python library locally.
- On the local computer, set up a Kafka consumer.
- Consume data from the same Kafka topic ('BTCUSDT-1min') to receive the streaming data.<br>
[consumer.py](https://github.com/victor-w-dev/kafka_streaming_crypto/blob/main/consumer.py)<br>

Running the Demo
============
- Start zookeeper first, then Kafka broker on Azure VM<br>
  <img src="https://github.com/victor-w-dev/kafka_streaming_crypto/blob/main/img/10_start_zookeeper_kafka_server.PNG" width="75%" height="75%"><br>
- Start the Kafka producer script on Azure VM
- Observe the data being published to the Kafka topic.<br>
  <img src="https://github.com/victor-w-dev/kafka_streaming_crypto/blob/main/img/10_run_producer.PNG" width="75%" height="75%"><br>
- Run the Kafka consumer script on local machine to consume the data, using Spyder as IDE.<br>
  <img src="https://github.com/victor-w-dev/kafka_streaming_crypto/blob/main/img/10_run_consumer.PNG" width="75%" height="75%"><br>
