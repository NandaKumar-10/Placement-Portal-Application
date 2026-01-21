<script setup>
import {ref} from 'vue'

  const name = ref('hello')
</script>

<template>
  <div>
    <p>Hello from vue {{ name }}</p>
  </div>
</template>

<style>
</style>