<template>
  <div class="container">
  <div class="header">
    <div class=title> Sync the DB</div>
    <div class="buttons">
    <button @click="addDataInTable">AddDataInTable</button>
    <button @click="displayData">Refresh Local DB</button>
    <button @click="stopTheSync">Stop Sync</button>
    <button @click="getDataFromTable">Get Data API</button>
  </div>
  <div> No of Rows: {{ tableData[0]?.rows.length }}</div>
  <div> The values can be taken in consideration only on init</div>
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
      <tr v-for="(item, index) in tableData[0]?.rows" :key="index"  >
        <td>{{ item[1]?.id}}</td>
        <td>{{ item.name }}</td>
        <td>{{ item.type }}</td>
        <td>{{ item.description_1 }}</td>
        <td>{{ item.description_2 }}</td>
        <td>{{ item.description_3 }}</td>
        <td>{{ item.description_4 }}</td>
        <td>{{ item.description_5 }}</td>
        <td>{{ item.description_6 }}</td>
        <td>{{ item.description_7 }}</td>
        <td>{{ item.description_8 }}</td>
        <td>{{ item.description_9 }}</td>
        <td>{{ item.description_10 }}</td>
      </tr>
    </tbody>
  </table>
</div>
</template>

<script setup>
import { PGlite } from '@electric-sql/pglite';
import { electricSync } from '@electric-sql/pglite-sync';
import { live } from "@electric-sql/pglite/live"
import { onDeactivated, onMounted, ref } from "vue";
import { ShapeStream, Shape } from "@electric-sql/client";



let pg ,shapeSync
const tableData = ref("")
const endReceivedFromAPI = ref(new Date().getTime());
const startTime = ref(new Date().getTime());
const endReciveFromSubscribe = ref(new Date().getTime());

  const diff1 = ref(0)
  const diff2 = ref(0)

onMounted(async () => {
  pg = await PGlite.create({
    dataDir: 'idb://my-database',
    extensions: {
      live,
      electric: electricSync({
        //debug: true
      })
    }
  })

  //Create Local PGlite Table
  await pg.exec(`
  CREATE TABLE IF NOT EXISTS movies (
    id SERIAL PRIMARY KEY ,
    name TEXT,
    type TEXT,
    description_1 TEXT,
    description_2 TEXT,
    description_3 TEXT,
    description_4 TEXT,
    description_5 TEXT,
    description_6 TEXT,
    description_7 TEXT,
    description_8 TEXT,
    description_9 TEXT,
    description_10 TEXT,
    created_year TEXT
  );
`)
  startTime.value = new Date().getTime();
  //create the Sync from the Remote DB
   shapeSync = await pg.electric.syncShapeToTable({
    shape: {url: `http://localhost:3000/v1/shape/movies`}, // localhost:3000 is the electric server and 'movies'it is the remote pg table
    table: 'movies', // The name of your local table
    primaryKey: ['id'], // Primary key columns
    subscribe: true,
    plugins: "sync",
    shapeKey: 'movies'
  });

  shapeSync.subscribeOnceToUpToDate(() => {
    console.log("=== The shape caught up to the main Postgres === ")
    endReciveFromSubscribe.value = new Date().getTime();
    diff1.value = endReciveFromSubscribe.value - startTime.value;
    console.log("SYNC time = ", endReciveFromSubscribe.value - startTime.value)
    displayData();
  })

  /* 
    await pg.exec(`INSERT INTO movies (id, name, type, description_1, description_2, description_3, description_4, description_5, description_6, description_7, description_8, description_9, description_10, created_year ) VALUES 
    ( '999999999','name', 'type', 'desc', 'desc', 'desc', 'desc', 'desc', 'desc', 'desc', 'desc', 'desc', 'desc', '2021')`);
    */
})

const stopTheSync = () => {
    console.log("unsubscribe")
    shapeSync.unsubscribe();
  }

const displayData = async () => {
  tableData.value = await pg.exec(`Select * from movies`);
  console.log("Local DB Data =  ", tableData.value)
}

const addDataInTable = () => {
  fetch('http://127.0.0.1:5000/test').then( () =>{
    console.log ("about 5k data added to the remote table")
    displayData();
  })
}

const getDataFromTable = () => {
  startTime.value = new Date().getTime();
  fetch('http://127.0.0.1:5000/getData').then( () =>{ 
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