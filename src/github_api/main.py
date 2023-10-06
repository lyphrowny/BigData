from githubkit import GitHub, TokenAuthStrategy, Response

import orjson

import anyio

from itertools import count, pairwise
from functools import partial
# 60
github = GitHub(TokenAuthStrategy("your_token_here")


def split_into_n_sized_chunks(iterable, chunk_size):
    idxs = pairwise(range(0, len(iterable) + chunk_size, chunk_size))
    return [iterable[slice(*slic)] for slic in idxs]


async def write(where: anyio.Path, what: bytes):
    await where.write_bytes(orjson.dumps(orjson.Fragment(what)))


def construct_path(what, root: anyio.Path, suffix=".json"):
    return root.joinpath(what).with_suffix(suffix)


def producer(coro):
    async def wrapper(*a, name, send_channel, **kw):
        async with send_channel:
            await send_channel.send((name, await coro(*a, **kw)))

    return wrapper


def consumer(misc, recieve_channel):
    async def wrapper():
        async with recieve_channel:
            async for key, value in recieve_channel:
                misc[key] = value

    return wrapper


async def get_repo_misc(**load):
    global github
    gr = github.rest

    misc = {}

    async with anyio.create_task_group() as tg:
        send_channel, recieve_channel = anyio.create_memory_object_stream[dict]()
        async with send_channel, recieve_channel:
            for coro_name, coro in {
                "full_repo": gr.repos.async_get,
                "langs": gr.repos.async_list_languages,
                "profile": gr.repos.async_get_community_profile_metrics,
                "readme": gr.repos.async_get_readme,
                "deps": gr.dependency_graph.async_export_sbom,
            }.items():
                tg.start_soon(
                    partial(
                        producer(coro),
                        **load,
                        name=coro_name,
                        send_channel=send_channel.clone(),
                    )
                )
            tg.start_soon(consumer(misc, recieve_channel.clone()))
    return misc


def _producer(coro):
    async def wrapper(*a, send_channel, **kw):
        async with send_channel:
            await send_channel.send(await coro(*a, **kw))

    return wrapper


def _consumer(store: list, recieve_channel):
    async def wrapper():
        async with recieve_channel:
            async for value in recieve_channel:
                store.append(value)

    return wrapper


async def get_pages(coro, *, n_concur, per_page: int = 100, page_num: int = 0, **load):
    if page_num < 0:
        raise RuntimeError("page_num(%i) is < 0" % page_num)
    if page_num:
        return (await coro(per_page=per_page, page=page_num, **load),)

    pages = []
    page_num = count(1)
    has_data = True

    while has_data:
        curr_pages = []
        async with anyio.create_task_group() as tg:
            send_channel, recieve_channel = anyio.create_memory_object_stream[
                Response
            ]()
            async with send_channel, recieve_channel:
                for _ in range(n_concur):
                    tg.start_soon(
                        partial(
                            _producer(coro),
                            send_channel=send_channel.clone(),
                            per_page=per_page,
                            page=next(page_num),
                            **load,
                        )
                    )
                tg.start_soon(_consumer(curr_pages, recieve_channel.clone()))

        curr_pages = list(filter(lambda v: v.content != b"[]", curr_pages))
        if len(curr_pages) != n_concur:
            has_data = False
        pages.extend(curr_pages)

    return pages


def __producer(coro):
    async def wrapper(*a, obj, send_channel, **kw):
        async with send_channel:
            await send_channel.send((obj, await coro(*a, **kw)))

    return wrapper


def __consumer(store: dict, recieve_channel):
    async def wrapper():
        async with recieve_channel:
            async for key, value in recieve_channel:
                store[key] = value

    return wrapper


async def get_list(coro, _list, _list_kws, n_concur, **load):
    if n_concur <= 0:
        raise RuntimeError("n_concur (%i) should be > 0")

    res = {}
    for objs in split_into_n_sized_chunks(_list, n_concur):
        async with anyio.create_task_group() as tg:
            send_channel, recieve_channel = anyio.create_memory_object_stream[
                Response
            ]()
            async with send_channel, recieve_channel:
                for obj in objs:
                    if not isinstance(obj, (list, tuple)):
                        load.update({_list_kws[0]: obj})
                    else:
                        load.update({*zip(_list_kws, obj)})
                    tg.start_soon(
                        partial(
                            __producer(coro),
                            obj=obj,
                            send_channel=send_channel.clone(),
                            **load,
                        )
                    )
                tg.start_soon(__consumer(res, recieve_channel.clone()))

    return res


async def mkdir(what):
    path = anyio.Path(what)
    await path.mkdir(parents=True, exist_ok=True)
    return path


async def main():
    global github

    gr = github.rest

    print((await gr.rate_limit.async_get()).parsed_data.resources.core)
    # exit(0)
    # owner, repo = "python-trio pytest-trio".split()
    owner, repo = "pdm-project pdm".split()
    # owner, repo = "pre-commit pre-commit-hooks".split()
    load = {"owner": owner, "repo": repo}

    n_concur = 10

    users_path = await mkdir("data/temp/users")

    root_path = anyio.Path(f"data/temp/repos/{repo}")
    await root_path.mkdir(parents=True, exist_ok=True)

    rpath = partial(construct_path, root=anyio.Path(""))
    misc = await get_repo_misc(**load)

    misc_path = await mkdir(root_path.joinpath("misc"))
    for key, value in misc.items():
        await write(rpath(misc_path.joinpath(key)), value.content)

    repo = orjson.loads(misc["full_repo"].content)["full_name"]

    contrib_pages = await get_pages(
        gr.repos.async_list_contributors, n_concur=10, **load
    )
    logins = [
        contrib["login"]
        for page in contrib_pages
        for contrib in orjson.loads(page.content)
    ]
    repo_contribs_path = await mkdir(root_path.joinpath("contribs"))
    await write(rpath(repo_contribs_path.joinpath("contribs")), str(logins))

    full_users = await get_list(
        gr.users.async_get_by_username,
        logins,
        _list_kws=("username",),
        n_concur=n_concur,
    )

    for uname, full_user in full_users.items():
        u_path = await mkdir(users_path.joinpath(uname))
        await write(rpath(u_path.joinpath(uname)), full_user.content)

    commit_pages = await get_pages(
        gr.repos.async_list_commits, n_concur=n_concur, **load
    )
    commits_path = await mkdir(root_path.joinpath("commits"))
    await write(
        rpath(commits_path.joinpath("all_commits")),
        str([page.content for page in commit_pages]),
    )

    shas = [
        commit["sha"] for page in commit_pages for commit in orjson.loads(page.content)
    ]
    commits = await get_list(
        gr.repos.async_get_commit, shas, _list_kws=("ref",), n_concur=n_concur, **load
    )
    cmts_path = await mkdir(commits_path.joinpath("commits"))
    for sha, full_commit in commits.items():
        await write(rpath(cmts_path.joinpath(sha)), full_commit.content)

    print("wrote commits")

    issues_pages = await get_pages(
        gr.issues.async_list_for_repo, n_concur=n_concur, **load, state="all"
    )
    issues_path = await mkdir(root_path.joinpath("issues"))
    await write(
        rpath(issues_path.joinpath("all_issues")),
        str([page.content for page in issues_pages]),
    )
    issue_numbers = [
        issue["number"] for page in issues_pages for issue in orjson.loads(page.content)
    ]
    issues = await get_list(
        gr.issues.async_get,
        issue_numbers,
        _list_kws=("issue_number",),
        n_concur=n_concur,
        **load,
    )
    iss_path = await mkdir(issues_path.joinpath("issues"))
    iss_dirs = {}
    for is_num, issue in issues.items():
        iss_dirs[is_num] = await mkdir(iss_path.joinpath(f"{is_num:06}"))
        await write(rpath(iss_dirs[is_num].joinpath("issue")), issue.content)

    print("wrote issues")

    # TODO
    #  add pages to timelines
    timelines = await get_list(
        gr.issues.async_list_events_for_timeline,
        issue_numbers,
        _list_kws=("issue_number",),
        n_concur=n_concur,
        **load,
        per_page=100,
    )
    for is_num, timeline in timelines.items():
        await write(rpath(iss_dirs[int(is_num)].joinpath("timeline")), timeline.content)

    print("wrote timelines")

    pulls_numbers = [
        issue["number"]
        for page in issues_pages
        for issue in orjson.loads(page.content)
        if "pull_request" in issue
    ]
    p_reviews = await get_list(
        gr.pulls.async_list_review_comments,
        pulls_numbers,
        _list_kws=("pull_number",),
        n_concur=n_concur,
        **load,
    )
    for p_num, review in p_reviews.items():
        await write(rpath(iss_dirs[p_num].joinpath("review_comments")), review.content)

    print((await gr.rate_limit.async_get()).parsed_data.resources.core)

    # TODO
    #  add return
    #  guess, dict[key] = Response is OK


if __name__ == "__main__":
    anyio.run(main, backend="asyncio")
