import json

with open("retire_output.json", "r") as f:
    data = json.load(f)

main_data = data['data']

unique_dicts = []

for item in main_data:
    results = item['results']

    if results:
        component_key = 'component'
        version_key = 'version'

        component_value = results[0].get(component_key)
        version_value = results[0].get(version_key)

        vulnerabilities = results[0]['vulnerabilities']

        for vuln in vulnerabilities:
            current_dict = {
                component_key: component_value,
                version_key: version_value,
                "justification": "False Positive"
            }
            if vuln['severity'] == "high" and current_dict not in unique_dicts:
                unique_dicts.append(current_dict)

print("[")
for index, item in enumerate(unique_dicts):
    print(json.dumps(item, indent=4), end="")
    if index != len(unique_dicts) - 1:  # if it's not the last item
        print(",")
    else:
        print("\n",end="")
print("]")
