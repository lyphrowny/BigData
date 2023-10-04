# Methods of API

The current document presents methods of github API, that firstly were hand-picked, then each method was called and analyzed. All the methods are separated into three groups:

* **Definitely use**

    Method's name is in bold. These methods provide the crucial info.

* *Maybe use*

    Method's name is in italic. Method's description has **Maybe use** "label". These methods might be useful, but there is no worthy use case for them, or these methods are for fine-grained control, i.e. get all the comments for a particular issue.

* Won't use

    Method's description has **Won't use** "label". These methods are usually superseded by `definitely use` methods: don't add any new info, which can be obtained through `definitely use` methods.

The boundary line between `maybe use` and `won't use` is blurred, as well as between `definitely use` and `maybe use` (less blurred), but not between `definitely use` and `won't use`.

Each group of methods has the methods' differentiation and description. At the end of each group there is a supposed workflow.



# Global workflow

* Get all the users / orgs. Get the full user, followers, following. Get `async_list_repos_watched_by_user`, `sync_list_repos_starred_by_user`, all the repos. Get all the orgs, a user is part of `async_list_for_user`.
    * For each org get its public members `async_list_public_members`.
* For each repo get a full one (`async_get`), get all the "meta" info: topics (`async_get_all_topics`), languages (`async_list_languages`), tags (`async_list_tags`), some metrics (`async_get_community_profile_metrics`), contributors (`async_list_contributors`), releases (`async_list_releases`), forks (`async_list_forks`), commits per week (`async_get_participation_stats`), daily-hourly commits (`asycn_get_punch_card_stats`), `async_list_watchers_for_repo`, `async_list_stargazers_by_user`.
    * Get all the repo's issues via `async_list_for_repo`, for each issue get its timeline via `async_list_events_for_timeline` to get all the needed events (`commented`, `reviewed`, etc.). Such events have different attributes to get the time of creation.
    * Get all the PRs through `async_list_for_repo`, get all the PR's numbers. For each PR, get the full PR via `async_get`, get the PR's review comments via `async_list_review_comments`. Maybe get all the files affected by the PR (`async_list_files`), get all the commits (`async_list_commits`).
    * Download repo's tarball
    * List all the workflows with `async_list_repo_workflows`. For each get its runs with `async_list_workflow_runs`.
    * Get all the packages, this repo depends on `async_export_sbom`



## users

* **async_list**

    Get all the users (not full).

* **async_get_by_username**

    Get a full user. Full user has `name`, `location`, `public_repos` (number), `bio`, `hireable`, `public_gists` (number), `followers` (number), `following` (number), `created_at`, ... attributes, which not full user doesn't have.

* **async_list_followers_for_user**

    Get all the users, following this user.

* **async_list_following_for_user**

    Get all the users, this user follows.

* async_check_following_for_user

    Check whether a particular user follows another user. **Won't use**

* *async_list_gpg_keys_for_user*

    Get all the public gpg keys for a particular user. **Maybe use**

* *async_list_public_keys_for_user*

    Get all the public keys for a particular user. **Maybe use**

* *async_list_social_accounts_for_user*

    Get all the social accounts for a particular user. **Maybe use**

* async_list_ssh_signing_keys_for_user

    Get the ssh signing keys for a particular user. **Won't use**

### Workflow

Get all the Github users with `async_list` (iteratively, not at once). For each user get a full user (`async_get_by_username`) and its followers and following (`async_list_followers_for_user` and `async_list_followers_for_user` respectively).



## repos

* **async_list_for_org**

    Get all the repos of a particular organization.

* **async_get**

    Get a full repo (doesn't matter, whether it's a user's one or an org's)

* *async_list_activities*

    Get all the repo's activity. (Don't know what's the difference between events). **Maybe use**

* *async_list_branches*

    Get all the repo's branches. Has `name`, `protected` (bool), `sha` (last commit sha) attributes. **Maybe use**

* *async_get_branch*

    Get the full repo's branch. Only last commit, protection is in more detail. **Maybe use**

* async_list_commit_comments_for_repo

    Get all the repo's commit comments. Cumbersome to use, better get all the pr's commits and then their comments (`pulls.async_get_commits`). **Won't use**

* **async_get_commit_comment**

    Get a comment for a particular commit.

* async_list_commits

    Get all the repo's commits. Cumbersome to use, better get all the pr's commits (`pulls.async_get_commits`). **Won't use**

* *async_list_comments_for_commit*

    Get all the comments for a commit. **Maybe use**

* async_list_pull_requests_associated_with_commit

    Get all the PRs, which are associated with a particular commit. **Won't use**

* **async_get_commit**

    Get the full commit.

* async_get_combined_status_for_ref

    Get the overall status for a particular commit. **Won't use**

