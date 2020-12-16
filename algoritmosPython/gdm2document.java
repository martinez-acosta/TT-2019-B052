package es.unican.istr.mortadelo.gdm.transformations.gdm2document;

import columnFamilyDataModel.ColumnFamilyDataModelPackage;
import documentDataModel.ArrayField;
import documentDataModel.Document;
import documentDataModel.DocumentDataModel;
import documentDataModel.DocumentDataModelFactory;
import documentDataModel.Field;
import documentDataModel.PrimitiveField;
import documentDataModel.PrimitiveType;
import es.unican.istr.mortadelo.gdm.lang.gdmLang.Attribute;
import es.unican.istr.mortadelo.gdm.lang.gdmLang.Entity;
import es.unican.istr.mortadelo.gdm.lang.gdmLang.Feature;
import es.unican.istr.mortadelo.gdm.lang.gdmLang.GdmLangPackage;
import es.unican.istr.mortadelo.gdm.lang.gdmLang.Inclusion;
import es.unican.istr.mortadelo.gdm.lang.gdmLang.Model;
import es.unican.istr.mortadelo.gdm.lang.gdmLang.Query;
import es.unican.istr.mortadelo.gdm.lang.gdmLang.Reference;
import es.unican.istr.mortadelo.gdm.lang.gdmLang.Type;
import es.unican.istr.mortadelo.gdm.transformations.common.Tree;
import java.io.File;
import java.io.IOException;
import java.util.ArrayList;
import java.util.Collection;
import java.util.Collections;
import java.util.List;
import java.util.Map;
import java.util.Set;
import org.eclipse.emf.common.util.EList;
import org.eclipse.emf.common.util.URI;
import org.eclipse.emf.ecore.EObject;
import org.eclipse.emf.ecore.resource.Resource;
import org.eclipse.emf.ecore.resource.impl.ResourceSetImpl;
import org.eclipse.emf.ecore.xmi.impl.XMIResourceFactoryImpl;
import org.eclipse.xtext.xbase.lib.CollectionLiterals;
import org.eclipse.xtext.xbase.lib.Conversions;
import org.eclipse.xtext.xbase.lib.Exceptions;
import org.eclipse.xtext.xbase.lib.Functions.Function1;
import org.eclipse.xtext.xbase.lib.InputOutput;
import org.eclipse.xtext.xbase.lib.IterableExtensions;
import org.eclipse.xtext.xbase.lib.ListExtensions;
import org.eclipse.xtext.xbase.lib.Pair;
import org.eclipse.xtext.xbase.lib.StringExtensions;

@SuppressWarnings("all")
public class Gdm2Document {
  public static void main(final String[] args) {
    try {
      final String example = "venues";
      InputOutput.<String>println("GDM to document logical model");
      InputOutput.<String>println(String.format("Example: %s", example));
      final long totalStart = System.currentTimeMillis();
      final Resource.Factory.Registry reg = Resource.Factory.Registry.INSTANCE;
      final Map<String, Object> m = reg.getExtensionToFactoryMap();
      XMIResourceFactoryImpl _xMIResourceFactoryImpl = new XMIResourceFactoryImpl();
      m.put("model", _xMIResourceFactoryImpl);
      GdmLangPackage.eINSTANCE.eClass();
      ColumnFamilyDataModelPackage.eINSTANCE.eClass();
      String _format = String.format("../es.unican.istr.mortadelo.gdm.examples/%s.model", example);
      final File input = new File(_format);
      final ResourceSetImpl resSet = new ResourceSetImpl();
      final Resource inputResource = resSet.getResource(URI.createURI(input.getCanonicalPath()), 
        true);
      EObject _get = inputResource.getContents().get(0);
      final Model gdm = ((Model) _get);
      final long start = System.currentTimeMillis();
      final DocumentDataModel columnFamilyDM = Gdm2Document.transformGdm2Document(gdm);
      final long end = System.currentTimeMillis();
      String _format_1 = String.format("../es.unican.istr.mortadelo.gdm.examples/document/%sDOC.model", example);
      final File output = new File(_format_1);
      final Resource outputResource = resSet.createResource(
        URI.createURI(output.getCanonicalPath()));
      outputResource.getContents().add(columnFamilyDM);
      try {
        outputResource.save(Collections.EMPTY_MAP);
      } catch (final Throwable _t) {
        if (_t instanceof IOException) {
          final IOException e = (IOException)_t;
          e.printStackTrace();
        } else {
          throw Exceptions.sneakyThrow(_t);
        }
      }
      final long totalEnd = System.currentTimeMillis();
      InputOutput.<String>println("Transformation finished");
      InputOutput.<String>println(String.format("Transformation time: %d ms", Long.valueOf((end - start))));
      InputOutput.<String>println(
        String.format("Total time (read/write files and models): %d ms", 
          Long.valueOf((totalEnd - totalStart))));
    } catch (Throwable _e) {
      throw Exceptions.sneakyThrow(_e);
    }
  }
  
