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
    # Obtenemos las queries en donde aparezca la entidad "me" in el elemento "from_"
    
    entityToQueries = []
    for q in queries:
        if q.from_.entity.name == me.name:
            entityToQueries.append(q)
    
    # Obtenemos todos los elementos Inclusion de cada query en entityToQueries
    
    return accessTree

def populateDocumentType(dt, accessTree):
    root = ''
    return root

def main():
    
    gdmModel = loadModel("Static_model_test.xmi")
    
    ddmModel = ddm.DocumentDataModel()

    # Obtenemos las entidades de los elementos From
    mainEntities = set()
    for q in gdmModel.queries:
        mainEntities.add(q.from_.entity)

     
    for me in mainEntities:
        collection = ddm.Collection(name=me.name,root=ddm.Document(name="root")) # Por cada entidad en mainEntities creamos una colección
        accessTree = allQueryPaths(me,gdmModel.queries)
        root = populateDocumentType(collection.root,accessTree)
        collection.root = root
        ddmModel.collections.append(collection)
    
    hola = "hola"
    


if __name__ == '__main__':
    main()