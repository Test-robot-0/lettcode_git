import json 
import config
import base64
import requests
from datetime import date
from collections import Counter
import github.modules as modules
import database.repository as repository



def upload_file(path, content, message, generate, new_current_id):

    TOKEN = config.TOKEN
    OWNER = config.OWNER
    REPO  = config.REPO
    url = f"{config.URL}{path}"
    sha = None

    solution_sha, readme_sha = repository.get_sha(new_current_id)
    root_readme_sha = repository.get_root_sha()

    if generate.lower() == "root_readme":
        sha = root_readme_sha
    elif generate.lower() == "solution" :
        sha = solution_sha
    elif generate.lower() == "readme":
        sha = readme_sha

        
    data = {
        "message": message,
        "content": base64.b64encode(content.encode()).decode(),
    }

    if sha is not None:
        data["sha"] = sha



    headers = {
    "Authorization": f"Bearer {TOKEN}",
    "Accept": "application/vnd.github+json"
    }


    r = requests.put(url, headers=headers, json=data)

    if r.status_code == 422 or 409:
                
        sha = modules.get_sha(url, TOKEN)
        data["sha"] = sha
        r = requests.put(url, headers=headers, json=data)
    

    if r.status_code == 200 or 201:
        print(r.json())
        new_sha = r.json()["content"]["sha"]

        if generate.lower() == "root_readme":
            repository.update_root_readme_sha(new_sha)
            

        elif generate.lower() == "solution" :
            repository.update_solution_sha(new_sha, new_current_id)

        elif generate.lower() == "readme":            
            repository.update_readme_sha(new_sha, new_current_id)
    else:
        print("Status code :", r.status_code)
    
    repository.commit()
    #print(path, r.status_code)
    return r.status_code



def gen_readme(new_current_id):

    frontend_id, title, title_slug, difficulty, language, runtime, memory, topic_tags, question, stats = repository.get_readme_solutions(new_current_id)

    readme = f"""
# {frontend_id}.  {title}

{"🟢 Easy" if difficulty == "Easy" else ("🟡 Medium"if difficulty == "Medium" else "🔴 Hard")} &nbsp;&nbsp;&nbsp; ⚙️ {language} &nbsp;&nbsp;&nbsp; ⏱ {runtime} &nbsp;&nbsp;&nbsp; 💾 {memory}



{"&nbsp;&nbsp;&nbsp;".join(f"`{topic_tags[i]["name"]}`" for i in range(0, len(topic_tags)))}


## Overview

<div align="center">
<table>
<tr>

<td valign="top">

<h3> Problem</h3>

|Property            |Value        |
|--------------------|-------------|
|Problem ID          |**{frontend_id}**|
|Difficulty          |**{difficulty}**|
|Leetcode Link       |[link!](https://leetcode.com/problems/{title_slug}/description/)

</td>

<td valign="top">
<h3> Community Stats</h3>


| Metric          | Count                         |
|-----------------|------------------------------:|
|Total Submission |**{stats["totalSubmission"]}** |
|Total Accepted   |**{stats["totalAccepted"]}**   |
|Acceptance Rate  |**{stats["acRate"]}**          |


</td>


</tr>
</table>
</div>


## Question
{question}

<br>
<p align="right">Last Sync: {date.today()} &nbsp;</p>
"""
    
    return readme




def root_gen_readme(new_current_id):

    counter = Counter()

    new = repository.get_table_rootReadme()
    language_table = repository.get_language_by_group()
    tags = repository.get_tags()
    memory_runtime = repository.avg_mem_run()
    avg_memory, avg_runtime = modules.avg_runtime_memory(memory_runtime)
    easy, medium, hard, total = repository.group_difficulty()
    frontend_id, title_slug, difficulty = repository.get_root_readme_solutions(new_current_id)
    

    for row in tags:

        if row and row[0]:
            tag_list = json.loads(row[0])
            cleaned_list = [tag["name"] for tag in tag_list]
            counter.update(cleaned_list)

    updated_counter = counter.most_common(4)


    table = f"\n".join(
    f"| {index} | {i[0]:04} | [{i[1]}]({i[2]}/{i[0]:04}_{i[6]}) | {f"🟢&nbsp;Easy" if i[2] == "Easy" else (f"🟡&nbsp;Medium" if i[2] == "Medium" else f"🔴&nbsp;Hard")} | {i[3]} | {i[4]} | {i[5]} | [Link!](https://leetcode.com/problems/{i[6]}) |"
    for index, i in enumerate(new, start=1)
    )
    
    #tags_batch = " ".join(
    #    f"`{item["name"]}`"
    #    for row in tags
    #    for item in json.loads(row[0])
    #)   

    tags_batch = "&nbsp;".join(
        f"<code>{i}</code>" for i in counter
    ) 

    readme = f"""
# Leetcode Solutions

<div align="center">
{tags_batch}

### Dashboard

<table>
<tr>
<td valign="top">

<h3> Statistics</h3>

| Metric | Count |
|-------|-------------:|
|Total  | **{total}**  |
|Easy   | **{easy}**   |
|Medium | **{medium}** |
|Hard   | **{hard}**   |

</td>

<td valign="top">

<h3> Top Topics</h3>

| Topic | Count |
|-------|------:|
| {updated_counter[0][0]} | **{updated_counter[0][1]}** |
{f"| {updated_counter[1][0]} | **{updated_counter[1][1]}** |" if len(updated_counter) >= 2 else ""}
{f"| {updated_counter[2][0]} | **{updated_counter[2][1]}** |"if len(updated_counter) >= 3 else ""}
{f"| {updated_counter[3][0]} | **{updated_counter[3][1]}** |"if len(updated_counter) == 4 else ""}


</td>

<td valign="top">

<h3> Languages</h3>

| Language | Count |
|----------|------:|
| {language_table[0][0]} | **{language_table[0][1]}** |
{f"| {language_table[1][0]} | **{language_table[1][1]}** |" if len(language_table) >= 2 else ""}
{f"| {language_table[2][0]} | **{language_table[2][1]}** |"if len(language_table) >= 3 else ""}
{f"| {language_table[3][0]} | **{language_table[3][1]}** |"if len(language_table) == 4 else ""}

</td>

<td valign="top">

<h3> Activity</h3>

| Metric          | Value              |
|-----------------|-------------------:|
| Runtime Avg     | **{avg_runtime}**  |
| Memory Avg      | **{avg_memory}**   |
| Latest Problem  | **[{frontend_id}]({difficulty}/{frontend_id:04}_{title_slug})**|
| Last Updated    | **{date.today()}** |  


</td>
</tr>
</table>
<div>

---

Automatically synchronized from LeetCode.

| # | Id | Problem |   Difficulty  | Language | Runtime | Memory | Leetcode Link |
|---|----|---------|---------------|----------|---------|--------|:-------------:|
{table}

<br>
<p align="right">Last Sync: {date.today()} &nbsp;</p>

"""
    return readme


