# RoboCup Rescue Simulator(RCRS)-Gym Integration
 
(Linux) Instructions to download, build and run the RoboCup Rescue Simulator (RCRS) integrated with gym interface

## 1. Software Pre-Requisites

* Git
* Gradle 3.4+
* OpenJDK Java 8+
* Python 3.5+
* Openai Gym

## 2. Download project from GitHub

`$ git clone https://github.com/animeshgoyal9/RoboCup-Gym.git` 

## 3. Compile

Open two terminals

In the first terminal, navigate to the `rcrs-server` root directory and compile 

`$ ./gradlew clean`

`$ ./gradlew completeBuild`

In the second terminal, navigate to the `rcrs-adf-sample-master` root directory and compile 

`$ ./clean`

`$ ./compile.sh`

Close the second terminal

## 4. Execute

In the first terminal, navigate to the boot folder in  `rcrs-server-master` directory and run the following python file 

`$ testing.py`












