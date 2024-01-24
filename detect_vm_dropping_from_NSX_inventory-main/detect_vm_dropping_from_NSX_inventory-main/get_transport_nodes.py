import json
import requests
import configparser
import warnings
import logging

# Suppress warnings related to unverified HTTPS requests.
# This is common when dealing with self-signed certificates in development environments.
warnings.simplefilter('ignore', category=requests.packages.urllib3.exceptions.InsecureRequestWarning)

# Configure logging to display messages with timestamps and severity levels.
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Load NSX Manager credentials and URL from a configuration file.
# This approach keeps sensitive data out of the script itself.
config = configparser.ConfigParser()
config.read('config_nsx.ini')
username = config['NSXmanager']['username']
password = config['NSXmanager']['password']
fqdn = config['NSXmanager']['fqdn']

def get_transport_nodes():
    # Construct the API endpoint URL.
    url = f"https://{fqdn}/api/v1/transport-nodes"

    # Make an HTTPS GET request to the NSX Manager API.
    # Authentication is handled via HTTP Basic Auth.
    response = requests.get(url, auth=(username, password), verify=False)

    # Parse the JSON response into a Python dictionary.
    transport_nodes = response.json()

    # Initialize a list to hold the names of ESXi hosts.
    esxi_hosts = []

    # Iterate over the transport nodes and extract the display names of ESXi hosts.
    for node in transport_nodes.get('results', []):
        node_deployment_info = node.get('node_deployment_info', {})
        if node_deployment_info.get('resource_type') == 'HostNode':
            esxi_hosts.append(node.get('display_name'))

    return esxi_hosts

def write_to_json(data, filename):
    """Write the given data to a JSON file."""
    # Open the file in write mode and dump the data as JSON.
    with open(filename, 'w') as file:
        json.dump(data, file, indent=4)

def main():
    # Fetch the list of ESXi hosts from the NSX Manager.
    esxi_hosts = get_transport_nodes()

    # Log the list of hosts.
    logging.info(f"ESXi Hosts with NSX: {esxi_hosts}")

    # Write the list of hosts to a JSON file.
    write_to_json(esxi_hosts, 'nsx_esxi_host_list.json')

if __name__ == '__main__':
    main()
