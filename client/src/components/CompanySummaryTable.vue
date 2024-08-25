<template>
  <Table class="text-gray-900">
    <TableCaption class="text-md font-semibold py-4">企業情報</TableCaption>
    <TableBody>
      <TableRow class="border-b">
        <TableHead class="font-medium py-2">Ticker</TableHead>
        <TableCell>AAPL</TableCell>
      </TableRow>

      <TableRow class="border-b">
        <TableHead class="font-medium py-2">Company Name</TableHead>
        <TableCell>Apple Inc</TableCell>
      </TableRow>

      <TableRow class="border-b">
        <TableHead class="font-medium py-2">Exchange</TableHead>
        <TableCell>NASDAQ/NMS (GLOBAL MARKET)</TableCell>
      </TableRow>

      <TableRow class="border-b">
        <TableHead class="font-medium py-2">Industry</TableHead>
        <TableCell>Technology</TableCell>
      </TableRow>

      <TableRow class="border-b">
        <TableHead class="font-medium py-2">Country</TableHead>
        <TableCell>US</TableCell>
      </TableRow>

      <TableRow class="border-b">
        <TableHead class="font-medium py-2">Currency</TableHead>
        <TableCell>USD</TableCell>
      </TableRow>

      <TableRow class="border-b">
        <TableHead class="font-medium py-2">Market Capitalization</TableHead>
        <TableCell>1415993</TableCell>
      </TableRow>

      <TableRow class="border-b">
        <TableHead class="font-medium py-2">IPO Date</TableHead>
        <TableCell>1980-12-12</TableCell>
      </TableRow>

      <TableRow class="border-b">
        <TableHead class="font-medium py-2">Phone Number</TableHead>
        <TableCell>14089961010</TableCell>
      </TableRow>

      <TableRow class="border-b">
        <TableHead class="font-medium py-2">Shares Outstanding</TableHead>
        <TableCell>4375.47998046875</TableCell>
      </TableRow>

      <TableRow class="border-b">
        <TableHead class="font-medium py-2">Website</TableHead>
        <TableCell>
          <a href="https://www.apple.com/" class="text-blue-500 hover:underline"
            >Apple Website</a
          >
        </TableCell>
      </TableRow>

      <TableRow class="border-b">
        <TableHead class="font-medium py-2">Logo</TableHead>
        <TableCell>
          <img
            src="https://static.finnhub.io/logo/87cb30d8-80df-11ea-8951-00000000092a.png"
            alt="Apple Logo"
            class="w-16 h-16 object-contain"
          />
        </TableCell>
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