* async_list_commit_statuses_for_ref

    Get all the statuses for a particular commit. **Won't use**

* **async_get_community_profile_metrics**

    Get some info on a repo, aka profile metrics.

* async_compare_commits

    Comparas two commits. **Won't use**

* *async_get_content*

    Get content of a particular repo's file. Content is encoded in `base64`. **Maybe use**

* **async_list_contributors**

    Get all the repo's contributors. Has `contributions` (number) attribute.

* async_list_deployments

    Get all the repo's deployments. **Won't use**

* async_get_deployment

    Get a repo's particular deployment. **Won't use**

* async_list_deployment_statuses

    **Won't use**

* async_get_deployment_status

    **Won't use**

* async_get_all_environments

    Get all the repo's environments. Has some info about protection rules. **Won't use**

* async_get_environment

    Get a particular repo's environment. Seems not to differ with response from `async_get_all_environments`. **Won't use**

* **async_list_forks**

    Get all the repos, that are forks of a particular repo.

* **async_list_languages**

    Get all the languages, used in a particular repo.

* *async_get_readme*

    Get the repo's readme. Content is encoded with `base64`. Want to download the whole repo, so this is not needed. **Maybe use**

* async_get_readme_in_directory

    Get readme in a particular directory. **Won't use**

* **async_list_releases**

    Get all the repo's releases.

* async_get_latest_release

    Get the latest release. Will be getting all the releases with `async_list_releases`, so this one is not needed. **Won't use**

* async_get_release

    Get the repo's full release. The response doesn't differ from `async_list_releases`. **Won't use**

* async_get_code_frequency_stats

    Supposedly, get the frequency stats of a particular repo. Got empty response on 2 repos. **Won't use**

* async_get_commit_activity_stats

    Supposedly, get the commit activity stats of a particular repo. Got empty response on 2 repos. **Won't use**

* async_get_contributors_stats

    Supposedly, get the contributors stats of a particular repo. Got empty response on 2 repos. **Won't use**

* **async_get_participation_stats**

    Get the number of commits per week.

