<template>
  <div class="bg-gray-100">
    <Popover v-model="open">
      <PopoverTrigger as-child>
        <Button
          variant="outline"
          role="combobox"
          :aria-expanded="open"
          class="w-[200px] justify-between"
        >
          {{
            value
              ? frameworks.find((framework) => framework.value === value)?.label
              : 'Select framework...'
          }}
          <ChevronsUpDown class="ml-2 h-4 w-4 shrink-0 opacity-50" />
        </Button>
      </PopoverTrigger>
      <PopoverContent class="w-[200px] p-0">
        <Command v-model="searchTerm">
          <CommandInput placeholder="Search framework..." />
          <CommandEmpty>No framework found.</CommandEmpty>
          <CommandList>
            <CommandGroup>
              <CommandItem
                v-for="framework in filteredFrameworks"
                :key="framework.value"
                :value="framework.value"
                @select="
                  value = framework.value;
                  open = false;
                "
              >
                <Check
                  :class="
                    cn(
                      'mr-2 h-4 w-4',
                      value === framework.value ? 'opacity-100' : 'opacity-0'
                    )
                  "
                />
                {{ framework.label }}
              </CommandItem>
            </CommandGroup>
          </CommandList>
        </Command>
      </PopoverContent>
    </Popover>
    <Button> Submit </Button>
  </div>
</template>

<script setup lang="ts">
import { Check, ChevronsUpDown } from 'lucide-vue-next';

import { ref, computed } from 'vue';
import { cn } from '@/lib/utils';
import { Button } from '../components/ui/button';
import {
  Command,
  CommandEmpty,
  CommandGroup,
  CommandInput,
  CommandItem,
  CommandList,
} from '../components/ui/command';
import {
  Popover,
  PopoverContent,
  PopoverTrigger,
} from '../components/ui/popover';

const frameworks = [
  { value: 'next.js', label: 'Next.js' },
  { value: 'sveltekit', label: 'SvelteKit' },
  { value: 'nuxt', label: 'Nuxt' },
  { value: 'remix', label: 'Remix' },
  { value: 'astro', label: 'Astro' },
];

const open = ref(false);
const searchTerm = ref('');
const filteredFrameworks = computed(() => {
  return frameworks.filter((framework) =>
    framework.label.toLowerCase().includes(searchTerm.value.toLowerCase())
  );
});
const value = ref('');
</script>

<style scoped></style>
