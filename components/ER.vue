<template>
  <v-container fluid>
    <client-only>
      <vue-snotify></vue-snotify>
    </client-only>
    <v-row no-gutters style="height: 80vh" dense class="ma-0 pa-0">
      <v-col
        v-if="mostrarPaleta"
        cols="2"
        class="white lighten-2 fill-height d-flex flex-column"
      >
        <v-btn
          :download="scriptName"
          :href="urlFile"
          @click="downloadGoJSData()"
        >
          Descargar Gojs</v-btn
        >
        <div
          v-show="mostrarPaleta"
          id="myPaletteDiv"
          style="
            width: 100%;
            display: flex;
            border: solid 0px black;
            height: 70%;           
          "
        ></div>
        <div v-show="mostrarPaleta" id="myInspectorDiv"></div>
      </v-col>
      <v-col class="white fill-height d-flex flex-column">
        <!-- We make a div to contain both the Diagram div and the context menu (such that they are siblings)
         so that absolute positioning works easily.
         This DIV containing both MUST have a non-static CSS position (we use position: relative)
         so that our context menu's absolute coordinates work correctly. -->
        <div style="position: relative; height: 100%">
          <div
            id="myDiagramDiv"
            style="
              width: 100%;
              display: flex;
              border: solid 1px black;
              height: 100%;
            "
          ></div>
          <ul id="contextMenu" class="menu">
            <li
              id="givenValue"
              class="menu-item"
              @click="givenValue('givenValue')"
            >
              Respecto al atributo (=)
            </li>
            <li><hr /></li>
            <li
              id="findValue"
              class="menu-item"
              @click="findValue('findValue')"
            >
              Encontrar el atributo
            </li>
          </ul>
        </div>
      </v-col>
      <v-col cols="3">
        <div id="myOverviewDiv"></div>
        <div v-show="mostrarPaleta" id="myNotes" class="h-50" scrollable>
          <v-col cols="12">
            <v-card color="white" max-width="400">
              <v-card-subtitle class="headline" color>
                Notas:
              </v-card-subtitle>
              <v-card-text>
                Modelo relacional
              </v-card-text>
              <v-card-subtitle class="caption">
                <v-icon small left>mdi-table-row-height</v-icon>
                <span class="font-weight-light"
                  >DataSize: es el tamaño de dato para la transformación a
                  sentencias SQL, este campo solo acepta valores entre 1 y
                  255.</span
                >
              </v-card-subtitle>
              <v-card-subtitle class="caption">
                <v-icon small left>mdi-format-list-bulleted-type</v-icon>
                <span class="font-weight-light"
                  >DataType: es el tipo de dato para la transformación a
                  sentencias SQL, se consideran solo los tipos de datos mas
                  utilizads en MySQL.</span
                >
              </v-card-subtitle>
              <v-card-subtitle class="caption">
                <v-icon small left>mdi-null</v-icon>
                <span class="font-weight-light"
                  >NotNull: es el indicador para señalar si el atributo puede
                  ser o no nulo en la transformación a sentencias SQL.</span
                >
              </v-card-subtitle>
              <v-card-subtitle class="caption">
                <v-icon small left>mdi-debug-step-out</v-icon>
                <span class="font-weight-light"
                  >Auto Increment: es el indicador para señalar si el atributo
                  incrementara su valor de manera automatica en la
                  transformación a sentencias SQL, esta propiedad solo es tomada
                  en cuenta para los tipos de datos int y bigint.</span
                >
              </v-card-subtitle>
              <v-card-subtitle>
                Modelo no relacional
              </v-card-subtitle>
              <v-card-subtitle class="caption">
                <v-icon small left>mdi-group</v-icon>
                <span class="font-weight-light"
                  >GDMType: es el tipo de dato que adoptará el atributo en la
                  tranformación al gdm del modelo NoSQL.</span
                >
              </v-card-subtitle>
            </v-card>
          </v-col>
        </div>
      </v-col>
    </v-row>
    <!-- Dialog/modals -->
    <v-dialog
      v-model="diagramErrors"
      scrollable
      min-width="450"
      max-width="600"
    >
      <v-card>
        <v-card-title class="headline">
          Errores en el diagrama entidad-relación
        </v-card-title>
        <v-card-text>
          <v-list v-for="(item, key, index) in msgDiagramErrors" :key="index">
            <v-list-item two-line>
              <v-list-item-content>
                <v-list-item-title>
                  {{ mapErrors[key] }}
                </v-list-item-title>
                <v-list-item-subtitle v-for="(msgError, i) in item" :key="i">
                  {{ msgError }}
                </v-list-item-subtitle>
              </v-list-item-content>
            </v-list-item>
          </v-list>
        </v-card-text>

        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn color="green darken-1" text @click="diagramErrors = false"
            >De acuerdo</v-btn
          >
        </v-card-actions>
      </v-card>
    </v-dialog>
    <!-- Dialog/modals -->
    <v-dialog v-model="validDiagram" scrollable min-width="450" max-width="600">
      <v-card>
        <v-card-title class="headline">
          Diagrama entidad-relación
        </v-card-title>
        <v-card-text font-size="24px">
          {{ msgDiagramErrors }}
          <br />
          Puede proceder a crear las consultas de acceso para el modelo
          noSQL(paso 2) o si lo prefiere obtener las sentencias SQL(paso 3).
        </v-card-text>

        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn left outlined color="indigo darken-1" to="/workspace/queries">
            Paso 2
          </v-btn>
          <v-btn left outlined color="indigo" to="/workspace/sentencesSQL">
            Paso 3
          </v-btn>
          <v-btn color="success" @click="validDiagram = false">
            OK
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </v-container>
</template>
<script type="module">
import { go } from 'gojs/release/go-module'
import 'gojs/extensionsJSM/Figures'
import { mapGetters } from 'vuex'
import { Inspector } from 'gojs/extensionsJSM/DataInspector'

