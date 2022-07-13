import json


def parse_sunburst(csv: str):
    reverse_dict = {}

    # go through each line of results, excluding the header
    for line in csv.split('\n')[1:-1]:
        iri, label, parent, count = [elem.strip() for elem in line.split(',')]
        
        try:
            reverse_dict[parent].append({'iri': iri, 'label': label, 'count': count})
        except KeyError:
            reverse_dict[parent] = [{'iri': iri, 'label': label, 'count': count}]

    #base_node = {'iri': 'http://www.w3.org/2002/07/owl#Thing', 'label': 'Thing'}
    base_node = {'iri': 'http://purl.obolibrary.org/obo/BFO_0000001', 'label': 'Entity'}

    return json.dumps(make_children(base_node, reverse_dict))

def make_children(node, reverse_dict):

    obj = {'name': node['label'], 'iri': node['iri']}
    if node['iri'] in reverse_dict:
        children = []
        for child in reverse_dict[node['iri']]:
            children.append(make_children(child, reverse_dict))
        obj['children'] = children
    else:
        obj['size'] = node['count']
    
    return obj

    