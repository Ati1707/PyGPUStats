# PyGPUStats

[![License](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)

A Python library for easy retrieval and monitoring of NVIDIA GPU statistics using `nvidia-smi`.

## Features

- Retrieve comprehensive GPU statistics including:
  - Temperature
  - Memory usage (used/free/total)
  - GPU utilization
  - Power consumption
  - Fan speed
  - Power limits
- Multiple access patterns:
  - Get all GPUs
  - Get first GPU
  - Get specific number of GPUs
  - Get GPU by ID
- Automatic data refresh on each request

## Requirements
- NVIDIA GPU with appropriate drivers installed
- `nvidia-smi` executable available in system PATH

## Usage

```python
from gpu_stats import GPUStats

stats = GPUStats()

# Get all GPUs
all_gpus = stats.get_all_gpus()

# Get first GPU
first_gpu = stats.get_first_gpu()

# Get specific GPU by ID
gpu_0 = stats.get_gpu_by_id(0)

# Print formatted output
stats.get_clean_output()
```
## Example Output with get_clean_output()
```python
GPU 0: NVIDIA GeForce RTX 3080
  Temperature: 72°C
  Memory: 8192/10240 MiB
  Utilization: 45%
  Power: 220/250W
```
