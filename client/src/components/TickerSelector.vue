<template>
  <Popover v-model:open="open">
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
import { fetchCompanyProfile as getCompanyProfile } from "@/services/companyProfiles";

const frameworks = [
  { value: "TSLA", label: "Tesla" },
  { value: "AAPL", label: "Apple" },
  { value: "GOOGL", label: "Alphabet" },
];
const open = ref(false);
const selectedSymbol = ref("");

const fetchCompanyProfileData = async (symbol: string) => {
  try {
    const response = await getCompanyProfile(symbol);
    console.log("API Response:", response);
  } catch (error) {
    console.error("API Request Failed:", error);
  }
};

const handleSelect = (framework: { value: string; label: string }) => {
  selectedSymbol.value = framework.value;
  console.log(selectedSymbol.value);
  open.value = false;
  fetchCompanyProfileData(framework.value);
};
</script>
