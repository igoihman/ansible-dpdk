#!/usr/bin/python
import subprocess


class FilterModule(object):
    def filters(self):
        return {
            'get_pci_addresses': self.get_pci_addresses,
            'get_cpu_list': self.get_cpu_list
        }

    def _get_pci_address(self, nic):
        cat_proc = subprocess.Popen(
            "cat /sys/class/net/{}/device/uevent".format(nic).split(),
            stdout=subprocess.PIPE)
        grep_proc = subprocess.Popen("grep PCI_SLOT_NAME ".split(),
                                     stdin=cat_proc.stdout,
                                     stdout=subprocess.PIPE)
        cut_proc = subprocess.Popen(" cut -d= -f2".split(),
                                    stdin=grep_proc.stdout,
                                    stdout=subprocess.PIPE)
        output, error = cut_proc.communicate()
        return output

    def _get_nic_cpu_list(self, nic):
        cmd = "cat /sys/class/net/{}/device/local_cpulist".format(nic)
        proc = subprocess.Popen(cmd.split(), stdout=subprocess.PIPE)
        output, error = proc.communicate()
        return output

    def _is_first_core_zero(self, cores):
        return cores[:1] == '0'

    def _remove_first_core(self, cores):
        if cores[1] == '-':
            return '1' + cores[1:]
        elif cores[1] == ',':
            return cores[2:]
        else:
            return ""

    def get_cpu_list(self, nics):
        cores = []
        for nic in nics:
            local_cpu_list = self._get_nic_cpu_list(nic)
            if self._is_first_core_zero(local_cpu_list):
                local_cpu_list = self._remove_first_core(local_cpu_list)
            if local_cpu_list not in cores:
                cores.append(local_cpu_list)
        return ','.join(cores)

    def get_pci_addresses(self, nics):
        pci_addresses = []
        for nic in nics:
            pci_addresses.append(self._get_pci_address(nic))
        return pci_addresses
