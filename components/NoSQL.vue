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
  data() {
    return {
      myDiagram: ''
    }
  },
  computed: {
    ...mapGetters({})
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
            alignment: go.Spot.Center,
            margin: new go.Margin(0, 24, 0, 2), // leave room for Button
            font: 'bold 16px sans-serif'
          },
          new go.Binding('text', 'key')
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
    const nodeDataArray = [
      {
        key: 'Product',
        items: [
          {
            name: 'productId',
            type: 'ID',
            iskey: true,
            figure: 'Decision',
            color: colors.red
          },
          {
            name: 'name',
            type: 'text',
            iskey: false,
            figure: 'Decision',
            color: colors.red
          },
          {
            name: 'description',
            type: 'text',
            iskey: false,
            figure: 'Decision',
            color: colors.red
          },
          {
            name: 'price',
            type: 'float',
            iskey: false,
            figure: 'Decision',
            color: colors.red
          },
          {
            name: 'categoryArray',
            iskey: false,
            figure: 'Hexagon',
            color: 'purple'
          }
        ]
      },
      {
        key: 'Client',
        items: [
          {
            name: 'SupplierID',
            iskey: true,
            figure: 'Decision',
            color: colors.red
          },
          {
            name: 'CompanyName',
            iskey: false,
            figure: 'Hexagon',
            color: colors.blue
          },
          {
            name: 'ContactName',
            iskey: false,
            figure: 'Hexagon',
            color: colors.blue
          },
          {
            name: 'Address',
            iskey: false,
            figure: 'Hexagon',
            color: colors.blue
          }
        ]
      },
      {
        key: 'Purchase',
        items: [
          {
            name: 'CategoryID',
            iskey: true,
            figure: 'Decision',
            color: colors.red
          },
          {
            name: 'CategoryName',
            iskey: false,
            figure: 'Hexagon',
            color: colors.blue
          },
          {
            name: 'Description',
            iskey: false,
            figure: 'Hexagon',
            color: colors.blue
          },
          {
            name: 'Picture',
            iskey: false,
            figure: 'TriangleUp',
            color: colors.pink
          }
        ]
      }
    ]
    this.myDiagram.model = $(go.GraphLinksModel, {
      copiesArrays: true,
      copiesArrayObjects: true,
      nodeDataArray
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
    loadModel() {}
  }
}
</script>

<style></style>