  public static DocumentDataModel transformGdm2Document(final Model gdm) {
    final DocumentDataModelFactory docFactory = DocumentDataModelFactory.eINSTANCE;
    final DocumentDataModel docModel = docFactory.createDocumentDataModel();
    final Function1<Query, Entity> _function = (Query q) -> {
      return q.getFrom().getEntity();
    };
    
    final Set<Entity> mainEntities = IterableExtensions.<Entity>toSet(ListExtensions.<Query, Entity>map(gdm.getQueries(), _function));
    final Function1<Entity, Pair<Entity, Iterable<Query>>> _function_1 = (Entity me) -> {
      final Function1<Query, Boolean> _function_2 = (Query q) -> {
        return Boolean.valueOf(q.getFrom().getEntity().equals(me));
      };
      Iterable<Query> _filter = IterableExtensions.<Query>filter(gdm.getQueries(), _function_2);
      return Pair.<Entity, Iterable<Query>>of(me, _filter);
    };

    final Iterable<Pair<Entity, Iterable<Query>>> entityToQueries = IterableExtensions.<Entity, Pair<Entity, Iterable<Query>>>map(mainEntities, _function_1);
    
    final Function1<Pair<Entity, Iterable<Query>>, Pair<Entity, Tree<Reference>>> _function_2 = (Pair<Entity, Iterable<Query>> e2q) -> {
      Entity _key = e2q.getKey();
      Tree<Reference> _createAccessTree = Gdm2Document.createAccessTree(e2q.getValue());
      return Pair.<Entity, Tree<Reference>>of(_key, _createAccessTree);
    };

    final Map<Entity, Tree<Reference>> entity2accessTree = CollectionLiterals.<Entity, Tree<Reference>>newImmutableMap(((Pair<? extends Entity, ? extends Tree<Reference>>[])Conversions.unwrapArray(IterableExtensions.<Pair<Entity, Iterable<Query>>, Pair<Entity, Tree<Reference>>>map(entityToQueries, _function_2), Pair.class)));

    for (final Entity entity : mainEntities) {
      {
        final Tree<Reference> tree = entity2accessTree.get(entity);
        Collection<Tree<Reference>> _values = entity2accessTree.values();
        final ArrayList<Tree<Reference>> otherTrees = new ArrayList<Tree<Reference>>(_values);
        otherTrees.remove(tree);
        Gdm2Document.completeAccessTree(entity, tree, otherTrees);
      }
    }
    
    for (final Entity entity_1 : mainEntities) {
      {
        final Tree<Reference> tree = entity2accessTree.get(entity_1);
        final documentDataModel.Collection newCol = docFactory.createCollection();
        newCol.setName(entity_1.getName());
        final Document docType = docFactory.createDocument();
        docType.setName("root");
        newCol.setRoot(docType);
        Gdm2Document.populateDocument(docType, docFactory, entity_1, tree, mainEntities);
        docModel.getCollections().add(newCol);
      }
    }
    return docModel;

  }
  
  /**
   * Obtains the access tree of an entity, including the reference traversed
   *  for each step of the path
   * 
   *  @returns A tree of pairs (traversed reference, destination entity)
   */
  private static Tree<Reference> createAccessTree(final Iterable<Query> queries) {
    final Tree<Reference> tree = new Tree<Reference>(null);
    for (final Query query : queries) {
      EList<Inclusion> _inclusions = query.getInclusions();
      for (final Inclusion inclusion : _inclusions) {
        {
          Tree<Reference> auxTree = tree;
          EList<Reference> _refs = inclusion.getRefs();
          for (final Reference ref : _refs) {
            {
              final Tree<Reference> child = auxTree.add(ref);
              auxTree = child;
            }
          }
        }
      }
    }
    return tree;
  }
  
