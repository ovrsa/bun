<template>
  <div class="charts-container">
    <div class="chart">
      <LineChart
        :data="filteredData.indicators"
        index="date"
        :categories="categories"
        :y-formatter="
          (tick) => (typeof tick === 'number' ? tick.toFixed(2) : '')
        "
        :colors="colors"
      />
    </div>

    <div class="chart">
      <LineChart
        :data="filteredData.volume"
        index="date"
        :categories="['volume']"
        :y-formatter="
          (tick) => (typeof tick === 'number' ? tick.toFixed(2) : '')
        "
        :colors="['#673AB7']"
      />
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, watch, onMounted } from "vue";
import { LineChart } from "../ui/chart-line";

const props = defineProps({
  selectedPeriod: Number,
});

const stockPrices = ref([]);
const filteredData = ref({
  indicators: [],
  volume: [],
});

const categories = [
  "close",
  "high",
  "low",
  "moving_average_20",
  "moving_average_50",
  "moving_average_200",
];

const colors = [
  "#4CAF50", // 終値 (close): 緑
  "#808080", // 高値 (high): グレー
  "#808080", // 安値 (low): グレー
  "#2196F3", // 20日移動平均: 青
  "#9C27B0", // 50日移動平均: 紫
  "#795548", // 200日移動平均: 茶色
];

const extractStockIndicators = (data) =>
  data.map((entry) => ({
    date: entry.date,
    close: entry.close,
    high: entry.high,
    low: entry.low,
    moving_average_20: entry.moving_average_20,
    moving_average_50: entry.moving_average_50,
    moving_average_200: entry.moving_average_200,
  }));

const extractVolume = (data) =>
  data.map((entry) => ({
    date: entry.date,
    volume: entry.volume,
  }));

// localStorageからデータを取得
onMounted(() => {
  const storedData = localStorage.getItem("stockPrices");
  if (storedData) {
    stockPrices.value = JSON.parse(storedData);
    filterDataByPeriod(props.selectedPeriod);
  }
});

// 期間の変更を監視し、データを再フィルタリング
watch(
  () => props.selectedPeriod,
  (newPeriod) => {
    filterDataByPeriod(newPeriod);
  }
);

// 期間でデータをフィルタリングする関数
const filterDataByPeriod = (days) => {
  const now = new Date();
  const pastDate = new Date(now);
  pastDate.setDate(now.getDate() - days);

  const filtered = stockPrices.value.filter(
    (entry) => new Date(entry.date) >= pastDate
  );

  filteredData.value = {
    indicators: extractStockIndicators(filtered),
    volume: extractVolume(filtered),
  };
};
</script>

<style scoped></style>
