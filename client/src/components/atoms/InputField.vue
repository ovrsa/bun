<template>
  <div class="space-y-1">
    <input
      :type="type"
      v-model="inputValue"
      :class="inputClass"
      :placeholder="placeholder"
    />
    <p v-if="errorMessage" class="text-red-500 text-xs">{{ errorMessage }}</p>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'

const props = defineProps({
  type: { type: String, default: 'text' },
  modelValue: String,
  placeholder: String,
  errorMessage: String,
})

const emits = defineEmits(['update:modelValue'])

const inputValue = computed({
  get: () => props.modelValue,
  set: value => emits('update:modelValue', value),
})

const inputClass =
  'w-full p-2 border border-gray-300 rounded-lg bg-white bg-opacity-50 placeholder-gray-400'
</script>