  private static void completeAccessTree(final Entity entity, final Tree<Reference> tree, final Collection<Tree<Reference>> otherTrees) {
    for (final Tree<Reference> oTree : otherTrees) {
      {
        final List<Tree<Reference>> treeNodes = Gdm2Document.searchEntity(entity, oTree);
        for (final Tree<Reference> treeNode : treeNodes) {
          Gdm2Document.addTreeNode(tree, treeNode);
        }
      }
    }
  }
  
  private static List<Tree<Reference>> searchEntity(final Entity entity, final Tree<Reference> tree) {
    final ArrayList<Tree<Reference>> treeNodes = new ArrayList<Tree<Reference>>();
    List<Tree<Reference>> _children = tree.getChildren();
    for (final Tree<Reference> child : _children) {
      {
        boolean _equals = child.getData().getEntity().equals(entity);
        if (_equals) {
          treeNodes.add(child);
        }
        treeNodes.addAll(Gdm2Document.searchEntity(entity, child));
      }
    }
    return treeNodes;
  }
  
  private static void addTreeNode(final Tree<Reference> tree, final Tree<Reference> treeNode) {
    List<Tree<Reference>> _children = treeNode.getChildren();
    for (final Tree<Reference> child : _children) {
      {
        final Tree<Reference> addedChild = tree.add(child.getData());
        Gdm2Document.addTreeNode(addedChild, child);
      }
    }
  }
  
  private static void populateDocument(final Document document, final DocumentDataModelFactory docFactory, final Entity entity, final Tree<Reference> tree, final Set<Entity> mainEntities) {
    Gdm2Document.addAttributes(document, entity, docFactory);
    List<Tree<Reference>> _children = tree.getChildren();
    for (final Tree<Reference> child : _children) {
      {
        final Reference reference = child.getData();
        Field newField = null;
        boolean _contains = mainEntities.contains(reference.getEntity());
        if (_contains) {
          newField = docFactory.createPrimitiveField();
          String _firstLower = StringExtensions.toFirstLower(reference.getEntity().getName());
          String _plus = (_firstLower + "Ref");
          newField.setName(_plus);
          ((PrimitiveField) newField).setType(PrimitiveType.ID);
        } else {
          newField = docFactory.createDocument();
          newField.setName(StringExtensions.toFirstLower(reference.getEntity().getName()));
          Gdm2Document.populateDocument(((Document) newField), docFactory, reference.getEntity(), child, mainEntities);
        }
        boolean _equals = reference.getCardinality().equals("1");
        boolean _not = (!_equals);
        if (_not) {
          final ArrayField arrayField = docFactory.createArrayField();
          String _name = newField.getName();
          String _plus_1 = (_name + "Array");
          arrayField.setName(_plus_1);
          arrayField.setType(newField);
          document.getFields().add(arrayField);
        } else {
          document.getFields().add(newField);
        }
      }
    }
  }
  
  private static void addAttributes(final Document document, final Entity entity, final DocumentDataModelFactory docFactory) {
    final Function1<Feature, Boolean> _function = (Feature f) -> {
      return Boolean.valueOf((f instanceof Attribute));
    };
    Iterable<Feature> _filter = IterableExtensions.<Feature>filter(entity.getFeatures(), _function);
    for (final Feature attr : _filter) {
      {
        final PrimitiveField field = docFactory.createPrimitiveField();
        field.setName(attr.getName());
        field.setType(Gdm2Document.convertType(((Attribute) attr).getType()));
        document.getFields().add(field);
      }
    }
  }
  
  private static PrimitiveType convertType(final Type type) {
    if (type != null) {
      switch (type) {
        case ID:
          return PrimitiveType.ID;
        case NUMBER:
          return PrimitiveType.FLOAT;
        case DATE:
          return PrimitiveType.DATE;
        case TIMESTAMP:
          return PrimitiveType.TIMESTAMP;
        case BOOLEAN:
          return PrimitiveType.BOOLEAN;
        default:
          return PrimitiveType.TEXT;
      }
    } else {
      return PrimitiveType.TEXT;
    }
  }
}
