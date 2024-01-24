# NSX-VCenter Inventory Synchronization Checker

## Overview
This repository contains a set of scripts designed to identify virtual machines (VMs) that are impacted by inventory synchronization issues between NSX Manager and vCenter. The scripts collectively work to compare the list of VMs from both NSX Manager and vCenter, highlighting discrepancies that might indicate synchronization problems.

## Workflow
The project consists of several scripts that are executed in a specific order to produce the final output. The flow is as follows:

1. **get_transport_nodes.py**
   - **Purpose**: Fetches a list of ESXi hosts managed by NSX.
   - **Output**: `nsx_esxi_host_list.json` (List of ESXi hosts)

2. **get_nsx_manager_vm_list.py** and **make_vm_list_vcenter.ps1**
   - **Purpose**: 
     - `get_nsx_manager_vm_list.py`: Fetches the list of VMs from NSX Manager.
     - `make_vm_list_vcenter.ps1`: Fetches the list of VMs from vCenter.
   - **Output**: 
     - `nsx_view_vms_on_nsx_hosts.json` (List of VMs from NSX view)
     - `vcenter_view_vms_on_nsx_hosts.json` (List of VMs from vCenter view)

3. **compare_nsx_and_vcenter.py**
   - **Purpose**: Compares the VM lists from NSX and vCenter to find differences.
   - **Output**: `vcenter_diff_and_nsx_diff.json` (List of VMs present in one view but not the other)

## Usage
To use these scripts, follow the steps in the order mentioned above. Ensure that the necessary configuration files (`config_nsx.ini` and `config.json`) are properly set up with the correct credentials and URLs for NSX Manager and vCenter.

1. Run `get_transport_nodes.py` to generate `nsx_esxi_host_list.json`.
2. Use `nsx_esxi_host_list.json` as input for `get_nsx_manager_vm_list.py` and `make_vm_list_vcenter.ps1`.
3. Finally, run `compare_nsx_and_vcenter.py` to produce the `vcenter_diff_and_nsx_diff.json` file, which contains the differences between the NSX and vCenter VM lists.

## Requirements
- Python 3.x
- PowerShell (for `make_vm_list_vcenter.ps1`)
- Access to NSX Manager and vCenter with appropriate credentials.

## Configuration
Ensure that `config_nsx.ini` and `config.json` are configured with the correct NSX Manager and vCenter details, respectively. These files should contain the necessary URLs, usernames, and passwords.

## Contributing
Contributions to this project are welcome. Please ensure that any pull requests or issues are descriptive and relevant to the project's goals.

## Contact
daryl.allen@sscinc.com
