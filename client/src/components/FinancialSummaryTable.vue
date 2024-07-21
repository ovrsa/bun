<template>
  <Table>
    <TableCaption>財務サマリー（単位: 百万円）</TableCaption>
    <TableHeader>
      <TableRow>
        <TableHead class="w-[200px]">項目</TableHead>
        <TableHead v-for="date in dates" :key="date">{{ date }}</TableHead>
      </TableRow>
    </TableHeader>
    <TableBody>
      <TableRow v-for="item in financeSummary" :key="item.name">
        <TableCell class="font-medium">{{ item.name }}</TableCell>
        <TableCell v-for="value in item.values" :key="value">{{
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

// 現在の日付を基準に過去5年間の3月31日を取得
const today = new Date();
const currentYear = today.getFullYear();
const dates = ref([]);

// TODO: 日付のデータを取得する処理を実装
// 財務サマリー項目と値
const financeSummary = ref([
  {
    name: 'Total Revenue',
    values: ['905,204', '862,585', '866,702', '1,020,456', '1,050,000'],
  },
  {
    name: 'Normalized EBITDA',
    values: ['38,287', '36,805', '46,749', '52,919', '55,000'],
  },
  {
    name: 'Net Debt',
    values: ['239,932', '228,258', '225,651', '267,459', '280,000'],
  },
  {
    name: 'Stockholders Equity',
    values: ['132,629', '142,833', '160,173', '178,311', '190,000'],
  },
  {
    name: 'Free Cash Flow',
    values: ['15,046', '10,590', '4,431', '-29,767', '-25,000'],
  },
  {
    name: 'Capital Expenditure',
    values: ['-24,132', '-22,771', '-14,818', '-29,743', '-30,000'],
  },
]);
</script>

<style scoped></style>
