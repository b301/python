import scapy.all


MENU = """
[#] Choose an option [#]

1. Sniff
2. Analyze
3. Get Certificate
4. List NICs
5. Exit

[>] Pick: """


def analyze(capture: scapy.plist.PacketList) -> None:
    information = f"""[#] Details [#]

    Packets: {len(capture)}

    Enter `-1` as index to quit
    """

    print(information)
    packet_index = print("[+] Pick a packet (index): ")
    while packet_index != "-1":
        if packet_index in range(1, len(capture) + 1):
            print(scapy.all.ls(capture[packet_index]))

        packet_index = input("[+] Pick a packet (index): ")

    return


def main():
    print("[*] Welcome to miniScapy.proj [*]")
    option = input(MENU)
    capture = None

    while option != '5':
        if option == '1':
            counter = input("[+] How many packets do you wish to capture? ")
            filter_args = input("[+] Enter filter arguments: ")
            iface = input("[+] Choose a network interface: ")
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
