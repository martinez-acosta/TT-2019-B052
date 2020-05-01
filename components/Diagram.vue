<template>
  <v-app>
    <div style="width: 100%; display: flex; justify-content: space-between">
      <div
        id="myDiagramDiv"
        style="flex-grow: 1; height: 600px; border: solid 1px black"
      ></div>
      <div
        id="myPaletteDiv"
        style="width: 200px; background-color: whitesmoke; border: solid 1px black"
      ></div>
    </div>
    <div id="buttons">
      <v-btn color="primary" @click="saveModel">Save</v-btn>
      <v-btn color="primary" @click="loadModel">Load</v-btn>
      <v-btn @click="addNode">Add Child to Gamma</v-btn>

      <v-textarea
        v-model="diagramaObtenido"
        auto-grow
        style="width:100%;height:250px"
      ></v-textarea>
    </div>
  </v-app>
</template>

<script>
import go from 'gojs'
import { mapGetters } from 'vuex'

export default {
  data() {
    return {
      myDiagram: '',
      diagramData: {
        // Diagrama prueba
        nodeDataArray: [
          { key: 1, text: 'Alpha', color: 'lightblue' },
          { key: 2, text: 'Beta', color: 'orange' },
          { key: 3, text: 'Gamma', color: 'lightgreen' },
          { key: 4, text: 'Delta', color: 'pink' }
        ],
        linkDataArray: [
          { from: 1, to: 2 },
          { from: 1, to: 3 },
          { from: 3, to: 4 }
        ]
      },
      currentNode: '',
      savedModel: '',
      counter: 1, // used by addNode
      counter2: 4 // used by modifyStuff
    }
  },
  computed: {
    ...mapGetters({
      existeDiagrama: 'diagram/existDiagram',
      diagramaObtenido: 'diagram/getDiagram'
    }),
    currentNodeText: {
      get() {
        const node = this.currentNode
        if (node instanceof go.Node) {
          return node.data.text
        } else {
          return ''
        }
      },
      set(val) {
        const node = this.currentNode
        if (node instanceof go.Node) {
          const model = this.model()
          model.startTransaction()
          model.setDataProperty(node.data, 'text', val)
          model.commitTransaction('edited text')
        }
      }
    }
  },
  mounted() {
    /* Siempre el objeto será creado cuando el componente entre en el hook mounted(). Es decir, debemos recuperar el estado anterior del diagrama mediante un estado compartido entre componentes en Vuex o por otro medio. Falta implementarlo. */
    const $ = go.GraphObject.make // for conciseness in defining templates
    this.myDiagram = $(
      go.Diagram,
      'myDiagramDiv', // Creamos el diagrama en el div con el identificar myDiagramDiv
      {
        // Opciones del diagrama
        layout: $(go.TreeLayout, {
          angle: 90,
          arrangement: go.TreeLayout.ArrangementHorizontal
        }),
        // enable undo & redo
        'undoManager.isEnabled': true
      }
    )

    // define a simple Node template
    /*  myDiagram.nodeTemplate = $(
      go.Node,
      'Auto', // the Shape will go around the TextBlock
      $(
        go.Shape,
        'RoundedRectangle',
        { strokeWidth: 0, fill: 'white' }, // default fill is white
        // Shape.fill is bound to Node.data.color
        new go.Binding('fill', 'color')
      ),
      $(
        go.TextBlock,
        { margin: 8 }, // some room around the text
        // TextBlock.text is bound to Node.data.key
        new go.Binding('text', 'key')
      )
    )
    */
    this.myDiagram.nodeTemplate = $(
      go.Node,
      'Auto',
      $(
        go.Shape,
        {
          fill: 'white',
          strokeWidth: 0,
          portId: '',
          fromLinkable: true,
          toLinkable: true,
          cursor: 'pointer'
        },
        new go.Binding('fill', 'color')
      ),
      $(
        go.TextBlock,
        { margin: 8, editable: true },
        new go.Binding('text').makeTwoWay()
      )
    )

    this.myDiagram.linkTemplate = $(
      go.Link,
      { relinkableFrom: true, relinkableTo: true },
      $(go.Shape),
      $(go.Shape, { toArrow: 'OpenTriangle' })
    )
    // but use the default Link template, by not setting Diagram.linkTemplate
    if (this.existeDiagrama) {
      this.myDiagram.model = new go.GraphLinksModel()
      this.myDiagram.model = go.Model.fromJson(this.diagramaObtenido)
      const pos = this.myDiagram.model.modelData.position
      if (pos) this.myDiagram.initialPosition = go.Point.parse(pos)
    } else {
      this.myDiagram.model = new go.GraphLinksModel(
        /* Creamos el modelo de datos, está conformado por dos partes, los nodos y los links, [nodos], [links] donde los links tienen la estructura { from: a, to: b } siendo a, b las llaves de los objetos que están en el arreglo nodos */
        // diagramData está definido como un elemento de data() del componente en Vue
        this.diagramData.nodeDataArray,
        this.diagramData.linkDataArray
      )
    }
  },
  beforeDestroy() {
    this.saveModel()
  },
  middleware: 'authenticated',
  layout: 'workspace', // layout de la aplicación (esto es de nuxt)
  methods: {
    // get access to the GoJS Model of the GoJS Diagram
    model() {
      return this.$refs.hola.model()
    },

    // tell the GoJS Diagram to update based on the arbitrarily modified model data
    updateDiagramFromData() {
      this.$refs.diag.updateDiagramFromData()
    },

    // this event listener is declared on the <diagram>
    modelChanged(e) {
      if (e.isTransactionFinished) {
        // show the model data in the page's TextArea
        this.savedModelText = e.model.toJson()
      }
    },

    changedSelection(e) {
      const node = e.diagram.selection.first()
      if (node instanceof go.Node) {
        this.currentNode = node
        this.currentNodeText = node.data.text
      } else {
        this.currentNode = null
        this.currentNodeText = ''
      }
    },
    saveDiagramProperties() {
      this.myDiagram.model.modelData.position = go.Point.stringify(
        this.myDiagram.position
      )
    },
    loadDiagramProperties(e) {
      // set Diagram.initialPosition, not Diagram.position, to handle initialization side-effects
      const pos = this.myDiagram.model.modelData.position
      if (pos) this.myDiagram.initialPosition = go.Point.parse(pos)
    },
    // Here we modify the GoJS Diagram's Model using its methods,
    // which can be much more efficient than modifying some memory and asking
    // the GoJS Diagram to find differences and update accordingly.
    // Undo and Redo will work as expected.
    addNode() {
      const model = this.myDiagram.model
      model.startTransaction()
      model.setDataProperty(model.findNodeDataForKey(4), 'color', 'purple')
      const data = { text: 'NEW ' + this.counter++, color: 'yellow' }
      model.addNodeData(data)
      model.addLinkData({ from: 3, to: model.getKeyForNodeData(data) })
      model.commitTransaction('added Node and Link')

      // also manipulate the Diagram by changing its Diagram.selection collection
      // const diagram = this.myDiagram.diagram
      // diagram.select(diagram.findNodeForData(data))
    },

    // Here we modify VUE's view model directly, and
    // then ask the GoJS Diagram to update everything from the data.
    // This is less efficient than calling the appropriate GoJS Model methods.
    // NOTE: Undo will not be able to restore all of the state properly!!
    modifyStuff() {
      const data = this.diagramData
      data.nodeDataArray[0].color = 'red'
      // Note here that because we do not have the GoJS Model,
      // we cannot find out what values would be unique keys, for reference by the link data.
      data.nodeDataArray.push({
        key: ++this.counter2,
        text: this.counter2.toString(),
        color: 'orange'
      })
      data.linkDataArray.push({ from: 2, to: this.counter2 })
      this.updateDiagramFromData()
    },
    saveModel() {
      this.saveDiagramProperties()
      this.savedModel = this.myDiagram.model.toJson()
      this.myDiagram.isModified = false
      //  console.log('savedModel: ' + this.savedModel)
      this.$store.dispatch('diagram/save', {
        savedModel: this.savedModel
      })
    },
    loadModel() {}
  }
}
</script>

<style>
#myDiagramDiv {
  width: 1000px;
  height: 1000px;
}
</style>
