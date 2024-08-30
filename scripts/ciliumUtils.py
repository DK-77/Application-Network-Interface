def kind_to_kind_mapping(str):
    
    if str == 'ANINetworkPolicy':
        return 'CiliumNetworkPolicy'
    else:
        return 'CiliumClusterwideNetworkPolicy'

def selector_to_endpointSelector_mapping(labels):

    dct = {}
    if len(labels) > 1:
        for label in labels:
            pass
    else:
        parts = labels[0].split("=")
        dct[parts[0].strip()] = parts[1].strip()
    return dct

def egress_to_egress_mapping(rule_list):

    lst = []
    for rule in rule_list:
        if 'action' in rule and rule['action'] == 'Allow' and len(rule) == 1:
            dct = {}
            dct['toEntities'] = ['all']
            lst.append(dct)
        # lly for allow with endpoints
        # lly for deny
        # lly for deny with endpoints
    return lst 

def ingress_to_ingress_mapping(rule_list):

    lst = []
    for rule in rule_list:
        if 'action' in rule and rule['action'] == 'Allow' and len(rule) == 1:
            dct = {}
            dct['fromEntities'] = ['all']
            lst.append(dct)
        elif 'action' in rule and rule['action'] == 'Allow' and len(rule) > 1:
            dct = {}
            dct['fromEndpoints'] = []
            dct1 = {}
            dct1['matchLabels'] = {}
            parts = rule['from']['target'].split("=")
            dct1['matchLabels'][parts[0].strip()] = parts[1].strip()
            dct['fromEndpoints'].append(dct1)
            lst.append(dct)
        # lly for deny
        # lly for deny with endpoints 
    return lst