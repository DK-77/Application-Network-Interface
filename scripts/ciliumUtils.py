def policy_name(i,policy):
    labels_src = ''
    labels_dst = ''
    if 'labels' in policy['source'] and 'labels' in policy['destination']:

        for ind,label in enumerate(policy['source']['labels']):    
            for key,value in label.items():    
                if ind == 0:
                    labels_src += key + " == " + value
                else:
                    labels_src += " && " + key + " == " + value

        for ind,label in enumerate(policy['destination']['labels']):    
            for key,value in label.items():    
                if ind == 0:
                    labels_dst += key + " == " + value
                else:
                    labels_dst += " && " + key + " == " + value

    else:
        ## need to check other selection criteria
        print(f"Cannot generate a policy as no labels are mentioned for source or destination in rule number - {i+1}")
    return labels_src,labels_dst

def set_src_endpointSelector(src,labels):
    src['spec']['endpointSelector'] = {}
    src['spec']['endpointSelector']['matchLabels'] = {}
    for label in labels:
        for key,value in label.items():
            src['spec']['endpointSelector']['matchLabels'][key] = value
    return src

def set_dst_endpointSelector(dst,labels):
    dst['spec']['endpointSelector'] = {}
    dst['spec']['endpointSelector']['matchLabels'] = {}
    for label in labels:
        for key,value in label.items():
            dst['spec']['endpointSelector']['matchLabels'][key] = value
    return dst

def set_src_ingress_and_egress(src_policy,rule):
    
    if rule['action'] == 'allow':

        dct1 = {}
        dct1['fromEndpoints'] = []
        dct2 = {}
        dct2['matchLabels'] = {}
        for r in rule['destination']['labels']:
            for key,value in r.items():
                dct2['matchLabels'][key] = value
        dct1['fromEndpoints'].append(dct2) 

        if 'ingress' not in src_policy['spec']:
            src_policy['spec']['ingress'] = []

        src_policy['spec']['ingress'].append(dct1)
        
        dct1 = {}
        dct1['toEndpoints'] = []
        dct2 = {}
        dct2['matchLabels'] = {}
        for r in rule['destination']['labels']:
            for key,value in r.items():
                dct2['matchLabels'][key] = value
        dct1['toEndpoints'].append(dct2) 

        if 'egress' not in src_policy['spec']:
            src_policy['spec']['egress'] = []
        
        src_policy['spec']['egress'].append(dct1)    
    
    else:

        dct1 = {}
        dct1['fromEndpoints'] = []
        dct2 = {}
        dct2['matchLabels'] = {}
        for r in rule['destination']['labels']:
            for key,value in r.items():
                dct2['matchLabels'][key] = value
        dct1['fromEndpoints'].append(dct2) 

        if 'ingressDeny' not in src_policy['spec']:
            src_policy['spec']['ingressDeny'] = []

        src_policy['spec']['ingressDeny'].append(dct1)
        
        dct1 = {}
        dct1['toEndpoints'] = []
        dct2 = {}
        dct2['matchLabels'] = {}
        for r in rule['destination']['labels']:
            for key,value in r.items():
                dct2['matchLabels'][key] = value
        dct1['toEndpoints'].append(dct2) 

        if 'egressDeny' not in src_policy['spec']:
            src_policy['spec']['egressDeny'] = []
        
        src_policy['spec']['egressDeny'].append(dct1)
    
    return src_policy

def set_dst_ingress_and_egress(dst_policy,rule):

    if rule['action'] == 'allow':

        dct1 = {}
        dct1['fromEndpoints'] = []
        dct2 = {}
        dct2['matchLabels'] = {}
        for r in rule['source']['labels']:
            for key,value in r.items():
                dct2['matchLabels'][key] = value
        dct1['fromEndpoints'].append(dct2) 

        if 'ingress' not in dst_policy['spec']:
            dst_policy['spec']['ingress'] = []

        dst_policy['spec']['ingress'].append(dct1)
        
        dct1 = {}
        dct1['toEndpoints'] = []
        dct2 = {}
        dct2['matchLabels'] = {}
        for r in rule['source']['labels']:
            for key,value in r.items():
                dct2['matchLabels'][key] = value
        dct1['toEndpoints'].append(dct2) 

        if 'egress' not in dst_policy['spec']:
            dst_policy['spec']['egress'] = []
        
        dst_policy['spec']['egress'].append(dct1)    
    
    else:

        dct1 = {}
        dct1['fromEndpoints'] = []
        dct2 = {}
        dct2['matchLabels'] = {}
        for r in rule['source']['labels']:
            for key,value in r.items():
                dct2['matchLabels'][key] = value
        dct1['fromEndpoints'].append(dct2) 

        if 'ingressDeny' not in dst_policy['spec']:
            dst_policy['spec']['ingressDeny'] = []

        dst_policy['spec']['ingressDeny'].append(dct1)
        
        dct1 = {}
        dct1['toEndpoints'] = []
        dct2 = {}
        dct2['matchLabels'] = {}
        for r in rule['source']['labels']:
            for key,value in r.items():
                dct2['matchLabels'][key] = value
        dct1['toEndpoints'].append(dct2) 

        if 'egressDeny' not in dst_policy['spec']:
            dst_policy['spec']['egressDeny'] = []
        
        dst_policy['spec']['egressDeny'].append(dct1)
    
    return dst_policy