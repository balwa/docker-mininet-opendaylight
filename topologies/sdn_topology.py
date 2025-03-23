#!/usr/bin/env python3

"""
SDN Traffic Engineering Lab
Custom topology with Mininet and OpenDaylight integration
"""

from mininet.net import Mininet
from mininet.node import Controller, RemoteController, OVSKernelSwitch
from mininet.cli import CLI
from mininet.log import setLogLevel, info
from mininet.link import TCLink
import time
import requests
import json
import matplotlib.pyplot as plt
import numpy as np
import threading
import os

class SDNTopology:
    """Creates and manages a software-defined network topology with OpenDaylight integration."""
    
    def __init__(self, controller_ip='192.168.10.64', controller_port=6633):
        self.controller_ip = controller_ip
        self.controller_port = controller_port
        self.net = None
        self.switches = []
        self.hosts = []
        self.stats = {'bandwidth': [], 'latency': [], 'timestamp': []}
        self.odl_base_url = f"http://{controller_ip}:8181/restconf"
        self.odl_auth = ('admin', 'admin')  # Default ODL credentials
        self.measurement_running = False
        
    def build_topology(self):
        """Builds a custom network topology with multiple paths between hosts."""
        
        # Create Mininet with remote controller
        self.net = Mininet(
            controller=RemoteController,
            switch=OVSKernelSwitch,
            link=TCLink,
            autoSetMacs=True
        )
        
        # Add controller
        c0 = self.net.addController(
            'c0', 
            controller=RemoteController,
            ip=self.controller_ip,
            port=self.controller_port
        )
        
        # Create switches
        for i in range(1, 8):
            switch = self.net.addSwitch(f's{i}')
            self.switches.append(switch)
            
        # Create hosts (one per edge switch)
        h1 = self.net.addHost('h1', ip='10.0.0.1/24')
        h2 = self.net.addHost('h2', ip='10.0.0.2/24')
        h3 = self.net.addHost('h3', ip='10.0.0.3/24')
        h4 = self.net.addHost('h4', ip='10.0.0.4/24')
        
        self.hosts = [h1, h2, h3, h4]
        
        # Connect hosts to edge switches
        self.net.addLink(h1, self.switches[0], bw=10)  # 10 Mbps links to hosts
        self.net.addLink(h2, self.switches[3], bw=10)
        self.net.addLink(h3, self.switches[4], bw=10)
        self.net.addLink(h4, self.switches[6], bw=10)
        
        # Create network core with redundant paths
        # Primary path (low capacity, low latency)
        self.net.addLink(self.switches[0], self.switches[1], bw=5, delay='5ms')
        self.net.addLink(self.switches[1], self.switches[3], bw=5, delay='5ms')
        
        # Secondary path (high capacity, higher latency)
        self.net.addLink(self.switches[0], self.switches[2], bw=20, delay='15ms')
        self.net.addLink(self.switches[2], self.switches[3], bw=20, delay='15ms')
        
        # Additional links
        self.net.addLink(self.switches[1], self.switches[4], bw=10, delay='10ms')
        self.net.addLink(self.switches[2], self.switches[5], bw=10, delay='10ms')
        self.net.addLink(self.switches[4], self.switches[6], bw=8, delay='8ms')
        self.net.addLink(self.switches[5], self.switches[6], bw=8, delay='8ms')
        
        # Start the network
        self.net.build()
        c0.start()
        for switch in self.switches:
            switch.start([c0])
        
        info('*** Network is running\n')
        
    def start_network(self):
        """Start the Mininet network."""
        if not self.net:
            self.build_topology()
        
        self.net.start()
        
        # Wait for OpenDaylight to discover the topology
        info('*** Waiting for OpenDaylight to discover the topology...\n')
        time.sleep(15)
        
    def configure_odl_flow_rules(self, path='primary'):
        """Configure flow rules in OpenDaylight to control traffic paths."""
        
        info(f'*** Configuring {path} path flow rules in OpenDaylight\n')
        
        # In a real implementation, this would use OpenDaylight's REST API
        # to install flow rules directing traffic along specific paths
        
        if path == 'primary':
            # Primary path: s1 -> s2 -> s4
            self._install_path_flow(0, 1, 3, '10.0.0.2')
        elif path == 'secondary':
            # Secondary path: s1 -> s3 -> s4
            self._install_path_flow(0, 2, 3, '10.0.0.2')
        elif path == 'balanced':
            # Install load balancing flow rules
            # (This is a simplified version; a real implementation would be more complex)
            self._install_balanced_flows()
            
        info('*** Flow rules installed\n')
        
    def _install_path_flow(self, src_sw, mid_sw, dst_sw, dst_ip):
        """Helper method to install flow rules for a specific path."""
        
        # For educational purposes, this is a simplified version
        # In production, you would use actual node IDs from OpenDaylight
        
        headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        }
        
        # Example flow rule for the first hop
        flow_rule = {
            "flow": [{
                "id": f"flow-{src_sw}-to-{mid_sw}",
                "match": {
                    "ethernet-match": {
                        "ethernet-type": {"type": "2048"}  # IPv4
                    },
                    "ipv4-destination": f"{dst_ip}/32"
                },
                "instructions": {
                    "instruction": [{
                        "order": 0,
                        "apply-actions": {
                            "action": [{
                                "output-action": {
                                    "output-node-connector": f"{mid_sw+1}"  # Simplified port numbering
                                },
                                "order": 0
                            }]
                        }
                    }]
                }
            }]
        }
        
        # This is a placeholder. In a real implementation, you would:
        # 1. Get the actual node IDs from OpenDaylight
        # 2. Install the proper flow rules using OpenDaylight's REST API
        # Example request (commented out as it won't work without actual IDs):
        # requests.put(
        #     f"{self.odl_base_url}/config/opendaylight-inventory:nodes/node/openflow:{src_sw+1}/flow-node-inventory:table/0/flow/flow-{src_sw}-to-{mid_sw}",
        #     auth=self.odl_auth,
        #     headers=headers,
        #     data=json.dumps(flow_rule)
        # )
        
        # Similarly for the second hop (mid_sw to dst_sw)
        
    def _install_balanced_flows(self):
        """Install load balancing flow rules."""
        # In a real implementation, this would install flow rules that split traffic
        # between multiple paths based on source/destination IP, ports, or other criteria
        pass
        
    def run_iperf_test(self, h1_name='h1', h2_name='h2', duration=10):
        """Run an iperf test between two hosts."""
        
        h1 = self.net.get(h1_name)
        h2 = self.net.get(h2_name)
        
        # Start iperf server on h2
        h2.cmd(f'iperf -s -p 5001 &')
        
        # Wait for server to start
        time.sleep(1)
        
        # Run iperf client on h1
        info(f'*** Running iperf test from {h1_name} to {h2_name} for {duration} seconds\n')
        result = h1.cmd(f'iperf -c {h2.IP()} -t {duration} -i 1')
        
        # Stop the server
        h2.cmd('kill %iperf')
        
        info('*** Iperf test completed\n')
        info(result)
        
        return result
    
    def start_measurement(self, interval=1.0):
        """Start collecting network measurements."""
        self.measurement_running = True
        self.measurement_thread = threading.Thread(target=self._collect_measurements, args=(interval,))
        self.measurement_thread.daemon = True
        self.measurement_thread.start()
        
    def stop_measurement(self):
        """Stop collecting network measurements."""
        self.measurement_running = False
        if hasattr(self, 'measurement_thread'):
            self.measurement_thread.join(timeout=2)
            
    def _collect_measurements(self, interval):
        """Collect network measurements periodically."""
        while self.measurement_running:
            timestamp = time.time()
            
            # Collect bandwidth measurements from switches
            bw_utilization = self._get_port_stats()
            
            # Collect latency measurements between hosts
            latency = self._measure_latency()
            
            # Store measurements
            self.stats['timestamp'].append(timestamp)
            self.stats['bandwidth'].append(bw_utilization)
            self.stats['latency'].append(latency)
            
            time.sleep(interval)
            
    def _get_port_stats(self):
        """Get port statistics from switches via OpenDaylight."""
        # In a real implementation, this would query OpenDaylight's REST API for port statistics
        # For educational purposes, we return a simulated value
        return np.random.uniform(1, 10)  # Simulated bandwidth in Mbps
    
    def _measure_latency(self):
        """Measure latency between hosts."""
        # In a real implementation, this would use ping to measure actual latency
        # For educational purposes, we return a simulated value
        return np.random.uniform(5, 30)  # Simulated latency in ms
            
    def plot_measurements(self):
        """Plot collected network measurements."""
        if not self.stats['timestamp']:
            info('*** No measurement data to plot\n')
            return
            
        # Convert timestamps to relative time
        start_time = self.stats['timestamp'][0]
        rel_time = [t - start_time for t in self.stats['timestamp']]
        
        plt.figure(figsize=(12, 6))
        
        # Plot bandwidth
        plt.subplot(1, 2, 1)
        plt.plot(rel_time, self.stats['bandwidth'], 'b-')
        plt.xlabel('Time (s)')
        plt.ylabel('Bandwidth (Mbps)')
        plt.title('Bandwidth Utilization')
        
        # Plot latency
        plt.subplot(1, 2, 2)
        plt.plot(rel_time, self.stats['latency'], 'r-')
        plt.xlabel('Time (s)')
        plt.ylabel('Latency (ms)')
        plt.title('Network Latency')
        
        # Save the figure
        plt.tight_layout()
        plt.savefig('network_measurements.png')
        info('*** Measurements plotted and saved to network_measurements.png\n')
        
    def simulate_link_failure(self, src_switch, dst_switch):
        """Simulate a link failure between two switches."""
        if not self.net:
            info('*** Network not running\n')
            return
            
        src = self.switches[src_switch]
        dst = self.switches[dst_switch]
        
        # Find the link between the switches
        for link in self.net.links:
            if (link.intf1.node == src and link.intf2.node == dst) or \
               (link.intf1.node == dst and link.intf2.node == src):
                # Bring the link down
                info(f'*** Simulating link failure between {src.name} and {dst.name}\n')
                src.cmd(f'ifconfig {link.intf1.name} down')
                dst.cmd(f'ifconfig {link.intf2.name} down')
                return
                
        info(f'*** No link found between {src_switch} and {dst_switch}\n')
        
    def restore_link(self, src_switch, dst_switch):
        """Restore a previously failed link between two switches."""
        if not self.net:
            info('*** Network not running\n')
            return
            
        src = self.switches[src_switch]
        dst = self.switches[dst_switch]
        
        # Find the link between the switches
        for link in self.net.links:
            if (link.intf1.node == src and link.intf2.node == dst) or \
               (link.intf1.node == dst and link.intf2.node == src):
                # Bring the link up
                info(f'*** Restoring link between {src.name} and {dst.name}\n')
                src.cmd(f'ifconfig {link.intf1.name} up')
                dst.cmd(f'ifconfig {link.intf2.name} up')
                return
                
        info(f'*** No link found between {src_switch} and {dst_switch}\n')
        
    def run_cli(self):
        """Run Mininet CLI."""
        CLI(self.net)
        
    def stop_network(self):
        """Stop the Mininet network."""
        if self.net:
            info('*** Stopping network\n')
            self.net.stop()
            self.net = None
            
