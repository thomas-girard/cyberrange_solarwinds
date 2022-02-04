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
            dico_process[proc.name().split(".")[0].lower()] = proc.pid # it's necessary to split in order to remove potentially ".exe"

        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass
    return dico_process

def create_dico_service():
    """
    Get all service name and return a dictionary
    """

    list_service = list(psutil.win_service_iter())
    dico_service = {}
    for name_instance in range(len(list_service)):
        dico_service[list_service[name_instance].name().lower()] = psutil.win_service_get(list_service[name_instance].name()).as_dict()
    return dico_service


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
    list_int = []
    for k in range(len(list)):
        list_int.append(int(list[k]))
    return list_int


if __name__ == "__main__":

    dico_process = create_dico_process()

    dico_service = create_dico_service()

    try:
        list_hash = get_list_hash("hash.txt")
        detection_bool_process = False
        for process in [*dico_process]:
            hash_process = calculate_hash(process)
            if hash_process in list_hash:
                print("Detection of a process in the list : ", process)
                detection_bool_process = True

        if detection_bool_process == False:
            print("No process is in the hash list !")
    except:
        pass

    try:
        list_hash = get_list_hash("hash.txt")
        detection_bool_service = False
        for service in [*dico_service]:
            hash_service = calculate_hash(process)
            if hash_service in list_hash:
                print("Detection of a service in the list : ", process)
                detection_bool_service = True

                if dico_service[service]['pid'] is not None:
                    print("attempt to kill the service...")
                    try:
                        os.kill(dico_service[service]['pid'], 9)
                        print("Service killed ! ")
                    except:
                        print("Failure to stop service")

        if detection_bool_service == False:
            print("No service is in the hash list !")
    except:
        pass
    

    input("Press enter to exit...")