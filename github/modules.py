import requests

def get_sha(url, token):

    headers = {
    "Authorization": f"Bearer {token}",
    "Accept": "application/vnd.github+json"
    }

    r = requests.get(url, headers=headers)

    if r.status_code == 200:
        return r.json()["sha"]
    
    return None

#def get_sha(path):
#    
#    OWNER = "Test-robot-0"
#    REPO = "leetcode"
#    url = f"https://api.github.com/repos/{OWNER}/{REPO}/contents/leetcode-solutions/{path}"
#
#    r = requests.get(url)
#
#    if r.status_code == 200:
#        return r.json()["sha"]
#
#    return "None"
#
#

def avg_runtime_memory(memory_runtime):

    memory_sum = runtime_sum = 0
    memory_count = runtime_count = 1

    for i in memory_runtime:
        
        mem = float(i[0].replace(" MB", ""))
        memory_sum += mem
        memory_count += 1

        run = float(i[1].replace(" ms", ""))
        runtime_sum += run
        runtime_count += 1
    
    return f"{memory_sum/memory_count:.2f} MB", f"{runtime_sum/runtime_count:.2f} ms"

  