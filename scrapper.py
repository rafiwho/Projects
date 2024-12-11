import requests 
from bs4 import BeautifulSoup 
from datetime import datetime, timezone 
 
 
def fetch_atcoder(username, start_date, end_date): 
    start_epoch = int(start_date.replace(tzinfo=timezone.utc).timestamp()) 
    end_epoch = int(end_date.replace(tzinfo=timezone.utc).timestamp()) 
 
    url = f"https://kenkoooo.com/atcoder/atcoder-api/v3/user/submissions?user={username}&from_second={start_epoch}" 
    response = requests.get(url) 
    data = response.json() 
    solved = set() 
 
    cnt = 0 
    for submission in data: 
        if submission["result"] == "AC": 
            cnt += 1 
         
        epoch_time = submission["epoch_second"] 
 
        if submission["result"] == "AC" and start_epoch <= epoch_time <= end_epoch: 
            problem_id = submission["problem_id"] 
            solved.add(problem_id) 
 
    return len(solved) 
 
def fetch_codeforces(username, start_date, end_date): 
    url = f"https://codeforces.com/api/user.status?handle={username}" 
    response = requests.get(url).json() 
    solved = set() 
 
    if response["status"] != "OK": 
        raise Exception("Error fetching Codeforces data") 
 
    for submission in response["result"]: 
        timestamp = datetime.fromtimestamp(submission["creationTimeSeconds"]) 
        if start_date <= timestamp <= end_date and submission["verdict"] == "OK": 
            problem_id = (submission["problem"]["contestId"], submission["problem"]["index"]) 
            solved.add(problem_id) 
 
    return len(solved) 
 
def fetch_vjudge(username, start_date, end_date): 
    solved = set() 
 
    for i in range(0, 500, 20): 
        url = f"https://vjudge.net/status/data?draw=1&start={i}&length=20&un={username}&OJId=All&probNum=&res=1&language=&onlyFollowee=false&orderBy=run_id&_=1733989696512" 
        response = requests.get(url) 
        data = response.json() 
 
        for submission in data["data"]: 
            unix_time = submission["time"] 
            date = datetime.fromtimestamp(unix_time / 1000, timezone.utc).strftime("%Y-%m-%d") 
            submission_date = datetime.strptime(date, "%Y-%m-%d") 
 
            if start_date <= submission_date <= end_date and submission["status"] == "Accepted": 
                problem_id = submission["problemId"] 
                solved.add(problem_id) 
 
    return len(solved) 
 
def main(): 
    username_atcoder = "rafiwho" 
    username_codeforces = "rafiwho" 
    username_vjudge = "rafiwho" 
 
    start_date = datetime(2024, 5, 20) 
    end_date = datetime(2024, 12, 10) 
 
    atcoder_count = fetch_atcoder(username_atcoder,start_date,end_date) 
    codeforces_count = fetch_codeforces(username_codeforces, start_date, end_date) 
    vjudge_count = fetch_vjudge(username_vjudge, start_date, end_date) 
 
    print(f"AtCoder Solved: {atcoder_count}") 
    print(f"Codeforces Solved: {codeforces_count}") 
    print(f"Vjudge Solved: {vjudge_count}") 
    print(f"Total Solved: {atcoder_count + codeforces_count + vjudge_count}") 
 
if __name__ == "__main__": 
    main()