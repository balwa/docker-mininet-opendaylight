#!/usr/bin/env python3

"""
OpenDaylight Controller Interaction Module
Provides functionality to interact with the OpenDaylight controller's REST API
"""

import requests
import json
import time
import logging
from requests.auth import HTTPBasicAuth

class ODLController:
    """Interface for interacting with the OpenDaylight controller."""
    
    def __init__(self, ip='opendaylight', port=8181, username='admin', password='admin'):
        """Initialize the ODL controller interface with connection parameters."""
        self.base_url = f"http://{ip}:{port}/restconf"
        self.auth = HTTPBasicAuth(username, password)
        self.headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        }
        self.logger = self._setup_logger()
    
    def _setup_logger(self):
        """Set up logging for the ODL controller module."""
        logger = logging.getLogger('odl_controller')
        logger.setLevel(logging.INFO)
        
        # Create console handler
        ch = logging.StreamHandler()
        ch.setLevel(logging.INFO)
        
        # Create formatter
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        ch.setFormatter(formatter)
        
        # Add handler to logger
        logger.addHandler(ch)
        
        return logger
    
    def get_topology(self):
        """Retrieve the network topology from OpenDaylight."""
        url = f"{self.base_url}/operational/network-topology:network-topology"
        
        try:
            response = requests.get(url, auth=self.auth, headers=self.headers)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            self.logger.error(f"Failed to retrieve topology: {e}")
            return None
    
    def get_nodes(self):
        """Retrieve all OpenFlow nodes (switches) from OpenDaylight."""
        url = f"{self.base_url}/operational/opendaylight-inventory:nodes"
        
        try:
            response = requests.get(url, auth=self.auth, headers=self.headers)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            self.logger.error(f"Failed to retrieve nodes: {e}")
            return None
    
    def get_node_connectors(self, node_id):
        """Retrieve all connectors (ports) for a specific node."""
        url = f"{self.base_url}/operational/opendaylight-inventory:nodes/node/{node_id}"
        
        try:
            response = requests.get(url, auth=self.auth, headers=self.headers)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            self.logger.error(f"Failed to retrieve connectors for node {node_id}: {e}")
            return None
    
    def get_flows(self, node_id):
        """Retrieve all flow rules for a specific node."""
        url = f"{self.base_url}/operational/opendaylight-inventory:nodes/node/{node_id}/flow-node-inventory:table/0"
        
        try:
            response = requests.get(url, auth=self.auth, headers=self.headers)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            self.logger.error(f"Failed to retrieve flows for node {node_id}: {e}")
            return None
    
    def install_flow(self, node_id, flow_id, flow_body):
        """Install a flow rule on a specific node."""
        url = f"{self.base_url}/config/opendaylight-inventory:nodes/node/{node_id}/flow-node-inventory:table/0/flow/{flow_id}"
        
        try:
            response = requests.put(url, auth=self.auth, headers=self.headers, data=json.dumps(flow_body))
            response.raise_for_status()
            self.logger.info(f"Flow {flow_id} installed on node {node_id}")
            return True
        except requests.exceptions.RequestException as e:
            self.logger.error(f"Failed to install flow {flow_id} on node {node_id}: {e}")
            return False
    
    def delete_flow(self, node_id, flow_id):
        """Delete a flow rule from a specific node."""
        url = f"{self.base_url}/config/opendaylight-inventory:nodes/node/{node_id}/flow-node-inventory:table/0/flow/{flow_id}"
        
        try:
            response = requests.delete(url, auth=self.auth, headers=self.headers)
            response.raise_for_status()
            self.logger.info(f"Flow {flow_id} deleted from node {node_id}")
            return True
        except requests.exceptions.RequestException as e:
            self.logger.error(f"Failed to delete flow {flow_id} from node {node_id}: {e}")
            return False
    
    def get_node_statistics(self, node_id):
        """Retrieve statistics for a specific node."""
        url = f"{self.base_url}/operational/opendaylight-inventory:nodes/node/{node_id}/node-connector"
        
        try:
            response = requests.get(url, auth=self.auth, headers=self.headers)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            self.logger.error(f"Failed to retrieve statistics for node {node_id}: {e}")
            return None
    
    def create_shortest_path_flows(self, source_host, dest_host, path_preference='shortest'):
        """
        Create flow rules for the shortest path between hosts.
        
        Args:
            source_host: Source host IP or MAC
            dest_host: Destination host IP or MAC
            path_preference: 'shortest', 'least_hops', or 'highest_bandwidth'
        """
        # This would require topology analysis and path computation
        # Simplified implementation for educational purposes
        self.logger.info(f"Creating {path_preference} path flows from {source_host} to {dest_host}")
        
        # In a real implementation, this would:
        # 1. Get the complete topology
        # 2. Find the path according to preference
        # 3. Install appropriate flow rules on each switch along the path
        
        # For now, log that this is a placeholder
        self.logger.warning("This is a placeholder implementation. Actual path computation required.")
        return True
    
    def create_load_balanced_flows(self, source_ip, dest_ip, path_count=2):
        """
        Create flow rules to load balance traffic across multiple paths.
        
        Args:
            source_ip: Source IP address
            dest_ip: Destination IP address
            path_count: Number of paths to distribute traffic across
        """
        self.logger.info(f"Creating load-balanced flows from {source_ip} to {dest_ip} across {path_count} paths")
        
        # In a real implementation, this would:
        # 1. Find multiple paths between source and destination
        # 2. Install flow rules that hash traffic across these paths
        
        # For now, log that this is a placeholder
        self.logger.warning("This is a placeholder implementation. Actual multi-path routing required.")
        return True
    
    def wait_for_topology_discovery(self, timeout=30, poll_interval=2):
        """
        Wait for OpenDaylight to discover the complete topology.
        
        Args:
            timeout: Maximum time to wait in seconds
            poll_interval: Time between polls in seconds
            
        Returns:
            bool: True if discovery appears complete, False if timeout reached
        """
        self.logger.info(f"Waiting for topology discovery (timeout: {timeout}s)")
        
        start_time = time.time()
        while time.time() - start_time < timeout:
            # Get the current topology
            topology = self.get_topology()
            
            if not topology:
                self.logger.warning("Could not retrieve topology, retrying...")
                time.sleep(poll_interval)
                continue
                
            # Check if we have switches and links in the topology
            # This is a simplified check, a real implementation would be more sophisticated
            if 'network-topology' in topology and 'topology' in topology['network-topology']:
                for topo in topology['network-topology']['topology']:
                    if 'node' in topo and 'link' in topo:
                        if len(topo['node']) > 0 and len(topo['link']) > 0:
                            self.logger.info(f"Topology discovery complete. Found {len(topo['node'])} nodes and {len(topo['link'])} links.")
                            return True
                            
            self.logger.info("Topology discovery in progress...")
            time.sleep(poll_interval)
            
        self.logger.warning(f"Topology discovery timed out after {timeout}s")
        return False

