<template>
  <Popover v-model="open">
    <PopoverTrigger as-child>
      <Button
        variant="outline"
        role="combobox"
        :aria-expanded="open"
        class="w-[150px] justify-between"
      >
        {{ selectedSymbol ? selectedSymbol : "Select Ticker" }}
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
                    selectedSymbol === ticker.label
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
import { ref, computed, onMounted } from "vue";
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

const tickerList = [
  { value: "TSLA", label: "Tesla" },
  { value: "AAPL", label: "Apple" },
  { value: "GOOGL", label: "Alphabet" },
  { value: "MSFT", label: "Microsoft" },
];

const open = ref(false);
const selectedSymbol = ref(localStorage.getItem("selectedTicker") || "");
const searchTerm = ref("");
const store = useStore();

const filteredTickerList = computed(() =>
  tickerList.filter((ticker) =>
    ticker.label.toLowerCase().includes(searchTerm.value.toLowerCase())
  )
);

const emit = defineEmits(["selectTicker"]);
const handleSelect = async (ticker: { value: string; label: string }) => {
  selectedSymbol.value = ticker.label;
  localStorage.setItem("selectedTicker", ticker.label);
  open.value = false;

  emit("selectTicker", ticker.label);

  try {
    await store.dispatch("companyProfile/fetchCompanyProfile", ticker.value);
    await store.dispatch(
      "companyFinancials/fetchCompanyFinancials",
      ticker.value
    );
    await store.dispatch("stockPrices/fetchStockPrices", ticker.value);
    console.log("Dispatch succeeded");
  } catch (error) {
    console.error("Dispatch failed:", error);
  }
};

onMounted(() => {
  const savedTicker = localStorage.getItem("selectedTicker");
  if (savedTicker) {
    selectedSymbol.value = savedTicker;
  }
});
</script>
