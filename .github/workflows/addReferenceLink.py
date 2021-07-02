import os

github_token = os.environ['TOKEN']
git_repo_name = os.environ['CI_REPOSITORY_NAME']
git_repo_owner = os.environ['CI_REPOSITORY_OWNER']

readmefilename = "README.md"

with open(readmefilename, 'r') as filehandle:
    readmecontent = filehandle.read()

readmecontent = readmecontent.replace("<CI_REPOSITORY_OWNER>", git_repo_owner)
readmecontent = readmecontent.replace("<CI_REPOSITORY_NAME>", git_repo_name)

with open(readmefilename, 'w') as filehandle:
    filehandle.write(readmecontent)
