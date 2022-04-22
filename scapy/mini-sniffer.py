import scapy.all
import scapy.packet


MENU = """
[#] Choose an option [#]

1. Sniff
2. Analyze
3. Get Certificate
4. List Network Interfaces
5. Exit

[>] Pick: """


def analyze(capture: scapy.plist.PacketList) -> None:
    """
    Function that acts a client for the analysis
    """
    summary = f"""[#] Details [#]

    Packets: {len(capture)}
    Data: {''}

    Enter `-1` as an index to quit
    """

    print(summary)
    packet_index = input("[+] Pick a packet (index): ")
    while packet_index != "-1":
        try:
            packet_index = int(packet_index)
        except ValueError:
            print("[!] ERROR: packet (index) must be an integer (number) [!]")

        if isinstance(packet_index, int):
            if packet_index in range(1, len(capture) + 1):
                print(scapy.all.ls(capture[packet_index]))
            elif packet_index != "-1":
                print(f"[!] ERROR: There is no such packet index `{packet_index}` [!]\n\
                    [#] The range is 1-f{len(capture)} [#]")

        packet_index = input("[+] Pick a packet (index): ")


    return


def main():
    print("[*] Welcome to miniScapy.proj [*]")
    option = input(MENU)
    capture = None

    while option != '5':
        if option == '1':
            counter = input("[+] How many packets do you wish to capture? ")
            filter_args = input("[+] Enter filter arguments (default: all): ")
            iface = input("[+] Choose a network interface (defualt: all): ")
            
            if filter_args == "all": filter_args = ''
            if iface == "all": iface = ''

            print("[#] Initailize packet sniffing [#]\n")
            try:
                capture = scapy.all.sniff(
                        iface=iface,
                        filter=filter_args,
                        count=int(counter),
                        prn=lambda data: data.summary()
                    )
            except OSError as e:
                print(f"[!] ERROR: {e.args[0].decode()} [!]")
            except ValueError as e:
                print(f"[!] ERROR: number of packets has to be of type int (a number) [!]")

            print("[#] End packet sniffing [#]\n")

        elif option == '2':
            if capture:
                analyze(capture)
            else:
                print("[!] ERROR: There is no capture to analyze [!]")

        elif option == '3':
            pass

        elif option == '4':    
            print(scapy.all.show_interfaces())

        else:
            print(f"[!] ERROR: There is no such option `{option}` [!]")

        option = input(MENU)

    print("[#] You are now exiting miniScapy.proj, Goodbye! [#]")

    return




if __name__ == "__main__":
    main()


# scapy.all.ls(packet)
# scapy.all.hexdump(packet)
# packet.show()
# packet: scapy.layers.l2.Ether
