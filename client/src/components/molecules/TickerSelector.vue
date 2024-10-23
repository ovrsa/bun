<template>
  <Popover v-model="open">
    <PopoverTrigger as-child>
      <Button
        variant="outline"
        role="combobox"
        :aria-expanded="open"
        class="w-[150px] justify-between"
      >
        {{ selectedTicker ? selectedTicker : "Select Ticker" }}
        <ChevronsUpDown class="ml-2 h-4 w-4 opacity-50" />
      </Button>
    </PopoverTrigger>
    <PopoverContent class="w-[300px]">
      <Command>
        <CommandInput placeholder="Search Ticker..." v-model="searchTerm" />
        <CommandEmpty>No ticker found.</CommandEmpty>
        <CommandList>
          <CommandGroup>
            <CommandItem
              v-for="ticker in filteredTickerList"
              :key="ticker.label"
              :value="ticker.label"
              @select="handleSelect(ticker)"
            >
              <Check
                :class="
                  cn(
                    'mr-2 h-4 w-4',
                    selectedTicker === ticker.label
                      ? 'opacity-100'
                      : 'opacity-0'
                  )
                "
              />
              {{ ticker.label }}
            </CommandItem>
          </CommandGroup>
        </CommandList>
      </Command>
    </PopoverContent>
  </Popover>
</template>

<script setup lang="ts">
import { ref } from "vue";
import { cn } from "@/lib/utils";
import { useTicker } from "@/composables/useTicker";
import { Button } from "@/components/ui/button";
import {
  Command,
  CommandEmpty,
  CommandGroup,
  CommandInput,
  CommandItem,
  CommandList,
} from "@/components/ui/command";
import {
  Popover,
  PopoverContent,
  PopoverTrigger,
} from "@/components/ui/popover";

const emit = defineEmits(["selectTicker"]);

const open = ref(false);
const { searchTerm, selectedTicker, filteredTickerList, selectTicker } =
  useTicker();

const handleSelect = (ticker: { value: string; label: string }) => {
  selectTicker(ticker);
  emit("selectTicker", ticker.label);
  open.value = false;
};
</script>
