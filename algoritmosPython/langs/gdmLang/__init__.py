
from .gdmLang import getEClassifier, eClassifiers
from .gdmLang import name, nsURI, nsPrefix, eClass
from .gdmLang import Model, AnnotatableElement, Annotation, Entity, Feature, Attribute, Reference, Type, Query, AttributeSelection, Alias, From, Inclusion, BooleanExpression, Comparison, AndConjunction, OrConjunction, Equality, Inequality, MoreThan, MoreThanOrEqual, LessThan, LessThanOrEqual


from . import gdmLang

__all__ = ['Model', 'AnnotatableElement', 'Annotation', 'Entity', 'Feature', 'Attribute', 'Reference', 'Type', 'Query', 'AttributeSelection', 'Alias', 'From', 'Inclusion',
           'BooleanExpression', 'Comparison', 'AndConjunction', 'OrConjunction', 'Equality', 'Inequality', 'MoreThan', 'MoreThanOrEqual', 'LessThan', 'LessThanOrEqual']

eSubpackages = []
eSuperPackage = None
gdmLang.eSubpackages = eSubpackages
gdmLang.eSuperPackage = eSuperPackage

Model.entities.eType = Entity
Model.queries.eType = Query
AnnotatableElement.annotations.eType = Annotation
Entity.features.eType = Feature
Reference.entity.eType = Entity
Query.projections.eType = AttributeSelection
Query.from_.eType = From
Query.inclusions.eType = Inclusion
Query.condition.eType = BooleanExpression
Query.orderingAttributes.eType = AttributeSelection
AttributeSelection.refAlias.eType = Alias
AttributeSelection.attribute.eType = Attribute
From.entity.eType = Entity
From.alias.eType = Alias
Inclusion.refAlias.eType = Alias
Inclusion.refs.eType = Reference
Inclusion.alias.eType = Alias
Comparison.selection.eType = AttributeSelection
AndConjunction.left.eType = BooleanExpression
AndConjunction.right.eType = BooleanExpression
OrConjunction.left.eType = BooleanExpression
OrConjunction.right.eType = BooleanExpression

otherClassifiers = [Type]

for classif in otherClassifiers:
    eClassifiers[classif.name] = classif
    classif.ePackage = eClass

for classif in eClassifiers.values():
    eClass.eClassifiers.append(classif.eClass)

for subpack in eSubpackages:
    eClass.eSubpackages.append(subpack.eClass)