export default {
  props: {
    showpallete: { type: Boolean, default: true },
    readonly: { type: Boolean, default: false }
  },
  css: ['gojs/extensionsJSM/DataInspector.css'],
  data() {
    return {
      myDiagram: '',
      myPalette: '',
      myInspector: '',
      PathPatterns: '',
      myContextMenu: '',
      cxElement: '',
      urlFile: '',
      scriptName: '',
      node: '',
      myOverview: '',
      mostrarPaleta: this.showpallete,
      soloLectura: this.readonly,
      diagramErrors: false,
      mapErrors: {
        entities_errors: 'Errores en entidades.',
        general_errors: 'Errores generales.',
        attrs_errors: 'Errores en atributos.',
        relations_errors: 'Errores en relaciones.'
      },
      msgDiagramErrors: '',
      validDiagram: false
    }
  },
  computed: {
    ...mapGetters({
      thereIsDiagram: 'vuexER/existDiagram',
      diagramaObtenido: 'vuexER/getDiagram'
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
        'draggingTool.dragsLink': false,
        'draggingTool.isGridSnapEnabled': true,
        'linkingTool.isUnconnectedLinkValid': false,
        'linkingTool.portGravity': 10,
        'relinkingTool.isUnconnectedLinkValid': false,
        'relinkingTool.portGravity': 10,
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

    /** ******************* Menú contextual *******************************/
    // This is the actual HTML context menu:
    this.cxElement = document.getElementById('contextMenu')

    // Since we have only one main element, we don't have to declare a hide method,
    // we can set mainElement and GoJS will hide it automatically
    if (this.soloLectura) {
      this.myContextMenu = $(go.HTMLInfo, {
        show: this.showContextMenu,
        hide: this.hideContextMenu
      })
    }

    /* Creamos el modelo de datos, está conformado por dos partes, los nodos y los links, [nodos], [links] donde los links tienen la estructura { from: a, to: b } siendo a, b las llaves de los objetos que están en el arreglo nodos */
    this.myDiagram.nodeTemplate = $(
      go.Node,
      'Spot',
      {
        contextMenu: this.mostrarMenuContextual(),
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

    this.myDiagram.contextMenu = this.myContextMenu
    // We don't want the div acting as a context menu to have a (browser) context menu!
    this.cxElement.addEventListener(
      'contextmenu',
      function(e) {
        e.preventDefault()
        return false
      },
      false
    )

    this.PathPatterns = new go.Map()

    this.definePathPattern('parcial', 'M0 0 L1 0')
    this.definePathPattern('total', 'M0 0 L1 0 M0 3 L1 3')

    this.myDiagram.linkTemplate = $(
      go.Link, // the whole link panel
      {
        selectionAdorned: true,
        selectionAdornmentTemplate: linkSelectionAdornmentTemplate,
        layerName: 'Foreground',
        reshapable: true,
        routing: go.Link.AvoidsNodes,
        curve: go.Link.JumpOver
      },
      $(
        go.Shape, // the link's path shape
        { isPanelMain: true, stroke: 'parcial' },
        new go.Binding('stroke', 'participacion', (f) => {
          return f === '' ? 'parcial' : 'total'
        }),
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
    if (this.mostrarPaleta)
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
          text: { show: false },
          // key would be automatically added for nodes, but we want to declare it read-only also:
          // key: { readOnly: true, show: Inspector.showIfPresent },
          // color would be automatically added for nodes, but we want to declare it a color also:
          // color: { show: Inspector.showIfPresent, type: 'color' },
          type: { readOnly: true, show: false, type: 'type' },
          figure: {
            readOnly: true,
            show: false,
            type: 'figure'
          },
          fill: { readOnly: true, show: false, type: 'fill' },
          key: { readOnly: true, show: false, type: 'key' },
          loc: { readOnly: true, show: false, type: 'loc' },
          size: { readOnly: true, show: false, type: 'size' },
          // Comments and LinkComments are not in any node or link data (yet), so we add them here:
          Comments: { show: false },
          LinkComments: { show: false },
          cardinality: {
            show: Inspector.showIfLink,
            type: 'select',
            choices(node, propName) {
              if (Array.isArray(node.data.choices)) return node.data.choices
              return ['1', 'N', 'M']
            }
          },
          participacion: {
            show: Inspector.showIfLink,
            type: 'select',
            choices(node, propName) {
              if (Array.isArray(node.data.choices)) return node.data.choices
              return ['parcial', 'total']
            }
          },
          // isGroup: { readOnly: true, show: Inspector.showIfPresent },
          // flag: { show: Inspector.showIfNode, type: 'checkbox' },
          dataType: {
            show: Inspector.showIfNode,
            type: 'select',
            choices(node, propName) {
              if (Array.isArray(node.data.choices)) return node.data.choices
              return [
                'int',
                'bigint',
                'float',
                'double',
                'decimal',
                'char',
                'varchar',
                'blob',
                'text',
                'date',
                'time',
                'timestap'
              ]
            }
          },
          gdmType: {
            show: Inspector.showIfNode,
            type: 'select',
            choices(node, propName) {
              if (Array.isArray(node.data.choices)) return node.data.choices
              return ['text', 'number', 'timestamp', 'boolean', 'date']
            }
          },
          dataSize: {
            show: Inspector.showIfNode,
            type: 'number',
            defaultValue: 1,
            choices(node, propName) {
              if (Array.isArray(node.data.choices)) return node.data.choices
              return [...Array(256).keys()]
            }
          },
          notNull: { show: Inspector.showIfNode, type: 'checkbox' },
          autoIncrement: { show: Inspector.showIfNode, type: 'checkbox' },

          choices: { show: false }, // must not be shown at all
          to: { readOnly: true, show: false },
          from: { readOnly: true, show: false },
          // an example of specifying the <input> type
          password: { show: Inspector.showIfPresent, type: 'password' }
        }
      })

    /** *****************Paleta***********************/
    // initialize the Palette that is on the left side of the page
    if (this.mostrarPaleta)
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
              dataType: 'varchar',
              fill: 'white'
            },
            {
              type: 'weakEntity',
              text: 'Entidad débil',
              figure: 'FramedRectangle',
              dataType: 'varchar',
              fill: 'white'
            },
            {
              type: 'relation',
              text: 'Relación',
              figure: 'Diamond',
              dataType: 'varchar',
              fill: 'white'
            },
            {
              type: 'weakRelation',
              text: 'Relación débil',
              figure: 'weakDiamond',
              dataType: 'varchar',
              fill: 'white'
            },
            {
              type: 'attribute',
              text: 'Atributo',
              figure: 'Ellipse',
              dataType: 'varchar',
              gdmType: 'text',
              fill: 'white'
            },
            {
              type: 'keyAttribute',
              text: 'clave',
              figure: 'Ellipse',
              dataType: 'varchar',
              gdmType: 'text',
              isUnderline: true,
              fill: 'white'
            },
            {
              type: 'derivedAttribute',
              text: 'derivado',
              figure: 'Ellipse',
              dataType: 'varchar',
              gdmType: 'text',
              fill: 'white',
              strokeDashArray: [4, 2]
            },
            {
              type: 'multivalueAttribute',
              text: 'multivalor',
              figure: 'FramedEllipse',
              dataType: 'varchar',
              gdmType: 'text',
              fill: 'white'
              // strokeDashArray: [4, 2]
            }
          ])
        }
      )
    if (this.soloLectura) {
      // this.myDiagram.isReadOnly = true
      // quitamos los listeners del diagrama solo lectura
      this.$nuxt.$off('axiosSaveModel')
      this.$nuxt.$off('axiosLoadModel')
      this.$nuxt.$off('cleanCanvas')
      this.$nuxt.$off('validateDiagram')
    } else {
      // Listeners de SubNavBar.vue
      this.$nuxt.$on('axiosSaveModel', () => {
        this.axiosSaveModel()
      })

      this.$nuxt.$on('axiosLoadModel', () => {
        this.axiosLoadModel()
      })

      this.$nuxt.$on('cleanCanvas', () => {
        this.cleanCanvas()
      })

      this.$nuxt.$on('validateDiagram', () => {
        this.validateDiagram()
      })
    }

    this.myOverview = $(
      go.Overview,
      'myOverviewDiv', // the HTML DIV element for the Overview
      {
        observed: this.myDiagram,
        // _viewPosition: new go.Point(100, 10),
        contentAlignment: go.Spot.Center
      }
    ) // tell it which Diagram to show and pan

    // Whenever the Diagram.position or Diagram.scale change,
    // update the position of all simple Parts that have a _viewPosition property.
    this.myDiagram.addDiagramListener('ViewportBoundsChanged', function(e) {
      e.diagram.commit(function(dia) {
        // only iterates through simple Parts in the diagram, not Nodes or Links
        dia.parts.each(function(part) {
          // and only on those that have the "_viewPosition" property set to a Point
          if (part._viewPosition) {
            part.position = dia.transformViewToDoc(part._viewPosition)
            part.scale = 1 / dia.scale
          }
        })
      }, 'fix Parts')
    })
  },
  beforeDestroy() {
    this.vuexSaveModel()
    // Eliminamos los listeners de SubNavBar.vue
    this.$nuxt.$off('axiosSaveModel')
    this.$nuxt.$off('axiosLoadModel')
    this.$nuxt.$off('cleanCanvas')
    this.$nuxt.$off('validateDiagram')
  },
  middleware: 'authenticated',
  layout: 'workspace', // layout de la aplicación (esto es de nuxt)
  methods: {
    mostrarMenuContextual() {
      if (this.soloLectura) return this.myContextMenu
    },
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
      this.$nuxt.$loading.start()

      this.$store
        .dispatch('axiosER/save', {
          savedModel: this.savedModel
        })
        .then(() => {
          this.$nuxt.$loading.finish()
          this.$snotify.success('Guardado correctamente.')
        })
        .catch(() => {
          this.$nuxt.$loading.fail()
          this.$nuxt.$loading.finish()
          this.$snotify.error(
            '¡Algo ocurrió! El diagrama no ha sido guardado, intente más tarde.'
          )
        })
    },
    axiosLoadModel() {
      this.$nuxt.$loading.start()
      this.$store
        .dispatch('axiosER/getLastDiagram')
        .then((response) => {
          this.$nuxt.$loading.finish()
          this.myDiagram.model = go.Model.fromJson(response.data.diagram)
          this.$snotify.success('Diagrama cargado correctamente.')
        })
        .catch(() => {
          this.$nuxt.$loading.fail()
          this.$nuxt.$loading.finish()
          this.$snotify.error(
            '¡Algo ocurrió! No se ha encontrado un diagrama asociado a este perfil.'
          )
        })
    },
    cleanCanvas() {
      this.myDiagram.model = go.Model.fromJson({})
    },
    validateDiagram() {
      this.saveDiagramProperties()
      const diagram = this.myDiagram.model.toJson()
      this.$store
        .dispatch('axiosER/validateDiagram', diagram)
        .then((response) => {
          this.$nuxt.$loading.finish()
          this.validDiagram = true
          this.msgDiagramErrors = 'El diagrama es valido estructuralmente.'
        })
        .catch((error) => {
          switch (error.response.status) {
            case 400:
              this.$snotify.warning(error.response.data.message)
              break
            case 406:
              this.diagramErrors = true
              this.msgDiagramErrors = error.response.data
              break
            case 500:
              this.$snotify.error('¡Algo salió mal!.')
              break
          }
        })
    },
    convertToSQL() {},
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
    },
    /** ************Menú contextual*******************/
    hideCX() {
      if (this.myDiagram.currentTool instanceof go.ContextMenuTool) {
        this.myDiagram.currentTool.doCancel()
      }
    },
    showContextMenu(obj, diagram, tool) {
      // Show only the relevant buttons given the current state.
      const cmd = diagram.commandHandler
      let hasMenuItem = false
      function maybeShowItem(elt, pred) {
        if (
          pred &&
          (obj.data.type === 'attribute' ||
            obj.data.type === 'keyAttribute' ||
            obj.data.type === 'derivedAttribute' ||
            obj.data.type === 'multivalueAttribute')
        ) {
          elt.style.display = 'block'
          hasMenuItem = true
        } else {
          elt.style.display = 'none'
        }
      }
      maybeShowItem(
        document.getElementById('givenValue'),
        cmd.canCutSelection()
      )
      // Now show the whole context menu element
      if (hasMenuItem) {
        this.cxElement.classList.add('show-menu')
        // we don't bother overriding positionfContextMenu, we just do it here:
        const mousePt = diagram.lastInput.viewPoint
        this.cxElement.style.left = mousePt.x + 5 + 'px'
        this.cxElement.style.top = mousePt.y + 'px'
      }
      // Optional: Use a `window` click listener with event capture to
      //           remove the context menu if the user clicks elsewhere on the page
      window.addEventListener('click', this.hideCX, true)
    },
    hideContextMenu() {
      this.cxElement.classList.remove('show-menu')
      // Optional: Use a `window` click listener with event capture to
      //           remove the context menu if the user clicks elsewhere on the page
      window.removeEventListener('click', this.hideCX, true)
    },
    // A custom command, for changing the color of the selected node(s).
    changeColor(diagram, color) {
      // Always make changes in a transaction, except when initializing the diagram.
      diagram.startTransaction('change color')
      diagram.selection.each(function(node) {
        if (node instanceof go.Node) {
          // ignore any selected Links and simple Parts
          // Examine and modify the data, not the Node directly.
          const data = node.data
          // Call setDataProperty to support undo/redo as well as
          // automatically evaluating any relevant bindings.
          diagram.model.setDataProperty(data, 'fill', color)
        }
      })
      diagram.commitTransaction('change color')
    },
    givenValue(type) {
      const diagram = this.myDiagram
      // Always make changes in a transaction, except when initializing the diagram.
      diagram.startTransaction('given value')
      diagram.selection.each((node) => {
        if (node instanceof go.Node) {
          // ignore any selected Links and simple Parts
          // Examine and modify the data, not the Node directly.
          const data = { ...node.data }

          // Call setDataProperty to support undo/redo as well as
          // Guardamos los datos del nodo solo si es un atributo
          if (
            data.type === 'keyAttribute' ||
            data.type === 'derivedAttribute' ||
            data.type === 'compositeAttribute' ||
            data.type === 'multivalueAttribute' ||
            data.type === 'attribute'
          ) {
            const nodoConectado = { ...this.getConnectedNode(node) }
            Promise.all([
              this.$store.dispatch(
                'vuexQueries/pushConnectedNode',
                nodoConectado
              ),
              this.$store.dispatch('vuexQueries/pushNode', data)
            ]).finally(() => {
              switch (type) {
                case 'givenValue':
                  this.$nuxt.$emit('emitGivenValue')
                  break
                case 'givenRange':
                  this.$nuxt.$emit('emitGivenRange')
                  break
                case 'givenSet':
                  this.$nuxt.$emit('emitGivenSet')
                  break
              }
            })
          }
        }
      })
      diagram.commitTransaction('value obtained')
      diagram.currentTool.stopTool()
    },
    findValue(type) {
      const diagram = this.myDiagram
      // Always make changes in a transaction, except when initializing the diagram.
      diagram.startTransaction('find value')
      diagram.selection.each((node) => {
        if (node instanceof go.Node) {
          // ignore any selected Links and simple Parts
          // Examine and modify the data, not the Node directly.
          const data = { ...node.data }

          // Call setDataProperty to support undo/redo as well as
          // Guardamos los datos del nodo solo si es un atributo
          if (
            data.type === 'keyAttribute' ||
            data.type === 'derivedAttribute' ||
            data.type === 'compositeAttribute' ||
            data.type === 'attribute'
          ) {
            const nodoConectado = { ...this.getConnectedNode(node) }
            Promise.all([
              this.$store.dispatch(
                'vuexQueries/pushConnectedNode',
                nodoConectado
              ),
              this.$store.dispatch('vuexQueries/pushNode', data)
            ]).finally(() => {
              switch (type) {
                case 'findValue':
                  this.$nuxt.$emit('emitFindValue')
                  break
              }
            })
          }
        }
      })
      diagram.commitTransaction('end find value')
      diagram.currentTool.stopTool()
    },
    getConnectedNode(node) {
      const key = node.findNodesConnected().first().key
      return this.myDiagram.findNodeForKey(key).data
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
    },
    downloadGoJSData() {
      this.saveDiagramProperties()
      const diagram = this.myDiagram.model.toJson()
      const scriptData = encodeURIComponent(diagram)
      // this.scriptName = 'prueba.txt'
      this.urlFile = `data:json/plain;charset=utf-8,${scriptData}` // application/sql
      this.$snotify.success('Archivo descargado. ')
    }
  }
}
</script>

