#!/usr/bin/env python3
"""
Update star counts for all profiles in the awesome list.
Usage: GITHUB_TOKEN=xxx python scripts/update_stars.py
"""
import json, urllib.request, time, os, re

TOKEN = os.environ.get('GITHUB_TOKEN', '')

def gh_api(url):
    headers = {'User-Agent': 'awesome-profile-updater'}
    if TOKEN:
        headers['Authorization'] = f'token {TOKEN}'
    req = urllib.request.Request(url, headers=headers)
    with urllib.request.urlopen(req, timeout=15) as resp:
        return json.loads(resp.read())

def get_total_stars(username):
    stars = 0
    page = 1
    while True:
        repos = gh_api(f"https://api.github.com/users/{username}/repos?per_page=100&page={page}&type=owner")
        if not repos:
            break
        for repo in repos:
            stars += repo.get('stargazers_count', 0)
        if len(repos) < 100:
            break
        page += 1
    return stars

def get_user_info(username):
    try:
        data = gh_api(f"https://api.github.com/users/{username}")
        stars = get_total_stars(username)
        return {
            'stars': stars,
            'followers': data.get('followers', 0),
            'name': data.get('name') or username,
            'bio': data.get('bio') or '',
            'avatar': data.get('avatar_url', ''),
        }
    except Exception as e:
        print(f"  Error: {username}: {e}")
        return None

# Extract usernames from README
with open('README.md') as f:
    content = f.read()

usernames = list(dict.fromkeys(re.findall(r'https://github\.com/([a-zA-Z0-9_-]+)\)', content)))
print(f"Found {len(usernames)} unique users")

results = {}
for i, username in enumerate(usernames):
    print(f"[{i+1}/{len(usernames)}] {username}...", end=' ', flush=True)
    info = get_user_info(username)
    if info:
        results[username] = info
        print(f"⭐{info['stars']:,}")
    time.sleep(0.2 if TOKEN else 1.0)

with open('data/user_stars.json', 'w') as f:
    json.dump(results, f, indent=2, ensure_ascii=False)

print(f"\nSaved {len(results)} user records to data/user_stars.json")
print("Now re-run the README generation to sort by updated stars.")
