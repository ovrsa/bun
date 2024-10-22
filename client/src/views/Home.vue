<template>
  <div class="pt-20">
    <header class="fixed top-0 left-0 w-full bg-gray-800 text-white py-4 z-50">
      <div
        class="flex justify-between items-center max-w-screen-xl mx-auto px-4"
      >
        <div class="flex items-center">
          <img src="/img/bun.png" alt="Bun Logo" class="h-10" />
          <div class="text-xl ml-7 cursor-pointer" @click="navigateToHome">
            Bun
          </div>
        </div>
        <DropDownMenu />
      </div>
    </header>

    <div class="max-w-screen-xl mx-auto flex flex-col gap-6 mt-8 px-4">
      <div class="flex items-center gap-4">
        <TickerSelector @selectTicker="handleTickerSelect" />
        <span class="text-2xl font-bold pl-2">{{ selectedLabel }}</span>
      </div>

      <div class="p-10 bg-gray-100 border-t border-black">
        <div class="text-sm">CHART RANGE</div>
        <div class="flex py-2">
          <button
            v-for="period in periods"
            :key="period.label"
            @click="setRange(period.days)"
            :class="[
              'px-4 py-2 border text-sm',
              selectedPeriod === period.days
                ? 'bg-blue-200 border-blue-500'
                : 'bg-white border-slate-300',
            ]"
          >
            {{ period.label }}
          </button>
        </div>
      </div>

      <!-- グラフ表示 -->
      <StockChart :selectedPeriod="selectedPeriod" />
    </div>

    <div class="max-w-screen-xl mx-auto mt-10 px-4">
      <div class="flex mb-4">
        <span
          @click="showOverview"
          :class="[
            'cursor-pointer px-4 py-2 text-sm border-b-2 font-bold',
            isOverview ? 'border-blue-500' : 'border-slate-300',
          ]"
        >
          Overview
        </span>
        <span
          @click="showSummary"
          :class="[
            'cursor-pointer px-4 py-2 text-sm border-b-2 font-bold',
            !isOverview ? 'border-blue-500' : 'border-slate-300',
          ]"
        >
          Summary
        </span>
      </div>

      <div v-if="isOverview">
        <CompanyProfile />
      </div>
      <div v-else>
        <FinancialSummaryTable />
      </div>
    </div>

    <footer class="bg-gray-800 text-white py-4 mt-10 w-full">
      <div class="max-w-screen-xl mx-auto text-center">
        <p>© 2024 Bun</p>
      </div>
    </footer>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from "vue";
import { useRouter } from "vue-router";
import DropDownMenu from "@/components/DropDownMenu.vue";
import CompanyProfile from "@/components/CompanyProfile.vue";
import FinancialSummaryTable from "@/components/CompanyFinancials.vue";
import TickerSelector from "@/components/TickerSelector.vue";
import StockChart from "@/components/StockChart.vue";

const isOverview = ref(true);
const selectedPeriod = ref(30);
const selectedLabel = ref(localStorage.getItem("selectedTicker") || "");

const periods = [
  { label: "1W", days: 7 },
  { label: "1M", days: 30 },
  { label: "6M", days: 180 },
  { label: "1Y", days: 365 },
  { label: "2Y", days: 730 },
  { label: "5Y", days: 1825 },
];

const handleTickerSelect = (label: string) => {
  selectedLabel.value = label;
  localStorage.setItem("selectedLabel", label);
};
const showOverview = () => (isOverview.value = true);
const showSummary = () => (isOverview.value = false);
const setRange = (days: number) => (selectedPeriod.value = days);

const router = useRouter();
const navigateToHome = () => router.push("/");
</script>

<style scoped></style>
