import yaml
import argparse
from calicoUtils import selector_to_selector_mapping, egress_to_egress_mapping, ingress_to_ingress_mapping, from_to_source_mapping, to_to_destination_mapping

parser = argparse.ArgumentParser(description='file name to parse')
parser.add_argument('policy', type=str, help='relative file path')
args = parser.parse_args()

with open( args.policy, 'r') as file:
    data = yaml.safe_load(file)


resource = {}
resource['apiVersion'] = "projectcalico.org/v3"
resource['kind'] = data['kind'].replace("ANI","")
resource['metadata'] = data['metadata']

resource['spec'] = {}
if 'selector' in data['spec']:
    if 'labels' in data['spec']['selector'] and len(data['spec']['selector']['labels'])>0:
        resource['spec']['selector'] = selector_to_selector_mapping(data['spec']['selector']['labels'])
if 'egress' in data['spec']:
    resource['spec']['egress'] = egress_to_egress_mapping(data['spec']['egress'])
if 'ingress' in data['spec']:
    resource['spec']['ingress'] = ingress_to_ingress_mapping(data['spec']['ingress'])
if 'types' in data['spec']:
    resource['spec']['types'] = data['spec']['types']

with open(resource['metadata']['name']+".yaml",'w') as file:
    yaml.dump(resource,file, default_flow_style=False)


        
