###Get the day with the most commits (globally)
- [ ] Done
```python
for each repo
    repo.get_stats_commit_activity()
```


###Build a "social" tree
- [ ] Done
```python
users = deque(curr_user)
visited = set() # might be way too inefficient memory-wise
followers = []
following = []

i = 0
while not users:
    user = users.popleft()
    visited.add(user)
    for follower in user.get_followers():
        path: follower -> user
        if follower not in visited:
            users.append(follower)
    for following in user.get_following():
        path: user -> following
        if following not in visited:
            users.append(following)
```


###Languages
- [ ] Done

    repo.size # to get the number of bytes of total code
    repo.get_languages() # get the number of bytes of code, written in a specific language


###Load some part of the repo
- [ ] Done

    repo.get_contents(path) # path is the path to the content

    or

    use bare github api, because pygithub doesn't have such a method
    https://docs.github.com/en/rest/repos/contents?apiVersion=2022-11-28#download-a-repository-archive-tar

    or

    repo.get_git_tree(sha)


###Analyse README
- [ ] Done

    What should we do with it?
    repo.get_readme()


###Get reactions on issues' comments
- [ ] Done

    Analyse the most used one, smth like that
    Issue -> IssueComment -> get_reactions()

    or 

    Issue -> get_reactions()

    or

    pull requests (maybe bare github api)

    or 

    for a release (maybe bare github api)


###Average response time by any user for a particular repository
- [ ] Done
```python
for issue in issues:
    comments = issue.get_comments() # or issue.get_comment(id)
    for comment in comments:
        comment.user
        comment.created_at
```