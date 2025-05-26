import requests
import json
import urllib.parse

username = "XStrachey"
repos = requests.get(f"https://api.github.com/users/{username}/repos").json()

language_totals = {}
for repo in repos:
    lang_url = repo.get('languages_url')
    langs = requests.get(lang_url).json()
    for lang, count in langs.items():
        language_totals[lang] = language_totals.get(lang, 0) + count

total = sum(language_totals.values())
language_percent = {k: round(v / total * 100, 1) for k, v in language_totals.items() if total > 0}

labels = list(language_percent.keys())
data = list(language_percent.values())

chart = {
    "type": "radar",
    "data": {
        "labels": labels,
        "datasets": [{
            "label": "Language Usage",
            "data": data,
            "backgroundColor": "rgba(34,202,236,0.2)",
            "borderColor": "rgba(34,202,236,1)"
        }]
    }
}

encoded_chart = urllib.parse.quote(json.dumps(chart))
img_url = f"https://quickchart.io/chart?c={encoded_chart}"

start_tag = "<!-- radar-start -->"
end_tag = "<!-- radar-end -->"

with open("README.md", "r") as f:
    content = f.read()

before = content.split(start_tag)[0] + start_tag + "\n"
after = "\n" + end_tag + content.split(end_tag)[1]

new_section = f"![Language Radar]({img_url})"
with open("README.md", "w") as f:
    f.write(before + new_section + after)
