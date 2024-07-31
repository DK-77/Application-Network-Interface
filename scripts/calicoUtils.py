
def from_to_source_mapping(rule):
    
    dct = {}
    dct['action'] = rule['action']
    dct['source'] = {}
    dct['source']['selector'] = rule['from']['target'].replace("=","==")
    return dct

def to_to_destination_mapping(rule):
    
    dct = {}
    dct['action'] = rule['action']
    dct['destination'] = {}
    dct['destination']['selector'] = rule['to']['target'].replace("=","==")
    return dct

def selector_to_selector_mapping(labels):
    
    if len(labels) > 1:
        for str in labels:
            pass
    elif len(labels) == 1:
        pair = labels[0].replace("=","==")
        return pair

def ingress_to_ingress_mapping(rule_list):

    lst = []
    for rule in rule_list:
        if 'from' not in rule:
            lst.append(rule)
        else:
            dct = from_to_source_mapping(rule)
            lst.append(dct)
    return lst

def egress_to_egress_mapping(rule_list):
    
    lst = []
    for rule in rule_list:
        if 'to' not in rule:
            lst.append(rule)
        else:
            dct = to_to_destination_mapping(rule)
            lst.append(dct)
    return lst