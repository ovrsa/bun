<template>
  <div class="h-full min-h-screen flex justify-center items-center w-full">
    <div
      class="bg-white p-8 rounded-lg shadow-lg max-w-sm w-full backdrop-filter backdrop-blur-lg bg-opacity-30 border border-gray-100"
    >
      <SignupForm />
    </div>
  </div>
</template>

<script setup lang="ts">
import SignupForm from '../components/SignupForm.vue';
</script>

<style scoped>
.container {
  background: linear-gradient(to bottom right, #f5f6ff, #f5f6ff);
}
</style>
