<template>
  <Table class="text-gray-900">
    <TableCaption class="text-md font-semibold py-4"
      >財務サマリー（単位: ドル）</TableCaption
    >
    <TableHeader>
      <TableRow>
        <TableHead class="w-[200px] font-medium py-2">項目</TableHead>
        <TableHead v-for="date in dates" :key="date" class="font-medium py-2">{{
          date
        }}</TableHead>
      </TableRow>
    </TableHeader>
    <TableBody>
      <TableRow
        v-for="item in financeSummary"
        :key="item.name"
        class="border-b"
      >
        <TableCell class="py-2">{{ item.name }}</TableCell>
        <TableCell v-for="value in item.values" :key="value" class="py-2">{{
          value
        }}</TableCell>
      </TableRow>
    </TableBody>
  </Table>
</template>

<script setup lang="ts">
import {
  Table,
  TableBody,
  TableCaption,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from '../components/ui/table';
import { ref } from 'vue';

const dates = ref([
  '2024-03-31',
  '2023-03-31',
  '2022-03-31',
  '2021-03-31',
  '2020-03-31',
]);

const financeSummary = ref([
  {
    name: 'Total Revenue',
    values: ['5,000,000', '5,000,000', '5,000,000', '5,000,000', '5,000,000'],
  },
  {
    name: 'EBITDA',
    values: ['1,000,000', '1,000,000', '1,000,000', '1,000,000', '1,000,000'],
  },
  {
    name: 'Stockholders Equity',
    values: ['3,000,000', '3,000,000', '3,000,000', '3,000,000', '3,000,000'],
  },
  {
    name: 'Free Cash Flow',
    values: ['500,000', '500,000', '500,000', '500,000', '500,000'],
  },
  {
    name: 'Capital Expenditure',
    values: ['100,000', '100,000', '100,000', '100,000', '100,000'],
  },
  {
    name: 'Total Assets',
    values: [
      '338,516,000',
      '338,516,000',
      '338,516,000',
      '338,516,000',
      '338,516,000',
    ],
  },
  {
    name: 'Total Liabilities',
    values: [
      '248,028,000',
      '248,028,000',
      '248,028,000',
      '248,028,000',
      '248,028,000',
    ],
  },
  {
    name: 'Gross Profit',
    values: [
      '98,392,000',
      '98,392,000',
      '98,392,000',
      '98,392,000',
      '98,392,000',
    ],
  },
  {
    name: 'Net Income/Loss',
    values: [
      '55,256,000',
      '55,256,000',
      '55,256,000',
      '55,256,000',
      '55,256,000',
    ],
  },
  {
    name: 'Operating Expenses',
    values: [
      '34,462,000',
      '34,462,000',
      '34,462,000',
      '34,462,000',
      '34,462,000',
    ],
  },
]);
</script>

<style scoped>
.table-caption {
  font-size: 1.25rem;
  font-weight: 600;
}

.table-cell,
.table-head {
  padding: 0.75rem 1rem;
}

.table-row {
  border-bottom: 1px solid #e5e7eb;
}

.table-head {
  font-weight: 600;
  background-color: #f3f4f6;
}
</style>
