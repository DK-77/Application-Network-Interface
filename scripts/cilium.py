import yaml
import argparse
from ciliumUtils import kind_to_kind_mapping, selector_to_endpointSelector_mapping, egress_to_egress_mapping, ingress_to_ingress_mapping

parser = argparse.ArgumentParser(description='file name to parse')
parser.add_argument('policy', type=str, help='relative file path')
args = parser.parse_args()

with open( args.policy, 'r') as file:
    data = yaml.safe_load(file)

resource = {}
resource['apiVersion'] = 'cilium.io/v2'
resource['kind'] = kind_to_kind_mapping(data['kind'])
resource['metadata'] = data['metadata']

resource['spec'] = {}
if 'selector' in data['spec']:
    if 'labels' in data['spec']['selector'] and len(data['spec']['selector']['labels'])>0:
        resource['spec']['endpointSelector'] = {}
        resource['spec']['endpointSelector']['matchLabels'] = selector_to_endpointSelector_mapping(data['spec']['selector']['labels'])
if 'egress' in data['spec']:
    resource['spec']['egress'] = egress_to_egress_mapping(data['spec']['egress'])
if 'ingress' in data['spec']:
    resource['spec']['ingress'] = ingress_to_ingress_mapping(data['spec']['ingress'])

with open(resource['metadata']['name']+".yaml",'w') as file:
    yaml.dump(resource,file, default_flow_style=False)