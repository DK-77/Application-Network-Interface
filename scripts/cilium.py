import yaml
import copy
from ciliumUtils import policy_name,set_src_endpointSelector,set_dst_endpointSelector,set_src_ingress_and_egress,set_dst_ingress_and_egress

def parseToCiliumPolicy(file):

    with open( file, 'r') as file:
        data = yaml.safe_load(file)

    resource = {}
    resource['apiVersion'] = 'cilium.io/v2'
    resource['kind'] = data['kind'].replace("ANI","Cilium") # need to look into it
    resource['metadata'] = data['metadata']

    resource['spec'] = {}
    
    if 'control-policies' in data['spec']:
        
        resources = {}  # dict of all the resources for which policies need to be made and corresponding policies.
        
        for i,policy in enumerate(data['spec']['control-policies']):
            labels_src,labels_dst = policy_name(i,policy)
            if labels_src != '':
                src = copy.deepcopy(resource)
                dst = copy.deepcopy(resource)
                src['metadata']['name'] = labels_src
                dst['metadata']['name'] = labels_dst
                src = set_src_endpointSelector(src,policy['source']['labels'])
                dst = set_dst_endpointSelector(dst,policy['destination']['labels'])
                resources[labels_src] = src
                resources[labels_dst] = dst
        
        for i,policy in enumerate(data['spec']['control-policies']):
            labels_src,labels_dst = policy_name(i,policy)
            if labels_src in resources:
                resources[labels_src] = set_src_ingress_and_egress(resources[labels_src],policy)
            if labels_dst in resources:
                resources[labels_dst] = set_dst_ingress_and_egress(resources[labels_dst],policy)

    else:
        print("No Control-Policies Specified.\n")

    for key,value in resources.items():
        with open(key+".yaml",'w') as file:
            yaml.dump(value,file, default_flow_style=False)