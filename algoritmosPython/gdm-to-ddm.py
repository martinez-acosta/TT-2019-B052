import langs.gdmLang as gdm
import langs.ddmLang as ddm
from pyecore.resources import ResourceSet, URI
from pyecore.resources.xmi import XMIResource

class Tree(object):
    "Generic tree node."
    def __init__(self, name='root', children=None,data=None):
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
        self.children.append(node)

def loadModel(input_file):
    rset = ResourceSet()
    # register the metamodel (available in the generated files)
    rset.metamodel_registry[gdm.nsURI] = gdm
    rset.resource_factory['gdm'] = lambda uri: XMIResource(uri)  
    resource = rset.get_resource(URI(input_file))
    model = resource.contents[0]

    return model

def populateDocumentType(dt, accessTree):
    root = ''
    return root


def createAccessTree(queries):
    tree = Tree()

    for query in queries:
        for inclusion in query.inclusions:
            auxTree = tree
            for ref in inclusion.refs:
                child = Tree(name=ref.name,data=ref)
                auxTree.add_child(child)
                auxTree = child
    
    return tree

def getTree(entity2accessTree, entity):

    for pair in entity2accessTree:
        if pair[0] == entity:
            tree = pair[1]

    return tree

def getAllTreesBut(entity2accessTree,tree):
    lista = []

    for pair in entity2accessTree:
        if pair[1] != tree:
            lista.append(pair[1])
    return lista

def searchEntity(entity,tree):
    treeNodes = []
    for child in tree.children:
        if child.data.entity == entity:
            treeNodes.append(child)
        treeNodes.append(searchEntity(entity,child))
    return treeNodes 

def completeAccessTree(entity, tree, othersTrees):

    for oTree in othersTrees:
        treeNodes = searchEntity(entity,oTree)
        for treeNode in treeNodes:
            tree.add_child(treeNode)
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

    for entity in mainEntities:
      tree = getTree(entity2accessTree,entity)
      othersTrees = getAllTreesBut(entity2accessTree,tree)
      completeAccessTree(entity, tree, othersTrees)
    
    for entity in mainEntities:
        
      


    
    


if __name__ == '__main__':
    main()