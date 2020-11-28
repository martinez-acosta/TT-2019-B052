<template>
  <v-container>
    <v-row no-gutters style="height: 80vh" dense class="ma-0 pa-0">
      <v-col class="white fill-height d-flex flex-column">
        <div style="position: relative;   height: 100%;">
          <div
            id="myDiagramDiv"
            style="width: 100%; display: flex; border: solid 1px black; height: 100%;"
          ></div>
        </div>
      </v-col>
    </v-row>
  </v-container>
</template>
<script type="module">
import { go } from 'gojs/release/go-module'
import 'gojs/extensionsJSM/Figures'
import { mapGetters } from 'vuex'

export default {
  props: {},
  css: ['gojs/extensionsJSM/DataInspector.css'],
  data() {
    return {
      myDiagram: ''
    }
  },
  computed: {
    ...mapGetters({
      thereIsDiagram: 'vuexER/existDiagram',
      diagramaObtenido: 'vuexER/getDiagram'
    })
  },
  mounted() {
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
      {
        locationSpot: go.Spot.Center
      },
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

    this.PathPatterns = new go.Map()

    this.definePathPattern('simple', 'M0 0 L1 0')
    this.definePathPattern('total', 'M0 0 L1 0 M0 3 L1 3')

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
        go.Shape, // the link's path shape
        { isPanelMain: true, stroke: 'simple' },
        new go.Binding('stroke', 'participacion'),
        new go.Binding(
          'pathPattern',
          'participacion',
          this.convertPathPatternToShape
        )
      ),
      $(
        go.TextBlock, // the "cardinality" label
        {
          text: '',
          textAlign: 'center',
          font: 'bold 14px sans-serif',
          stroke: '#1967B3',
          editable: true,
          segmentOffset: new go.Point(0, -10),
          segmentOrientation: go.Link.OrientUpright
        },
        new go.Binding('text', 'cardinality').makeTwoWay()
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

    // Para cargar el diagrama por si hay uno existente
    if (this.thereIsDiagram) {
      this.myDiagram.model = new go.GraphLinksModel()
      this.myDiagram.model = go.Model.fromJson(this.diagramaObtenido)
      const pos = this.myDiagram.model.modelData.position
      if (this.soloLectura) {
        // this.myDiagram.allowCopy = false
        // this.myDiagram.allowDelete = false
        // this.myDiagram.allowClipboard = false
        this.myDiagram.allowTextEdit = false
        this.myDiagram.allowLink = false
        this.myDiagram.allowReLink = false
        this.myDiagram.allowUndo = false
      }
      if (pos) this.myDiagram.initialPosition = go.Point.parse(pos)
    } else {
      this.myDiagram.model = new go.GraphLinksModel()
    }

    // select a Node, so that the first Inspector shows something
    this.myDiagram.select(this.myDiagram.nodes.first())
  },
  beforeDestroy() {},
  middleware: 'authenticated',
  layout: 'workspace', // layout de la aplicación (esto es de nuxt)
  methods: {
    // tell the GoJS Diagram to update based on the arbitrarily modified model data
    updateDiagramFromData() {
      this.$refs.diag.updateDiagramFromData()
    },
    saveDiagramProperties() {
      this.myDiagram.model.modelData.position = go.Point.stringify(
        this.myDiagram.position
      )
    },
    vuexSaveModel() {
      this.saveDiagramProperties()
      this.savedModel = this.myDiagram.model.toJson()
      this.myDiagram.isModified = false
      this.$store.dispatch('vuexER/save', {
        savedModel: this.savedModel
      })
    },
    vuexLoadModel() {
      this.$store.dispatch('vuexER/getLastDiagram')
    },
    axiosSaveModel() {
      this.saveDiagramProperties()
      this.savedModel = this.myDiagram.model.toJson()
      this.myDiagram.isModified = false
      this.$store
        .dispatch('axiosER/save', {
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
    axiosLoadModel() {
      this.$store
        .dispatch('axiosER/getLastDiagram')
        .then((response) => {
          this.myDiagram.model = go.Model.fromJson(response.data.diagram)
          this.$snotify.success('Diagrama cargado correctamente.')
        })
        .catch(() => {
          this.$snotify.error(
            '¡Algo ocurrió! No se ha encontrado un diagrama asociado a este perfil.'
          )
        })
    },
    cleanCanvas() {
      this.myDiagram.model = go.Model.fromJson({})
    },
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
    },
    definePathPattern(name, geostr, color, width, cap) {
      const $ = go.GraphObject.make
      if (typeof name !== 'string' || typeof geostr !== 'string')
        throw new Error(
          'invalid name or geometry string argument: ' + name + ' ' + geostr
        )
      if (color === undefined) color = 'black'
      if (width === undefined) width = 1
      if (cap === undefined) cap = 'square'
      this.PathPatterns.set(
        name,
        $(go.Shape, {
          geometryString: geostr,
          fill: 'transparent',
          stroke: color,
          strokeWidth: width,
          strokeCap: cap
        })
      )
    },
    convertPathPatternToShape(name) {
      if (!name) return null
      return this.PathPatterns.get(name)
    }
  }
}
</script>

<style></style>
