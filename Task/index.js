const axios = require('axios')
const http = require('http');
const uuidv4 = require('uuid/v4');

const { Client, logger, Variables } = require('camunda-external-task-client-js');


const config = { baseUrl: 'http://localhost:8080/engine-rest', use: logger };


const client = new Client(config);

const BASE_URL = "http://localhost:8000/"

client.subscribe('book-create-booking', async function({ task, taskService }) {
    const flight_number = task.variables.get('flight_number');
    const username = task.variables.get('username');
    const passengers = task.variables.get('passengers');
    const processVariables = new Variables();
    try {
      await axios.get(BASE_URL+'flights/'+flight_number+'/');
      let result = await axios.post(BASE_URL+'bookings/', {
        user: username,
        flight: flight_number,
        passengers: passengers,
        number: uuidv4(),
        status: 'pending'
      });
      processVariables.set('created', true);
    } catch(error) {
      processVariables.set('created', false);
    }
    await taskService.complete(task, processVariables);
});

// client.subscribe('book-create-invoice', async function({ task, taskService }) {
//   await taskService.complete(task);
// });

// client.subscribe('book-notify-payment-gateway', async function({ task, taskService }) {
//   await taskService.complete(task);
// });

// client.subscribe('book-cancel-booking', async function({ task, taskService }) {
//   await taskService.complete(task);
// });
  
  