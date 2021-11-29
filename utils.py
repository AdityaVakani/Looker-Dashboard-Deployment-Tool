import os
import sys 
import fileinput
import string
import shutil


# Function to get connection details from text file and create dictionary
def get_credentials(filepath):
    f = open(filepath, 'r')
    answer = {}
    for line in f:
        k, v = line.strip().split('=')
        answer[k.strip()] = v.strip()
    f.close()
    return answer

# Function to get string inputs and replacement strings from user input and add to list
def string_input(textToSearch,textToReplace):
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
        print("Backing Up Destination Folder Data JSON")
        os.system('gzr space export {0} --host {3}  --client_id={1} --client_secret={2} --port 443 --dir backup'.format(destination_folder_no,client_id,client_secret,host))
        print("Finshed Backing Up Destination Folder Data JSON")
    elif backup_flg.lower() == "no":
        print("Not Backing Up Destination Folder")
    
    else: 
        print("Invalid Input Not Backing Up Folder")