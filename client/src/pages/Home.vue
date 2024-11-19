<template>
  <HomeTemplate @logoClick="navigateToHome" @logout="handleLogout">
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

      <StockChart
        :selectedPeriod="selectedPeriod"
        :selectedTicker="selectedLabel"
      />
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
  </HomeTemplate>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { useStore } from 'vuex'
import { useRouter } from 'vue-router'

import HomeTemplate from '@/components/templates/HomeTemplate.vue'
import TickerSelector from '@/components/molecules/TickerSelector.vue'
import StockChart from '@/components/organisms/StockChart.vue'
import CompanyProfile from '@/components/organisms/CompanyProfile.vue'
import FinancialSummaryTable from '@/components/organisms/CompanyFinancials.vue'

const router = useRouter()
const navigateToHome = () => router.push('/')

const isOverview = ref(true)
const selectedPeriod = ref(365)
const selectedLabel = ref(localStorage.getItem('selectedTicker') || '')
const periods = [
  { label: '1W', days: 7 },
  { label: '1M', days: 30 },
  { label: '6M', days: 180 },
  { label: '1Y', days: 365 },
  { label: '2Y', days: 730 },
  { label: '5Y', days: 1825 },
]

const store = useStore()

const handleTickerSelect = (label: string) => {
  selectedLabel.value = label
  localStorage.setItem('selectedTicker', label)
}

const handleLogout = () => {
  store.dispatch('auth/logout')
}

const showOverview = () => (isOverview.value = true)
const showSummary = () => (isOverview.value = false)
const setRange = (days: number) => (selectedPeriod.value = days)
</script>

<style scoped></style>
