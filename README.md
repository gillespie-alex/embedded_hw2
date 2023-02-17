<!-- ABOUT THE PROJECT -->
## About The Project

This project is to design a software utility which can be invoked in two modes:
1. Inventory Mode to record all unique ID's of Controllers and Sensors and store to file
2. Polling Mode to continuously read sensor data and store to file for as long as utility running




<p align="right">(<a href="#readme-top">back to top</a>)</p>



### Built With


* Python 3.7

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- Why Python -->
## Why Python

Obviously Python is not the best language for low level performance, but was chosen mainly because:
* Given time constraints I wanted to create a verifiable and testable model quickly, which could then be taken to build in a more low level performance optimized language
* Along with this, some unit testing I performed is extremely easy with pytest in Python

<!-- GETTING STARTED -->
## Getting Started

The only non standard library used is Pytest, which would need to be installed. But, this is
not necessary to run the core program. This is only used for some unit tests within the Sensor.py
module if one wants to play around with them.

### Prerequisites

* Python3
  ```sh
  # windows users:
  Download py3 executable and run
  # Windows/Linux users:
  python --version
  # Anything over 3.7 will work
  ```
* pytest
  ```sh
  # Windows/Linux users:
  pip install -U pytest
  ```





### Installation

_Steps before running python script_

1. Unzip the repo 
   
2. Change Directories into 'CPU_dir'

3. Open python CPU.py file and change lines 6 & 7 to the relative paths on your local computer
   ```py
   # Windows users must use double backslash between directories
   sys.path.insert(0, 'C:\\Users\\path_to_file\\embedded_hw2\\Sensor_dir')
   sys.path.insert(0, 'C:\\Users\\path_to_file\\embedded_hw2\\Sensor_dir')
   
   # Linux
   sys.path.insert(0, '~/path_to_file/embedded_hw2_Sensor_dir')
   sys.path.insert(0, '~/path_to_file/embedded_hw2_Sensor_dir')
   ```
   
   
5. Lauch python file with
   ```sh
   python run.py
   ```
   
6. Stop .py file ^C and all output is stored in inventory.txt and logs.txt

### Resources
* https://jenkov.com/tutorials/java-concurrency/producer-consumer.html#:~:text=The%20producer%20consumer%20pattern%20is,that%20needs%20to%20be%20done.
* https://pages.cs.wisc.edu/~remzi/OSTEP/cpu-sched.pdf (pg. 7)
* https://docs.pytest.org/en/7.1.x/contents.html
   

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- USAGE EXAMPLES
## Usage

Use this space to show useful examples of how a project can be used. Additional screenshots, code examples and demos work well in this space. You may also link to more resources.

_For more examples, please refer to the [Documentation](https://example.com)_

<p align="right">(<a href="#readme-top">back to top</a>)</p>
--> 

