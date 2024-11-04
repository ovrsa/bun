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
import { ref, watch, computed, onMounted } from 'vue'
import { useStore } from 'vuex'
import { LineChart } from '../ui/chart-line'
import { StockEntry, OrderEntry } from '@/types/interfaces'

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

const props = defineProps({
  selectedPeriod: Number,
  selectedTicker: String,
})

const store = useStore()
const stockPrices = computed(
  () => store.getters['stockPrices/stockPrices'] || []
)

// ローディング状態とエラー状態も取得可能
const loading = computed(() => store.getters['stockPrices/loading'])
const error = computed(() => store.getters['stockPrices/error'])

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

const filterDataByPeriod = (days: number) => {
  if (!stockPrices.value || stockPrices.value.length === 0) {
    filteredData.value = { indicators: [], volume: [] }
    return
  }
  const now = new Date()
  const pastDate = new Date(now)
  pastDate.setDate(now.getDate() - days)
  const filtered = stockPrices.value.filter(
    (entry: OrderEntry) => new Date(entry.date) >= pastDate
  )
  filteredData.value = {
    indicators: extractStockIndicators(filtered),
    volume: extractVolume(filtered),
  }
}

// 初期化時にローカルストレージからデータをロード
onMounted(() => {
  store.dispatch('stockPrices/initStockPrices')
  if (stockPrices.value && stockPrices.value.length > 0) {
    filterDataByPeriod(props.selectedPeriod ?? 365)
  }
})

// stockPrices の変更を監視して、データが取得されたらグラフを更新
watch(
  stockPrices,
  newStockPrices => {
    if (newStockPrices && newStockPrices.length > 0) {
      filterDataByPeriod(props.selectedPeriod ?? 365)
    } else {
      filteredData.value = { indicators: [], volume: [] }
    }
  },
  { immediate: true }
)

// selectedPeriod の変更を監視してグラフを更新
watch(
  () => props.selectedPeriod,
  newPeriod => {
    if (newPeriod !== undefined) {
      filterDataByPeriod(newPeriod)
    }
  }
)
</script>
