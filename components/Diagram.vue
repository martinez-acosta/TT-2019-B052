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
      myPalette: '',
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
      'myDiagramDiv', // must name or refer to the DIV HTML element
      {
        grid: $(go.Panel, 'Grid'),
        'draggingTool.dragsLink': true,
        'draggingTool.isGridSnapEnabled': true,
        'linkingTool.isUnconnectedLinkValid': true,
        'linkingTool.portGravity': 20,
        'relinkingTool.isUnconnectedLinkValid': true,
        'relinkingTool.portGravity': 20,
        'relinkingTool.fromHandleArchetype': $(go.Shape, 'Diamond', {
          segmentIndex: 0,
          cursor: 'pointer',
          desiredSize: new go.Size(8, 8),
          fill: 'tomato',
          stroke: 'darkred'
        }),
        'relinkingTool.toHandleArchetype': $(go.Shape, 'Diamond', {
          segmentIndex: -1,
          cursor: 'pointer',
          desiredSize: new go.Size(8, 8),
          fill: 'darkred',
          stroke: 'tomato'
        }),
        'linkReshapingTool.handleArchetype': $(go.Shape, 'Diamond', {
          desiredSize: new go.Size(7, 7),
          fill: 'lightblue',
          stroke: 'deepskyblue'
        }),
        'rotatingTool.handleAngle': 270,
        'rotatingTool.handleDistance': 30,
        'rotatingTool.snapAngleMultiple': 15,
        'rotatingTool.snapAngleEpsilon': 15,
        'undoManager.isEnabled': true
      }
    )

    const nodeSelectionAdornmentTemplate = $(
      go.Adornment,
      'Auto',
      $(go.Shape, {
        fill: null,
        stroke: 'deepskyblue',
        strokeWidth: 1.5,
        strokeDashArray: [4, 2]
      }),
      $(go.Placeholder)
    )

    const nodeResizeAdornmentTemplate = $(
      go.Adornment,
      'Spot',
      { locationSpot: go.Spot.Right },
      $(go.Placeholder),
      $(go.Shape, {
        alignment: go.Spot.TopLeft,
        cursor: 'nw-resize',
        desiredSize: new go.Size(6, 6),
        fill: 'lightblue',
        stroke: 'deepskyblue'
      }),
      $(go.Shape, {
        alignment: go.Spot.Top,
        cursor: 'n-resize',
        desiredSize: new go.Size(6, 6),
        fill: 'lightblue',
        stroke: 'deepskyblue'
      }),
      $(go.Shape, {
        alignment: go.Spot.TopRight,
        cursor: 'ne-resize',
        desiredSize: new go.Size(6, 6),
        fill: 'lightblue',
        stroke: 'deepskyblue'
      }),

      $(go.Shape, {
        alignment: go.Spot.Left,
        cursor: 'w-resize',
        desiredSize: new go.Size(6, 6),
        fill: 'lightblue',
        stroke: 'deepskyblue'
      }),
      $(go.Shape, {
        alignment: go.Spot.Right,
        cursor: 'e-resize',
        desiredSize: new go.Size(6, 6),
        fill: 'lightblue',
        stroke: 'deepskyblue'
      }),

      $(go.Shape, {
        alignment: go.Spot.BottomLeft,
        cursor: 'se-resize',
        desiredSize: new go.Size(6, 6),
        fill: 'lightblue',
        stroke: 'deepskyblue'
      }),
      $(go.Shape, {
        alignment: go.Spot.Bottom,
        cursor: 's-resize',
        desiredSize: new go.Size(6, 6),
        fill: 'lightblue',
        stroke: 'deepskyblue'
      }),
      $(go.Shape, {
        alignment: go.Spot.BottomRight,
        cursor: 'sw-resize',
        desiredSize: new go.Size(6, 6),
        fill: 'lightblue',
        stroke: 'deepskyblue'
      })
    )

    const nodeRotateAdornmentTemplate = $(
      go.Adornment,
      { locationSpot: go.Spot.Center, locationObjectName: 'CIRCLE' },
      $(go.Shape, 'Circle', {
        name: 'CIRCLE',
        cursor: 'pointer',
        desiredSize: new go.Size(7, 7),
        fill: 'lightblue',
        stroke: 'deepskyblue'
      }),
      $(go.Shape, {
        geometryString: 'M3.5 7 L3.5 30',
        isGeometryPositioned: true,
        stroke: 'deepskyblue',
        strokeWidth: 1.5,
        strokeDashArray: [4, 2]
      })
    )

    this.myDiagram.nodeTemplate = $(
      go.Node,
      'Spot',
      { locationSpot: go.Spot.Center },
      new go.Binding('location', 'loc', go.Point.parse).makeTwoWay(
        go.Point.stringify
      ),

      {
        selectable: true,
        selectionAdornmentTemplate: nodeSelectionAdornmentTemplate
      },
      {
        resizable: true,
        resizeObjectName: 'PANEL',
        resizeAdornmentTemplate: nodeResizeAdornmentTemplate
      },
      {
        rotatable: false,
        rotateAdornmentTemplate: nodeRotateAdornmentTemplate
      },
      new go.Binding('angle').makeTwoWay(),
      // the main object is a Panel that surrounds a TextBlock with a Shape
      $(
        go.Panel,
        'Auto',
        { name: 'PANEL' },
        new go.Binding('desiredSize', 'size', go.Size.parse).makeTwoWay(
          go.Size.stringify
        ),
        $(
          go.Shape,
          'Rectangle', // default figure
          {
            portId: '', // the default port: if no spot on link data, use closest side
            fromLinkable: true,
            toLinkable: true,
            cursor: 'pointer',
            fill: 'white', // default color
            strokeWidth: 2
          },
          new go.Binding('figure'),
          new go.Binding('fill')
        ),
        $(
          go.TextBlock,
          {
            font: 'bold 11pt Helvetica, Arial, sans-serif',
            margin: 8,
            maxSize: new go.Size(160, NaN),
            wrap: go.TextBlock.WrapFit,
            editable: true
          },
          new go.Binding('text').makeTwoWay()
        )
      ),
      // four small named ports, one on each side:
      this.makePort('T', go.Spot.Top, false, true),
      this.makePort('L', go.Spot.Left, true, true),
      this.makePort('R', go.Spot.Right, true, true),
      this.makePort('B', go.Spot.Bottom, true, false),
      {
        // handle mouse enter/leave events to show/hide the ports
        mouseEnter(e, node) {
          // this.showSmallPorts(node, true)
          node.ports.each((port) => {
            if (port.portId !== '') {
              // don't change the default port, which is the big shape
              port.fill = 'rgba(0,0,0,.3)'
            }
          })
        },
        mouseLeave(e, node) {
          // this.showSmallPorts(node, false)
          node.ports.each((port) => {
            if (port.portId !== '') {
              // don't change the default port, which is the big shape
              port.fill = null
            }
          })
        }
      }
    )
    const linkSelectionAdornmentTemplate = $(
      go.Adornment,
      'Link',
      $(
        go.Shape,
        // isPanelMain declares that this Shape shares the Link.geometry
        { isPanelMain: true, fill: null, stroke: 'deepskyblue', strokeWidth: 0 }
      ) // use selection object's strokeWidth
    )

    this.myDiagram.linkTemplate = $(
      go.Link, // the whole link panel
      {
        selectable: true,
        selectionAdornmentTemplate: linkSelectionAdornmentTemplate
      },
      { relinkableFrom: true, relinkableTo: true, reshapable: true },
      {
        routing: go.Link.AvoidsNodes,
        curve: go.Link.JumpOver,
        corner: 5,
        toShortLength: 0
      },
      new go.Binding('points').makeTwoWay(),
      $(
        go.Shape, // the link path shape
        { isPanelMain: true, strokeWidth: 2 }
      ),
      $(
        go.Shape, // the arrowhead
        { toArrow: '', stroke: null }
      ),
      $(
        go.Panel,
        'Auto',
        new go.Binding('visible', 'isSelected').ofObject(),
        $(
          go.Shape,
          'RoundedRectangle', // the link shape
          { fill: '#F8F8F8', stroke: null }
        ),
        $(
          go.TextBlock,
          {
            textAlign: 'center',
            font: '10pt helvetica, arial, sans-serif',
            stroke: '#919191',
            margin: 2,
            minSize: new go.Size(10, NaN),
            editable: true
          },
          new go.Binding('text').makeTwoWay()
        )
      )
    )

    go.Shape.defineFigureGenerator('EllipseInRectangle', function(shape, w, h) {
      const geo = new go.Geometry()
      geo.add(
        new go.PathFigure(0, 0)
          .add(new go.PathSegment(go.PathSegment.Line, w, 0))
          .add(new go.PathSegment(go.PathSegment.Line, w, h))
          .add(new go.PathSegment(go.PathSegment.Line, 0, h))
          .add(new go.PathSegment(go.PathSegment.Line, 0, 0))
      )
      geo.add(
        new go.PathFigure(0, 0).add(
          new go.PathSegment(
            go.PathSegment.Arc,
            180,
            360,
            w / 2,
            h / 2,
            w / 2,
            h / 2
          )
        )
      )
      geo.spot1 = new go.Spot(0, 0, 25, 25)
      geo.spot2 = new go.Spot(1, 1, -25, -25)
      return geo
    })

    go.Shape.defineFigureGenerator('weakDiamond', function(shape, w, h) {
      let param1 = shape ? shape.parameter1 : NaN
      let param2 = shape ? shape.parameter2 : NaN
      if (isNaN(param1)) param1 = 8 // default values PARAMETER 1 is for WIDTH
      if (isNaN(param2)) param2 = 8 // default values PARAMETER 2 is for HEIGHT

      const geo = new go.Geometry()
      const fig = new go.PathFigure(0.5 * w, 0, true)
      geo.add(fig)
      // outer diamond, clockwise
      fig.add(new go.PathSegment(go.PathSegment.Line, 0, 0.5 * h))
      fig.add(new go.PathSegment(go.PathSegment.Line, 0.5 * w, h))
      fig.add(new go.PathSegment(go.PathSegment.Line, w, 0.5 * h).close())
      if (param1 < w / 2 && param2 < h / 2) {
        // inner diamond, counter-clockwise
        fig.add(new go.PathSegment(go.PathSegment.Move, 0.5 * w, param2)) // subpath
        fig.add(
          new go.PathSegment(go.PathSegment.Line, w - param1 * 2, 0.5 * h)
        )
        fig.add(new go.PathSegment(go.PathSegment.Line, 0.5 * w, h - param2))
        fig.add(
          new go.PathSegment(go.PathSegment.Line, param1 * 2, 0.5 * h).close()
        )
      }
      geo.spot1 = new go.Spot(0, 0, 25, 25)
      geo.spot2 = new go.Spot(1, 1, -25, -25)
      return geo
    })

    go.Shape.defineFigureGenerator('FramedEllipse', function(shape, w, h) {
      const geo = new go.Geometry()
      geo.add(
        new go.PathFigure(0, 0)
          .add(new go.PathSegment(go.PathSegment.Line, w, 0))
          .add(new go.PathSegment(go.PathSegment.Line, w, h))
          .add(new go.PathSegment(go.PathSegment.Line, 0, h))
          .add(new go.PathSegment(go.PathSegment.Line, 0, 0))
      )
      geo.add(
        new go.PathFigure(0, 0).add(
          new go.PathSegment(
            go.PathSegment.Arc,
            180,
            360,
            w / 2,
            h / 2,
            w / 2,
            h / 2
          )
        )
      )
      geo.spot1 = new go.Spot(0, 0, 25, 25)
      geo.spot2 = new go.Spot(1, 1, -25, -25)
      return geo
    })

    go.Shape.defineFigureGenerator('FramedRectangle', function(shape, w, h) {
      let param1 = shape ? shape.parameter1 : NaN
      let param2 = shape ? shape.parameter2 : NaN
      if (isNaN(param1)) param1 = 8 // default values PARAMETER 1 is for WIDTH
      if (isNaN(param2)) param2 = 8 // default values PARAMETER 2 is for HEIGHT

      const geo = new go.Geometry()
      const fig = new go.PathFigure(0, 0, true)
      geo.add(fig)
      // outer rectangle, clockwise
      fig.add(new go.PathSegment(go.PathSegment.Line, w, 0))
      fig.add(new go.PathSegment(go.PathSegment.Line, w, h))
      fig.add(new go.PathSegment(go.PathSegment.Line, 0, h).close())
      if (param1 < w / 2 && param2 < h / 2) {
        // inner rectangle, counter-clockwise
        fig.add(new go.PathSegment(go.PathSegment.Move, param1, param2)) // subpath
        fig.add(new go.PathSegment(go.PathSegment.Line, param1, h - param2))
        fig.add(new go.PathSegment(go.PathSegment.Line, w - param1, h - param2))
        fig.add(
          new go.PathSegment(go.PathSegment.Line, w - param1, param2).close()
        )
      }
      geo.setSpots(0, 0, 1, 1, param1, param2, -param1, -param2)
      return geo
    })

    // Para cargar el diagrama por si hay uno ya existente

    /* Creamos el modelo de datos, está conformado por dos partes, los nodos y los links, [nodos], [links] donde los links tienen la estructura { from: a, to: b } siendo a, b las llaves de los objetos que están en el arreglo nodos */

    if (this.existeDiagrama) {
      this.myDiagram.model = new go.GraphLinksModel()
      this.myDiagram.model = go.Model.fromJson(this.diagramaObtenido)
      const pos = this.myDiagram.model.modelData.position
      if (pos) this.myDiagram.initialPosition = go.Point.parse(pos)
    } else {
      this.myDiagram.model = new go.GraphLinksModel()
    }
    /** *****************Paleta***********************/
    // initialize the Palette that is on the right side of the page
    this.myPalette = $(
      go.Palette,
      'myPaletteDiv', // must name or refer to the DIV HTML element
      {
        maxSelectionCount: 1,
        nodeTemplateMap: this.myDiagram.nodeTemplateMap, // share the templates used by myDiagram
        // simplify the link template, just in this Palette
        linkTemplate: $(
          go.Link,
          {
            // because the GridLayout.alignment is Location and the nodes have locationSpot == Spot.Center,
            // to line up the Link in the same manner we have to pretend the Link has the same location spot
            locationSpot: go.Spot.Center,
            selectionAdornmentTemplate: $(
              go.Adornment,
              'Link',
              { locationSpot: go.Spot.Center },
              $(go.Shape, {
                isPanelMain: true,
                fill: null,
                stroke: 'deepskyblue',
                strokeWidth: 0
              })
            )
          },
          {
            routing: go.Link.AvoidsNodes,
            curve: go.Link.JumpOver,
            corner: 5,
            toShortLength: 4
          },
          new go.Binding('points'),
          $(
            go.Shape, // the link path shape
            { isPanelMain: true, strokeWidth: 2 }
          )
        ),
        model: new go.GraphLinksModel(
          [
            // specify the contents of the Palette
            {
              category: 'entity',
              text: 'Entidad',
              figure: 'Rectangle',
              fill: 'white'
            },
            {
              category: 'weakEntity',
              text: 'Entidad débil',
              figure: 'FramedRectangle',
              fill: 'yellow'
            },
            {
              category: 'atribute',
              text: 'Atributo',
              figure: 'Ellipse',
              fill: 'white'
            },
            {
              category: 'atributeComposite',
              text: 'Att compuesto',
              figure: 'FramedEllipse',
              fill: 'white'
            },
            {
              category: 'weakRelation',
              text: 'Relación débil',
              figure: 'weakDiamond',
              fill: 'white'
            },
            {
              category: 'relation',
              text: 'Relación',
              figure: 'Diamond',
              fill: 'lightskyblue'
            }
          ],
          [
            // the Palette also has a disconnected Link, which the user can drag-and-drop
            {
              points: new go.List(/* go.Point */).addAll([
                new go.Point(0, 0),
                new go.Point(30, 0),
                new go.Point(30, 40),
                new go.Point(60, 40)
              ])
            }
          ]
        )
      }
    )
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
    loadModel() {},
    // Define a function for creating a "port" that is normally transparent.
    // The "name" is used as the GraphObject.portId, the "spot" is used to control how links connect
    // and where the port is positioned on the node, and the boolean "output" and "input" arguments
    // control whether the user can draw links from or to the port.

    makePort(name, spot, output, input) {
      const $ = go.GraphObject.make
      // the port is basically just a small transparent square
      return $(go.Shape, 'Circle', {
        fill: null, // not seen, by default; set to a translucent gray by showSmallPorts, defined below
        stroke: null,
        desiredSize: new go.Size(7, 7),
        alignment: spot, // align the port on the main Shape
        alignmentFocus: spot, // just inside the Shape
        portId: name, // declare this object to be a "port"
        fromSpot: spot,
        toSpot: spot, // declare where links may connect at this port
        fromLinkable: output,
        toLinkable: input, // declare whether the user may draw links to/from here
        cursor: 'pointer' // show a different cursor to indicate potential link point
      })
    },
    showSmallPorts(node, show) {
      node.ports.each(function(port) {
        if (port.portId !== '') {
          // don't change the default port, which is the big shape
          port.fill = show ? 'rgba(0,0,0,.3)' : null
        }
      })
    }
  }
}
</script>

<style>
#myDiagramDiv {
  width: 1000px;
  height: 1000px;
}
</style>
