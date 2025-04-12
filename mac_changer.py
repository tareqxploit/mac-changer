import subprocess
import optparse
import re

def get_arguments():
    parser = optparse.OptionParser()
    parser.add_option("-i", "--interface", dest="interface", help="Interface to change its MAC address")
    parser.add_option("-m", "--mac", dest="new_mac", help="New MAC address to assign")
    (options, arguments) = parser.parse_args()

    if not options.interface:
        parser.error("[-] Please specify the interface. Use --help for more info.")
    elif not options.new_mac:
        parser.error("[-] Please specify a new MAC address. Use --help for more info.")

    return options

def change_mac(interface, new_mac):
    print(f"[+] Changing MAC address for {interface} to {new_mac}")
    subprocess.run(["sudo", "ifconfig", interface, "down"])
    subprocess.run(["sudo", "ifconfig", interface, "hw", "ether", new_mac])
    subprocess.run(["sudo", "ifconfig", interface, "up"])

def get_current_mac(interface):
    try:
        ifconfig_result = subprocess.check_output(["ifconfig", interface]).decode()
        match = re.search(r'ether\s+([0-9a-f:]{17})', ifconfig_result)

        if match:
            return match.group(1)  # Only the MAC address
        else:
            print("[-] Could not read MAC address.")
            return None
    except subprocess.CalledProcessError:
        print(f"[-] Failed to run ifconfig on {interface}.")
        return None

# Main script
options = get_arguments()

# Get MAC before
old_mac = get_current_mac(options.interface)
print(f"[i] Current MAC before change: {old_mac}")

# Change it
change_mac(options.interface, options.new_mac)

# Get MAC after
new_mac = get_current_mac(options.interface)
print(f"[i] Current MAC after change: {new_mac}")

# Confirm change
if new_mac == options.new_mac:
    print("[+] MAC address was successfully changed!")
else:
    print("[-] MAC address change failed.")
