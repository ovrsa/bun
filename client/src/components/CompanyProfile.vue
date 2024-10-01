<template>
  <Table class="text-gray-900">
    <TableCaption class="text-md font-semibold py-4">企業情報</TableCaption>
    <TableBody v-if="companyProfile">
      <!-- ティッカー -->
      <TableRow class="border-b">
        <TableHead class="font-medium py-2">Ticker</TableHead>
        <TableCell>{{ companyProfile.ticker }}</TableCell>
      </TableRow>

      <!-- 会社名 -->
      <TableRow class="border-b">
        <TableHead class="font-medium py-2">Company Name</TableHead>
        <TableCell>{{ companyProfile.company_name }}</TableCell>
      </TableRow>

      <!-- 取引所 -->
      <TableRow class="border-b">
        <TableHead class="font-medium py-2">Exchange</TableHead>
        <TableCell>{{ companyProfile.exchange }}</TableCell>
      </TableRow>

      <!-- 業界 -->
      <TableRow class="border-b">
        <TableHead class="font-medium py-2">Industry</TableHead>
        <TableCell>{{ companyProfile.finnhub_industry }}</TableCell>
      </TableRow>

      <TableRow class="border-b">
        <TableHead class="font-medium py-2">Country</TableHead>
        <TableCell>{{ companyProfile.country }}</TableCell>
      </TableRow>

      <TableRow class="border-b">
        <TableHead class="font-medium py-2">Currency</TableHead>
        <TableCell>{{ companyProfile.currency }}</TableCell>
      </TableRow>

      <!-- 時価総額 -->
      <TableRow class="border-b">
        <TableHead class="font-medium py-2">Market Capitalization</TableHead>
        <TableCell>{{ companyProfile.market_capitalization }}</TableCell>
      </TableRow>

      <!-- IPO 日付 -->
      <TableRow class="border-b">
        <TableHead class="font-medium py-2">IPO Date</TableHead>
        <TableCell>{{ companyProfile.ipo_date }}</TableCell>
      </TableRow>

      <!-- 電話番号 -->
      <TableRow class="border-b">
        <TableHead class="font-medium py-2">Phone Number</TableHead>
        <TableCell>{{ companyProfile.phone }}</TableCell>
      </TableRow>

      <!-- 発行株数 -->
      <TableRow class="border-b">
        <TableHead class="font-medium py-2">Shares Outstanding</TableHead>
        <TableCell>{{ companyProfile.share_outstanding }}</TableCell>
      </TableRow>

      <!-- ウェブサイト -->
      <TableRow class="border-b">
        <TableHead class="font-medium py-2">Website</TableHead>
        <TableCell>
          <a
            :href="companyProfile.website_url"
            class="text-blue-500 hover:underline"
          >
            {{ companyProfile.website_url }}
          </a>
        </TableCell>
      </TableRow>

      <!-- ロゴ -->
      <TableRow class="border-b">
        <TableHead class="font-medium py-2">Logo</TableHead>
        <TableCell>
          <img
            :src="companyProfile.logo_url"
            :alt="`${companyProfile.company_name} Logo`"
            class="w-16 h-16 object-contain"
          />
        </TableCell>
      </TableRow>
    </TableBody>
    <TableBody v-else>
      <TableRow>
        <TableCell colspan="2" class="text-center">
          No company information available.
        </TableCell>
      </TableRow>
    </TableBody>
  </Table>
</template>

<script setup lang="ts">
import { computed } from "vue";
import { useStore } from "vuex";
import {
  Table,
  TableBody,
  TableCaption,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "./ui/table";

const store = useStore();
const companyProfile = computed(() => store.state.companyProfile.profile);

console.log("Company Profile from Store:", companyProfile.value);
</script>
