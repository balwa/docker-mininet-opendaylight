# SDN Traffic Engineering Lab

This project demonstrates Software-Defined Networking (SDN) concepts using Mininet and OpenDaylight. It focuses on traffic engineering, fault tolerance, and network visualization

## Overview

1. Create a virtual network topology with Mininet
2. Connect it to the OpenDaylight controller
3. Configure traffic engineering policies
4. Test network performance under different conditions
5. Visualize network statistics
6. Experiment with fault tolerance mechanisms

## Prerequisites

- Linux environment only amd64 supported
- docker compose
- matplotlib
- numpy
- requests

## Installation

### 1. Install Python dependencies

```bash
pip install matplotlib numpy requests
```

## Project Files

- `sdn_topology.py`: Main code that creates the network topology and connects to OpenDaylight
- `experiments.py`: Pre-defined experiments for students to run

## Usage

1. Start OpenDaylight and ensure it's running:
```bash
cd karaf-0.13.1
./bin/karaf
```

2. Run the main experiment:
```bash
python3 sdn_topology.py
```

## Network Topology

The project creates a custom network topology with:
- 7 OpenFlow switches (s1-s7)
- 4 hosts (h1-h4)
- Multiple paths between hosts with different bandwidth and latency characteristics:
  - Primary path: Lower capacity (5Mbps), low latency (5ms)
  - Secondary path: Higher capacity (20Mbps), higher latency (15ms)

## Lab Assignments

### Lab 1: Network Creation and Verification
- Create the topology and verify connectivity
- Observe how OpenDaylight discovers the network
- Use the ODL web interface to view the topology

### Lab 2: Performance Testing
- Run iperf tests between hosts
- Measure throughput and latency
- Observe flow rules installed by ODL

### Lab 3: Fault Tolerance
- Implement a link failure scenario
- Measure network convergence time
- Compare performance before and after failover

### Lab 4: Traffic Engineering
- Implement different QoS policies
- Configure path selection based on application requirements
- Visualize traffic patterns

## Advanced Topics

For courses covering advanced networking concepts:
- Implement security policies using OpenDaylight
- Create custom northbound applications
- Integrate with containerized applications
