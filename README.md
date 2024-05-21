# kafka_crypto_bybit_streaming
A demo to demonstrate how to set up a remote Kafka-based data streaming pipeline for collecting and processing cryptocurrency data using Python
### 1) Setting up a remote Kafka Linux server
- Create an Azure Virtual Machine (VM) with Ubuntu Linux.
  - Use Linux (ubuntu 22.04) and Standard B2s (2 vcpus, 4 GiB memory)
  <img src="" width="60%" height="60%"><br>
  - Connect from local machine (Windows) PowerShell using SSH private key file provided by Azure
  <img src="" width="60%" height="60%"><br>
  <img src="" width="60%" height="60%"><br>
- Install Kafka on the VM.
  - Update the package in Linux
  - Install Java Development Kit <br>
  <img src="" width="60%" height="60%"><br>
### 2) SSH Key Setup
- Generate an SSH key (public key) using PuTTY.
  - [PuTTY MSI (‘Windows Installer’)](https://www.chiark.greenend.org.uk/~sgtatham/putty/latest.html)
  - Open the PuTTY Key Generator to load the private key<br>
  <img src="" width="45%" height="45%"><br>
  - Conversion -> Export OpenSSH Key -> Save this public key somewhere
### 3) Accessing the VM via Visual Studio Code (VS Code)
- Open VS Code on local machine.
- Install the “Remote - SSH” extension.<br>
  <img src="" width="45%" height="45%"><br>
- Use the SSH configuration (Host: VM name, User name, HostName: VM IP address, IdentityFile: public key location) to connect the Azure VM from VS Code.<br>
  <img src="" width="45%" height="45%"><br>
### 4) Kafka-Python Installation
- In the VM, install the kafka-python library using pip:
- ```pip install kafka-python```
### 5) Bybit API Data Collection Script
- Write a Python script that interacts with the Bybit API to retrieve crypto data.
- This script will act as Kafka producer, publishing crypto data to a Kafka topic.
### 6) Kafka Producer Configuration:
- Configure Kafka producer to send data to a specific Kafka topic.
- Ensure that the topic name aligns with the use case (e.g., “crypto-data-topic”).
### 7) Local Consumer Setup:
- On the local computer, set up a Kafka consumer.
- Install the kafka-python library locally.
- Consume data from the same Kafka topic (“crypto-data-topic”) to receive the streaming data.
### 8) Running the Demo:
- Start the Kafka producer script on Azure VM.
- Observe the data being published to the Kafka topic.
- Run the Kafka consumer script on local machine to consume the data.
