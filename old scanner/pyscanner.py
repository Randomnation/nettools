import socket
import sys
import Queue
from math import ceil
from multiprocessing import Process

queue = Queue.Queue()


def chunk(chunks):
    chunk_size = int(ceil(len(port_range) / float(chunks)))
    chunk_blocks_list = []
    chunk_start = 0
    chunk_end = chunk_size
    for c in range(0, chunks):
        chunk_blocks_list.append(port_range[chunk_start:chunk_end])
        chunk_start = chunk_end
        chunk_end += chunk_size
    return chunk_blocks_list


def do_scan(_block=[], remoteServerIP = ''):

    for port in _block:

        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(5)
            result = sock.connect_ex((remoteServerIP, port))

            if result == 0:
                print "Port {}: \t Open".format(port)
            # else:
            #     print "Port {}: \t Not Open".format(port)
            sock.close()

        except socket.gaierror:
            print 'Hostname could not be reached. Exiting'
            sys.exit()

        except socket.error:
            print "Couldn't connect to server. Exiting"
            sys.exit()
    return


def thread_scan(ip):
    for block in chunk_blocks:
        p = Process(target=do_scan, kwargs={'_block': block, 'remoteServerIP': ip})
        p.start()


def get_data(string):
    output = raw_input(string)
    return output

if __name__ == '__main__':
    remote_server = raw_input("Enter a remote host to scan: ")
    start_port = raw_input("Start port: ")
    end_port = raw_input("End port: ")
    chunks = raw_input("Number of ports at once: ")
    start_port = int(start_port)
    end_port = int(end_port)
    chunks = int(chunks)
    port_range = range(start_port, end_port)
    remoteServerIP = socket.gethostbyname(remote_server)
    print "Host: " + remoteServerIP
    chunk_blocks = chunk(chunks)
    thread_scan(remoteServerIP)