"""Definition of meta model 'gdmLang'."""
from functools import partial
import pyecore.ecore as Ecore
from pyecore.ecore import *


name = 'gdmLang'
nsURI = 'http://www.unican.es/istr/mortadelo/gdm/lang/GdmLang'
nsPrefix = 'gdmLang'

eClass = EPackage(name=name, nsURI=nsURI, nsPrefix=nsPrefix)

eClassifiers = {}
getEClassifier = partial(Ecore.getEClassifier, searchspace=eClassifiers)
Type = EEnum('Type', literals=['NUMBER', 'TEXT', 'DATE', 'BOOLEAN', 'ID', 'TIMESTAMP'])


class Model(EObject, metaclass=MetaEClass):

    entities = EReference(ordered=True, unique=True, containment=True, derived=False, upper=-1)
    queries = EReference(ordered=True, unique=True, containment=True, derived=False, upper=-1)

    def __init__(self, *, entities=None, queries=None):
        # if kwargs:
        #    raise AttributeError('unexpected arguments: {}'.format(kwargs))

        super().__init__()

        if entities:
            self.entities.extend(entities)

        if queries:
            self.queries.extend(queries)


class AnnotatableElement(EObject, metaclass=MetaEClass):

    name = EAttribute(eType=EString, unique=True, derived=False, changeable=True)
    annotations = EReference(ordered=True, unique=True, containment=True, derived=False, upper=-1)

    def __init__(self, *, annotations=None, name=None):
        # if kwargs:
        #    raise AttributeError('unexpected arguments: {}'.format(kwargs))

        super().__init__()

        if name is not None:
            self.name = name

        if annotations:
            self.annotations.extend(annotations)


class Annotation(EObject, metaclass=MetaEClass):

    name = EAttribute(eType=EString, unique=True, derived=False, changeable=True)

    def __init__(self, *, name=None):
        # if kwargs:
        #    raise AttributeError('unexpected arguments: {}'.format(kwargs))

        super().__init__()

        if name is not None:
            self.name = name


class AttributeSelection(EObject, metaclass=MetaEClass):

    alias = EAttribute(eType=EString, unique=True, derived=False, changeable=True)
    refAlias = EReference(ordered=True, unique=True, containment=False, derived=False)
    attribute = EReference(ordered=True, unique=True, containment=False, derived=False)

    def __init__(self, *, refAlias=None, attribute=None, alias=None):
        # if kwargs:
        #    raise AttributeError('unexpected arguments: {}'.format(kwargs))

        super().__init__()

        if alias is not None:
            self.alias = alias

        if refAlias is not None:
            self.refAlias = refAlias

        if attribute is not None:
            self.attribute = attribute


class Alias(EObject, metaclass=MetaEClass):

    name = EAttribute(eType=EString, unique=True, derived=False, changeable=True)

    def __init__(self, *, name=None):
        # if kwargs:
        #    raise AttributeError('unexpected arguments: {}'.format(kwargs))

        super().__init__()

        if name is not None:
            self.name = name


class From(EObject, metaclass=MetaEClass):

    entity = EReference(ordered=True, unique=True, containment=False, derived=False)
    alias = EReference(ordered=True, unique=True, containment=True, derived=False)

    def __init__(self, *, entity=None, alias=None):
        # if kwargs:
        #    raise AttributeError('unexpected arguments: {}'.format(kwargs))

        super().__init__()

        if entity is not None:
            self.entity = entity

        if alias is not None:
            self.alias = alias


class Inclusion(EObject, metaclass=MetaEClass):

    refAlias = EReference(ordered=True, unique=True, containment=False, derived=False)
    refs = EReference(ordered=True, unique=False, containment=False, derived=False, upper=-1)
    alias = EReference(ordered=True, unique=True, containment=True, derived=False)

    def __init__(self, *, refAlias=None, refs=None, alias=None):
        # if kwargs:
        #    raise AttributeError('unexpected arguments: {}'.format(kwargs))

        super().__init__()

        if refAlias is not None:
            self.refAlias = refAlias

        if refs:
            self.refs.extend(refs)

        if alias is not None:
            self.alias = alias


