<template>
  <div class="charts-container">
    <div class="period-selector">
      <span
        v-for="(period, index) in periods"
        :key="index"
        :class="{ active: selectedPeriod === period.days }"
        @click="setRange(period.days)"
      >
        {{ period.label }}
      </span>
    </div>

    <div class="chart">
      <LineChart
        :data="filteredData.indicators"
        index="date"
        :categories="[
          'close',
          'high',
          'low',
          'moving_average_20',
          'moving_average_50',
          'moving_average_200',
        ]"
        :y-formatter="
          (tick) => (typeof tick === 'number' ? tick.toFixed(2) : '')
        "
        :colors="colors"
      />
      <h2>株価指標</h2>
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
      <h2>取引量</h2>
    </div>
  </div>
</template>

<script setup lang="ts">
import { LineChart } from "../components/ui/chart-line";
import { ref, onMounted } from "vue";

const stockPrices = ref([]);
const filteredData = ref([]);
const selectedPeriod = ref(7); // デフォルトで1週間の期間を選択

const periods = [
  { label: "1週間", days: 7 },
  { label: "1ヶ月", days: 30 },
  { label: "6ヶ月", days: 180 },
  { label: "1年", days: 365 },
  { label: "2年", days: 730 },
  { label: "5年", days: 1825 },
];

// カテゴリーと色の設定
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

// 必要なフィールドのみを抽出
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

// localStorageからデータを取得して初期化
onMounted(() => {
  const storedData = localStorage.getItem("stockPrices");
  if (storedData) {
    stockPrices.value = JSON.parse(storedData);
    setRange(selectedPeriod.value); // デフォルト期間でフィルタリング
  }
});

// 期間のフィルタリング処理
// 期間でフィルタリングし、必要なデータのみを抽出
const setRange = (days: number) => {
  selectedPeriod.value = days;
  const now = new Date();
  const pastDate = new Date(now);
  pastDate.setDate(now.getDate() - days);

  const filtered = stockPrices.value.filter(
    (entry) => new Date(entry.date) >= pastDate
  );

  // 株価指標と取引量をそれぞれ抽出
  filteredData.value = {
    indicators: extractStockIndicators(filtered),
    volume: extractVolume(filtered),
  };
};
</script>

<style scoped>
.charts-container {
  display: flex;
  flex-direction: column;
  gap: 20px;
  height: 90%;
  padding: 10px;
  position: relative;
}

.period-selector {
  display: flex;
  justify-content: flex-end;
  gap: 20px;
}

.period-selector span {
  cursor: pointer;
  font-size: 18px;
  color: #555;
  transition: color 0.3s ease;
  border-bottom: 2px solid transparent;
}

.period-selector span:hover {
  color: #000;
}

.period-selector span.active {
  font-weight: bold;
  color: #000;
  border-bottom: 2px solid #888888;
}

.chart {
  width: 100%;
  height: 45%;
}

h2 {
  text-align: center;
  margin-bottom: 10px;
}
</style>
