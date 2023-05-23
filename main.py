import threading,time
from socket import *

#in lines 5-11 I define a new class named ScannerTool, that will get from the user:
#5 variables, which are: the desired ip address for scaning, in which port to start
#the scan, in which port to end the scan, how many threads to use in the scan,
#and maximum time to set that every socket will wait for a connection
class ScannerTool:
    def __init__(self, ip_address,port_start,port_end,threads,socket_waiting_time):
        self.ip_address = ip_address
        self.port_start = port_start
        self.port_end = port_end
        self.threads = threads
        self.socket_waiting_time = socket_waiting_time
#in the "start" function we set what would be the range of ports that will be scaned by each thread
#according to the range of ports the user want to scan and number of threads he wants to use,
#and  then we call the function "check_ports"
    def start(self):
        threads = []
        total_ports_to_scan =  self.port_end - self.port_start+1
        number_of_ports_per_scan = total_ports_to_scan//self.threads
        port_start = self.port_start
        port_end = number_of_ports_per_scan + port_start - 1
        print("\n\n[+] scanning started")
        for thread in range(self.threads):
            t = threading.Thread(target=self.check_ports, args=(port_start,port_end))
            t.start()
            threads.append(t)
            port_start+=number_of_ports_per_scan
            port_end += number_of_ports_per_scan
        for thread in threads:
            thread.join()
    #the "check_ports" function receive a starting port and end port and get the result of
    #the  every port scan from "is_open" function. if the value is 0 it means that the port
    #is open and hence a relevant message will be printed
    def check_ports(self,port_start, port_end):
        for port in range(port_start, port_end):
            result = self.is_open(port)
            if result == 0:
                print("[+] port {0} | open".format(port))
    #the "is_open" function set the socket of the port scanning and do the process of connecting
    #to specific port and ip address with scan.connect_ex(). the function will return the result of the scan
    #to result variable
    def is_open(self, port):
        try:
            scan = socket(AF_INET, SOCK_STREAM)
            scan.settimeout(self.socket_waiting_time)
            result = scan.connect_ex((self.ip_address, port))
            return result
        except Exception as e:
            print(e)

print('''---------------------------------------
Welcome to network mapper -> v1.05 beta
by sagisar1
---------------------------------------\n''')

while True:
    print("1. IPv4 scanning")
    option = input("insert option: 1 or [e]xit > ")
    if option == "1":
        ip_address = input("enter ip address to scan: >")
        start_port = int(input("enter port number to start from: >"))
        end_port = int(input("enter port number to end the scan: >"))
        threads = int(input("enter number of threads: >"))
        time_out = int(input("enter time_out for every port scan"))
        scan1 = ScannerTool(ip_address, start_port, end_port, threads, time_out)
        start_time = time.time()
        scan1.start()
        scanning_time = time.time() - start_time
        print("scan finished in {0} seconds\n".format(scanning_time))
    if option == "e":
        break







