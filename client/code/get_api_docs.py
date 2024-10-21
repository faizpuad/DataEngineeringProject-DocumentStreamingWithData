# Below serve as example on how this script should look like and not represent the full script
#import related libraru here

# Fetch OpenAPI JSON
response = requests.get("http://localhost:xx/openapi.json")

if response.status_code == 200:
    openapi_json = response.json()

    # Convert JSON to YAML
    openapi_yaml = yaml.dump(openapi_json, sort_keys=False)

    with open("openapi.yaml", "w") as file:
        file.write(openapi_yaml)
    print("OpenAPI documentation saved as openapi.yaml")
else:
    print("Failed to retrieve OpenAPI JSON")
