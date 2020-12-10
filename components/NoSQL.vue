<template>
  <v-container>
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
      myOverview: ''
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
    const nodeDataArray = [
      {
        name: 'categoryArray',
        type: 'documentDataModel:ArrayField',
        items: [
          {
            name: 'category',
            type: 'documentDataModel:Document',
            subtype: 'Document',
            figure: 'Rectangle',
            color: '#FFD700'
          }
        ],
        subtype: 'Array',
        parentKey: 1,
        key: 2,
        figure: 'Hexagon',
        color: '#6ea5f8'
      },
      {
        name: 'category',
        type: 'documentDataModel:Document',
        items: [
          {
            name: 'categoryId',
            type: 'ID',
            subtype: 'PrimitiveField',
            figure: 'Decision',
            color: '#be4b15'
          },
          {
            name: 'name',
            type: 'TEXT',
            subtype: 'PrimitiveField',
            figure: 'Decision',
            color: '#be4b15'
          },
          {
            name: 'description',
            type: 'TEXT',
            subtype: 'PrimitiveField',
            figure: 'Decision',
            color: '#be4b15'
          }
        ],
        subtype: 'Document',
        parentKey: 2,
        key: 3,
        figure: 'Rectangle',
        color: '#FFD700'
      },
      {
        name: 'Product',
        subtype: 'Collection',
        key: 1,
        items: [
          {
            name: 'productId',
            type: 'ID',
            subtype: 'PrimitiveField',
            figure: 'Decision',
            color: '#be4b15'
          },
          {
            name: 'name',
            type: 'TEXT',
            subtype: 'PrimitiveField',
            figure: 'Decision',
            color: '#be4b15'
          },
          {
            name: 'description',
            type: 'TEXT',
            subtype: 'PrimitiveField',
            figure: 'Decision',
            color: '#be4b15'
          },
          {
            name: 'price',
            type: 'FLOAT',
            subtype: 'PrimitiveField',
            figure: 'Decision',
            color: '#be4b15'
          },
          {
            name: 'categoryArray',
            type: 'documentDataModel:ArrayField',
            subtype: 'Array',
            parentKey: 1,
            figure: 'Hexagon',
            color: '#6ea5f8'
          }
        ]
      },
      {
        name: 'purchaseRefArray',
        type: 'documentDataModel:ArrayField',
        items: [
          {
            name: 'purchaseRef',
            type: 'ID',
            subtype: 'PrimitiveField',
            figure: 'Decision',
            color: '#be4b15'
          }
        ],
        subtype: 'Array',
        parentKey: 4,
        key: 5,
        figure: 'Hexagon',
        color: '#6ea5f8'
      },
      {
        name: 'Client',
        subtype: 'Collection',
        key: 4,
        items: [
          {
            name: 'clientId',
            type: 'ID',
            subtype: 'PrimitiveField',
            figure: 'Decision',
            color: '#be4b15'
          },
          {
            name: 'name',
            type: 'TEXT',
            subtype: 'PrimitiveField',
            figure: 'Decision',
            color: '#be4b15'
          },
          {
            name: 'nationality',
            type: 'TEXT',
            subtype: 'PrimitiveField',
            figure: 'Decision',
            color: '#be4b15'
          },
          {
            name: 'purchaseRefArray',
            type: 'documentDataModel:ArrayField',
            subtype: 'Array',
            parentKey: 4,
            figure: 'Hexagon',
            color: '#6ea5f8'
          }
        ]
      },
      {
        name: 'purchaseLineArray',
        type: 'documentDataModel:ArrayField',
        items: [
          {
            name: 'purchaseLine',
            type: 'documentDataModel:Document',
            subtype: 'Document',
            figure: 'Rectangle',
            color: '#FFD700'
          }
        ],
        subtype: 'Array',
        parentKey: 6,
        key: 7,
        figure: 'Hexagon',
        color: '#6ea5f8'
      },
      {
        name: 'purchaseLine',
        type: 'documentDataModel:Document',
        items: [
          {
            name: 'quantity',
            type: 'FLOAT',
            subtype: 'PrimitiveField',
            figure: 'Decision',
            color: '#be4b15'
          },
          {
            name: 'unitPrice',
            type: 'FLOAT',
            subtype: 'PrimitiveField',
            figure: 'Decision',
            color: '#be4b15'
          },
          {
            name: 'productRef',
            type: 'ID',
            subtype: 'PrimitiveField',
            figure: 'Decision',
            color: '#be4b15'
          }
        ],
        subtype: 'Document',
        parentKey: 7,
        key: 8,
        figure: 'Rectangle',
        color: '#FFD700'
      },
      {
        name: 'address',
        type: 'documentDataModel:Document',
        items: [
          {
            name: 'street',
            type: 'TEXT',
            subtype: 'PrimitiveField',
            figure: 'Decision',
            color: '#be4b15'
          },
          {
            name: 'postalCode',
            type: 'TEXT',
            subtype: 'PrimitiveField',
            figure: 'Decision',
            color: '#be4b15'
          },
          {
            name: 'city',
            type: 'TEXT',
            subtype: 'PrimitiveField',
            figure: 'Decision',
            color: '#be4b15'
          },
          {
            name: 'country',
            type: 'TEXT',
            subtype: 'PrimitiveField',
            figure: 'Decision',
            color: '#be4b15'
          }
        ],
        subtype: 'Document',
        parentKey: 6,
        key: 9,
        figure: 'Rectangle',
        color: '#FFD700'
      },
      {
        name: 'bill',
        type: 'documentDataModel:Document',
        items: [
          {
            name: 'billId',
            type: 'ID',
            subtype: 'PrimitiveField',
            figure: 'Decision',
            color: '#be4b15'
          },
          {
            name: 'billDate',
            type: 'DATE',
            subtype: 'PrimitiveField',
            figure: 'Decision',
            color: '#be4b15'
          },
          {
            name: 'billingData',
            type: 'TEXT',
            subtype: 'PrimitiveField',
            figure: 'Decision',
            color: '#be4b15'
          }
        ],
        subtype: 'Document',
        parentKey: 6,
        key: 10,
        figure: 'Rectangle',
        color: '#FFD700'
      },
      {
        name: 'Purchase',
        subtype: 'Collection',
        key: 6,
        items: [
          {
            name: 'purchaseId',
            type: 'ID',
            subtype: 'PrimitiveField',
            figure: 'Decision',
            color: '#be4b15'
          },
          {
            name: 'year',
            type: 'FLOAT',
            subtype: 'PrimitiveField',
            figure: 'Decision',
            color: '#be4b15'
          },
          {
            name: 'month',
            type: 'FLOAT',
            subtype: 'PrimitiveField',
            figure: 'Decision',
            color: '#be4b15'
          },
          {
            name: 'day',
            type: 'FLOAT',
            subtype: 'PrimitiveField',
            figure: 'Decision',
            color: '#be4b15'
          },
          {
            name: 'totalAmount',
            type: 'FLOAT',
            subtype: 'PrimitiveField',
            figure: 'Decision',
            color: '#be4b15'
          },
          {
            name: 'bill',
            type: 'documentDataModel:Document',
            subtype: 'Document',
            parentKey: 6,
            figure: 'Rectangle',
            color: '#FFD700'
          },
          {
            name: 'address',
            type: 'documentDataModel:Document',
            subtype: 'Document',
            parentKey: 6,
            figure: 'Rectangle',
            color: '#FFD700'
          },
          {
            name: 'purchaseLineArray',
            type: 'documentDataModel:ArrayField',
            subtype: 'Array',
            parentKey: 6,
            figure: 'Hexagon',
            color: '#6ea5f8'
          }
        ]
      }
    ]
    const linkDataArray = [
      { to: 1, from: 2 },
      { to: 2, from: 3 },
      { to: 4, from: 5 },
      { to: 6, from: 7 },
      { to: 7, from: 8 },
      { to: 6, from: 9 },
      { to: 6, from: 10 }
    ]

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
    loadModel() {}
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
