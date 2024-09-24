import requests
import yaml

# Fetch OpenAPI JSON
response = requests.get("http://localhost:8000/openapi.json")

if response.status_code == 200:
    openapi_json = response.json()
    
    # Convert JSON to YAML
    openapi_yaml = yaml.dump(openapi_json, sort_keys=False)
    
    with open("openapi.yaml", "w") as file:
        file.write(openapi_yaml)
    print("OpenAPI documentation saved as openapi.yaml")
else:
    print("Failed to retrieve OpenAPI JSON")
