<template>
  <div class="p-4 h-screen flex flex-col">
    <!-- ヘッダー -->
    <div class="flex justify-end items-center mb-4">
      <DropDownMenu />
    </div>

    <div class="flex flex-col md:flex-row gap-4 flex-grow">
      <!-- 左要素 -->
      <div class="basis-1/7 md:basis-1/7 max-w-xs">
        <TickerSelector />
      </div>

      <!-- 中央要素 -->
      <div class="basis-2/6 md:basis-2/6 flex-grow">
        <div class="overflow-y-auto" style="max-height: calc(100vh - 150px)">
          <CompanyProfile class="mb-20" />
          <FinancialSummaryTable />
        </div>
      </div>

      <!-- 右要素 -->
      <div class="basis-3/6 md:basis-3/6">
        <div class="flex justify-end mb-8">
          <Button>Reconnect</Button>
        </div>
        <Graph />
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import DropDownMenu from "@/components/DropDownMenu.vue";
import CompanyProfile from "@/components/CompanyProfile.vue";
import FinancialSummaryTable from "@/components/CompanyFinancials.vue";
import TickerSelector from "@/components/TickerSelector.vue";
import Graph from "@/components/Graph.vue";
import { Button } from "../components/ui/button";
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
