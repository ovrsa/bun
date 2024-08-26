<script setup lang="ts">
import { LineChart } from '../components/ui/chart-line';

const lastPriceData = [
  { time: '10:00:01', value: 7296.89 },
  { time: '10:00:02', value: 7297.45 },
  { time: '10:00:03', value: 7295.5 },
];

const volumeData = [
  { time: '10:00:01', value: 0.011467 },
  { time: '10:00:02', value: 0.012345 },
  { time: '10:00:03', value: 0.009876 },
];

const formatCurrency = (value: number) => {
  return `$ ${value.toFixed(2)}`;
};

const formatVolume = (value: number) => {
  return value.toFixed(6);
};

const formatTime = (time: string) => {
  return time.split(':')[2];
};
</script>

<template>
  <div class="charts-container">
    <div class="chart">
      <h2>Last Price</h2>
      <LineChart
        :data="lastPriceData"
        index="time"
        :categories="['value']"
        :y-formatter="
          (tick) => (typeof tick === 'number' ? formatCurrency(tick) : '')
        "
        :colors="['#4CAF50']"
        :margin="{ top: 20, right: 20, left: 60 }"
        :show-tooltip="true"
        :show-legend="false"
        :show-grid-line="true"
        :show-x-axis="true"
      />
    </div>
    <div class="chart">
      <h2>Volume</h2>
      <LineChart
        :data="volumeData"
        index="time"
        :categories="['value']"
        :y-formatter="
          (tick) => (typeof tick === 'number' ? formatVolume(tick) : '')
        "
        :colors="['#2196F3']"
        :margin="{ top: 20, right: 20, left: 60 }"
        :show-tooltip="true"
        :show-legend="false"
        :show-grid-line="true"
        :show-x-axis="true"
      />
    </div>
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
