import psutil
from psutil import AccessDenied
import sys, os
from fnv1a import FNV1a


def create_dico_process():
    """
    Get all process name and return a dictionary
    """

    dico_process =  {}
    for proc in psutil.process_iter():
        try:
            dico_process[proc.name().split("/")[0]] = proc.pid

        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass
    return dico_process


def calculate_hash(string):
    """
    The hash is calculated by performing a FNV-1a 64bit hash of the lowercase string then XOR by 6605813339339102567.
    """

    hasher = FNV1a()
    return int(hasher.hash(string), 16) ^ 6605813339339102567

def get_list_hash(name):
    """
    return the list of sunburst hash
    """

    with open(name, 'r') as hash_doc:
        list = hash_doc.readlines()
    return list


if __name__ == "__main__":
    dico_process = create_dico_process()
    list_hash = get_list_hash("hash.txt")

    for process in [*dico_process]:
        hash_process = calculate_hash(process)
        if hash_process in list_hash:
            print("Detection of a process in the list : ", process)


    print("there is no running process in the hash list !")
    #print(calculate_hash('autopsy'))

    #print(list_hash)

    #print(dico_process)
    input("Press enter to exit...")