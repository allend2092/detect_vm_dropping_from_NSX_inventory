# Read configuration from JSON file
# This configuration includes details like vCenter Server address and login credentials.
$config = Get-Content -Path 'config.json' | ConvertFrom-Json

# Connect to vCenter Server with the -Force parameter to bypass SSL certificate validation
# This is useful in environments where SSL certificates are self-signed or not properly configured.
try {
    Connect-VIServer -Server $config.vCenterServer -User $config.username -Password $config.password -Force
} catch {
    # If connection fails, write an error message and exit the script.
    Write-Error "Failed to connect to vCenter Server: $_"
    exit
}

# Import file nsx_esxi_host_list.json and dump entries into an array
# This file contains a list of ESXi host names managed by NSX.
$nsxHosts = Get-Content -Path 'nsx_esxi_host_list.json' | ConvertFrom-Json

# Initialize an array to hold all VMs
# This array will store VM objects fetched from each ESXi host.
$allVms = @()

# Cycle through the array with a for loop and run command to get VMs from each host
# This loop fetches VMs that are currently powered on from each listed ESXi host.
foreach ($hostName in $nsxHosts) {
    Write-Host $hostName
    $vms = Get-VMHost -Name $hostName | Get-VM | Where-Object { $_.PowerState -eq "PoweredOn" }
    Write-Host $vms
    $allVms += $vms
}

# Convert VM objects to a simple custom object and output to a JSON file
# This step simplifies the VM objects to include only their names.
$vmOutput = $allVms | Select-Object Name
$vmOutput | ConvertTo-Json | Set-Content -Path 'vcenter_view_vms_on_nsx_hosts.json'

# Disconnect from vCenter Server
# It's important to cleanly disconnect from the server after operations are complete.
Disconnect-VIServer -Server $config.vCenterServer -Confirm:$false

