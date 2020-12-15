import langs.ddmLang as ddm
from pyecore.resources import ResourceSet, URI
from pyecore.resources.xmi import XMIResource


rset = ResourceSet()
# register the metamodel (available in the generated files)
rset.metamodel_registry[ddm.nsURI] = ddm
rset.resource_factory['ddm'] = lambda uri: XMIResource(uri)  
resource = rset.get_resource(URI("documents.models/venuesDOC.model"))
model = resource.contents[0]

print("pause")
