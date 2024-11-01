<template>
  <Table class="text-gray-900">
    <TableBody v-if="companyProfile">
      <TableRow class="border-b">
        <TableHead class="font-medium py-2">Company Name</TableHead>
        <TableCell>{{ companyProfile.company_name }}</TableCell>
      </TableRow>

      <TableRow class="border-b">
        <TableHead class="font-medium py-2">Sector</TableHead>
        <TableCell>{{ companyProfile.sector }}</TableCell>
      </TableRow>

      <TableRow class="border-b">
        <TableHead class="font-medium py-2">Market Category</TableHead>
        <TableCell>{{ companyProfile.market_category }}</TableCell>
      </TableRow>

      <TableRow class="border-b">
        <TableHead class="font-medium py-2">Address</TableHead>
        <TableCell>{{ companyProfile.address }}</TableCell>
      </TableRow>

      <TableRow class="border-b">
        <TableHead class="font-medium py-2">Phone Number</TableHead>
        <TableCell>{{ companyProfile.phone_number }}</TableCell>
      </TableRow>

      <TableRow class="border-b">
        <TableHead class="font-medium py-2">Founding Year</TableHead>
        <TableCell>{{ companyProfile.founding_year }}</TableCell>
      </TableRow>

      <TableRow class="border-b">
        <TableHead class="font-medium py-2">Number of Employees</TableHead>
        <TableCell>{{ companyProfile.employee_count }}</TableCell>
      </TableRow>

      <TableRow class="border-b">
        <TableHead class="font-medium py-2">Outstanding Shares</TableHead>
        <TableCell>{{ companyProfile.outstanding_shares }}</TableCell>
      </TableRow>

      <TableRow class="border-b">
        <TableHead class="font-medium py-2">Market Capitalization</TableHead>
        <TableCell>{{ companyProfile.market_capitalization }}</TableCell>
      </TableRow>

      <TableRow class="border-b">
        <TableHead class="font-medium py-2"
          >Average Trading Volume (10 days)</TableHead
        >
        <TableCell>{{ companyProfile.average_trading_volume_10d }}</TableCell>
      </TableRow>

      <TableRow class="border-b">
        <TableHead class="font-medium py-2">Business Description</TableHead>
        <TableCell>{{ companyProfile.business_description }}</TableCell>
      </TableRow>
    </TableBody>
  </Table>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { useStore } from 'vuex'
import {
  Table,
  TableBody,
  TableCaption,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from '../ui/table'

const store = useStore()
const companyProfile = computed(() => store.state.companyProfile.profile)
</script>
