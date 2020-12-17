import json 
import xmltodict 
from queue import LifoQueue


x = 0

def getPrimitiveField(item):
    obj = {
        'name': item['@name'],
        'type': item['@type'],
        'subtype': 'PrimitiveField',
        'figure': 'Decision',
        'color': '#be4b15'
        }
    return obj

def getItemsDocument(child):
    fields = []
    for field in child['fields']:
        if ( field['@xsi:type'] == 'documentDataModel:PrimitiveField'):
            fields.append(getPrimitiveField(field))    
        if ( field['@xsi:type'] == 'documentDataModel:Document'):
            fields.append({ 
                    'name': field['@name'],
                    'type': field['@xsi:type'],
                    'subtype': 'Document',
                    'figure': 'Rectangle',
                    'color': '#FFD700'
                    }
                )
        if ( field['@xsi:type'] == 'documentDataModel:ArrayField'):
            fields.append({ 
                'name': field['@name'],
                'type': field['@xsi:type'],
                'subtype': 'Array',
                'figure': 'Hexagon',
                'color': '#6ea5f8'
                }
            )    
    return fields

def getItemsArray(child):
    fields = []
    field = child['type']
    if ( field['@xsi:type'] == 'documentDataModel:PrimitiveField'):
        fields.append(getPrimitiveField(field))    
    if ( field['@xsi:type'] == 'documentDataModel:Document'):
        fields.append({ 
                'name': field['@name'],
                'type': field['@xsi:type'],
                'subtype': 'Document',
                'figure': 'Rectangle',
                'color': '#FFD700'
                }
            )
    if ( field['@xsi:type'] == 'documentDataModel:ArrayField'):
        fields.append({ 
            'name': field['@name'],
            'type': field['@xsi:type'],
            'subtype': 'Array',
            'figure': 'Hexagon',
            'color': '#6ea5f8'
            }
        )
    return fields

def generateKey():
    global x
    x = x + 1 
    return x
#input_file = "prueba_ddm.xmi"
input_file = "documents.models/venuesDOC.model"
with open(input_file) as xml_file: 
      
    data_dict = xmltodict.parse(xml_file.read()) 
    xml_file.close() 
  
    # generate the object using json.dumps()  
    # corresponding to json data 
      
    #json_data = json.dumps(data_dict) 

    collections = data_dict['documentDataModel:DocumentDataModel']['collections']
    nodeDataArray = []
    linksDataArray = []

    for collection in collections:
        # Obtenemos el documento raíz
        root = collection['root']
        collection_data = {}
        collection_data['name'] = collection['@name'] 
        collection_data['subtype'] = 'Collection' 
        collection_data['key'] = generateKey()
        stack = LifoQueue(maxsize = 1000)
        collection_data['items'] = []
        
        # Cada elemento del documento raíz puede ser de tipo primitivo, documento o un arreglo
        for field in root['fields']:
            
            # Si es un tipo primitivo
            if ( field['@xsi:type'] == 'documentDataModel:PrimitiveField'):
                collection_data['items'].append(getPrimitiveField(field))
                print(field)

            # Si es un documento
            if ( field['@xsi:type'] == 'documentDataModel:Document'):
                # Añadimos la referencia del documento
                collection_data['items'].append({ 
                    'name': field['@name'],
                    'type': field['@xsi:type'],
                    'subtype': 'Document',
                    'parentKey': collection_data['key'], 
                    #'key': generateKey(),
                    'figure': 'Rectangle',
                    'color': '#FFD700'
                    }
                )
                field['parentKey'] = collection_data['key']
                stack.put(field)
                
                print(field)
            
            # Si es un arreglo
            if ( field['@xsi:type'] == 'documentDataModel:ArrayField'):
                
                 # Añadimos la referencia del arreglo
                 collection_data['items'].append({ 
                     'name': field['@name'],
                     'type': field['@xsi:type'],
                     'subtype': 'Array',
                     'parentKey': collection_data['key'], 
                     #'key': generateKey(),
                     'figure': 'Hexagon',
                     'color': '#6ea5f8'
                     }
                 )
                 field['parentKey'] = collection_data['key']
                 stack.put(field)
                 print(field)         
        
        while not stack.empty():
            child =  stack.get()
            
            # Si es un documento
            if ( child['@xsi:type'] == 'documentDataModel:Document'):
                # Añadimos la referencia del documento
                items = getItemsDocument(child)
                new_key_parent = generateKey()
                nodeDataArray.append({ 
                    'name': child['@name'],
                    'type': child['@xsi:type'],
                    'items': items,
                    'subtype': 'Document',
                    'parentKey': child['parentKey'],
                    'key': new_key_parent,
                    'figure': 'Rectangle',
                    'color': '#FFD700'
                    }
                )
                # nodeDataArray.append(getDocument(field))
                for i in child['fields']:
                    i['parentKey'] = new_key_parent
                    stack.put(i)
            print(field)
            
            # Si es un arreglo
            if ( child['@xsi:type'] == 'documentDataModel:ArrayField'):  
                items = getItemsArray(child)
                 # Añadimos la referencia del arreglo

                new_key_parent = generateKey()
                nodeDataArray.append({ 
                     'name': child['@name'],
                     'type': child['@xsi:type'],
                     'items': items,
                     'subtype': 'Array',
                     'parentKey': child['parentKey'],
                     'key': new_key_parent,
                     'figure': 'Hexagon',
                     'color': '#6ea5f8'
                     }
                 )
                child['type']['parentKey'] = new_key_parent
                stack.put(child['type'])

            # Obtenemos contenidos de cada hijo recursivamente

            print(child)


        
        nodeDataArray.append(collection_data) 
    
    for node in nodeDataArray:
        if node['subtype'] != 'Collection':
            linksDataArray.append({
                'to': node['parentKey'] , 'from': node['key']
                })
        
    # Write the json data to output  
    # json file 
    data = {}
    json_nodeDataArray = json.dumps(nodeDataArray)
    json_linksDataArray = json.dumps(linksDataArray) 
    data["nodeDataArray"] = nodeDataArray 
    data["linkDataArray"] = linksDataArray
    ofile = "venuesLalo.json"
    with open(ofile, "w") as json_file:
        json_file.write(json.dumps(data)) 
        #json_file.write(json_nodeDataArray) 
        #json_file.write(json_linksDataArray)
        
        json_file.close() 

    prueba = "pausa"