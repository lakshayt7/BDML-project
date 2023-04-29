import urllib.request, json

# Change the limit value passed in this url to 'n' if you want to fetch 'n' traces.
link = 'http://128.105.145.26:16686/api/traces?service=nginx&lookback=2d&prettyPrint=true&limit=1000'
with urllib.request.urlopen(link) as url:
  data = json.load(url)

i = 0
for trace in data["data"]:
  json_object = json.dumps(trace, indent=4)
  with open("./traces/trace" + str(i) + ".json", "w") as out:
    out.write(json_object)
  i = i + 1