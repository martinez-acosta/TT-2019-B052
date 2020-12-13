import langs.gdmLang as gdm
from pyecore.resources import ResourceSet, URI
from pyecore.resources.xmi import XMIResource


def saveModel(model):
    # create a resourceSet that hold the contents of the gdm.ecore model and the instances we use/create
    rset = ResourceSet()
    # register the metamodel (available in the generated files)
    rset.metamodel_registry[gdm.nsURI] = gdm
    rset.resource_factory['gdm'] = lambda uri: XMIResource(uri)  

    resource = rset.create_resource(URI('Static_model_test.xmi'))
    resource.append(model)
    resource.save()
    return

def getEntity(model, name):
    entity = ''
    for item in model.entities.items:
        if item.name == name:
            entity = item
            break

    return entity

def populateEntity(model, lines, i):
    line = lines[i]
    name = line.split()[1]
    entity = getEntity(model, name)
    count = 1

    # entramos en un ciclo while hasta encontrar un '}' que indica fin de la entidad
    while not "}" in lines[i+count]:
        ln = lines[i+count].split()
        count += 1
        if "id" in ln[0]:                    
            attribute = gdm.Attribute(name=ln[1], type=ln[0].upper(),unique=True) 
            entity.features.append(attribute)
        
        if "text" in ln[0] and "[" in ln[0]:
            # Si es un arreglo
            x = ln[0].split("[")
            tipo = x[0]
            cardinalidad = x[1].split("]")[0]

            attribute = gdm.Attribute(name=ln[1], type=tipo.upper(), cardinality=cardinalidad)
            entity.features.append(attribute)
        elif "text" in ln[0]:

            attribute = gdm.Attribute(name=ln[1], type=ln[0].upper())
            entity.features.append(attribute) 
        
        if "number" in ln[0] and "[" in ln[0]:
            # Si es un arreglo
            x = ln[0].split("[")
            tipo = x[0]
            cardinalidad = x[1].split("]")[0]

            attribute = gdm.Attribute(name=ln[1], type=tipo.upper(), cardinality=cardinalidad)
            entity.features.append(attribute)
        elif "number" in ln[0]:
            attribute = gdm.Attribute(name=ln[1], type=ln[0].upper())
            entity.features.append(attribute) 
        
        
        if "ref" in ln[0]:
            name = ln[2]
            referencia = getEntity(model,ln[1].split("[")[0])
            cardinalidad = ln[1].split("[")[1].split("]")[0]

            reference = gdm.Reference(name=name, cardinality=cardinalidad, entity=referencia)
            entity.features.append(reference) 

    return

def main():

    # Creamos el modelo GDM
    model = gdm.Model()
    
    #userEntity = gdm.Entity(name="User")
    #venuesModel.entities.append(userEntity)
    
    input_file = open('gdm/venues.gdm', 'r') 
    lines = input_file.readlines()
    
    # Primero creamos las entidades, porque las necesitamos para crear las referencias
    for line in lines:
        if "entity " in line:
            entity = gdm.Entity(name=line.split()[1])
            model.entities.append(entity)

    # Parseamos el documento
    for i in range(len(lines)):
        line = lines[i]
        
        # Ignoramos los comentarios
        if "/*" in line or "* " in line or "*/" in line:
            continue
        
        # Si hay una entidad
        if "entity" in line:
            populateEntity(model, lines, i)
        
        # Si hay una consulta
        if "query" in line:
            
            continue
    saveModel(model)



if __name__ == '__main__':
    main()
