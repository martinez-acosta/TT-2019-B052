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

def main():
    
    gdmModel = loadModel("Static_model_test.xmi")
    ddmModel = ddm.DocumentDataModel()


if __name__ == '__main__':
    main()