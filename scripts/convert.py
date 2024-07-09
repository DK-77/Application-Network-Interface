from collections import OrderedDict as od
import yaml
import argparse

parser = argparse.ArgumentParser(description='file name to parse')
parser.add_argument('policy', type=str, help='relative file path')
args = parser.parse_args()


with open( args.policy, 'r') as file:
    data = yaml.safe_load(file)

resource = {}

if( data['apiVersion'] == "ani/v1" ):
    if( data['target'] == "baremetal" ):
        
        if( data['kind'] == "ani-network-policy" and data['cni'] == "calico" ):
            
            resource['apiVersion'] = "projectcalico.org/v3"
            if( data['namespace'] == "all" ):
                resource['kind'] = "GlobalNetworkPolicy"
            else:
                resource['kind'] = "NetworkPolicy"
            
            resource['metadata'] = data['metadata']
            resource['spec'] = {}
            
            types = []
            for val in data['spec']['types']:
                if val == "ingress":
                    types.append("Ingress")
                if val == "egress":
                    types.append("Egress")
            resource['spec']['types'] = types
        
        elif( data['kind'] == "ani-network-policy" and data['cni'] == "cilium" ):
            
            resource['apiVersion'] = "cilium.io/v2"
            if( data['namespace'] == "all" ):
                resource['kind'] = "CiliumClusterwideNetworkPolicy"
            else:
                resource['kind'] = "CiliumNetworkPolicy"
            
            resource['metadata'] = data['metadata']
            resource['spec'] = {}

            if 'endpointSelector' in data['spec']:
                resource['spec']['endpointSelector'] = data['spec']['endpointSelector']
            if 'nodeSelector' in data['spec']:
                resource['spec']['nodeSelector'] = data['spec']['nodeSelector']

            dct1 = {}
            dct2 = {}
            for val in data['spec']['types']:
                
                if val == "ingress":
                    dct1['fromEntities'] = ['all']
                    resource['spec']['ingressDeny'] = []
                    resource['spec']['ingressDeny'].append( dct1 )
                if val == "egress":
                    dct2['toEntities'] = ['all']
                    resource['spec']['egressDeny'] = []
                    resource['spec']['egressDeny'].append( dct2 )

            
    elif( "some other deployment" ):
        pass
elif( "some other version" ):
    pass

with open(resource['metadata']['name']+".yaml",'w') as file:
    yaml.dump(resource,file, default_flow_style=False)