class BooleanExpression(EObject, metaclass=MetaEClass):

    def __init__(self):
        # if kwargs:
        #    raise AttributeError('unexpected arguments: {}'.format(kwargs))

        super().__init__()


class Entity(AnnotatableElement):

    features = EReference(ordered=True, unique=True, containment=True, derived=False, upper=-1)

    def __init__(self, *, features=None, **kwargs):

        super().__init__(**kwargs)

        if features:
            self.features.extend(features)


class Feature(AnnotatableElement):

    cardinality = EAttribute(eType=EString, unique=True, derived=False, changeable=True)

    def __init__(self, *, cardinality=None, **kwargs):

        super().__init__(**kwargs)

        if cardinality is not None:
            self.cardinality = cardinality


class Query(AnnotatableElement):

    projections = EReference(ordered=True, unique=True, containment=True, derived=False, upper=-1)
    from_ = EReference(ordered=True, unique=True, containment=True, derived=False)
    inclusions = EReference(ordered=True, unique=True, containment=True, derived=False, upper=-1)
    condition = EReference(ordered=True, unique=True, containment=True, derived=False)
    orderingAttributes = EReference(ordered=True, unique=True,
                                    containment=True, derived=False, upper=-1)

    def __init__(self, *, projections=None, from_=None, inclusions=None, condition=None, orderingAttributes=None, **kwargs):

        super().__init__(**kwargs)

        if projections:
            self.projections.extend(projections)

        if from_ is not None:
            self.from_ = from_

        if inclusions:
            self.inclusions.extend(inclusions)

        if condition is not None:
            self.condition = condition

        if orderingAttributes:
            self.orderingAttributes.extend(orderingAttributes)


class Comparison(BooleanExpression):

    value = EAttribute(eType=EString, unique=True, derived=False, changeable=True)
    selection = EReference(ordered=True, unique=True, containment=True, derived=False)

    def __init__(self, *, selection=None, value=None, **kwargs):

        super().__init__(**kwargs)

        if value is not None:
            self.value = value

        if selection is not None:
            self.selection = selection


class AndConjunction(BooleanExpression):

    left = EReference(ordered=True, unique=True, containment=True, derived=False)
    right = EReference(ordered=True, unique=True, containment=True, derived=False)

    def __init__(self, *, left=None, right=None, **kwargs):

        super().__init__(**kwargs)

        if left is not None:
            self.left = left

        if right is not None:
            self.right = right


class OrConjunction(BooleanExpression):

    left = EReference(ordered=True, unique=True, containment=True, derived=False)
    right = EReference(ordered=True, unique=True, containment=True, derived=False)

    def __init__(self, *, left=None, right=None, **kwargs):

        super().__init__(**kwargs)

        if left is not None:
            self.left = left

        if right is not None:
            self.right = right


class Attribute(Feature):

    type = EAttribute(eType=Type, unique=True, derived=False, changeable=True)
    unique = EAttribute(eType=EBoolean, unique=True, derived=False, changeable=True)

    def __init__(self, *, type=None, unique=None, **kwargs):

        super().__init__(**kwargs)

        if type is not None:
            self.type = type

        if unique is not None:
            self.unique = unique


class Reference(Feature):

    entity = EReference(ordered=True, unique=True, containment=False, derived=False)

    def __init__(self, *, entity=None, **kwargs):

        super().__init__(**kwargs)

        if entity is not None:
            self.entity = entity


class Equality(Comparison):

    def __init__(self, **kwargs):

        super().__init__(**kwargs)


class Inequality(Comparison):

    def __init__(self, **kwargs):

        super().__init__(**kwargs)


class MoreThan(Comparison):

    def __init__(self, **kwargs):

        super().__init__(**kwargs)


class MoreThanOrEqual(Comparison):

    def __init__(self, **kwargs):

        super().__init__(**kwargs)


class LessThan(Comparison):

    def __init__(self, **kwargs):

        super().__init__(**kwargs)


class LessThanOrEqual(Comparison):

    def __init__(self, **kwargs):

        super().__init__(**kwargs)
