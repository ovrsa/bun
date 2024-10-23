<template>
  <button :type="type" :class="buttonClass" @click="onClick">
    <slot></slot>
  </button>
</template>

<script setup lang="ts">
defineProps<{
  type?: "button" | "submit" | "reset";
  onClick?: () => void;
}>();

const buttonClass = "w-full bg-blue-600 text-white py-2 rounded-lg";
</script>
