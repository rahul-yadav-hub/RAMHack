from sys import argv, exit

def print_usage():
        """Print the format for using the script"""
        print('Wrong format\nFormat:   {} <pid> <string to read> <string to write>'.format(argv[0]))
        exit(1)


def read_write_stack(pid, read_str, write_str):
        """Find read_str in the stack memory and replace it with write_str"""

        """Open /proc/pid/maps file to get the info of stack mem"""
        try:
                maps_file = open("/proc/{}/maps".format(pid), 'r')
        except IOError as e:
                print("Can't open file /proc/{}/maps: IOError: {}".format(pid, e))
                exit(1)
        stack_info = None
        """Find where stack memory info is starting"""
        for line in maps_file:
                if 'stack' in line:
                        stack_info = line.split()
        maps_file.close()
        if stack_info is None:
                print('No stack found!')
                exit(1)
        """Extract the address and permission of stack mem"""
        addr = stack_info[0].split('-')
        perms = stack_info[1]
        if 'r' not in perms or 'w' not in perms:
                print('stack does not have read and/or write permission')
                exit(0)
        """Open /proc/pid/mem file to read the actual content in stack mem"""
        try:
                mem_file = open("/proc/{}/mem".format(pid), 'rb+')
        except IOError as e:
                print("Can't open file /proc/{}/mem: IOError: {}".format(pid, e))
                exit(1)
        stack_start = int(addr[0], 16)
        stack_end = int(addr[1], 16)
        mem_file.seek(stack_start)
        stack = mem_file.read(stack_end - stack_start)
        """Dumping the entire data of stack mem in a file"""
        out=open("/root/ramData", 'wb')
        print("Ram data successfully dumped in /root/ramData \n")
        out.write(stack)
        """Searching the read_str string and replacing with write_str"""
        str_offset = stack.find(bytes(read_str, "ASCII"))
        if str_offset < 0:
                print("Can't find {} in /proc/{}/mem".format(read_str, pid))
                exit(1)
        mem_file.seek(stack_start + str_offset)
        mem_file.write(bytes(write_str + '\0', "ASCII"))
        print("Replaced value of string in RAM memory.....Check in running program!!!")
        out.close()

if (len(argv) == 4):
        pid = argv[1]
        search_str = argv[2]
        replace_str = argv[3]
        read_write_stack(pid, search_str, replace_str)
else:
        print_usage()
