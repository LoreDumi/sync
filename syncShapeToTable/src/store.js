// src/store.js
import { reactive } from 'vue';
import electric from './components/pgLite.vue';

const state = reactive({
  data: [],
});

async function fetchData() {
  const result = await electric.query('SELECT * FROM your_table');
  state.data = result.rows; // Assuming result.rows contains your data
}

async function initDatabase() {
  await electric.execute(`
    CREATE TABLE IF NOT EXISTS your_table (
      id SERIAL PRIMARY KEY,
      name TEXT
    )
  `);
}

export { state, fetchData, initDatabase };
