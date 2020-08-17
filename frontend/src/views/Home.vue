<template>
  <v-app>
    <v-main app>
      <div id="nodes">
        <div
          v-for="[depth, id] in depthCache"
          :key="id"
          :id="id"
          :node="id"
          class="node"
          @contextmenu="onContextMenu"
        >
          <div v-for="i in depth" :key="i" class="node-indent" :node="id"></div>
          <div class="node-content" :node="id">
            <p class="node-text" contenteditable :node="id">{{ nodes[id].content }}</p>
          </div>
        </div>
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
        content: 'Child of Hello World',
        parent: 'abc'
      }
    },
    depthCache: []
  }),
  methods: {
    buildDepthCache () {
      this.depthCache = Array.from(this._traverse(null, 0))
    },
    _traverse: function * (targetParentId, depth) {
      for (const id in this.nodes) {
        if (this.nodes[id].parent === targetParentId) {
          yield [depth, id]
          yield * this._traverse(id, depth + 1)
        }
      }
    },
    onContextMenu (event) {
      if (this.contextMenuOpen) {
        this.contextMenuOpen = false
        this.eventTarget = null
      } else {
        event.preventDefault()
        this.eventTarget = event.target.getAttribute('node')
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
    this.buildDepthCache()
  },
  components: { Footer }
}
</script>

<style lang="scss">
#nodes {
  height: 100%;

  .node {
    width: 100%;
    display: flex;
    padding: 0 1em;

    .node-indent {
      width: 1em;
      height: 1em;
    }

    .node-content {
      flex-grow: 1;

      .node-text {
        margin: 0;
        padding: 0.5em 0;
      }
    }
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
