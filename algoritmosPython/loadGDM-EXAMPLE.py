from pyecore.resources import ResourceSet, URI

rset = ResourceSet()
resource = rset.get_resource(URI('langs/GdmLang.ecore'))
mm_root = resource.contents[0]
rset.metamodel_registry[mm_root.nsURI] = mm_root
# At this point, the .ecore is loaded in the 'rset' as a metamodel
resource = rset.get_resource(URI('gdm.models/venues.model'))
model_root = resource.contents[0]
print("Pause")