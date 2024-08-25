<template>
  <div class="p-4 h-screen flex flex-col">
    <!-- ヘッダー -->
    <div class="flex justify-end items-center bg-blue-100 mb-4">
      <DropDownMenu />
    </div>

    <div class="flex flex-col md:flex-row gap-4 flex-grow">
      <!-- 左要素 -->
      <div class="basis-1/7 md:basis-1/7 bg-yellow-100 max-w-xs">
        <TickerSelector />
      </div>

      <!-- 中央要素 -->
      <div class="basis-2/6 md:basis-2/6 bg-green-100 flex-grow">
        <div class="overflow-y-auto" style="max-height: calc(100vh - 150px)">
          <CompanySummaryTable class="mb-20" />
          <FinancialSummaryTable />
        </div>
      </div>

      <!-- 右要素 -->
      <div class="basis-3/6 md:basis-3/6 bg-red-100">
        <Graph />
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import DropDownMenu from '@/components/DropDownMenu.vue';
import CompanySummaryTable from '@/components/CompanySummaryTable.vue';
import FinancialSummaryTable from '@/components/FinancialSummaryTable.vue';
import TickerSelector from '@/components/TickerSelector.vue';
import Graph from '@/components/Graph.vue';
</script>

<style scoped>
::-webkit-scrollbar {
  width: 6px;
}

::-webkit-scrollbar-track {
  background: #f1f1f1;
}

::-webkit-scrollbar-thumb {
  background: #888;
}

::-webkit-scrollbar-thumb:hover {
  background: #555;
}
</style>
