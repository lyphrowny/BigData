# Social graph of developers

* Get all the repos, which have at least some stars
* For each repo
    * Get all the commits (to analyze, who worked on each file)
    * Get all the PRs (what for?)


# World map of technologies

Which technologies are popular in a specific region

* Get all the repos, which have at least some stars
* For each repo
    * Get its languages
    * For each contributor
        * Get their location


# Natural language analysis

Determine how good the github community's English is

* Get all the repos, which have at least some stars
* For each repo
    * Get all the issues' comments (PRs included)
    * Get all the PRs' review comments
    * Get all the commit comments
    * Get README.md
    * Get docs (?)
    * Get the repo's about


# Reaction time in repos

Get the average reaction time on new issues, PRs

* Get all the repos, which have at least some stars
* For each repo
    * Get all issues' timelines (PRs included)


# Workflow

* Get all the repos <br/><br/>
    Either through `repos.async_list` and manually select the "right" ones
    OR use `search` <br/><br/>
    If one were to use `search`, its rate limit is 1800 req/hour, while `repos.async_list` has 5000 req/hour.
    `search` is limited in how many repos it can return: 4000 max. Maybe one can overcome this by using the exact number of stars in the request (for stars=100 get all the repos; increase stars, ...) (more than 4000 repos with the same number of stars?) <br/><br/>
    Overall, `search` seems to be better suited for the job, despite having limitations: I bet the number of repos with stars less than, say 100, is far more greater, than the difference in `search` and `repos.async_list` performance. <br/><br/>
    If one wants to use `repos.async_list` to look at each of the repos (300 000 000), it would take ~600 hours with one requester. **Solution**: to have 600 requesters :thumbsup: <br/><br/>
* Get the repo's languages (`repos.async_list_languages`)
* Get the repo's about (`repos.async_get_community_profile_metrics`)
* Get all the contributors (`repos.async_list_contributors`)
    * Get their location via requesting a full user (`users.async_get`)
* Get all the issues (`issues.async_list_for_repo`)
    * Get its timeline (via timeline one gets all the comments and commit comments. for review comments one has to call for them directly) (`issues.async_list_events_for_timeline`)
    * Get all the PRs' review comments (`pulls.async_list_review_comments`)
* Get the repo's README (`repos.async_get_readme`)
* Get all the commits (`repos.async_list_commits`)
    * Get the files changed in the commit via requesting a full commit (`repos.async_get_commit`)
* Get all the packages this repo depends on (`dependency_graph.async_export_sbom`)