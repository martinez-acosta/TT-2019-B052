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

def getQuery(model, name):
    query = ''
    for item in model.queries.items:
        if item.name == name:
            query = item
            break

    return query

def getRefs(entity,inclusion):
    refs = []
    feature_name = inclusion[-1]

    # Si hay una referencia anidada denotadada por más de un "." punto:
    if inclusion[0].count('.') > 1:
        ref = inclusion[0].split(".")[1]
        # primera referencia
        for item in entity.features.items:
            if item.name == ref:
                refs.append(item)
                # referencia anidada
                for i in item.entity.features.items:
                    if i.name == feature_name:
                        refs.append(i)
                        break
    else:
        for item in entity.features.items:
            if item.name == feature_name:
                refs.append(item)
                break
    return refs

def getRefAliasFromQuery(query,reference):
    refAlias = ''
    #Obtener la referencia en la query
    if not reference == query.from_.alias.name:
        for item in query.inclusions.items:
            if item.alias.name == reference:
                refAlias = item.alias
                break
    else:
        refAlias = query.from_.alias
    return refAlias

def getAttributeFromEntity(model, query, reference,attributeReference):
    feature = ''
    # Obtener el atributo de la entidad X por medio de una referencia en query
    
    # Obtenemos la entidad por su referencia
    # Si no está en el elemento from de la query, es una inclusión
    if not reference == query.from_.alias.name:
        for inclusion in query.inclusions.items:
            if inclusion.alias.name == reference:
                for ref in inclusion.refs:
                    if ref.name == reference:
                        entity = ref.entity
                        for i in entity.features.items:
                            if i.name == attributeReference:
                                feature = i
                                break
    else:
        entity = query.from_.entity
        for item in entity.features.items:
            if item.name == attributeReference:
                feature = item
                break
    
    return feature

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

def populateQuery(model, lines, i):
    line = lines[i]
    name = line.split()[1].strip(":")
    query = getQuery(model, name)
    
    
    ###### Elemento From ######
    count = 1
    while not "from " in lines[i+count]:
        count += 1    
    ln = lines[i+count].split()
    entity = getEntity(model,ln[1])
    query.from_ = gdm.From(entity=entity, alias=gdm.Alias(name=ln[3]))

    ###### Elemento Inclusion ######
    count = 1
    while not "including " in lines[i+count]:
        count += 1
    # indicamos inicio de la sección del elemento inclusion
    inclusions = [lines[i+count]]

    # obtenemos fin de la sección del elemento inclusion
    count += 1
    while not "where" in lines[i+count]:
        inclusions.append(lines[i+count])
        count += 1

    inclusions = [s.replace(',', '').replace('\n', '').replace('including','') for s in inclusions]
    inclusions = [s.split() for s in inclusions]


    for inclusion in inclusions:
        ln = inclusion    
        alias = gdm.Alias(name=ln[2])
        refs = getRefs(entity,inclusion)            
        refAlias = query.from_.alias
        
        including = gdm.Inclusion(alias=alias, refAlias=refAlias, refs=refs)

        query.inclusions.append(including)
    
    ##### Elementos Select (Projection) ########
    count = 1
    while not "select " in lines[i+count]:
        count += 1
    # indicamos inicio de la sección de los elementos select
    selects = [lines[i+count]]

    # obtenemos fin de la sección de los elementos select
    count += 1
    while not "from" in lines[i+count]:
        selects.append(lines[i+count])
        count += 1

    selects = [s.replace(',', '').replace('\n', '').replace('select ','') for s in selects]
    selects = [s.split() for s in selects]
    selects = [item for sublist in selects for item in sublist]

    s = []
    for i in range(len(selects)):
        # Revisamos si el siguiente elemento contiene la palabra "as"
        if i+1 < len(selects) and selects[i+1] == "as":
            s.append(selects[i] + " " +selects[i+1] + " " + selects[i+2])
            i += 2
        else:
            s.append(selects[i])
    selects = s
    del s


    for select in selects:
        if " as " in select:
            ln = select.split(".")    
            
            alias = gdm.Alias(name=ln[2])
            attribute = getRefs(entity,inclusion)            
            refAlias = query.from_.alias
            
            projection = gdm.AttributeSelection(refAlias=refAlias, attribute=attribute)
        else:
            ln = select.split(".")    
            
            aliasEntity = ln[0]
            attributeOfAliasEntity = ln[1]
            attribute = getAttributeFromEntity(model, query, aliasEntity,attributeOfAliasEntity)
            refAlias = getRefAliasFromQuery(query,aliasEntity)
            
            projection = gdm.AttributeSelection(refAlias=refAlias, attribute=attribute)
            query.projections.append(projection)
            saveModel(model)

    ##### Elemento Condition #########
    saveModel(model)
    for i in range(len(lines)):
        line = lines[i]
        # Si hay una consulta
        if "query" in line:
            count = 1
            name = line.split()[1].strip(":")
            query = getQuery(model,name)
            
            # Elemento select 
            start_query = lines[i:]
            for j in range(len(start_query)):
                line = start_query[j]
                tmp = 1
                
                while not "select " in start_query[j+tmp]:
                    tmp += 1
                # Obtenemos todos las cadenas select
                start_select = start_query[j+tmp:]
                tmp = 1
                while not "from " in start_select[tmp]:
                    tmp += 1
                start_select = start_select[0:tmp]
                start_select = [s.replace(',', '').replace('\n', '').replace('select','') for s in start_select]

                elements = []
                for line in start_select:                    
                    x = line.split()
                    elements = elements + x
                
                for element in elements:
                    reference = element.split(".")[0]
                    attributeReference = element.split(".")[1]
                    refAlias = getRefAliasFromQuery(query,reference)
                    attribute = getAttributeFromEntity(model, query, reference,attributeReference)
                    projection = gdm.AttributeSelection(refAlias=refAlias, attribute=attribute)
                    query.projections.append(projection)
                    saveModel(model)
                    continue
    return
def main():

    # Creamos el modelo GDM
    model = gdm.Model()
    
    input_file = open('gdm/venues.gdm', 'r') 
    lines = input_file.readlines()
    
    # Primero creamos las entidades y las consultas, porque las necesitamos para crear las referencias
    for line in lines:
        if "entity " in line:
            entity = gdm.Entity(name=line.split()[1])
            model.entities.append(entity)
        if "query " in line:
            query = gdm.Query(name=line.split()[1].strip(":"))
            model.queries.append(query)

    # Parseamos el documento para agregar llenar las entidades
    for i in range(len(lines)):
        line = lines[i]
        
        # Ignoramos los comentarios
        if "/*" in line or "* " in line or "*/" in line:
            continue
        
        # Si es una entidad
        if "entity" in line:
            populateEntity(model, lines, i)

        # Si es una consulta            
        if "query" in line:
            populateQuery(model,lines,i)
            continue

    saveModel(model)



if __name__ == '__main__':
    main()
