import langs.gdmLang as gdm
import langs.ddmLang as ddm
from pyecore.resources import ResourceSet, URI
from pyecore.resources.xmi import XMIResource

def loadModel(input_file):
    rset = ResourceSet()
    # register the metamodel (available in the generated files)
    rset.metamodel_registry[gdm.nsURI] = gdm
    rset.resource_factory['gdm'] = lambda uri: XMIResource(uri)  
    resource = rset.get_resource(URI(input_file))
    model = resource.contents[0]

    return model

def allQueryPaths(me, queries):
    accessTree = ''
    # Obtenemos las queries en donde aparezca la entidad "me" en el elemento "from_"
    
    
    return accessTree

def populateDocumentType(dt, accessTree):
    root = ''
    return root

def main():
    
    gdmModel = loadModel("Static_model_test.xmi")
    
    ddmModel = ddm.DocumentDataModel()

    # Obtenemos las entidades de los elementos From
    # mainEntities = gdm.queries.map[q | q.from.entity].toSet    
    mainEntities = set(map(lambda q: q.from_.entity, gdmModel.queries))

    # entityToQueries =  mainEntities.map[me | me -> gdm.queries.filter[q | q.from.entity.equals(me)]]
    entityToQueries = list(map(lambda me: (me, list(filter(lambda q: q.from_.entity.name == me.name, gdmModel.queries))), mainEntities))
        

    hola = "hola"
    
    # f1_b = list( map(lambda x: list(map(lambda t: t.strip(), x.split(',', 1))), lst))
    # Though in most cases you should prefer list comprehensions to map calls:
    # f1_a = [[t.strip() for t in x.split(',', 1)] for x in lst]

    valor = "hola"
    

    
    #for me in mainEntities:
    #    collection = ddm.Collection(name=me.name,root=ddm.Document(name="root")) # Por cada entidad en mainEntities creamos una colección
    #    accessTree = allQueryPaths(me,gdmModel.queries)
    #    root = populateDocumentType(collection.root,accessTree)
    #    collection.root = root
    #    ddmModel.collections.append(collection)
    
    


if __name__ == '__main__':
    main()