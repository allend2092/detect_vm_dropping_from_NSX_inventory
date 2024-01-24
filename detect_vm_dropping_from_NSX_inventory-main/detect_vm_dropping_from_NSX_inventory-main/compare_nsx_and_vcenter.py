import json

# Function to read a JSON file and return its contents.
def read_json_file(file_path):
    with open(file_path, 'r') as file:
        return json.load(file)

# Function to extract VM names from NSX view data.
# The data is expected to be a list of VM names.
def extract_names_from_nsx_view(data):
    return set(data)  # Convert the list to a set for efficient comparison.

# Function to extract VM names from vCenter view data.
# The data is expected to be a list of dictionaries with 'Name' as a key.
def extract_names_from_vcenter_view(data):
    return set(vm['Name'] for vm in data)  # Extract 'Name' from each dictionary and convert to a set.

# Function to write data to a JSON file.
def write_to_json_file(data, file_path):
    with open(file_path, 'w') as file:
        json.dump(data, file, indent=4)  # Write data to file with pretty formatting.

# Main function to execute the script.
def main():
    # Read NSX and vCenter data from their respective JSON files.
    nsx_data = read_json_file('nsx_view_vms_on_nsx_hosts.json')
    vcenter_data = read_json_file('vcenter_view_vms_on_nsx_hosts.json')

    # Extract VM names from both NSX and vCenter data.
    nsx_vm_names = extract_names_from_nsx_view(nsx_data)
    vcenter_vm_names = extract_names_from_vcenter_view(vcenter_data)

    # Find differences between the two sets of VM names.
    diff_nsx_not_in_vcenter = nsx_vm_names - vcenter_vm_names  # VMs in NSX view but not in vCenter view.
    diff_vcenter_not_in_nsx = vcenter_vm_names - nsx_vm_names  # VMs in vCenter view but not in NSX view.

    # Prepare data for JSON output.
    output_data = {
        "VMs_in_NSX_view_but_not_in_vCenter_view": list(diff_nsx_not_in_vcenter),
        "VMs_in_vCenter_view_but_not_in_NSX_view": list(diff_vcenter_not_in_nsx)
    }

    # Write the differences to a JSON file.
    write_to_json_file(output_data, 'vcenter_diff_and_nsx_diff.json')

    print("Differences written to 'vcenter_diff_and_nsx_diff.json'")

# Entry point of the script.
if __name__ == '__main__':
    main()
