import time

from com.vmware.vcenter_client import Datacenter, Folder, Network


def get_network_backing(client,
                        porggroup_name,
                        datacenter_name,
                        portgroup_type):
    """
    Gets a standard portgroup network backing for a given Datacenter
    Note: The method assumes that there is only one standard portgroup
    and datacenter with the mentioned names.
    """
    datacenter = get_datacenter(client, datacenter_name)
    if not datacenter:
        print("Datacenter '{}' not found".format(datacenter_name))
        return None

    filter = Network.FilterSpec(datacenters=set([datacenter]),
                                names=set([porggroup_name]),
                                types=set([portgroup_type]))
    network_summaries = client.vcenter.Network.list(filter=filter)

    if len(network_summaries) > 0:
        network = network_summaries[0].network
        print("Selecting {} Portgroup Network '{}' ({})".
              format(portgroup_type, porggroup_name, network))
        return network
    else:
        print("Portgroup Network not found in Datacenter '{}'".
              format(datacenter_name))
        return None


def wait_for_guest_power_state(vsphere_client, vmId, desiredState, timeout):
    """
    Waits for the guest to reach the desired power state, or times out.
    """
    print("Waiting for guest power state {}".format(desiredState))
    start = time.time()
    timeout = start + timeout
    while timeout > time.time():
        time.sleep(1)
        curState = vsphere_client.vcenter.vm_settings.guest.Power.get(vmId).state
        if desiredState == curState:
            break
    if desiredState != curState:
        raise AssertionError('Timed out waiting for guest to reach desired power state')
    else:
        AssertionError(f'Took {time.time() - start} seconds for guest power state to change to {desiredState}')


def wait_for_power_operations_state(vsphere_client, vmId, desiredState, timeout):
    """
    Waits for the desired soft power operations state, or times out.
    """
    print('Waiting for guest power operations to be {}'.format(desiredState))
    start = time.time()
    timeout = start + timeout
    while timeout > time.time():
        time.sleep(1)
        curState = vsphere_client.vcenter.vm_settings.guest.Power.get(vmId).operations_ready
        if desiredState == curState:
            break
    if desiredState != curState:
        raise AssertionError('Timed out waiting for guest to reach desired operations ready state')
    else:
        AssertionError(
            f'Took {time.time() - start} seconds for guest operations ready state to change to {desiredState}')


def get_datacenter(client, datacenter_name):
    """
    Returns the identifier of a datacenter
    Note: The method assumes only one datacenter with the mentioned name.
    """

    filter_spec = Datacenter.FilterSpec(names=set([datacenter_name]))

    datacenter_summaries = client.vcenter.Datacenter.list(filter_spec)
    if len(datacenter_summaries) > 0:
        datacenter = datacenter_summaries[0].datacenter
        return datacenter
    else:
        return None


def get_folder(client, datacenter_name, folder_name):
    """
    Returns the identifier of a folder
    Note: The method assumes that there is only one folder and datacenter
    with the mentioned names.
    """
    datacenter = get_datacenter(client, datacenter_name)
    if not datacenter:
        print("Datacenter '{}' not found".format(datacenter_name))
        return None

    filter_spec = Folder.FilterSpec(type=Folder.Type.VIRTUAL_MACHINE,
                                    names=set([folder_name]),
                                    datacenters=set([datacenter]))

    folder_summaries = client.vcenter.Folder.list(filter_spec)
    if len(folder_summaries) > 0:
        folder = folder_summaries[0].folder
        print("Detected folder '{}' as {}".format(folder_name, folder))
        return folder
    else:
        print("Folder '{}' not found".format(folder_name))
        return None