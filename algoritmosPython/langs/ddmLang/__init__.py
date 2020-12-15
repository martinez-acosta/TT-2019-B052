
from .documentDataModel import getEClassifier, eClassifiers
from .documentDataModel import name, nsURI, nsPrefix, eClass
from .documentDataModel import DocumentDataModel, Collection, Field, Index, Document, PrimitiveField, ArrayField, PrimitiveType


from . import documentDataModel

__all__ = ['DocumentDataModel', 'Collection', 'Field', 'Index',
           'Document', 'PrimitiveField', 'ArrayField', 'PrimitiveType']

eSubpackages = []
eSuperPackage = None
documentDataModel.eSubpackages = eSubpackages
documentDataModel.eSuperPackage = eSuperPackage

DocumentDataModel.collections.eType = Collection
Collection.root.eType = Document
Collection.indexes.eType = Index
Index.fields.eType = Field
Document.fields.eType = Field
ArrayField.type.eType = Field

otherClassifiers = [PrimitiveType]

for classif in otherClassifiers:
    eClassifiers[classif.name] = classif
    classif.ePackage = eClass

for classif in eClassifiers.values():
    eClass.eClassifiers.append(classif.eClass)

for subpack in eSubpackages:
    eClass.eSubpackages.append(subpack.eClass)
