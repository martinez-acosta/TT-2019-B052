<template>
  <v-container>
    <v-row no-gutters style="height:80vh" dense>
      <v-col
        v-show="mostrarPaleta"
        cols="4"
        class="white lighten-2 fill-height d-flex flex-column"
      >
        <div
          v-show="mostrarPaleta"
          id="myPaletteDiv"
          style="width: 100%; display: flex; border: solid 0px black; height: 80%;"
        ></div>
        <div id="myInspectorDiv"></div>
      </v-col>
      <v-col class="white fill-height d-flex flex-column ">
        <div
          id="myDiagramDiv"
          style="width: 100%; display: flex; border: solid 1px black; height: 100%;"
        ></div>
      </v-col>
    </v-row>
  </v-container>
</template>
<script type="module">
import { go } from 'gojs/release/go-module'
import 'gojs/extensionsJSM/Figures'
import { mapGetters } from 'vuex'
import { Inspector } from 'gojs/extensionsJSM/DataInspector'

export default {
  props: {
    showpallete: { type: String, default: 'true' },
    readonly: { type: String, default: 'false' }
  },
  css: ['gojs/extensionsJSM/DataInspector.css'],
  data() {
    return {
      myDiagram: '',
      myPalette: '',
      myInspector: '',
      mostrarPaleta: this.showpallete,
      soloLectura: this.readonly
    }
  },
  computed: {
    ...mapGetters({
      thereIsDiagram: 'diagramER/existDiagram',
      diagramaObtenido: 'diagramER/getDiagram'
    })
  },
  mounted() {
    /* Siempre el objeto será creado cuando el componente entre en el hook mounted(). Es decir, 
    debemos recuperar el estado anterior del diagrama mediante un estado compartido entre componentes en Vuex 
    o por otro medio. Está implementado en Vuex. */
    const $ = go.GraphObject.make // for conciseness in defining templates

    // Definimos el diagrama
    this.myDiagram = $(
      go.Diagram,
      'myDiagramDiv', // must name or refer to the DIV HTML element
      {
        grid: $(go.Panel, 'Grid'),
        'draggingTool.dragsLink': true,
        'draggingTool.isGridSnapEnabled': true,
        'linkingTool.isUnconnectedLinkValid': true,
        'linkingTool.portGravity': 20,
        'relinkingTool.isUnconnectedLinkValid': false,
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
        'undoManager.isEnabled': true
      }
    )

    // Decoraciones de la selección y escalado
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

    const linkSelectionAdornmentTemplate = $(
      go.Adornment,
      'Link',
      $(
        go.Shape,
        // isPanelMain declares that this Shape shares the Link.geometry
        {
          isPanelMain: true,
          fill: null,
          stroke: 'deepskyblue',
          strokeWidth: 0
        }
      ) // use selection object's strokeWidth
    )

    /* Creamos el modelo de datos, está conformado por dos partes, los nodos y los links, [nodos], [links] donde los links tienen la estructura { from: a, to: b } siendo a, b las llaves de los objetos que están en el arreglo nodos */
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
            fill: 'transparent' // default color
            // strokeWidth: 2
          },
          new go.Binding('figure'),
          new go.Binding('fill'),
          new go.Binding('strokeDashArray')
        ),
        $(
          go.TextBlock,
          {
            font: 'bold 11pt Lato, Helvetica, Arial, sans-serif',
            margin: 10,
            maxSize: new go.Size(160, NaN),
            wrap: go.TextBlock.WrapFit,
            isMultiline: false,
            editable: true
          },
          new go.Binding('text').makeTwoWay(),
          new go.Binding('isUnderline')
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

    this.myDiagram.linkTemplate = $(
      go.Link, // the whole link panel
      {
        selectionAdorned: true,
        selectionAdornmentTemplate: linkSelectionAdornmentTemplate,
        layerName: 'Foreground',
        reshapable: true,
        routing: go.Link.AvoidsNodes,
        corner: 5,
        curve: go.Link.JumpOver
      },
      $(
        go.Shape, // the link shape
        { stroke: '#303B45', strokeWidth: 2.5 }
      ),
      $(
        go.TextBlock, // the "from" label
        {
          text: '',
          textAlign: 'center',
          font: 'bold 14px sans-serif',
          stroke: '#1967B3',
          editable: true,
          segmentIndex: 0,
          segmentOffset: new go.Point(NaN, NaN),
          segmentOrientation: go.Link.OrientUpright
        },
        new go.Binding('text', 'fromText').makeTwoWay()
      ),
      $(
        go.TextBlock, // the "to" label
        {
          text: '',
          textAlign: 'center',
          font: 'bold 14px sans-serif',
          stroke: '#1967B3',
          editable: true,
          segmentIndex: -1,
          segmentOffset: new go.Point(NaN, NaN),
          segmentOrientation: go.Link.OrientUpright
        },
        new go.Binding('text', 'toText').makeTwoWay()
      )
    )

    // Figuras generadas
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
        new go.PathFigure(0, h / 2).add(
          new go.PathSegment(
            go.PathSegment.Arc,
            180,
            360,
            w / 2,
            h / 2,
            w / 2,
            h / 2
          ).close()
        )
      )

      geo.add(
        new go.PathFigure(8, h / 2).add(
          new go.PathSegment(
            go.PathSegment.Arc,
            180,
            360,
            w / 2,
            h / 2,
            w / 2 - 8,
            h / 2 - 8
          ).close()
        )
      )

      geo.spot1 = new go.Spot(0, 0, 25, 25)
      geo.spot2 = new go.Spot(1, 1, -25, -25)
      return geo
    })

    // Para cargar el diagrama por si hay uno ya existente

    if (this.thereIsDiagram) {
      this.myDiagram.model = new go.GraphLinksModel()
      this.myDiagram.model = go.Model.fromJson(this.diagramaObtenido)
      const pos = this.myDiagram.model.modelData.position
      if (pos) this.myDiagram.initialPosition = go.Point.parse(pos)
    } else {
      this.myDiagram.model = new go.GraphLinksModel()
    }

    // select a Node, so that the first Inspector shows something
    this.myDiagram.select(this.myDiagram.nodes.first())
    this.myInspector = new Inspector('myInspectorDiv', this.myDiagram, {
      // allows for multiple nodes to be inspected at once
      multipleSelection: false,
      // max number of node properties will be shown when multiple selection is true
      showSize: 4,
      // when multipleSelection is true, when showAllProperties is true it takes the union of properties
      // otherwise it takes the intersection of properties
      showAllProperties: true,
      // uncomment this line to only inspect the named properties below instead of all properties on each object:
      // includesOwnProperties: false,
      properties: {
        text: { show: Inspector.showIfPresent },
        // key would be automatically added for nodes, but we want to declare it read-only also:
        // key: { readOnly: true, show: Inspector.showIfPresent },
        // color would be automatically added for nodes, but we want to declare it a color also:
        color: { show: Inspector.showIfPresent, type: 'color' },
        // Comments and LinkComments are not in any node or link data (yet), so we add them here:
        Comments: { show: Inspector.showIfNode },
        // LinkComments: { show: Inspector.showIfLink },
        toText: { show: Inspector.showIfLink },
        fromText: { show: Inspector.showIfLink },
        isGroup: { readOnly: true, show: Inspector.showIfPresent },
        // flag: { show: Inspector.showIfNode, type: 'checkbox' },
        /* state: {
          show: Inspector.showIfNode,
          type: 'select',
          choices(node, propName) {
            if (Array.isArray(node.data.choices)) return node.data.choices
            return ['one', 'two', 'three', 'four', 'five']
          }
        } */
        choices: { show: false }, // must not be shown at all
        to: { readOnly: true },
        from: { readOnly: true },
        // an example of specifying the <input> type
        password: { show: Inspector.showIfPresent, type: 'password' }
      }
    })

    /** *****************Paleta***********************/
    // initialize the Palette that is on the left side of the page
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
            locationSpot: go.Spot.Center
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
        model: new go.GraphLinksModel([
          // specify the contents of the Palette
          {
            type: 'entity',
            text: 'Entidad',
            figure: 'Rectangle',
            fill: 'white'
          },
          {
            type: 'atribute',
            text: 'Atributo',
            figure: 'Ellipse',
            fill: 'white'
          },
          {
            type: 'relation',
            text: 'Relación',
            figure: 'Diamond',
            fill: 'white'
          },
          {
            type: 'weakEntity',
            text: 'Entidad débil',
            figure: 'FramedRectangle',
            fill: 'white'
          },
          {
            type: 'keyAttribute',
            text: 'Atributo clave',
            figure: 'Ellipse',
            isUnderline: true,
            fill: 'white'
          },
          {
            type: 'derivedAttribute',
            text: 'att derivado',
            figure: 'Ellipse',
            fill: 'white',
            strokeDashArray: [4, 2]
          },
          {
            type: 'atributeComposite',
            text: 'Att compuesto',
            figure: 'FramedEllipse',
            fill: 'white',
            strokeDashArray: [4, 2]
          },
          {
            type: 'weakRelation',
            text: 'Relación débil',
            figure: 'weakDiamond',
            fill: 'white'
          }
        ])
      }
    )

    if (!this.soloLectura) this.myDiagram.isReadOnly = true
    // Listeners de SubNavBar.vue
    this.$nuxt.$on('saveModel', () => {
      this.saveModel()
    })

    this.$nuxt.$on('loadModel', () => {
      this.loadModel()
    })

    this.$nuxt.$on('cleanCanvas', () => {
      this.cleanCanvas()
    })
  },
  created() {},
  updated() {},
  beforeDestroy() {
    this.saveModel()
    // Eliminamos los listeners de SubNavBar.vue
    this.$nuxt.$off('saveModel')
    this.$nuxt.$off('loadModel')
    this.$nuxt.$off('cleanCanvas')
  },
  middleware: 'authenticated',
  layout: 'workspace', // layout de la aplicación (esto es de nuxt)
  methods: {
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
    saveModel() {
      this.saveDiagramProperties()
      this.savedModel = this.myDiagram.model.toJson()
      this.myDiagram.isModified = false
      this.$store
        .dispatch('diagramER/save', {
          savedModel: this.savedModel
        })
        .then(() => {
          this.$snotify.success('Guardado correctamente.')
        })
        .catch(() => {
          this.$snotify.error(
            '¡Algo ocurrió! El diagrama no ha sido guardado, intente más tarde.'
          )
        })
    },
    loadModel() {
      this.$store
        .dispatch('diagramER/getLastDiagram')
        .then((response) => {
          this.myDiagram.model = go.Model.fromJson(response.data.diagram)
          this.$snotify.success('Diagrama cargado correctamente.')
        })
        .catch((err) => {
          console.log(err)
          this.$snotify.error(
            '¡Algo ocurrió! No se ha encontrado un diagrama asociado a este perfil.'
          )
        })
    },
    cleanCanvas() {
      this.myDiagram.model = go.Model.fromJson({})
    },
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
        cursor: 'pointer', // show a different cursor to indicate potential link point
        mouseEnter(e, port) {
          // the PORT argument will be this Shape
          if (!e.diagram.isReadOnly) port.fill = 'rgba(255,0,255,0.5)'
        },
        mouseLeave(e, port) {
          port.fill = 'transparent'
        }
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
@import 'gojs/extensionsJSM/DataInspector.css';
</style>
