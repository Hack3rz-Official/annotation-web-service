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
    min: 0,
    // max: 3000,
    labels: {
      formatter: function (val) {
        return parseFloat(val).toFixed(0);
      },
    },
    title: {
      text: "time (ms)",
    },
  },
  yaxis: {
    tickAmount: 7,
    title: {
      text: "lines of code",
    },
  },
  legend: {
    position: "top",
  },
});

function recomputeStatistics() {
    recomputeSeries()
    recomputeTableData()
}

function recomputeSeries() {
  //   console.log("recompute series");
  let out = [];
  for (let language of languagesStore.languages) {
    // console.log(language);
    let d = {
      name: language.humanReadable,
      data: [],
    };
    for (let file of filesStore.filterFetchedFilesByLanguage(
      language.extension
    )) {
      //   console.log(file);
      if (!(file.status == "highlighted")) {
        continue;
      }
      d["data"].push([file.request.duration, file.loc]);
    }
    out.push(d);
  }
  series.value = out;
}

const tableData = ref([]);

function recomputeTableData() {
  const out = [];
  // stats for each language
  for (let language of languagesStore.languages) {
    let files = filesStore.filterFetchedFilesByLanguage(language.extension);
    let highlightedFiles = files.filter((file) => { return file.status == 'highlighted' })
    let times = highlightedFiles.map((file) => { return file.request.duration })
    let avgTime = Math.round(times.reduce((partialSum, a) => partialSum + a, 0) / times.length);
    console.log(language)
    console.log(files)
    out.push({
      name: language.humanReadable,
      filesCount: files.length,
      filesHighlightedCount: highlightedFiles.length,
      avgTime: avgTime,
    });
  }
  // stats total (all files)
  let files = filesStore.files
  let highlightedFiles = files.filter((file) => { return file.status == 'highlighted' })
  let times = highlightedFiles.map((file) => { return file.request.duration })
  let avgTime = Math.round(times.reduce((partialSum, a) => partialSum + a, 0) / times.length);
  out.push({
      name: 'Total',
      filesCount: files.length,
      filesHighlightedCount: highlightedFiles.length,
      avgTime: avgTime,
  });
  tableData.value = out;
}
</script>

<template>
  <div class="card-body">
    <button class="btn btn-primary mx-2" @click="recomputeStatistics()">
      Recompute Statistics
    </button>
    <apexchart
      type="scatter"
      height="350"
      :options="chartOptions"
      :series="series"
    ></apexchart>

    <div class="overflow-x-auto">
      <table class="table w-full">
        <!-- head -->
        <thead>
          <tr>
            <th>Language</th>
            <th># Files</th>
            <th># Highlighted</th>
            <th>Avg Time (ms)</th>
          </tr>
        </thead>
        <tbody>
          <tr
            v-for="language of tableData"
            :key="language.name"
            class="last-of-type:font-bold"
          >
            <td>{{ language.name }}</td>
            <td>{{ language.filesCount }}</td>
            <td>{{ language.filesHighlightedCount }}</td>
            <td>{{ language.avgTime }}</td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<style scoped lang="scss">
</style>
