import requests
import json
from datetime import datetime, date, timedelta
import time
import sys



USEFULL_OWNER_KEYS = {"type", "site_admin"}
USEFULL_KEYS = {"id",
                "owner",
                "fork",
                "created_at",
                "updated_at",
                "pushed_at",
                "size",
                "stargazers_count",
                "watchers_count",
                "language",
                "has_issues",
                "has_projects",
                "has_downloads",
                "has_wiki",
                "has_pages",
                "has_discussions",
                "forks_count",
                "mirror_url",
                "archived",
                "disabled",
                "open_issues_count",
                "license",
                "allow_forking",
                "is_template",
                "web_commit_signoff_required",
                "topics",
                "default_branch",
                "permissions",
                "network_count",
                "subscribers_count"}


def get_usefull_dict(raw: dict):
    keys = list(raw.keys())
    for key in keys:
        if key not in USEFULL_KEYS:
            raw.pop(key)
    # owner_keys = list(raw['owner'].keys())

    # for key in owner_keys:
    #     if key not in USEFULL_OWNER_KEYS:
    #         raw['owner'].pop(key)

    return raw

def infinite_requester(start_from):
    auth = ('', '')
    url = lambda _page: f"https://api.github.com/search/repositories?page={_page}" \
                               f"&sort=forks&per_page=100"

    response = requests.get(url(start_from), auth=auth)
    if response.status_code != 200:
        raise Exception
    raw = response.json()
    prepared = get_usefull_dict(raw)
    prepared['last_page'] = start_from
    return prepared






def save_repos_list(start_date: date, end_date: date):
    list_of_jsons = []
    DAY_INCREMENT = timedelta(days=1)
    auth = (sys.argv[1], sys.argv[2])
    tmp_date = start_date
    url = lambda _page, _date: f"https://api.github.com/search/repositories?page={_page}" \
                              f"&per_page=100&q=stars:>5+created:{str(_date)}"
    with tqdm(total=64, ncols=120) as pbar:
        while tmp_date >= end_date:
            for page in range(1, 11):
                str_url = url(page, tmp_date)
                response = requests.get(str_url, auth=auth)
                # prev_t = start_t
                # start_t = time.time()
                if response.status_code != 200:
                    # print(f"Time = {start_t-prev_t}")
                    print(f"Problem: {str_url}; {response.status_code}, {response.reason}")
                    if response.reason == 'rate limit exceeded':
                        print(f'Rate limit exceeded for request {str_url}')
                        time.sleep((60 - datetime.today().minute + 1) * 60)
                        print('Time to wake up')
                    else:
                        break
                raw = response.json()
                total_count = raw['total_count']
                repos = raw['items']

                if len(repos) == 0:
                    break

                for repo in repos:
                    repo_id = repo['id']
                    try:
                        list_of_jsons.append(get_usefull_dict(repo))
                    except Exception as e:
                        print(f"id={repo_id}, url={repo['url']}", e)

                # if total_count % 100 + 1 <= page:
                #     break
            pbar.update(1)
            pbar.set_description(f"Date: {str(tmp_date)}")
            tmp_date = tmp_date - DAY_INCREMENT
        return list_of_jsons


# def sort_by_dates(list_of_jsons):
#     last_date = list_of_jsons[0]['created_at'].split('T')[0]
#     by_dates = []
#     cur_date = []
#     for i in list_of_jsons:
#         cur_date = i['created_at'].split('T')[0]
#         if cur_date == last_date:
#             cur_date.append(i)
#         else:
#             by_dates.append(cur_date)
#             cur_date = list()
#     return by_dates

# if __name__ == "__main__":
#     start = date(2015, 3, 5)
#     end = date(2015, 1, 1)
#
#     save_repos(start, end)