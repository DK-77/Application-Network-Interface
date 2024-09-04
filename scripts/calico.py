import yaml
import copy
from calicoUtils import action_to_action_mapping,src_and_dst_to_rules_mapping

def parseToCalicoPolicy(file):
    
    with open( file , 'r') as file:
        data = yaml.safe_load(file)

    resource = {}
    resource['apiVersion'] = "projectcalico.org/v3"
    resource['kind'] = data['kind'].replace("ANI","") # need to look into it
    resource['metadata'] = data['metadata']

    resource['spec'] = {}

    if 'control-policies' in data['spec']:
        
        resource['spec']['egress'] = []
        resource['spec']['ingress'] = []
        ls = []

        for i,policy in enumerate(data['spec']['control-policies']):
            resource_src = copy.deepcopy(resource)
            resource_dst = copy.deepcopy(resource)
            dict_ingress, dict_egress = action_to_action_mapping(policy['action'])
            dict_ingress_src, dict_egress_src, dict_ingress_dst, dict_egress_dst, src_selector, dst_selector, flag = src_and_dst_to_rules_mapping(i,dict_ingress,dict_egress,policy['source'],policy['destination'])
            if flag:
                resource_src['spec']['ingress'].append(dict_ingress_src)
                resource_src['spec']['egress'].append(dict_egress_src)
                resource_dst['spec']['ingress'].append(dict_ingress_dst)
                resource_dst['spec']['egress'].append(dict_egress_dst)
                resource_src['spec']['selector'] = src_selector
                resource_dst['spec']['selector'] = dst_selector
                ls.append(resource_src)
                ls.append(resource_dst)

        for i,resource in enumerate(ls):
            with open("policy-"+str(i+1)+".yaml",'w') as file:
                yaml.dump(resource,file, default_flow_style=False)

    else:
        print("No Control-Policies Specified.\n")


        
