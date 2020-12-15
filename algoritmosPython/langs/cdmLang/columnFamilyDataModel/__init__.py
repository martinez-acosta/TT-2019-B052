
from .columnFamilyDataModel import getEClassifier, eClassifiers
from .columnFamilyDataModel import name, nsURI, nsPrefix, eClass
from .columnFamilyDataModel import ColumnFamilyDataModel, ColumnFamily, Table, Column, Type, SimpleType, Collection, List, Set, Map, Tuple, UserDefinedType, Field, Key, PartitionKey, ClusteringKey, PrimitiveType


from . import columnFamilyDataModel

__all__ = ['ColumnFamilyDataModel', 'ColumnFamily', 'Table', 'Column', 'Type', 'SimpleType', 'Collection', 'List',
           'Set', 'Map', 'Tuple', 'UserDefinedType', 'Field', 'Key', 'PartitionKey', 'ClusteringKey', 'PrimitiveType']

eSubpackages = []
eSuperPackage = None
columnFamilyDataModel.eSubpackages = eSubpackages
columnFamilyDataModel.eSuperPackage = eSuperPackage

ColumnFamilyDataModel.tables.eType = Table
Table.columnFamilies.eType = ColumnFamily
Table.columns.eType = Column
Table.partitionKeys.eType = PartitionKey
Table.clusteringKeys.eType = ClusteringKey
Column.type.eType = Type
Column.columnFamily.eType = ColumnFamily
UserDefinedType.fields.eType = Field
Field.type.eType = Type
Key.column.eType = Column

otherClassifiers = [PrimitiveType]

for classif in otherClassifiers:
    eClassifiers[classif.name] = classif
    classif.ePackage = eClass

for classif in eClassifiers.values():
    eClass.eClassifiers.append(classif.eClass)

for subpack in eSubpackages:
    eClass.eSubpackages.append(subpack.eClass)
