import { ref, computed, onMounted } from "vue";
import { useStore } from "vuex";

const selectedTicker = ref(localStorage.getItem("selectedTicker") || "");
const searchTerm = ref("");

const tickerList = [
  { value: "TSLA", label: "Tesla" },
  { value: "AAPL", label: "Apple" },
  { value: "GOOGL", label: "Alphabet" },
  { value: "MSFT", label: "Microsoft" },
];

export function useTicker() {
  const store = useStore();

  const filteredTickerList = computed(() =>
    tickerList.filter((ticker) =>
      ticker.label.toLowerCase().includes(searchTerm.value.toLowerCase())
    )
  );

  const selectTicker = async (ticker: { value: string; label: string }) => {
    selectedTicker.value = ticker.label;
    localStorage.setItem("selectedTicker", ticker.label);

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
      selectedTicker.value = savedTicker;
    }
  });

  return {
    searchTerm,
    selectedTicker,
    filteredTickerList,
    selectTicker,
  };
}
