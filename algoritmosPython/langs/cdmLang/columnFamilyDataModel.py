"""Definition of meta model 'columnFamilyDataModel'."""
from functools import partial
import pyecore.ecore as Ecore
from pyecore.ecore import *


name = 'columnFamilyDataModel'
nsURI = 'http://columnFamilyDataModel.mortadelo.istr.unican.es'
nsPrefix = 'columnFamilyDataModel'

eClass = EPackage(name=name, nsURI=nsURI, nsPrefix=nsPrefix)

eClassifiers = {}
getEClassifier = partial(Ecore.getEClassifier, searchspace=eClassifiers)
PrimitiveType = EEnum('PrimitiveType', literals=[
                      'INT', 'FLOAT', 'TEXT', 'DATE', 'TIMESTAMP', 'ID', 'BOOLEAN'])


class ColumnFamilyDataModel(EObject, metaclass=MetaEClass):

    tables = EReference(ordered=True, unique=True, containment=True, derived=False, upper=-1)

    def __init__(self, *, tables=None):
        # if kwargs:
        #    raise AttributeError('unexpected arguments: {}'.format(kwargs))

        super().__init__()

        if tables:
            self.tables.extend(tables)


class ColumnFamily(EObject, metaclass=MetaEClass):

    name = EAttribute(eType=EString, unique=True, derived=False, changeable=True)

    def __init__(self, *, name=None):
        # if kwargs:
        #    raise AttributeError('unexpected arguments: {}'.format(kwargs))

        super().__init__()

        if name is not None:
            self.name = name


class Table(EObject, metaclass=MetaEClass):

    name = EAttribute(eType=EString, unique=True, derived=False, changeable=True)
    columnFamilies = EReference(ordered=True, unique=True,
                                containment=True, derived=False, upper=-1)
    columns = EReference(ordered=True, unique=True, containment=True, derived=False, upper=-1)
    partitionKeys = EReference(ordered=True, unique=True, containment=True, derived=False, upper=-1)
    clusteringKeys = EReference(ordered=True, unique=True,
                                containment=True, derived=False, upper=-1)

    def __init__(self, *, name=None, columnFamilies=None, columns=None, partitionKeys=None, clusteringKeys=None):
        # if kwargs:
        #    raise AttributeError('unexpected arguments: {}'.format(kwargs))

        super().__init__()

        if name is not None:
            self.name = name

        if columnFamilies:
            self.columnFamilies.extend(columnFamilies)

        if columns:
            self.columns.extend(columns)

        if partitionKeys:
            self.partitionKeys.extend(partitionKeys)

        if clusteringKeys:
            self.clusteringKeys.extend(clusteringKeys)


class Column(EObject, metaclass=MetaEClass):

    name = EAttribute(eType=EString, unique=True, derived=False, changeable=True)
    type = EReference(ordered=True, unique=True, containment=True, derived=False)
    columnFamily = EReference(ordered=True, unique=True, containment=False, derived=False)

    def __init__(self, *, name=None, type=None, columnFamily=None):
        # if kwargs:
        #    raise AttributeError('unexpected arguments: {}'.format(kwargs))

        super().__init__()

        if name is not None:
            self.name = name

        if type is not None:
            self.type = type

        if columnFamily is not None:
            self.columnFamily = columnFamily


@abstract
class Type(EObject, metaclass=MetaEClass):

    def __init__(self):
        # if kwargs:
        #    raise AttributeError('unexpected arguments: {}'.format(kwargs))

        super().__init__()


class Field(EObject, metaclass=MetaEClass):

    name = EAttribute(eType=EString, unique=True, derived=False, changeable=True)
    type = EReference(ordered=True, unique=True, containment=True, derived=False)

    def __init__(self, *, name=None, type=None):
        # if kwargs:
        #    raise AttributeError('unexpected arguments: {}'.format(kwargs))

        super().__init__()

        if name is not None:
            self.name = name

        if type is not None:
            self.type = type


@abstract
class Key(EObject, metaclass=MetaEClass):

    column = EReference(ordered=True, unique=True, containment=False, derived=False)

    def __init__(self, *, column=None):
        # if kwargs:
        #    raise AttributeError('unexpected arguments: {}'.format(kwargs))

        super().__init__()

        if column is not None:
            self.column = column


class SimpleType(Type):

    type = EAttribute(eType=PrimitiveType, unique=True, derived=False, changeable=True)

    def __init__(self, *, type=None, **kwargs):

        super().__init__(**kwargs)

        if type is not None:
            self.type = type


@abstract
class Collection(Type):

    type = EAttribute(eType=PrimitiveType, unique=True, derived=False, changeable=True)

    def __init__(self, *, type=None, **kwargs):

        super().__init__(**kwargs)

        if type is not None:
            self.type = type


class Tuple(Type):

    types = EAttribute(eType=PrimitiveType, unique=True, derived=False, changeable=True, upper=-1)

    def __init__(self, *, types=None, **kwargs):

        super().__init__(**kwargs)

        if types:
            self.types.extend(types)


class UserDefinedType(Type):

    name = EAttribute(eType=EString, unique=True, derived=False, changeable=True)
    fields = EReference(ordered=True, unique=True, containment=True, derived=False, upper=-1)

    def __init__(self, *, name=None, fields=None, **kwargs):

        super().__init__(**kwargs)

        if name is not None:
            self.name = name

        if fields:
            self.fields.extend(fields)


class PartitionKey(Key):

    def __init__(self, **kwargs):

        super().__init__(**kwargs)


class ClusteringKey(Key):

    def __init__(self, **kwargs):

        super().__init__(**kwargs)


class List(Collection):

    def __init__(self, **kwargs):

        super().__init__(**kwargs)


class Set(Collection):

    def __init__(self, **kwargs):

        super().__init__(**kwargs)


class Map(Collection):

    keyType = EAttribute(eType=PrimitiveType, unique=True, derived=False, changeable=True)

    def __init__(self, *, keyType=None, **kwargs):

        super().__init__(**kwargs)

        if keyType is not None:
            self.keyType = keyType
