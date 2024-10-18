<template>
  <Table class="text-gray-900">
    <TableCaption class="text-md font-semibold py-4">
      Financial Summary
    </TableCaption>
    <TableHeader>
      <TableRow>
        <TableHead class="w-[200px] font-medium py-2">Item</TableHead>
        <TableHead v-for="date in dates" :key="date" class="font-medium py-2">
          {{ date }}
        </TableHead>
      </TableRow>
    </TableHeader>
    <TableBody>
      <TableRow
        v-for="item in financeSummary"
        :key="item.name"
        class="border-b"
      >
        <TableCell class="py-2">{{ item.name }}</TableCell>
        <TableCell
          v-for="(value, index) in item.values"
          :key="index"
          class="py-2"
        >
          {{ value }}
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
} from "./ui/table";
import { computed } from "vue";
import { useStore } from "vuex";

const store = useStore();

// ストアからデータを取得
const financialsData = computed(() => store.state.companyFinancials.data);
console.log("Company Financials from Store:", financialsData.value);

const dates = computed(() => {
  if (financialsData.value) {
    return financialsData.value.map((financial) => financial.fiscal_year);
  }
  return [];
});

const financeSummary = computed(() => {
  if (financialsData.value) {
    const fields = [
      { key: "total_revenue", name: "Total Revenue" },
      { key: "normalized_ebitda", name: "Normalized EBITDA" },
      { key: "stockholders_equity", name: "Stockholders Equity" },
      { key: "free_cash_flow", name: "Free Cash Flow" },
      { key: "capital_expenditures", name: "Capital Expenditure" },
      { key: "total_assets", name: "Total Assets" },
      { key: "total_liabilities", name: "Total Liabilities" },
      { key: "gross_profit", name: "Gross Profit" },
      { key: "net_income_loss", name: "Net Income/Loss" },
      { key: "net_debt", name: "Net Debt" },
      { key: "enterprise_value", name: "Enterprise Value" },
      { key: "ebitda_margin", name: "EBITDA Margin" },
      { key: "net_debt_to_ebitda", name: "Net Debt to EBITDA" },
      { key: "roa", name: "ROA" },
      { key: "roe", name: "ROE" },
      { key: "debt_to_equity", name: "Debt to Equity" },
      { key: "operating_margin", name: "Operating Margin" },
      { key: "cash_from_operations", name: "Cash from Operations" },
      { key: "change_in_working_capital", name: "Change in Working Capital" },
    ];

    return fields.map((field) => {
      return {
        name: field.name,
        values: financialsData.value.map((financial) => {
          const value = financial[field.key as keyof typeof financial];
          return value !== null ? value.toLocaleString() : "N/A";
        }),
      };
    });
  }
  return [];
});
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