* **async_get_punch_card_stats**

    Get daily-hourly number of commits. [[0-6 (day), 0-23 (hour), \# commits], ...]

* **async_list_tags**

    Get all the release tags, i.e. "v0.22.0"

* **async_download_tarball_archive**

    Get the tarball of the latest release, with the latest sha.

* **async_get_all_topics**

    Get all the topics for a particular repo. Like repo tags.

* async_download_zipball_archive

    Same as tarball, but zipball. **Won't use**

* async_list_public

    Get all the public repos. **Won't use**

* **async_list_for_user**

    Get all the repos for a particular user.

### Workflow

For each user / org get all the repos (`async_list_for_user`, `async_list_for_org`). For each repo get a full one (`async_get`), get all the "meta" info: topics (`async_get_all_topics`), languages (`async_list_languages`), tags (`async_list_tags`), some metrics (`async_get_community_profile_metrics`), contributors (`async_list_contributors`), releases (`async_list_releases`), forks (`async_list_forks`), commits per week (`async_get_participation_stats`), daily-hourly commits (`asycn_get_punch_card_stats`).



## orgs

* async_list

    Get all the organizations. One can get the organization with `users.async_list`, there will be `type` attribute with `Organization` value. `users.async_list` gives more info. **Won't use**

* async_get

    Get a full organization. One can get the full organization with `users.async_get` with more info. **Won't use**

* async_list_members

    Get all the org's members. Seems this is the same as `async_list_public_members`, however if an authenticated user is a part of the org, private members will be returned. **Won't use**

* async_check_membership_for_user

    Check whether a particular user is a member of the org. **Won't use**

* **async_list_public_members**

    Get all the org's public members.

* async_check_public_membership_for_user

    Check whether a particular user is a public member of the org. **Won't use**

* **async_list_for_user**

    Get all the orgs a particular user is part of.

### Workflow

For each user get all the orgs, which they are a part of (`async_list_for_user`), get all the public members (`async_list_public_members`).



## issues

* async_list

    List issues assigned to the authenticated user across all visible repositories including owned repositories, member repositories, and organization repositories. **Won't use**

* async_list_for_org

    List issues in an organization assigned to the authenticated user. **Won't use**

* *async_list_assignees*

    Get all the repo assignees. No info to which issue / pr they were assigned. Response of `async_get_for_repo` contains assignees for each issue. **Maybe use**

* **async_list_for_repo**

    Get all the repo issues. Contains info about `assignee` (`assignees`), `labels`, `comments` (number), `id`, `number`.

* *async_list_comments_for_repo*

    Get all the repo comments. The comments sorted by their creation time. Might be useful if just a dump is needed. Seems cumbersome to use if one wants to retrieve all the comments for a particular issue (need to extract the issue number from `issue_url`). Reactions are included for each comment, has `created_at` and `updated_at` timestamps. **Maybe use**

* async_get_comment

    Get info for a particular comment. The response doesn't differ from `async_list_comments_for_repo` (no new info). **Won't use**

* async_list_events_for_repo

    Get all the events for the repo. `merged`, `closed`, `referenced`, `head_ref_deleted`. **Won't use**

* async_get_event

    Get the info about a particular event. The response doesn't differ from `async_list_events_for_repo`. **Won't use**

* *async_get*

    Get the issue and its labels. The response doesn't differ from `async_list_for_repo`. **Maybe use**

* *async_list_comments*

    Get all the comments for a particular issue. The response doesn't differ from `async_list_comments_for_repo`. Doesn't have `reviewed` event. **Maybe use**

* async_list_events

    Get (almost) all the events for a particular issue. There are no events, such as `commented`, `reviewed`. It that sense `async_list_events_for_timeline` seems more preferable. **Won't use**

* async_list_labels_on_issue

    No need as the labels are received with the `async_get` method. **Won't use**

* **async_list_events_for_timeline**

    Get all the events for the issue sorted by a time created. Can be used to evaluate the response time. Useful events: `reviewed`, `commented`, `commited` (commit has date of creation under `user`) (others?). All the events have different attributes to get the time.

* **async_list_labels_for_repo**

    Get all the labels for repo.

* async_get_label

    Get the label by its name. Not related to any issue. Completely covered by `async_list_labels_for_repo`. **Won't use**

* *async_list_milestones*

    Get all the repo's milestones. There are `title`, `open_issues`(just number), `closed_issues`(just number) in the response. Milestones can be `open` and `closed` (and `all`). **Maybe use**

* async_get_milestone

    Get a particular milestone. The response doesn't differ from `async_list_milestones`. **Won't use**

* *async_list_labels_for_milestone*

    Get all the labels for a particular milestone. This info is unique, i.e. wasn't (=can't be?) obtained through any other method. **Maybe use**

### Workflow

Get all the repo's issues via `async_list_for_repo`, for each issue get its timeline via `async_list_events_for_timeline` to get all the needed events (`commented`, `reviewed`, etc.). Such events have different attributes to get the time of creation.



## pulls

* *async_list*

    Get all the repo's PRs. Most attributes are accessible through the issue's `pull_request` attribute (`merged_at`, `diff_url`, `patch_url`), though the issue doesn't have `commits_url`, `review_comments_url`, `review_comment_url`, `statuses_url`; and PR doesn't have `auto_merge`, `active_lock_reason`, `events_url`. **Maybe use**

* async_list_review_comments_for_repo

    Get all the repo's review_comments. These are sorted in the order of creation time. Seems cumbersome to use, since one can get all the review comments for a particular PR through `async_get_review_comments`. **Won't use**

* async_get_review_comment

    Get the PR's review comment. The response is identical to `async_list_review_comments`. **Won't use**

* **async_get**

    Get the full PR. There are some attributes, which the PR, obtained through `async_list`, doesn't have: `mergeable`,`rebaseable`,`mergeable_state`,`merged_by`,`comments` (number),`review_comments` (number),`maintainer_can_modify`,`commits` (number),`additions` (number),`deletions` (number).

* **async_list_review_comments**

    Get all the PR's review comments. These are not listed as issue's events.

* *async_list_commits*

    Get all the commits for a particular PR. **Maybe use**

* *async_list_files*

    Get all the files, modified by a particular PR. Each file has `changed`, `additions`, `deletions` attributes. **Maybe use**

* async_check_if_merged

    Check whether a particular PR is merged. The body is empty, the result is in the return code: `204` - merged, `404` - not merged. Such an info is contained in the full PR (`async_get`) in `merged` attribute. **Won't use**

* async_list_requested_reviewers

    Get all the requested reviewers for a particular issue. The response doesn't differ from full PR (`async_get`) in `requested_reviewers` and `requested_teams` attributes. **Won't use**

* async_list_reviews

    Get all the reviews for a particular PR. This doesn't include review comments, only comments (head comment for a review comment). The same response can be obtained via `async_list_events_for_timeline`. One can also get the reviewers of the PR, `state: approved`, or `state: chagnes_requested`. **Won't use**

* async_get_review

    Get the review for a particular PR. The response doesn't differ from `async_list_reviews`. **Won't use**

* async_list_comments_for_review

    Get all the comments for a particular review. The same response can be obtained through `async_list_review_comments`. **Won't use**

### Workflow

Get all the PRs through `async_list_for_repo`, get all the PR's numbers. For each PR, get the full PR via `async_get`, get the PR's review comments via `async_list_review_comments`. Maybe get all the files affected by the PR (`async_list_files`), get all the commits (`async_list_commits`).



## reactions

* async_list_for_commit_comment

    List the reactions to a commit comment. Couldn't find the appropriate comment. Both the review comments and plain comments have reactions in their responses. **Won't use**

* async_list_for_issue_comment

    Get the reactions for an issue comment. Empty body, if there are no reactions, else the list of reactions, with a timestamp and a user, who made the reaction. Both the review comments and plain comments have reactions in their responses (except for a timestamp and a user). **Won't use**

* async_list_for_issue

    Get the reactions for an issue. Empty body, if there are no reactions, else the list of reactions, with a timestamp and a user, who made the reaction. Both the review comments and plain comments have reactions in their responses (except for a timestamp and a user). **Won't use**

* async_list_for_pull_request_review_comment

    Supposedly, get the reactions for a PR review comment. Empty body, if there are no reactions, else the list of reactions, with a timestamp and a user, who made the reaction. Both the review comments and plain comments have reactions in their responses (except for a timestamp and a user). **Won't use**

* async_list_for_release

    Get the reactions for a particular release. Empty body, if there are no reactions, else the list of reactions, with a timestamp and a user, who made the reaction. Both the review comments and plain comments have reactions in their responses (except for a timestamp and a user). **Won't use**

### Workflow

Well, most of the methods have **Won't use** label. That's because, the overall reactions (without user differentiation) seem appropriate and sufficient. If info, such as who placed a reaction and when, is needed, these methods can be used.



## code of conduct

* async_get_all_codes_of_conduct
* async_get_conduct_code

### Workflow

Some code of conducts: `citizen`, `covenant`. **Won't use**



## activity

* async_list_public_events

    Get all the public events for a particular user. **Won't use**

* async_get_feeds

    Feeds. **Won't use**

* *async_list_public_events_for_repo_network*

    Get all the public events for a particular repo. **Maybe use**

* *async_list_public_org_events*

    Get all the events for a particular org. **Maybe use**

* *async_list_repo_events*

    Get all the events for a particular repo. **Maybe use**

* **async_list_stargazers_for_repo**

    Get all the stargazers for a particular repo.

* **async_list_watchers_for_repo**

    Get all the subscribers for a particular repo.

* *async_list_public_events_for_user*

    Get all the public events for a particular user. **Maybe use**

* **async_list_repos_starred_by_user**

    Get all the repos, starred by a particular user.

* **async_list_repos_watched_by_user**

    Get all the repos, to which a particular user is subscribed.

### Workflow

I'd say, events are useless (because I cannot think of a way to use them).
For a particular user, `async_list_repos_watched_by_user`, `async_list_repos_starred_by_user`.
For a particular repo, `async_list_watchers_for_repo`, `async_list_stargazers_by_user`.



## actions

* async_download_artifact

    Need a `repo:read` token permission to download. **Won't use**

* async_get_actions_cache_list

    Get all the actions' caches. **Won't use**

* async_get_artifact

    Get a particular artifact. The response doesn't differ from `async_list_artifacts_for_repo`. **Won't use**

* async_get_workflow

    Get a repo's particular workflow. The response doesn't differ from `async_list_repo_workflows`. **Won't use**

* async_get_workflow_usage

    Billing. **Won't use**

* async_list_artifacts_for_repo

    Get all the artifacts for a particular repo. I assume, artifacts are the result of some job. **Won't use**

* **async_list_repo_workflows**

    Get all the repo's workflows.

* **async_list_workflow_runs**

    Get all the runs for a particular workflow.

### Workflow

List all the workflows with `async_list_repo_workflows`. For each get its runs with `async_list_workflow_runs`.



## checks

* *async_list_for_ref*

    Get all the check runs for a particular commit. **Maybe use**

* *async_list_suites_for_ref*

    Get all the check suites for a particular commit. **Maybe use**



## dependency_graph

* *async_export_sbom*

    Get the packages, this repo depends on. Exports the software bill of materials (SBOM) for a repository in SPDX JSON format. **Maybe use**



## emojis

* async_get

    Get all the emojis, `name: url`. **Won't use**



## gists

Don't want to support



## gitignore

* *async_get_all_templates*

    Get all the templates (just names of languages, which have the template). **Maybe use**

* *async_get_template*

    Get a template for a particular language. **Maybe use**



## licenses

* async_get_all_commonly_used

    Get all the commonly used licenses. **Won't use**

* async_get

    Get info for a particular license. **Won't use**

* **async_get_for_repo**

    Get the repo's license.

### Workflow

For each repo get its license



## git

If one has a tarball of a repo, one also has .git directory with all the commits.
Don't want to support



## meta

* **async_get_octocat**

    Get the octocat with a piece of wisdom

* async_get_zen

    Get a piece of wisdom (with no octocat) **Won't use**

### Workflow

Send a periodic request from the site to get the octocat's wisdom