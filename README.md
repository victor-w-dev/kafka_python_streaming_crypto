# kafka_crypto_bybit_streaming
A demo to demonstrate how to set up a remote Kafka-based data streaming pipeline for collecting and processing cryptocurrency data using Python
### 1) Setting up a remote Kafka Linux server
- Create an Azure Virtual Machine (VM) with Ubuntu Linux.<br>
  Use Linux (ubuntu 22.04) and Standard B2s (2 vcpus, 4 GiB memory)<br>
  <img src="https://github.com/victor-w-dev/kafka_streaming_crypto/blob/main/img/1_VM.PNG" width="60%" height="60%"><br>
- Connect from local machine (Windows) PowerShell using SSH Private Key file provided by Azure
  <img src="https://github.com/victor-w-dev/kafka_streaming_crypto/blob/main/img/1_access_vm.png" width="60%" height="60%"><br>
  <img src="https://github.com/victor-w-dev/kafka_streaming_crypto/blob/main/img/1_powershell.png" width="60%" height="60%"><br>
### 2) Install Kafka on the VM.
- Update the package in Linux and install Java Development Kit <br>
  <img src="https://github.com/victor-w-dev/kafka_streaming_crypto/blob/main/img/2_install_java.PNG" width="60%" height="60%"><br>
- Download Kafka <br>
  <img src="https://github.com/victor-w-dev/kafka_streaming_crypto/blob/main/img/2_download_kafka.PNG" width="60%" height="60%"><br>
  <img src="https://github.com/victor-w-dev/kafka_streaming_crypto/blob/main/img/2_unzip_kafka.PNG" width="60%" height="60%"><br>
  <img src="https://github.com/victor-w-dev/kafka_streaming_crypto/blob/main/img/2_install_kafka_completed.PNG" width="60%" height="60%"><br>
### 3) SSH Public Key Setup
- Generate an SSH key (Public key) using PuTTY.
  - [PuTTY MSI (‘Windows Installer’)](https://www.chiark.greenend.org.uk/~sgtatham/putty/latest.html)
  - Open the PuTTY Key Generator to load the Private Key<br>
  <img src="https://github.com/victor-w-dev/kafka_streaming_crypto/blob/main/img/3_putty_ssh.PNG" width="45%" height="45%"><br>
  - Conversion -> Export OpenSSH Key -> Save this Public Key somewhere
### 4) Accessing the VM via Visual Studio Code (VS Code)
- Open VS Code on local machine.
- Install the “Remote - SSH” extension.<br>
  <img src="https://github.com/victor-w-dev/kafka_streaming_crypto/blob/main/img/4_extension_ssh.PNG" width="45%" height="45%"><br>
- Use the SSH configuration to connect the Azure VM from VS Code.<br>
  - Press F1 to search "Remote-SSH: Open SSH Configuration File..."<br>
  <img src="https://github.com/victor-w-dev/kafka_streaming_crypto/blob/main/img/4_search_box.PNG" width="45%" height="45%"><br>
  <img src="https://github.com/victor-w-dev/kafka_streaming_crypto/blob/main/img/4_config_location.PNG" width="45%" height="45%"><br>
  - Edit SSH configuration (can get information from Azure VM Overview Page for Host: VM name, User name, HostName: VM IP address, IdentityFile: Public Key location)
  <img src="https://github.com/victor-w-dev/kafka_streaming_crypto/blob/main/img/4_config.PNG" width="45%" height="45%"><br>
- Connect the VM<br>
  <img src="https://github.com/victor-w-dev/kafka_streaming_crypto/blob/main/img/4_vm_connect.PNG" width="45%" height="45%"><br>
- After successful connection, can manipulate files in VS code Explorer<br>
  <img src="https://github.com/victor-w-dev/kafka_streaming_crypto/blob/main/img/4_connected_explorer.PNG" width="45%" height="45%"><br>
### 5) Kafka-Python Installation
- Wuth connection with VM, install the kafka-python library using pip via VS code terminal:
- ```pip install kafka-python```
### 6) Configuration in server.properties in the remote Kafka broker so that local computer consumer can connect from it:
- In the configuration file for each **broker**, need to adjust `advertised.listeners` and set it either to **DNS name** or **public IP address** of the server where broker is hosted.<br>
Examples<br>
```advertised.listeners=PLAINTEXT://hostname:9092```<br>
```advertised.listeners=PLAINTEXT://176.11.12.1:9092```<br>
- Here, just a single broker to demo<br>
  <img src="https://github.com/victor-w-dev/kafka_streaming_crypto/blob/main/img/6_server_properties.PNG" width="45%" height="45%"><br>
### 7) Remote kafka-python producer Setup: Bybit API Data Collection Script
- Make sure python package pybit (Bybit API) installed
- Write a Python script that interacts with the Bybit API to retrieve crypto data.
- This script will act as Kafka producer, publishing crypto data to a Kafka topic.
### 8) Local Consumer Setup:
- On the local computer, set up a Kafka consumer.
- Install the kafka-python library locally.
- Consume data from the same Kafka topic (“crypto-data-topic”) to receive the streaming data.
### 9) Running the Demo:
- start zookeeper on Azure VM
- start Kafka broker on Azure VM
- Start the Kafka producer script on Azure VM.
- Observe the data being published to the Kafka topic.
- Run the Kafka consumer script on local machine to consume the data.
