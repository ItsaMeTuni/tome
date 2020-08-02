<template>
  <div id="nodes">
    <div v-for="[depth, node] in depthCache" :key="node.id" class="node">
      <div v-for="i in depth" :key="i" class="node-indent"></div>
      <div class="node-content">
        <p class="node-text" contenteditable>{{ node.content }}</p>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'Home',
  data: () => ({
    nodes: [
      {
        id: '1',
        content: 'Hello, World!',
        parent: null
      },
      {
        id: '2',
        content: 'Another thing',
        parent: null
      },
      {
        id: '3',
        content: 'Child of Hello World',
        parent: '1'
      }
    ],
    depthCache: []
  }),
  methods: {
    buildDepthCache () {
      this.depthCache = Array.from(this._traverse(null, 0))
    },
    _traverse: function * (targetParentId, depth) {
      for (const node of this.nodes) {
        if (node.parent === targetParentId) {
          yield [depth, node]
          yield * this._traverse(node.id, depth + 1)
        }
      }
    }
  },
  mounted () {
    this.buildDepthCache()
  }
}
</script>

<style lang="scss">
.node {
  width: 100%;
  display: flex
}
.node-indent {
  width: 1em;
  height: 1em;
}
.node-content {
  flex-grow: 1;
}
</style>
