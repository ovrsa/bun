<template>
  <Table>
    <TableCaption>企業情報</TableCaption>
    <TableBody>
      <TableRow>
        <TableHead>コード</TableHead>
        <TableCell>3</TableCell>
      </TableRow>
      <TableRow>
        <TableHead>会社名</TableHead>
        <TableCell>マルハニチロ</TableCell>
      </TableRow>
      <TableRow>
        <TableHead>市場・商品区分</TableHead>
        <TableCell>プライム（内国株式）</TableCell>
      </TableRow>
      <TableRow>
        <TableHead>33業種区分</TableHead>
        <TableCell>水産・農林業</TableCell>
      </TableRow>
      <TableRow>
        <TableHead>17業種区分</TableHead>
        <TableCell>食品</TableCell>
      </TableRow>
      <TableRow>
        <TableHead>最新株価（円）</TableHead>
        <TableCell>2672.0</TableCell>
      </TableRow>
      <TableRow>
        <TableHead>時価総額（百万円）</TableHead>
        <TableCell>134,804</TableCell>
      </TableRow>
      <TableRow>
        <TableHead>EV（百万円）</TableHead>
        <TableCell>450,767</TableCell>
      </TableRow>
      <TableRow>
        <TableHead>EBITDA（百万円）</TableHead>
        <TableCell>45,381</TableCell>
      </TableRow>
      <TableRow>
        <TableHead>EV/EBITDAマルチプル</TableHead>
        <TableCell>9.93</TableCell>
      </TableRow>
      <TableRow>
        <TableHead>会社説明</TableHead>
        <TableCell
          >Maruha Nichiro Corporation engages in the fishing, fish farming, food
          processing, trading, meat products, and distribution businesses in
          Japan and internationally.</TableCell
        >
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
</script>

<style scoped></style>
