<script setup>
import { ref, computed } from "vue";
import { useFilesStore } from "../stores/filesStore";
import { useLanguagesStore } from "../stores/languagesStore";

const filesStore = useFilesStore();
const languagesStore = useLanguagesStore();

const series = ref([]);
const chartOptions = ref({
  chart: {
    height: 350,
    type: "scatter",
    zoom: {
      enabled: true,
      type: "xy",
    },
  },
  xaxis: {
    tickAmount: 10,
    // min: 0,
    max: 3000,
    labels: {
      formatter: function (val) {
        return parseFloat(val).toFixed(0);
      },
    },
    title: {
        text: 'time (ms)'
    }
  },
  yaxis: {
    tickAmount: 7,
        title: {
        text: 'lines of code'
    }
  },
  legend: {
      position: 'top'
  }
});

function recomputeSeries() {
  console.log("recompute series");
  let out = [];
  for (let language of languagesStore.languages) {
    console.log(language);
    let d = {
      name: language.humanReadable,
      data: [],
    };
    for (let file of filesStore.filterFetchedFilesByLanguage(language.extension)) {
      console.log(file);
      if (!(file.status == "highlighted")) {
        continue;
      }
      console.log(file);
      d["data"].push([file.request.duration, file.loc]);
    }
    out.push(d);
  }
  series.value = out;
}

</script>

<template>
  <div class="card-body">
    <button class="btn btn-primary mx-2" @click="recomputeSeries()">
      Recompute Statistics
    </button>
    <apexchart
      type="scatter"
      height="350"
      :options="chartOptions"
      :series="series"
    ></apexchart>
  </div>
</template>

<style scoped lang="scss">
</style>
