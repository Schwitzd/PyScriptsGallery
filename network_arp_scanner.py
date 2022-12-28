import argparse
from scapy.all import srp, Ether, ARP


def get_arguments():
    """Get all arguments"""
    parser = argparse.ArgumentParser()
    parser.add_argument('-t', '--target', dest='target', help='Target IP/ IP Range')
    args = parser.parse_args()
    return args


def scan(ip):
    """Scan ip subnet"""
    arp_request = ARP(pdst=ip)
    broadcast = Ether(dst='ff:ff:ff:ff:ff:ff')
    arp_request_broadcast = broadcast / arp_request
    answered_list = srp(arp_request_broadcast, timeout=1, verbose=False)[0]

    clients_list= []
    for element in answered_list:
        client_dict ={'ip': element[1].psrc, 'mac': element[1].hwsrc}
        clients_list.append(client_dict)

    return clients_list


def print_result(results_list):
    """Print results"""
    print("IP\t\t\tMAC Address\n-------------------------------------------------------")
    for client in results_list:
        print(client['ip'] + "\t\t" + client['mac'])


if __name__ == '__main__':
    args = get_arguments()
    scan_result = scan(args.target)
    print_result(scan_result)
