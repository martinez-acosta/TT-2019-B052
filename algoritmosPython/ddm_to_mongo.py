import langs.ddmLang as ddm
from pyecore.resources import ResourceSet, URI
from pyecore.resources.xmi import XMIResource

def loadModelDDM(input_file):
    rset = ResourceSet()
    # register the metamodel (available in the generated files)
    rset.metamodel_registry[ddm.nsURI] = ddm
    rset.resource_factory['ddm'] = lambda uri: XMIResource(uri)  
    resource = rset.get_resource(URI(input_file))
    model = resource.contents[0]
    return model

def getMongoDBType(type_):
    if type_.name == "INT":
        tipo = "int"
    elif type_.name == "FLOAT":
        tipo = "double"
    elif type_.name == "TEXT":
        tipo = "string"
    elif type_.name == "DATE":
        tipo = "date"
    elif type_.name == "TIMESTAMP":
        tipo = "timestamp"
    elif type_.name == "BOOLEAN":
        tipo = "boolean"
    elif type_.name == "ID":
        tipo = "objectId"
    else:
        tipo = "string"

    return tipo

def generateField(output_file,field):
    if isinstance(field, ddm.PrimitiveField):
        generatePrimitiveField(output_file,field)
    elif isinstance(field, ddm.Document):
        generateDocumentField(output_file,field)
    elif isinstance(field, ddm.ArrayField):
        generateArrayField(output_file,field)
    return

def generateArrayField(output_file, field):
    output_file.write(field.name + ": {\n")
    output_file.write("    bsonType: \"array\",\n")
    output_file.write("    items: {\n")
    generateField(output_file,field.type)
    output_file.write("    }\n")
    output_file.write("  }\n")
    return

def generatePrimitiveField(output_file, field):
    output_file.write(field.name + ": { bsonType: \"" + getMongoDBType(field.type) + "\"}\n")
    return

def generateDocumentField(output_file,document):
    output_file.write("    bsonType: \"object\",\n")
    output_file.write("    properties: {\n")
    for field in document.fields:
        if isinstance(field, ddm.PrimitiveField):
            generatePrimitiveField(output_file,field)
        elif isinstance(field, ddm.Document):
            generateDocumentField(output_file,field)
        elif isinstance(field, ddm.ArrayField):
            generateArrayField(output_file,field)
        if field != document.fields[-1]:
                output_file.write(",")

    output_file.write("    }\n")
    return

def writeFile(output_file,collection):
    output_file.write("db.createCollection(\"" + collection.name + "\", {\n")
    output_file.write("  validator: {\n")
    output_file.write("    $jsonSchema: {")
    generateDocumentField(output_file,collection.root)
    output_file.write("    }\n}\n})\n")
    output_file.close()
    return
def main():
    ddmModel = loadModelDDM("prueba_ddm.xmi")
    ofile = "laloMongo.json"
    count = 0 
    for collection in ddmModel.collections:
        if count == 0:
            count += 1
            with open(ofile, 'w') as output_file:
                writeFile(output_file,collection)
        else:
            with open(ofile, 'a') as output_file:
                writeFile(output_file,collection)


                
    return


if __name__ == '__main__':
    main()