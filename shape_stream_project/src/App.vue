<template>
  <div class="container">
  <div class="header">
    <div class=title> Sync the DB</div>
    <div class="buttons">
    <button @click="addDataInTable">AddDataInTable</button>
    <button @click="displayData">Refresh Local DB</button>
  </div>
  <div> No of Rows: {{ tableData?.length }}</div>
  <div> Time using sync: {{diff1 }} </div>
  <div> Time using API: {{ diff2}} </div>
  </div>

  <table height="300px">
    <thead>
      <tr>
        <th class="text-left">
          ID
        </th>
        <th class="text-left">
           Movie Name
        </th>
        <th class="text-left">
           Show Type
        </th>
        <th class="text-left">
           Description
        </th>
        <th class="text-left">
           Description
        </th>
        <th class="text-left">
           Description
        </th>
        <th class="text-left">
           Description
        </th>
        <th class="text-left">
           Description
        </th>
        <th class="text-left">
           Description
        </th>
        <th class="text-left">
           Description
        </th>
        <th class="text-left">
           Description
        </th>
        <th class="text-left">
           Description
        </th>
        <th class="text-left">
           Description
        </th>
       
      </tr>
    </thead>
    <tbody>
      <tr v-for="(item, index) in tableData" :key="index"  >
        <td>{{ item[1]?.id}}</td>
        <td>{{ item[1]?.name }}</td>
        <td>{{ item[1]?.type }}</td>
        <td>{{ item[1]?.description_1 }}</td>
        <td>{{ item[1]?.description_2 }}</td>
        <td>{{ item[1]?.description_3 }}</td>
        <td>{{ item[1]?.description_4 }}</td>
        <td>{{ item[1]?.description_5 }}</td>
        <td>{{ item[1]?.description_6 }}</td>
        <td>{{ item[1]?.description_7 }}</td>
        <td>{{ item[1]?.description_8 }}</td>
        <td>{{ item[1]?.description_9 }}</td>
        <td>{{ item[1]?.description_10 }}</td>
      </tr>
    </tbody>
  </table>
</div>
</template>

<script setup>
import { computed, onMounted, ref, watch } from "vue";
import { ShapeStream, Shape } from "@electric-sql/client";



let pg
const tableData = ref("")
const endReceivedFromAPI = ref(new Date().getTime());
const startTime = ref(new Date().getTime());
const endReciveFromSubscribe = ref(new Date().getTime());

  const diff1 = ref(0)
  const diff2 = ref(0)

onMounted( async() => {
  const stream = new ShapeStream({
    url: `http://localhost:3000/v1/shape/movies`,
  })
  const shape = new Shape(stream)
  startTime.value = new Date().getTime();
  shape.subscribe(async shapeData => {
    // shapeData is a Map of the latest value of each row in a shape.
    endReciveFromSubscribe.value = new Date().getTime();
    diff1.value = endReciveFromSubscribe.value - startTime.value;
    console.log("SYNC time = ", endReciveFromSubscribe.value - startTime.value)
    tableData.value = Array.from(shapeData.entries() ).map( (el)=> {
      return [...el]
    })   
  })
  getDataFromTable();

})

const addDataInTable = () => {
  startTime.value = new Date().getTime();
  console.log("startDate = ", startTime.value);
  fetch('http://127.0.0.1:5000/test').then( () =>{
    console.log ("about 5k data added to the remote table")
    getDataFromTable()
  })
}

const getDataFromTable = () => {
  fetch('http://127.0.0.1:5000/getData').then( (data) => {
      endReceivedFromAPI.value = new Date().getTime();
      diff2.value = endReceivedFromAPI.value - startTime.value;
      console.log( "API time = ", endReceivedFromAPI.value - startTime.value)
    })
}

</script>

<style>
body {
  background-color: #080840;
}

table,
th,
td {
  border: 1px solid black;
  background-color: white;
}

.container {
  display: flex;
  justify-content: space-evenly;
  flex-direction: column;
  width: 100vw;
}

.header {
  display: flex;
  flex-direction: column;
  width: 50%;
  align-items: center;
  margin: 30px auto;
  color: white;
  font-size: large;
  justify-content: space-evenly;
  height: 200px;
}
.buttons {
  display: flex;
  justify-content: space-between;
  width: 50vw;
}
</style>