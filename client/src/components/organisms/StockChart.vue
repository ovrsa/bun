<template>
  <div class="charts-container">
    <div class="chart">
      <LineChart
        :data="filteredData.indicators"
        index="date"
        :categories="categories"
        :y-formatter="tick => (typeof tick === 'number' ? tick.toFixed(2) : '')"
        :colors="colors"
      />
    </div>

    <div class="chart">
      <LineChart
        :data="filteredData.volume"
        index="date"
        :categories="['volume']"
        :y-formatter="tick => (typeof tick === 'number' ? tick.toFixed(2) : '')"
        :colors="['#673AB7']"
      />
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, watch } from 'vue'
import { LineChart } from '../ui/chart-line'
import { StockEntry } from '@/types/interfaces'

const props = defineProps({
  selectedPeriod: Number,
  selectedTicker: String,
  stockData: Array as () => StockEntry[],
})

const stockPrices = ref<StockEntry[]>([])
const filteredData = ref({
  indicators: [] as Array<{
    date: string
    close: number
    high: number
    low: number
    moving_average_20?: number
    moving_average_50?: number
    moving_average_200?: number
  }>,
  volume: [] as Array<{
    date: string
    volume: number
  }>,
})

const categories: Array<
  | 'close'
  | 'high'
  | 'low'
  | 'moving_average_20'
  | 'moving_average_50'
  | 'moving_average_200'
> = [
  'close',
  'high',
  'low',
  'moving_average_20',
  'moving_average_50',
  'moving_average_200',
]

const colors = [
  '#4CAF50', // 終値 (close): 緑
  '#808080', // 高値 (high): グレー
  '#808080', // 安値 (low): グレー
  '#2196F3', // 20日移動平均: 青
  '#9C27B0', // 50日移動平均: 紫
  '#795548', // 200日移動平均: 茶色
]

const extractStockIndicators = (data: StockEntry[]) =>
  data.map(entry => ({
    date: entry.date,
    close: entry.close,
    high: entry.high,
    low: entry.low,
    moving_average_20: entry.moving_average_20,
    moving_average_50: entry.moving_average_50,
    moving_average_200: entry.moving_average_200,
  }))

const extractVolume = (data: StockEntry[]) =>
  data.map(entry => ({
    date: entry.date,
    volume: entry.volume,
  }))

// 期間でデータをフィルタリングする関数
const filterDataByPeriod = (days: number) => {
  const now = new Date()
  const pastDate = new Date(now)
  pastDate.setDate(now.getDate() - days)

  const filtered = stockPrices.value.filter(
    entry => new Date(entry.date) >= pastDate
  )
  filteredData.value = {
    indicators: extractStockIndicators(filtered),
    volume: extractVolume(filtered),
  }
}

// localStorageからデータを取得
const fetchData = (ticker: string) => {
  const storedData = localStorage.getItem('stockPrices')
  if (storedData) {
    stockPrices.value = JSON.parse(storedData)
    filterDataByPeriod(props.selectedPeriod ?? 365)
  } else {
    console.warn('No data found in localStorage')
  }
}

watch(
  () => props.selectedTicker,
  newTicker => {
    if (newTicker) {
      fetchData(newTicker)
    }
  },
  { immediate: true }
)

watch(
  () => props.selectedPeriod,
  newPeriod => {
    if (newPeriod !== undefined) {
      filterDataByPeriod(newPeriod)
    }
  }
)
</script>

<style scoped></style>
