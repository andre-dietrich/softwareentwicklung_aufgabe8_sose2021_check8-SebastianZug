from github2pandas.utility import Utility
from github2pandas.version import Version
from pathlib import Path
import os
import dataframe_image as dfi

github_token = os.environ['TOKEN']
git_repo_name = os.environ['CI_REPOSITORY_NAME']
git_repo_owner = os.environ['CI_REPOSITORY_OWNER']
    
default_data_folder = Path("repository/")

if __name__ == "__main__":
    print(git_repo_owner, git_repo_name)
    repo = Utility.get_repo(git_repo_owner, git_repo_name, github_token, default_data_folder)
    Version.no_of_proceses = 8
    Version.generate_version_pandas_tables(repo = repo, data_root_dir=default_data_folder)

    users = Utility.get_users(default_data_folder)
    pdCommits = Version.get_version(data_root_dir=default_data_folder)
    pdEdits = Version.get_version(data_root_dir=default_data_folder, filename=Version.VERSION_EDITS)

    pdEdits = pdEdits.merge(pdCommits[['commit_sha', 'author', 'commited_at']], left_on='commit_sha', right_on='commit_sha')
    pdEdits = pdEdits.merge(users[['anonym_uuid', 'login']], left_on='author', right_on='anonym_uuid')
    
    # Generate Table 
    pdFileEdits = pdEdits.groupby(['commit_sha']).first()
    counts = pdFileEdits.groupby(['login']).agg({'total_added_lines': 'sum', 'total_removed_lines': 'sum'}).reset_index()
    
    blacklist = ["github-classroom[bot]","actions-user"]
    counts = counts[~counts.login.isin(blacklist)]
    counts = counts.rename(columns={"login":               "|     login               |", 
                                    "total_added_lines":   "|  added_lines    |", 
                                    "total_removed_lines": "|  removed_lines  |"})

    dfi.export(counts, 'Contributions.png',  table_conversion='matplotlib')


