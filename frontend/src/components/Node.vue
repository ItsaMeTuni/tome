<template>
    <div
      :class="{
        'node': true,
        'root': isRoot
      }"
      :data-node="nodeData.id"
    >
      <div class="node-ident"></div>
      <div class="node-content">
        <p
          contenteditable
          :data-node="nodeData.id"
          @contextmenu="onContextMenu"
        >{{nodeData.content}}</p>
        <div
          class="node-children"
          :style="{
            '--line-color': lineColor
          }"
        >
          <node
            v-for="child of nodeData.children"
            :key="child.id"
            :node-data="child"
            @contextmenu="onContextMenu"
          ></node>
        </div>
      </div>
    </div>
</template>

<script>
// TODO: find better light and dark colors
const lineColorsLight = ['#F1A7F877', '#F8C4A777', '#EC777777', '#ECD97777']
const lineColorsDark = ['#F1A7F877', '#F8C4A777', '#EC777777', '#ECD97777']

export default {
  name: 'node',
  props: {
    nodeData: Object,
    isRoot: Boolean
  },
  data: () => ({
    lineColor: lineColorsLight[0]
  }),
  methods: {
    getRandomLineColor () {
      // eslint-disable-next-line
      let colors
      if (this.$vuetify.theme.dark) {
        colors = lineColorsDark
      } else {
        colors = lineColorsLight
      }

      return colors[Math.floor(Math.random() * colors.length)]
    },
    onContextMenu (e) {
      e.preventDefault()
      this.$emit('contextmenu', e)
    }
  },
  mounted () {
    this.lineColor = this.getRandomLineColor()
  }
}
</script>

<style lang="scss" scoped>

$ident-width: 4ch;
$font-size: 20px;
$text-line-height: 1.8em;
$line-horiz-space: .6ch;
$line-width: 3px;

.node {
  display: flex;
}

.node-content {
  display: flex;
  flex-direction: column;
  width: 100%;

  font-size: $font-size;

  p {
    margin: 0;
    line-height: $text-line-height;
    outline: none;
  }
}

.node-ident {
  position: relative;
  margin: 0 calc(#{$ident-width} / 2 - #{$line-width} / 2);
  width: $line-width;
  background-color: var(--line-color);

  .root > & {
    display: none;
  }

  :last-child > &
  {
    margin-bottom: calc(#{$text-line-height} / 2 - #{$line-width} / 2);
  }

  &::after
  {
    content: '';
    position: absolute;
    top: calc(#{$text-line-height} / 2 - #{$line-width} / 2);
    left: $line-width;
    right: calc(#{-$ident-width} / 2 + #{$line-horiz-space});

    display: block;

    height: $line-width;

    background-color: var(--line-color);
  }
}

</style>
