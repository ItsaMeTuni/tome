<template>
  <v-app>
    <v-main app>
      <div id="nodes">
        <node
          v-for="node in nodeTree"
          :key="node.id"
          :node-data="node"
          isRoot
          @contextmenu="onContextMenu"
        ></node>
      </div>
      <div
        id="nodes-context-menu"
        v-if="contextMenuOpen"
        :style="`top: ${contextMenuY}px; left: ${contextMenuX}px`"
      >
        <v-list>
          <v-list-item href="#">
            <v-list-item-icon>
              <v-icon>mdi-delete</v-icon>
            </v-list-item-icon>
            <v-list-item-title>Delete</v-list-item-title>
          </v-list-item>
          <v-list-item :href="'#' + eventTarget">
            <v-list-item-title>
              <code>{{ eventTarget }}</code>
            </v-list-item-title>
          </v-list-item>
        </v-list>
      </div>
      <div
        id="nodes-context-menu-blocker"
        v-if="contextMenuOpen"
        @mousedown.prevent.stop="closeContextMenu"
      ></div>
    </v-main>
    <Footer>
      <v-btn icon to="/settings/account" small>
        <v-icon>mdi-cog</v-icon>
      </v-btn>
    </Footer>
  </v-app>
</template>

<script>
import Footer from '@/components/Footer.vue'
import Node from '@/components/Node.vue'

export default {
  name: 'Home',
  data: () => ({
    contextMenuOpen: false,
    contextMenuX: 0,
    contextMenuY: 0,
    eventTarget: null,
    nodes: {
      abc: {
        id: 'abc',
        content: 'Hello, World!',
        parent: null
      },
      def: {
        id: 'def',
        content: 'Another thing',
        parent: null
      },
      ghi: {
        id: 'ghi',
        content: 'Child 0 of Hello World',
        parent: 'abc'
      },
      jkl: {
        id: 'jkl',
        content: 'Child 1 of Hello World',
        parent: 'abc'
      },
      mno: {
        id: 'mno',
        content: 'Child 2 of Hello World',
        parent: 'abc'
      },
      pqr: {
        id: 'pqr',
        content: 'Child 0 of Child 2 of Hello World',
        parent: 'jkl'
      }
    },
    nodeTree: []
  }),
  methods: {
    buildNodeTree: function * (targetParentId) {
      // TODO; Consuming the nodes from `this.nodes` before
      // building it's child tree would increase performance
      for (const nodeId in this.nodes) {
        const node = this.nodes[nodeId]
        if (node.parent === targetParentId) {
          node.children = Array.from(this.buildNodeTree(node.id))
          yield node
        }
      }
    },
    onContextMenu (event) {
      if (this.contextMenuOpen) {
        this.contextMenuOpen = false
        this.eventTarget = null
      } else {
        event.preventDefault()
        this.eventTarget = event.target.getAttribute('data-node')
        this.contextMenuOpen = true
        this.contextMenuX = event.pageX
        this.contextMenuY = event.pageY
      }
    },
    closeContextMenu () {
      this.contextMenuOpen = false
      this.eventTarget = null
    }
  },
  mounted () {
    this.nodeTree = Array.from(this.buildNodeTree(null))
  },
  components: { Footer, Node }
}
</script>

<style lang="scss" scoped>
#nodes {
  padding: 32px 24px 0 24px;

  height: 100%;

  .theme--light &
  {
    background-color: #f5f5f5;
    color: #393939;
  }

  .theme--dark &
  {
    background-color: #272727;
    color: #e4e4e4;
  }
}
#nodes-context-menu-blocker {
  height: 100vh;
  width: 100vw;
  position: absolute;
  opacity: 0;
  z-index: 100;
  left: 0;
  top: 0;
}
#nodes-context-menu {
  position: absolute;
  z-index: 200;
}
</style>
