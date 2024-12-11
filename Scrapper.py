import requests
from bs4 import BeautifulSoup
from datetime import datetime

def fetch_atcoder(username, start_date, end_date):
    url = f"https://atcoder.jp/users/{username}/history"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    rows = soup.find_all("tr", class_="table-row")
    solved = set()

    for row in rows:
        cols = row.find_all("td")
        if len(cols) < 2:
            continue
        date_str = cols[0].text.strip()
        problem_link = cols[1].find("a")
        if not problem_link:
            continue
        problem_id = problem_link["href"]
        date = datetime.strptime(date_str, "%Y-%m-%d")
        if start_date <= date <= end_date:
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
    url = f"https://vjudge.net/user/{username}"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    rows = soup.find_all("tr")
    solved = set()

    for row in rows:
        cols = row.find_all("td")
        if len(cols) < 6:
            continue
        date_str = cols[5].text.strip()
        try:
            date = datetime.strptime(date_str, "%Y-%m-%d")
        except ValueError:
            continue
        if start_date <= date <= end_date and "Accepted" in cols[3].text:
            problem_id = cols[1].text.strip()
            solved.add(problem_id)

    return len(solved)

def main():
    username_atcoder = "rafiwho"
    username_codeforces = "rafiwho"
    username_vjudge = "rafiwho"

    start_date = datetime(2024, 5, 20)
    end_date = datetime(2024, 12, 10)

    atcoder_count = fetch_atcoder(username_atcoder, start_date, end_date)
    codeforces_count = fetch_codeforces(username_codeforces, start_date, end_date)
    vjudge_count = fetch_vjudge(username_vjudge, start_date, end_date)

    print(f"AtCoder Solved: {atcoder_count}")
    print(f"Codeforces Solved: {codeforces_count}")
    print(f"Vjudge Solved: {vjudge_count}")
    print(f"Total Solved: {atcoder_count + codeforces_count + vjudge_count}")

if __name__ == "__main__":
    main()