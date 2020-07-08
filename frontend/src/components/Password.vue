<template>
  <v-text-field
    :label="label"
    name="password"
    :prepend-icon="prepend ? 'mdi-asterisk' : ''"
    :type="visible ? 'text' : 'password'"
    required
    :rules="[v => !!v || 'This field is required']"
    v-model="theValue"
    :outlined="outlined"
  >
    <template v-slot:append>
      <div class="v-input__icon v-input__icon--append">
        <v-btn icon @click="visible = !visible">
          <v-icon>
            {{ visible ? 'mdi-eye-off' : 'mdi-eye' }}
          </v-icon>
        </v-btn>
      </div>
    </template>
  </v-text-field>
</template>

<script>
export default {
  name: 'Password',
  data: () => ({
    visible: false
  }),
  props: {
    value: {
      type: String,
      default: ''
    },
    outlined: {
      type: Boolean,
      default: false
    },
    label: {
      type: String,
      default: 'Password'
    },
    prepend: {
      type: Boolean,
      default: false
    }
  },
  computed: {
    theValue: {
      get () {
        return this.value
      },
      set (val) {
        this.$emit('input', val)
      }
    }
  }
}
</script>
