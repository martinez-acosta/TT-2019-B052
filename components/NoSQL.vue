<template>
  <v-container fluid>
    <client-only>
      <vue-snotify></vue-snotify>
    </client-only>
    <v-row>
      <v-toolbar dense>
        <v-tooltip bottom>
          <template v-slot:activator="{ on, attrs }">
            <v-btn
              icon
              v-bind="attrs"
              :download="scriptName"
              v-on="on"
              @click="helpDialog = true"
            >
              <v-icon>mdi-download</v-icon>
            </v-btn>
          </template>
          <span>Descargar</span>
        </v-tooltip>

        <v-spacer></v-spacer>

        <v-tooltip bottom>
          <template v-slot:activator="{ on, attrs }">
            <v-btn icon v-bind="attrs" v-on="on">
              <v-icon>mdi-help</v-icon>
            </v-btn>
          </template>
          <span>Ayuda</span>
        </v-tooltip>
      </v-toolbar>
    </v-row>
    <v-row style="height: 80vh">
      <v-col cols="2"><div id="myOverviewDiv"></div></v-col>
      <v-col cols="10" class="white fill-height d-flex flex-column">
        <div style="position: relative;   height: 100%;">
          <div
            id="myDiagramDiv"
            style="width: 100%; display: flex; border: solid 1px black; height: 100%;"
          ></div>
        </div>
      </v-col>
    </v-row>
    <!-- Dialog/modals -->
    <v-dialog v-model="helpDialog" max-width="360">
      <v-card>
        <v-card-title class="headline">
          Modelo noSQL del diagrama ER
        </v-card-title>
        <v-card-text>
          Para crear el script de MongoDB proporcione un nombre para el archivo
          de descarga.
        </v-card-text>
        <v-card-subtitle>
          <v-text-field
            v-model="db_name"
            label="Nombre para el archivo"
          ></v-text-field>
        </v-card-subtitle>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn color="success" text @click="downloadScript()">Enviar</v-btn>
          <v-btn color="primary" text @click="helpDialog = false">Cerrar</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </v-container>
</template>
<script type="module">
import { go } from 'gojs/release/go-module'
import 'gojs/extensionsJSM/Figures'
import { mapGetters } from 'vuex'

