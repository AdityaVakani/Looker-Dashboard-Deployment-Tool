import os
import sys 
import fileinput
import string
import shutil


### TODO String Replacement Lists to be passed in function parameter and not refrence the global variable 
### TODO Allow option to use a map file in string replace to replace view names while migrating incase view name conventions arent followed  
### TODO Decouple Code and create functions for repeating code

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
def string_input():
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
def string_replace(fileToSearch):
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
def backup_folder(destination_folder_no):
    backup_flg = input("Do you want to Backup Destination Folder (Yes/No):")
    if backup_flg.lower() == "yes":
        print("Backing Up Destination Folder Data JSON")
        os.system('gzr space export {0} --host {3}  --client_id={1} --client_secret={2} --port 443 --dir backup'.format(destination_folder_no,client_id,client_secret,host))
        print("Finshed Backing Up Destination Folder Data JSON")
    elif backup_flg.lower() == "no":
        print("Not Backing Up Destination Folder")
    
    else: 
        print("Invalid Input Not Backing Up Folder")

## Start Of Deployment Tool
print("####################### Dashboard Deployment Tool V2 #############################")

# Get Connection Details from text file
conf = get_credentials("api3_key.txt")
client_id = conf['client_id']
client_secret = conf['client_secret']
host = conf['host']


while True:
    
    #Delete Content of Folder with Copied JSON before starting each loop and create empty lists to hold strings 
    delete_folder_contents("dash_json")
    textToSearch = []
    textToReplace = []

    print("""
    1) Folder Of Dashboard Deployment
    2) Dashboard Deployment 
    3) Exit

    """)

    deployment_option=input("Enter Choice (1,2,3) :")

    if deployment_option == '1':
        source_folder_no = input("Enter Folder Number To Copy From:")
        # Export JSON of selected folder
        os.system('gzr space export {0} --host {3}  --client_id={1} --client_secret={2} --port 443 --dir dash_json'.format(source_folder_no,client_id,client_secret,host))
        print("Copied Folder Contents To JSON")

        # Get Folder Name and name of json files for each dashboard
        dashboard_folder_name = os.listdir("dash_json")
        if len(dashboard_folder_name)>1:
            print("Error More Than 1 Folder Exists. Exiting Code To prevent Wrong data being used")
            sys.exit()    
        dashboard_json_names = os.listdir("dash_json/{0}".format(dashboard_folder_name[0]))
        
        # Exclude JSON of Space (Folder)
        for i in range (0 ,len(dashboard_json_names)):
            if "Space_" in dashboard_json_names[i]:
                del dashboard_json_names[i]

        destination_folder_no = input("Enter Folder Number To Copy To:")
        
        # Option to backup JSON of destination folder before starting 
        backup_folder(destination_folder_no)

        # Code to replace strings in JSON Files
        while True:
            string_replace_flg = input("Do you want to replace contents of JSON (YES/NO)")
            if string_replace_flg.lower() == "yes":
                string_input()
                for dashboard_json in dashboard_json_names:
                    string_replace("dash_json/{0}/{1}".format(dashboard_folder_name[0],dashboard_json))
                break
            elif string_replace_flg.lower() == "no":
                break
            else:
                print("Please enter yes or no ")
        
        # Deploy Dashboards
        for dashboard_json in dashboard_json_names:
            os.system('call gzr dashboard import "dash_json\{0}\{1}" {2} --host {5} --client_id={3} --client_secret={4} --port 443 --force'.format(dashboard_folder_name[0],dashboard_json,destination_folder_no,client_id,client_secret,host))


    elif deployment_option == "2":

        # Create List of dashboard ID's to be copied
        source_dashboard_list = []
        while True:
            source_dashboard_no =  input("Enter Dashboard Number To Copy From(0 To exit):")
            if source_dashboard_no == "0":
                break
            source_dashboard_list.append(source_dashboard_no)
        
        # Get JSON for selected Dashboard ID's
        for dashboard_id in source_dashboard_list:
            os.system('call gzr dashboard cat {0} --host {3}  --client_id={1} --client_secret={2} --port 443 --dir dash_json'.format(dashboard_id,client_id,client_secret,host))
        dashboard_json_names = os.listdir("dash_json")
        destination_folder_no = input("Enter Folder Number To Copy To:")

        # Option to backup JSON of destination folder before starting 
        backup_folder(destination_folder_no)

        # Code to replace Strings in JSON File
        while True:
            string_replace_flg = input("Do you want to replace contents of JSON (YES/NO):")
            if string_replace_flg.lower() == "yes":
                string_input()
                for dashboard_json in dashboard_json_names:
                    string_replace("dash_json/{0}".format(dashboard_json))
                break
            elif string_replace_flg.lower() == "no":
                break
            else:
                print("Please enter yes or no ")
        
        # Deploy Dashboards
        for dashboard_json in dashboard_json_names:
            os.system('call gzr dashboard import "dash_json\{0}" {1} --host {4} --client_id={2} --client_secret={3} --port 443 --force'.format(dashboard_json,destination_folder_no,client_id,client_secret,host))    

    # Exit Deployment Tool
    elif deployment_option == "3":
        break
    
    else:
        print("Enter Valid Option")
   



