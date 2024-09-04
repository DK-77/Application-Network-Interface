import copy

def action_to_action_mapping(action):
    dict_ingress = {}
    dict_egress = {}
    if action == 'allow':
        dict_ingress['action'] = 'allow'
        dict_egress['action'] = 'allow'
        return dict_ingress, dict_egress
    else:
        dict_ingress['action'] = 'deny'
        dict_egress['action'] = 'deny'
        return dict_ingress, dict_egress

def src_and_dst_to_rules_mapping(i,ingress,egress,src,dst):
    
    ingress_src = copy.deepcopy(ingress)
    egress_src = copy.deepcopy(egress)
    ingress_dst = copy.deepcopy(ingress)
    egress_dst = copy.deepcopy(egress)
    flag = True                       # means the labels are present and policy can be genrated
    src_selector = ''
    dst_selector = ''

    ingress_src['source'] = {}
    egress_src['destination'] = {}

    if 'labels' in dst:
        str1 = ''
        for i,label in enumerate(dst['labels']):    
            for key,value in label.items():    
                if i == 0:
                    str1 += key + " == " + value
                else:
                    str1 += " && " + key + " == " + value
        
        ingress_src['source']['selector'] = str1
        egress_src['destination']['selector'] = str1
        dst_selector = str1
    else:
        ## need to check other selection criteria
        print(f"Cannot generate a policy as no labels are mentioned for source in rule number - {i+1}") 
        flag = False

    ingress_dst['source'] = {}
    egress_dst['destination'] = {}
    
    if 'labels' in src:
        str1 = ''
        for i,label in enumerate(src['labels']):    
            for key,value in label.items():    
                if i == 0:
                    str1 += key + " == " + value
                else:
                    str1 += " && " + key + " == " + value
        ingress_dst['source']['selector'] = str1
        egress_dst['destination']['selector'] = str1
        src_selector = str1
    else:
        ## need to check for other selection criteria
        print(f"Cannot generate a policy as no labels are mentioned for destination in rule number - {i+1}") 
        flag = False

    return ingress_src, egress_src, ingress_dst, egress_dst, src_selector, dst_selector, flag
