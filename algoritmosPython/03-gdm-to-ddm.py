import langs.gdmLang as gdm
import langs.ddmLang as ddm
from pyecore.resources import ResourceSet, URI
from pyecore.resources.xmi import XMIResource

class Tree(object):
    "Generic tree node."
    def __init__(self, name=None, children=None,data=None):
        if name is not None:
            self.name = name
        self.children = []
        if children is not None:
            for child in children:
                self.add_child(child)
        if data is not None:
            self.data = data
    def __repr__(self):
        return self.name
    def add_child(self, node):
        assert isinstance(node, Tree)
        for child in self.children:
            if (child.data is None and node.data is None) or child.data == node.data:
                return child

        self.children.append(node)
        return node

def loadModel(input_file):
    rset = ResourceSet()
    # register the metamodel (available in the generated files)
    rset.metamodel_registry[gdm.nsURI] = gdm
    rset.resource_factory['gdm'] = lambda uri: XMIResource(uri)  
    resource = rset.get_resource(URI(input_file))
    model = resource.contents[0]

    return model

def saveModelDDM(model):
    # create a resourceSet that hold the contents of the gdm.ecore model and the instances we use/create
    rset = ResourceSet()
    # register the metamodel (available in the generated files)
    rset.metamodel_registry[ddm.nsURI] = ddm
    rset.resource_factory['ddm'] = lambda uri: XMIResource(uri)  

    resource = rset.create_resource(URI('prueba_ddm.xmi'))
    resource.append(model)
    resource.save()
    return

def addAttributes(document,entity):
     # features = list(filter(lambda f: isinstance(f,gdm.Attribute),entity.features))
    for attr in list(filter(lambda f: isinstance(f,gdm.Attribute),entity.features)):
        field = ddm.PrimitiveField()
        field.name = attr.name
        field.type = convertType(attr.type)
        document.fields.append(field)
    return

def convertType(type_):    
    if type_.name == "ID":
        ddmType = ddm.PrimitiveType.from_string("ID")
    elif type_.name == "NUMBER":
        ddmType = ddm.PrimitiveType.from_string("FLOAT")
    elif type_.name == "DATE":
        ddmType = ddm.PrimitiveType.from_string("DATE")
    elif type_.name == "TIMESTAMP":
        ddmType = ddm.PrimitiveType.from_string("TIMESTAMP")
    elif type_.name == "BOOLEAN":
        ddmType = ddm.PrimitiveType.from_string("BOOLEAN")
    else:
        ddmType = ddm.PrimitiveType.from_string("TEXT")

    return ddmType

def toFirstLower(test_str):
    return test_str[0].lower() + test_str[1:]

def populateDocument(document, entity, tree, mainEntities):
    addAttributes(document,entity)

    for child in tree.children:
        reference = child.data
        newField = None
        # si la referencia apunta a una entidad principal, en lugar de generar el documento creamos una referencia
        if any(map(lambda me: me == reference.entity, mainEntities)):
            newField = ddm.PrimitiveField()
            newField.name = toFirstLower(reference.entity.name) + "Ref"
            newField.type = ddm.PrimitiveType.from_string("ID")
        else: 
            newField = ddm.Document()
            newField.name = toFirstLower(reference.entity.name)
            populateDocument(newField, reference.entity, child, mainEntities)
      
        if (reference.cardinality != "1"):
            # encapsulate field in an array
            arrayField = ddm.ArrayField()
            arrayField.name = newField.name + "Array"
            arrayField.type = newField
            document.fields.add(arrayField)
        else:
            document.fields.add(newField)
        

    return 


def createAccessTree(queries):
    tree = Tree()

    for query in queries:
        for inclusion in query.inclusions:
            auxTree = tree
            for ref in inclusion.refs:
                child = auxTree.add_child(Tree(data=ref))
                auxTree = child
    
    return tree

def getTree(entity2accessTree, entity):

    for pair in entity2accessTree:
        if pair[0] == entity:
            tree = pair[1]

    return tree

def getAllTrees(entity2accessTree):
    lista = []

    for pair in entity2accessTree:
        #if pair[1] != tree:
        lista.append(pair[1])
    return lista

def addAllTreeNodes(treeNodes,lista):
    for item in lista:
        treeNodes.append(item)
    return 

def searchEntity(entity,tree):
    treeNodes = []
    for child in tree.children:
        if child.data.entity == entity:
            treeNodes.append(child)
        addAllTreeNodes(treeNodes, searchEntity(entity,child))
    return treeNodes 

def addTreeNode(tree, treeNode):
    for child in treeNode.children:
        addedChild = tree.add_child(Tree(data=child.data))
        addTreeNode(addedChild,child)
    return

def completeAccessTree(entity, tree, othersTrees):

    for oTree in othersTrees:
        treeNodes = searchEntity(entity,oTree)
        for treeNode in treeNodes:
            addTreeNode(tree,treeNode)
    return

def main():
    
    gdmModel = loadModel("Static_model_test.xmi")
    
    ddmModel = ddm.DocumentDataModel()

    # Obtenemos las entidades de los elementos From
    # mainEntities = gdm.queries.map[q | q.from.entity].toSet    
    mainEntities = set(map(lambda q: q.from_.entity, gdmModel.queries))

    # entityToQueries =  mainEntities.map[me | me -> gdm.queries.filter[q | q.from.entity.equals(me)]]
    entityToQueries = list(map(lambda me: (me, list(filter(lambda q: q.from_.entity.name == me.name, gdmModel.queries))), mainEntities))
        
    # val entity2accessTree = newImmutableMap(entityToQueries.map[e2q | e2q.key -> createAccessTree(e2q.value)])
    entity2accessTree = list(map(lambda e2q: ( e2q[0], createAccessTree(e2q[1])), entityToQueries))

    # Completamos cada árbol de acceso
    for entity in mainEntities:
      tree = getTree(entity2accessTree,entity)
      othersTrees = getAllTrees(entity2accessTree)
    #   for t in othersTrees:
    #       if t == tree:
    #           othersTrees.remove(t)
    #           hola = "hola"
      completeAccessTree(entity, tree, othersTrees)
    
    # Generamos las colecciones
    for entity in mainEntities:
        tree = getTree(entity2accessTree,entity)
        collection = ddm.Collection()
        collection.name = entity.name
        docType = ddm.Document()
        docType.name = "root"
        collection.root = docType
        populateDocument(docType,entity,tree,mainEntities)
        ddmModel.collections.append(collection)
        saveModelDDM(ddmModel)

    saveModelDDM(ddmModel)

    
if __name__ == '__main__':
    main()