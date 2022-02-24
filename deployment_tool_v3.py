import os
from utils import *





## Start Of Deployment Tool
print("####################### Dashboard Deployment Tool V2 #############################")

# Get Connection Details from text file
conf = get_credentials("api3_key.txt")
client_id = conf['client_id']
client_secret = conf['client_secret']
host = conf['host']

while True:
    
    # Delete Content of Folder with Copied JSON before starting each loop and create empty lists to hold strings 
    delete_folder_contents("dash_json")
    textToSearch = []
    textToReplace = []

    print("""
    1) Folder Of Dashboard Deployment
    2) Dashboard Deployment 
    3) Restore Backup
    4) Create Backup
    5) Exit

    """)

    deployment_option=input("Enter Choice (1,2,3,4) :")

    if deployment_option == '1':
        source_folder_no = input("Enter Folder Number To Copy From:")
        
        # Function in utils to the json data for all dashboards in selected folder
        space_export(source_folder_no,"dash_json",client_id,client_secret,host)
        print("Copied Folder Contents To JSON")


        dashboard_folder_name,dashboard_json_names = dashboard_json_files_from_folder("dash_json")

        destination_folder_no = input("Enter Folder Number To Copy To:")
        
        # Option to backup JSON of destination folder before starting 
        backup_folder(destination_folder_no,client_id,client_secret,host)

        # Code to replace strings in JSON Files
        while True:
            string_replace_flg = input("Do you want to replace contents of JSON (YES/NO):")
            if string_replace_flg.lower() == "yes":
                string_input(textToSearch,textToReplace)
                for dashboard_json in dashboard_json_names:
                    string_replace("dash_json/{0}/{1}".format(dashboard_folder_name[0],dashboard_json),textToSearch,textToReplace)
                break
            elif string_replace_flg.lower() == "no":
                break
            else:
                print("Please enter yes or no ")
        
        # Deploy Dashboards
        for dashboard_json in dashboard_json_names:
            print("Importing:",dashboard_json)
            dashboard_import('"dash_json\{0}\{1}"'.format(dashboard_folder_name[0],dashboard_json),destination_folder_no,host,client_id,client_secret)


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
           dashboard_cat(dashboard_id,host,client_id,client_secret,"dash_json")
        dashboard_json_names = os.listdir("dash_json")
        destination_folder_no = input("Enter Folder Number To Copy To:")

        # Option to backup JSON of destination folder before starting 
        backup_folder(destination_folder_no,client_id,client_secret,host)

        # Code to replace Strings in JSON File
        while True:
            string_replace_flg = input("Do you want to replace contents of JSON (YES/NO):")
            if string_replace_flg.lower() == "yes":
                string_input(textToSearch,textToReplace)
                for dashboard_json in dashboard_json_names:
                    string_replace('"dash_json/{0}"'.format(dashboard_json),textToSearch,textToReplace)
                break
            elif string_replace_flg.lower() == "no":
                break
            else:
                print("Please enter yes or no ")
        
        # Deploy Dashboards
        for dashboard_json in dashboard_json_names:
            print("Importing:",dashboard_json)
            dashboard_import('"dash_json\{0}"'.format(dashboard_json),destination_folder_no,host,client_id,client_secret)

    # restore backup from local file
    elif deployment_option == "3":
        restore_backup(client_id,client_secret,host)
    
    # create backup into local
    elif deployment_option == "4":
        source_folder_no = input("Enter Folder Number To Backup From:")
        backup_folder(source_folder_no,client_id,client_secret,host)

        
    # Exit Deployment Tool
    elif deployment_option == "5":
        break

    else:
        print("Enter Valid Option")
   



