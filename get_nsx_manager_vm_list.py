import json
import requests
import configparser
import warnings
import logging

# Suppress warnings related to unverified HTTPS requests.
# This is often necessary when dealing with self-signed certificates in development environments.
warnings.simplefilter('ignore', category=requests.packages.urllib3.exceptions.InsecureRequestWarning)

# Configure logging to display messages with timestamps and severity levels.
# This is useful for debugging and tracking the script's execution.
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Load NSX Manager credentials and URL from a configuration file.
# This approach keeps sensitive data like usernames and passwords out of the script.
config = configparser.ConfigParser()
config.read('config_nsx.ini')
username = config['NSXmanager']['username']
password = config['NSXmanager']['password']
fqdn = config['NSXmanager']['fqdn']

def fetch_nsx_vm_data(fqdn):
    # Base URL for the NSX Manager API endpoint to fetch virtual machine data.
    base_url = f"https://{fqdn}/api/v1/fabric/virtual-machines"
    all_vms = []  # List to store all fetched VM data.
    cursor = None  # Cursor for handling pagination.

    while True:
        # Construct the URL with the cursor parameter for pagination.
        url = base_url + (f"?cursor={cursor}" if cursor else "")
        response = requests.get(url, auth=(username, password), verify=False)

        # Check if the response is successful (HTTP status code 200).
        if response.status_code == 200:
            data = response.json()
            all_vms.extend(data['results'])  # Add the VM data to the all_vms list.

            # Update the cursor for the next page of data.
            cursor = data.get('cursor')
            if not cursor:
                break  # Exit the loop if there are no more pages.
        else:
            # Raise an exception if the API call fails.
            raise Exception(f"Failed to fetch VM data from NSX Manager: {response.status_code}")

    return all_vms

def read_esxi_host_list():
    # Read the list of ESXi hosts from a JSON file.
    with open('nsx_esxi_host_list.json', 'r') as file:
        return json.load(file)

def main():
    try:
        # Fetch VM data from NSX Manager.
        vm_data = fetch_nsx_vm_data(fqdn)
        # Read the list of ESXi hosts for filtering.
        esxi_hosts = read_esxi_host_list()

        # Filter VMs based on whether they are running on the specified ESXi hosts and are in the 'VM_RUNNING' power state.
        filtered_vms = [vm['display_name'] for vm in vm_data if vm['source']['target_display_name'] in esxi_hosts and vm['power_state'] == "VM_RUNNING"]

        # Write the filtered list of VMs to a JSON file.
        with open('nsx_view_vms_on_nsx_hosts.json', 'w') as file:
            json.dump(filtered_vms, file, indent=4)

        print("Filtered VMs written to 'nsx_view_vms_on_nsx_hosts.json'")

    except Exception as e:
        # Print any errors that occur during the script's execution.
        print(f"Error: {e}")

if __name__ == '__main__':
    main()
