# brain_pycore

[![Main - Page](https://img.shields.io/badge/Project-Zakhar%20the%20Robot-yellow)](https://zakhar-the-robot.github.io/doc/ "See the Project Main Page") [![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

Base python package for the Zakhar project.

## Content

The package consists of 6 main submodules:

- `dev` - Zakhar device descriptors
- `helpers` - format functions and other helpers
- `ros` - ROS convenience methods
- `zmq` - `ZmqClientThread`, `ZmqPublisherThread`, `ZmqServerThread`, `ZmqSubscriberThread`
- `logging` - global log (`logging.log`) and formatted local logs (`logging.new_logger`)
- `thread` - a stoppable extension of threading.Thread


## Installation

``` bash
pip install git+https://github.com/Zakhar-the-Robot/brain_pycore
```

## For Developers

From GitHub for a specific branch:

```bash
pip install git+https://github.com/Zakhar-the-Robot/brain_pycore@branch_name
```