export default {
  props: {},
  data() {
    return {
      myDiagram: '',
      myOverview: '',
      helpDialog: false,
      scriptName: 'TT-2019-B052.bson',
      urlFile: '#',
      db_name: ''
    }
  },
  computed: {
    ...mapGetters({
      nosqlDiagram: 'vuexQueries/getNoSQLDiagram'
    })
  },
  mounted() {
    const $ = go.GraphObject.make // for conciseness in defining templates
    this.myDiagram = $(
      go.Diagram,
      'myDiagramDiv', // must name or refer to the DIV HTML element
      {
        allowDelete: false,
        allowCopy: false,
        layout: $(go.ForceDirectedLayout),
        'undoManager.isEnabled': true
      }
    )
    const colors = {
      red: '#be4b15',
      green: '#52ce60',
      blue: '#6ea5f8',
      lightred: '#fd8852',
      lightblue: '#afd4fe',
      lightgreen: '#b9e986',
      pink: '#faadc1',
      purple: '#d689ff',
      orange: '#fdb400'
    }
    // the template for each attribute in a node's array of item data
    const itemTempl = $(
      go.Panel,
      'Horizontal',
      $(
        go.Shape,
        {
          desiredSize: new go.Size(15, 15),
          strokeJoin: 'round',
          strokeWidth: 3,
          stroke: null,
          margin: 2
        },
        new go.Binding('figure', 'figure'),
        new go.Binding('fill', 'color'),
        new go.Binding('stroke', 'color')
      ),
      $(
        go.TextBlock,
        {
          stroke: '#333333',
          font: 'bold 12px sans-serif',
          isMultiline: true,
          editable: false
        },
        new go.Binding('text', 'name')
      ),
      $(go.TextBlock, '', 'text', ': '),
      $(
        go.TextBlock,
        {
          stroke: '#333333',
          font: '10px sans-serif',
          isMultiline: true,
          editable: false
        },
        new go.Binding('text', 'type').makeTwoWay()
      )
    )
    // define the Node template, representing an entity
    this.myDiagram.nodeTemplate = $(
      go.Node,
      'Auto', // the whole node panel
      {
        selectionAdorned: true,
        resizable: true,
        layoutConditions: go.Part.LayoutStandard & ~go.Part.LayoutNodeSized,
        fromSpot: go.Spot.AllSides,
        toSpot: go.Spot.AllSides,
        isShadowed: true,
        shadowOffset: new go.Point(3, 3),
        shadowColor: '#C5C1AA'
      },
      new go.Binding('location', 'location').makeTwoWay(),
      // whenever the PanelExpanderButton changes the visible property of the "LIST" panel,
      // clear out any desiredSize set by the ResizingTool.
      new go.Binding('desiredSize', 'visible', function(v) {
        return new go.Size(NaN, NaN)
      }).ofObject('LIST'),
      // define the node's outer shape, which will surround the Table
      $(go.Shape, 'RoundedRectangle', {
        fill: 'white',
        stroke: '#eeeeee',
        strokeWidth: 3
      }),
      $(
        go.Panel,
        'Table',
        { margin: 8, stretch: go.GraphObject.Fill },
        $(go.RowColumnDefinition, {
          row: 0,
          sizing: go.RowColumnDefinition.None
        }),
        // the table header
        $(
          go.TextBlock,
          {
            row: 0,
            alignment: go.Spot.Left,
            margin: new go.Margin(0, 24, 0, 2), // leave room for Button
            font: 'bold 16px sans-serif'
          },
          new go.Binding('text', '', function(node) {
            return node.subtype + ' ' + node.name
          })
        ),
        // the collapse/expand button
        $(
          'PanelExpanderButton',
          'LIST', // the name of the element whose visibility this button toggles
          { row: 0, alignment: go.Spot.TopRight }
        ),
        // the list of Panels, each showing an attribute
        $(
          go.Panel,
          'Vertical',
          {
            name: 'LIST',
            row: 1,
            padding: 3,
            alignment: go.Spot.TopLeft,
            defaultAlignment: go.Spot.Left,
            stretch: go.GraphObject.Horizontal,
            itemTemplate: itemTempl
          },
          new go.Binding('itemArray', 'items')
        )
      ) // end Table Panel
    ) // end Node
    // create the model for the E-R diagram
    const nodeDataArray = this.nosqlDiagram
      ? this.nosqlDiagram.nodeDataArray
      : []
    const linkDataArray = this.nosqlDiagram
      ? this.nosqlDiagram.linkDataArray
      : []
    this.myDiagram.linkTemplate = $(
      go.Link,
      {
        relinkableFrom: false,
        relinkableTo: false, // let user reconnect links
        toShortLength: 4,
        fromShortLength: 2
      },
      $(go.Shape, { strokeWidth: 1.5 }),
      $(go.Shape, { toArrow: 'Standard', stroke: null })
    )

    this.myDiagram.model = $(go.GraphLinksModel, {
      copiesArrays: true,
      copiesArrayObjects: true,
      linkFromPortIdProperty: 'fromPort',
      linkToPortIdProperty: 'toPort',
      nodeDataArray,
      linkDataArray
    })
    // Set up an unmodeled Part as a legend, and place it directly on the diagram.
    this.myDiagram.add(
      $(
        go.Part,
        'Table',
        {
          layerName: 'Grid', // must be in a Layer that is Layer.isTemporary,

          _viewPosition: new go.Point(50, 120), // some position in the viewport,
          selectable: false
        },
        $(go.TextBlock, 'Nomenclatura', {
          row: 0,
          font: '700 14px Droid Serif, sans-serif'
        }), // end row 0
        $(
          go.Panel,
          'Horizontal',
          { row: 1, alignment: go.Spot.Left },
          $(go.Shape, 'Decision', {
            desiredSize: new go.Size(10, 10),
            fill: colors.red,
            margin: 5
          }),
          $(go.TextBlock, 'Primitive field', {
            font: '700 13px Droid Serif, sans-serif'
          })
        ), // end row 1
        $(
          go.Panel,
          'Horizontal',
          { row: 2, alignment: go.Spot.Left },
          $(go.Shape, 'Rectangle', {
            desiredSize: new go.Size(10, 10),
            fill: '#FFD700',
            margin: 5
          }),
          $(go.TextBlock, 'Document', {
            font: '700 13px Droid Serif, sans-serif'
          })
        ), // end row 2
        $(
          go.Panel,
          'Horizontal',
          { row: 3, alignment: go.Spot.Left },
          $(go.Shape, 'Hexagon', {
            desiredSize: new go.Size(10, 10),
            fill: colors.blue,
            margin: 5
          }),
          $(go.TextBlock, 'Array Field', {
            font: '700 13px Droid Serif, sans-serif'
          })
        ) // end row 3
      )
    )

    this.myOverview = $(
      go.Overview,
      'myOverviewDiv', // the HTML DIV element for the Overview
      {
        observed: this.myDiagram,
        // _viewPosition: new go.Point(50, 120), // some position in the viewport,
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
  beforeDestroy() {},
  middleware: 'authenticated',
  layout: 'workspace', // layout de la aplicación (esto es de nuxt)
  methods: {
    saveDiagramProperties() {
      this.myDiagram.model.modelData.position = go.Point.stringify(
        this.myDiagram.position
      )
    },
    saveModel() {
      this.saveDiagramProperties()
      this.savedModel = this.myDiagram.model.toJson()
      this.myDiagram.isModified = false
      //  console.log('savedModel: ' + this.savedModel)
      this.$store.dispatch('diagramRelational/save', {
        savedModel: this.savedModel
      })
    },
    loadModel() {
      this.myDiagram.model.nodeDataArray = this.nosqlDiagram.nodeDataArray
      this.myDiagram.model.linkDataArray = this.nosqlDiagram.linkDataArray
    },
    downloadScript() {
      this.$store
        .dispatch('axiosNoSQL/getMongoScript')
        .then((response) => {
          this.helpDialog = false
          const scriptData = encodeURIComponent(response.data)
          this.urlFile = `data:text/plain;charset=utf-8,${scriptData}` // application/sql
          const dbname = this.db_name ? this.db_name : 'tt2019-B052'
          this.scriptName = dbname + '.json'
          const link = document.createElement('a')
          link.href = this.urlFile
          link.setAttribute('download', this.scriptName) // or any other extension
          document.body.appendChild(link)
          link.click()
          this.$snotify.success('Archivo descargado.')
        })
        .catch(() => {
          const msg = 'Ocurrio un error al obtener el script de mongoDB'
          this.$snotify.error(msg)
        })
    }
  }
}
</script>

<style type="text/css">
#myOverviewDiv {
  /* position: absolute;*/
  width: 80%;
  height: 20%;
  display: flex;
  top: 0px;
  left: 0px;
  background-color: #f2f2f2;
  z-index: 300; /* make sure its in front */
  border: solid 1px #7986cb;
}
</style>