def create_example_flow(match_ip='10.0.0.2', output_port=2):
    """
    Create an example flow rule to forward traffic to a specific IP address.
    
    Args:
        match_ip: IP address to match in flow rule
        output_port: Port to forward matching traffic to
        
    Returns:
        dict: Flow rule configuration in OpenDaylight format
    """
    flow = {
        "flow": [
            {
                "id": f"flow-to-{match_ip.replace('.', '-')}",
                "priority": 100,
                "table_id": 0,
                "match": {
                    "ethernet-match": {
                        "ethernet-type": {
                            "type": 2048  # IPv4
                        }
                    },
                    "ipv4-destination": f"{match_ip}/32"
                },
                "instructions": {
                    "instruction": [
                        {
                            "order": 0,
                            "apply-actions": {
                                "action": [
                                    {
                                        "order": 0,
                                        "output-action": {
                                            "output-node-connector": str(output_port)
                                        }
                                    }
                                ]
                            }
                        }
                    ]
                }
            }
        ]
    }
    
    return flow

def main():
    """Test the ODL Controller module functionality."""
    # Set up logging
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)
    
    # Create controller instance
    controller = ODLController()
    
    # Wait for topology discovery
    if controller.wait_for_topology_discovery():
        # Get and display topology information
        topology = controller.get_topology()
        if topology:
            logger.info("Retrieved topology successfully")
            
        # Get and display nodes
        nodes = controller.get_nodes()
        if nodes and 'nodes' in nodes and 'node' in nodes['nodes']:
            node_list = nodes['nodes']['node']
            logger.info(f"Found {len(node_list)} nodes")
            
            # For the first node, get connectors and flows
            if node_list:
                node_id = node_list[0]['id']
                logger.info(f"Getting details for node {node_id}")
                
                # Get connectors
                connectors = controller.get_node_connectors(node_id)
                if connectors:
                    logger.info(f"Retrieved connectors for node {node_id}")
                
                # Get flows
                flows = controller.get_flows(node_id)
                if flows:
                    logger.info(f"Retrieved flows for node {node_id}")
                
                # Install example flow
                example_flow = create_example_flow()
                result = controller.install_flow(node_id, example_flow['flow'][0]['id'], example_flow)
                if result:
                    logger.info("Example flow installed successfully")
                    
                    # Delete the flow
                    delete_result = controller.delete_flow(node_id, example_flow['flow'][0]['id'])
                    if delete_result:
                        logger.info("Example flow deleted successfully")
    else:
        logger.error("Topology discovery failed")
        
if __name__ == "__main__":
    main()
