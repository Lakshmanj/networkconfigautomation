import os 
import subprocess
from github import Github   

#Replace thse with your own credentials
repo_name = "your_repo_name" 
github_token = "your_github_token"
command = "ls -l" #replace with your command you want to execute

#Get the Github repository
g = Github(github_token)
repo = g.get_user().get_repo(repo_name)

#Execute the command and get the output
output = subprocess.check_output(command.split()).decode("utf-8")

#Create a new file in the repository and write the output to it
filename = "output.txt" #replace with your desired filename
file_path = os.path.join(os.getcwd(), filename)
with open(file_path, "w") as f:
    f.write(output)

#Upload the file to the repository
with open(file_path, "rb") as f:
    contents = f.read()
    repo.create_file(filename, "Upload output of command", contents)

