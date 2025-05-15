import yaml
import os

# Services you want to extract
services_to_extract = [
    "adservice",
    "checkoutservice",
    "frontend",
    "paymentservice",
    "productcatalogservice"
]

# Paths
input_file = "deployment-service.yml"
output_dir = "k8s-deployments"

# Make sure output directory exists
os.makedirs(output_dir, exist_ok=True)

# Read the deployment-service.yml
with open(input_file, 'r') as f:
    docs = list(yaml.safe_load_all(f))

# Organize resources by service
service_resources = {service: [] for service in services_to_extract}

for doc in docs:
    if doc is None:
        continue
    metadata = doc.get('metadata', {})
    name = metadata.get('name', '')
    for service in services_to_extract:
        if service in name:
            service_resources[service].append(doc)

# Write each service's resources to its own file
for service, resources in service_resources.items():
    if resources:
        output_file = os.path.join(output_dir, f"{service}-deployment.yaml")
        with open(output_file, 'w') as f:
            for resource in resources:
                yaml.dump(resource, f)
                f.write('---\n')

print(f"✅ Done! YAML files are saved in '{output_dir}' folder.")
