"""Definition of meta model 'documentDataModel'."""
from functools import partial
import pyecore.ecore as Ecore
from pyecore.ecore import *


name = 'documentDataModel'
nsURI = 'http://documentDataModel.mortadelo.istr.unican.es'
nsPrefix = 'documentDataModel'

eClass = EPackage(name=name, nsURI=nsURI, nsPrefix=nsPrefix)

eClassifiers = {}
getEClassifier = partial(Ecore.getEClassifier, searchspace=eClassifiers)
PrimitiveType = EEnum('PrimitiveType', literals=[
                      'INT', 'FLOAT', 'TEXT', 'DATE', 'TIMESTAMP', 'BOOLEAN', 'ID'])


class DocumentDataModel(EObject, metaclass=MetaEClass):

    collections = EReference(ordered=True, unique=True, containment=True, derived=False, upper=-1)

    def __init__(self, *, collections=None):
        # if kwargs:
        #    raise AttributeError('unexpected arguments: {}'.format(kwargs))

        super().__init__()

        if collections:
            self.collections.extend(collections)


class Collection(EObject, metaclass=MetaEClass):

    name = EAttribute(eType=EString, unique=True, derived=False, changeable=True)
    root = EReference(ordered=True, unique=True, containment=True, derived=False)
    indexes = EReference(ordered=True, unique=True, containment=True, derived=False, upper=-1)

    def __init__(self, *, name=None, root=None, indexes=None):
        # if kwargs:
        #    raise AttributeError('unexpected arguments: {}'.format(kwargs))

        super().__init__()

        if name is not None:
            self.name = name

        if root is not None:
            self.root = root

        if indexes:
            self.indexes.extend(indexes)


@abstract
class Field(EObject, metaclass=MetaEClass):

    name = EAttribute(eType=EString, unique=True, derived=False, changeable=True)

    def __init__(self, *, name=None):
        # if kwargs:
        #    raise AttributeError('unexpected arguments: {}'.format(kwargs))

        super().__init__()

        if name is not None:
            self.name = name


class Index(EObject, metaclass=MetaEClass):

    name = EAttribute(eType=EString, unique=True, derived=False, changeable=True)
    fields = EReference(ordered=True, unique=True, containment=False, derived=False, upper=-1)

    def __init__(self, *, name=None, fields=None):
        # if kwargs:
        #    raise AttributeError('unexpected arguments: {}'.format(kwargs))

        super().__init__()

        if name is not None:
            self.name = name

        if fields:
            self.fields.extend(fields)


class Document(Field):

    fields = EReference(ordered=True, unique=True, containment=True, derived=False, upper=-1)

    def __init__(self, *, fields=None, **kwargs):

        super().__init__(**kwargs)

        if fields:
            self.fields.extend(fields)


class PrimitiveField(Field):

    type = EAttribute(eType=PrimitiveType, unique=True, derived=False, changeable=True)

    def __init__(self, *, type=None, **kwargs):

        super().__init__(**kwargs)

        if type is not None:
            self.type = type


class ArrayField(Field):

    type = EReference(ordered=True, unique=True, containment=True, derived=False)

    def __init__(self, *, type=None, **kwargs):

        super().__init__(**kwargs)

        if type is not None:
            self.type = type
