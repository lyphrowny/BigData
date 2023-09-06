from github import Github, Auth


def pad_print(what: list, *, padding_size: int =1):
    def _pad(line):
        return f"{chr(9)*padding_size}{line}"

    *_, = map(print, map(_pad, what))


def main():
    # use either the generated token (lower rate limit)
    # auth = Auth.Token("your_generated_token")
    # g = Github(auth=auth)
    # or don't (higher rate limit)
    g = Github()

    uname = "suragnair"
    user = g.get_user(uname)

    print(f"{uname}'s followers:")
    pad_print(user.get_followers())

    print(f"{uname} follows:")
    pad_print(user.get_following())

    print(f"{uname}'s repos and their contributors:")
    for repo in user.get_repos():
        print(f"\t{repo.name}")
        pad_print(repo.get_contributors(), padding_size=2)


if __name__ == "__main__":
    main()