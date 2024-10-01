<template>
  <Popover v-model="open">
    <PopoverTrigger as-child>
      <Button
        variant="outline"
        role="combobox"
        :aria-expanded="open"
        class="w-[200px] justify-between"
      >
        {{
          selectedSymbol
            ? frameworks.find((framework) => framework.value === selectedSymbol)
                ?.label
            : "Select Ticker"
        }}

        <ChevronsUpDown class="ml-2 h-4 w-4 shrink-0 opacity-50" />
      </Button>
    </PopoverTrigger>
    <PopoverContent class="w-[200px] p-0">
      <Command v-model="selectedSymbol">
        <CommandInput placeholder="Select Ticker..." />
        <CommandEmpty>No ticker found.</CommandEmpty>
        <CommandList>
          <CommandGroup>
            <CommandItem
              v-for="framework in frameworks"
              :key="framework.value"
              :value="framework.value"
              @select="handleSelect(framework)"
            >
              <Check
                :class="
                  cn(
                    'mr-2 h-4 w-4',
                    selectedSymbol === framework.value
                      ? 'opacity-100'
                      : 'opacity-0'
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
</template>

<script setup lang="ts">
import { ref } from "vue";
import { useStore } from "vuex";
import { cn } from "@/lib/utils";
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

const frameworks = [
  { value: "TSLA", label: "Tesla" },
  { value: "AAPL", label: "Apple" },
  { value: "GOOGL", label: "Alphabet" },
];
const open = ref(false);
const selectedSymbol = ref("");

const store = useStore();

const handleSelect = async (framework: { value: string; label: string }) => {
  selectedSymbol.value = framework.value;
  open.value = false;

  try {
    console.log("Dispatching fetchCompanyProfile with:", framework.value);
    await store.dispatch("companyProfile/fetchCompanyProfile", framework.value);
    console.log("Dispatch succeeded");
  } catch (error) {
    console.error("Dispatch failed:", error);
  }
};
</script>
