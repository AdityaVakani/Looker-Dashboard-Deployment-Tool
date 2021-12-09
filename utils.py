import os
import sys 
import fileinput
import string
import shutil
import datetime



# Function to get connection details from text file and create dictionary
def get_credentials(filepath):
    f = open(filepath, 'r')
    answer = {}
    for line in f:
        if line == "\n":
            continue
        k, v = line.strip().split('=')
        answer[k.strip()] = v.strip()
    f.close()
    return answer

# Function to populate lists with View names from the Map File     
def get_map(filepath,textToSearch,textToReplace):
    f = open(filepath, 'r')
    
    for line in f:
        if line == "\n":
            continue
        k, v = line.strip().split('=')
        if k.strip().lower()== "from":
            continue
        textToSearch.append(k.strip())
        textToReplace.append(v.strip())
    f.close()
    return textToSearch,textToReplace


# Function to get string inputs and replacement strings from user input and add to list
def string_input(textToSearch,textToReplace):
    while(True):
        use_map = input("Use a map file?(Yes/No) :")
        if use_map.lower() == "yes":
            textToSearch,textToReplace = get_map("view_map.txt",textToSearch,textToReplace)
            return
        elif use_map.lower()  == "no":
            break
        else:
            print("Enter Valid Input")
    while(True):
        print ("Enter '0' to exit from string replacement selector")
        x=input("Enter String to be Replaced: ")
        if(x == "0"):
            break
        textToSearch.append(x)
        y=input("Enter String to be Replace with: ")
        textToReplace.append(y)
        print("\n")

# Function to replace Strings in File 
def string_replace(fileToSearch,textToSearch,textToReplace):
    # Read in the file
    with open(fileToSearch, 'r',encoding='utf-8') as file :
        filedata = file.read()

    # Replace the target string
    for i in range(0,len(textToSearch)):
        filedata = filedata.replace(textToSearch[i], textToReplace[i])

    # Write the file out again
    with open(fileToSearch, 'w',encoding='utf-8') as file:
        file.write(filedata)

    print("Strings Replaced for file {0}".format(fileToSearch))

# Function to delete content of folder
def delete_folder_contents(folder):
    for filename in os.listdir(folder):
        file_path = os.path.join(folder, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print('Failed to delete %s. Reason: %s' % (file_path, e))

# Function to backup folder JSON
def backup_folder(destination_folder_no,client_id,client_secret,host):
    backup_flg = input("Do you want to Backup Destination Folder (Yes/No):")
    if backup_flg.lower() == "yes":
        time = str(format(datetime.datetime.today().strftime('%Y-%m-%d-%H-%M-%S')))
        os.mkdir("backup/{0}".format(time))
        print("Backing Up Destination Folder Data JSON")
        os.system('gzr space export {0} --host {3}  --client_id={1} --client_secret={2} --port 443 --no-verify-ssl --dir backup/{4}'.format(destination_folder_no,client_id,client_secret,host,time))
        foldername = os.listdir("backup/{0}".format(time))[0]
        os.rename("backup/{0}".format(time),"backup/{1}-{0}".format(time,foldername))
        files = os.listdir("backup/{1}-{0}/{1}".format(time,foldername))
        for file in files:
            file_name = os.path.join("backup/{1}-{0}/{1}".format(time,foldername), file)
            shutil.move(file_name, "backup/{1}-{0}".format(time,foldername))
            if "Space_" in file_name:
                os.remove("backup/{1}-{0}/{2}".format(time,foldername,file))

        os.rmdir("backup/{1}-{0}/{1}".format(time,foldername))
        print("Finshed Backing Up Destination Folder Data JSON")
    elif backup_flg.lower() == "no":
        print("Not Backing Up Destination Folder")
    
    else: 
        print("Invalid Input Not Backing Up Folder")


def restore_backup(client_id,client_secret,host):
    files = os.listdir("backup")
    for i in range(0,len(files)):
        print(i+1," : ",files[i])

    while True:   
        backup_folder_no = input("Input Number For the Backup file you would like to restore:")
        if int(backup_folder_no)>len(files):
            print("Enter Valid Number")
            continue
        confirm = input("Confirm selected folder {0} (yes/no) :".format(files[int(backup_folder_no)-1]))
        if confirm.lower() == "yes":
            break
        else:
            continue

    backup_file = files[int(backup_folder_no)-1]

    restore_backup_destination = input("Enter Folder Number you would like to restore the backup into :")

    print("Restoring Backup Into Destination Folder {0}".format(restore_backup_destination))

    backup_json_names = os.listdir("backup/{0}".format(backup_file))

    for i in range (0 ,len(backup_json_names)):
        if "Space_" in backup_json_names[i]:
            del backup_json_names[i]

    for backup_json in backup_json_names:
        print("Importing:",backup_json)
        os.system('call gzr dashboard import "backup\{0}\{1}" {2} --host {5} --client_id={3} --client_secret={4} --port 443 --no-verify-ssl --force'.format(backup_file,backup_json,restore_backup_destination,client_id,client_secret,host))