def run_experiment():
    """Run a complete experiment demonstrating traffic engineering with ODL."""
    
    setLogLevel('info')
    
    # Create and start the network
    topo = SDNTopology()
    topo.start_network()
    
    try:
        # Configure the primary path
        topo.configure_odl_flow_rules('primary')
        
        # Start measurements
        topo.start_measurement()
        
        # Run a baseline performance test
        info('*** Running baseline performance test\n')
        topo.run_iperf_test('h1', 'h2', duration=10)
        
        # Simulate a link failure on the primary path
        info('*** Simulating link failure on primary path\n')
        topo.simulate_link_failure(0, 1)  # s1-s2 link
        
        # Wait for the controller to detect and react to the failure
        time.sleep(10)
        
        # Run another performance test to verify failover
        info('*** Running performance test after link failure\n')
        topo.run_iperf_test('h1', 'h2', duration=10)
        
        # Restore the link
        topo.restore_link(0, 1)
        
        # Configure load balancing
        topo.configure_odl_flow_rules('balanced')
        
        # Run a final performance test with load balancing
        info('*** Running performance test with load balancing\n')
        topo.run_iperf_test('h1', 'h2', duration=10)
        
        # Stop measurements and plot results
        topo.stop_measurement()
        topo.plot_measurements()
        
        # Allow interactive experimentation
        info('*** Experiment completed. Starting CLI for interactive use.\n')
        topo.run_cli()
        
    finally:
        # Clean up
        topo.stop_network()

if __name__ == '__main__':
    # Run the experiment
    run_experiment()