<style>
@import 'gojs/extensionsJSM/DataInspector.css';
#myOverviewDiv {
  /*position: absolute;*/
  width: 50%;
  height: 150%;
  display: flex;

  /*top: 400px;
  left: 400px;*/
  background-color: #f2f2f2;
  z-index: 300; /* make sure its in front */
  border: solid 1px #7986cb;
}

/* CSS for the traditional context menu */
.menu {
  display: none;
  position: absolute;
  opacity: 0;
  margin: 0;
  padding: 8px 0;
  z-index: 999;
  box-shadow: 0 5px 5px -3px rgba(0, 0, 0, 0.2),
    0 8px 10px 1px rgba(0, 0, 0, 0.14), 0 3px 14px 2px rgba(0, 0, 0, 0.12);
  list-style: none;
  background-color: #ffffff;
  border-radius: 4px;
}
.menu-item {
  display: block;
  position: relative;
  min-width: 60px;
  margin: 0;
  padding: 6px 16px;
  font: bold 12px sans-serif;
  color: rgba(0, 0, 0, 0.87);
  cursor: pointer;
}
.menu-item::before {
  position: absolute;
  top: 0;
  left: 0;
  opacity: 0;
  pointer-events: none;
  content: '';
  width: 100%;
  height: 100%;
  background-color: #000000;
}
.menu-item:hover::before {
  opacity: 0.04;
}
.menu .menu {
  top: -8px;
  left: 100%;
}
.show-menu,
.menu-item:hover > .menu {
  display: block;
  opacity: 1;
}
</style>
