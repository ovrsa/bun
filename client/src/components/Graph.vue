<script setup lang="ts">
import { LineChart } from "../components/ui/chart-line";
import { ref, onMounted } from "vue";

const stockPrices = ref([]);

onMounted(() => {
  const storedData = localStorage.getItem("stockPrices");
  if (storedData) {
    stockPrices.value = JSON.parse(storedData);
  }
});
</script>

<template>
  <div>
    <LineChart
      :data="stockPrices"
      index="date"
      :categories="['close', 'high', 'low']"
      :y-formatter="(tick) => (typeof tick === 'number' ? tick.toFixed(2) : '')"
    />
    <LineChart
      :data="stockPrices"
      index="date"
      :categories="['volume']"
      :y-formatter="(tick) => (typeof tick === 'number' ? tick.toFixed(2) : '')"
    />
  </div>
</template>

<style scoped>
.charts-container {
  display: flex;
  flex-direction: column;
  gap: 20px;
  height: 90%;
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
