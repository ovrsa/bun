<template>
  <div>
    <header class="fixed top-0 left-0 w-full bg-gray-800 text-white py-4 z-50">
      <div
        class="flex justify-between items-center max-w-screen-xl mx-auto px-4"
      >
        <div class="flex items-center">
          <img src="/img/bun.png" alt="Bun Logo" class="h-10" />
          <div class="text-xl ml-7 cursor-pointer" @click="$emit('logoClick')">
            Bun
          </div>
        </div>
        <DropDownMenu @logout="$emit('logout')" />
      </div>
    </header>
    <main class="pt-20">
      <slot />
    </main>
    <footer class="bg-gray-800 text-white py-4 mt-10 w-full">
      <div class="max-w-screen-xl mx-auto text-center">
        <p>© 2024 Bun</p>
      </div>
    </footer>
  </div>
</template>

<script setup lang="ts">
import DropDownMenu from '@/components/molecules/DropDownMenu.vue'
</script>

<style scoped></style>
