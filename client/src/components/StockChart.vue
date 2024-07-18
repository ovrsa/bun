<template>
  <div ref="chart"></div>
</template>

<script lang="ts">
import { defineComponent, onMounted, ref } from 'vue';
import * as d3 from 'd3';

export default defineComponent({
  name: 'BarChart',
  setup() {
    const chart = ref<HTMLElement | null>(null);

    onMounted(() => {
      if (chart.value) {
        const data = [30, 86, 168, 281, 303, 365];
        const width = 500;
        const height = 500;

        const svg = d3
          .select(chart.value)
          .append('svg')
          .attr('width', width)
          .attr('height', height);

        svg
          .selectAll('rect')
          .data(data)
          .enter()
          .append('rect')
          .attr('x', (d, i) => i * 40)
          .attr('y', (d) => height - d)
          .attr('width', 35)
          .attr('height', (d) => d)
          .attr('fill', 'blue');
      }
    });

    return { chart };
  },
});
</script>

<style scoped>
div {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100vh;
}
</style>
