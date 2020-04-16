import os

def build_uid_list():
    uidset = []
    for line in open("/etc/passwd"):
        uidset.append(line.split(":")[2])
    return uidset



def walk_file_system(diretory):
    for folder, dirs, files in os.walk(diretory):
        for file in files:
            path = folder + "/" + file
            atributes = os.stat(path)
            if(atributes.st_uid not in build_uid_list()):
                print(path + " has no owner")


walk_file_system("home/pi/Movies")