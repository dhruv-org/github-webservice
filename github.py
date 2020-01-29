from github import Github

# First create a Github instance:

# or using an access token
g = Github("5e7b1d6424b422b7a4cedc433437717506640382")

for repo in g.get_user().get_repos():
    print(repo.name)
    repo.edit(has_wiki=False)
    # to see all the available attributes and methods
    print(dir(repo))