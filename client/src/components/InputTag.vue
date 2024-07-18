<script setup lang="ts">
import { ref } from 'vue';
import {
  TagsInput,
  TagsInputInput,
  TagsInputItem,
  TagsInputItemDelete,
  TagsInputItemText,
} from '../components/ui/tags-input';

const modelValue = ref([]);
</script>

<template>
  <TagsInput v-model="modelValue">
    <TagsInputItem v-for="item in modelValue" :key="item" :value="item">
      <TagsInputItemText />
      <TagsInputItemDelete />
    </TagsInputItem>

    <TagsInputInput placeholder="KK..." disabled />
  </TagsInput>
</template>
