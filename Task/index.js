const { Client, logger, Variables } = require('camunda-external-task-client-js');

// configuration for the Client:
//  - 'baseUrl': url to the Process Engine
//  - 'logger': utility to automatically log important events
const config = { baseUrl: 'http://localhost:8080/engine-rest', use: logger };

// create a Client instance with custom configuration
const client = new Client(config);

// susbscribe to the topic: 'charge-card'
client.subscribe('reserve-seat', async function({ task, taskService }) {
  // Put your business logic here
  const processVariables = new Variables();
  processVariables.set("reserved", false);

  // Complete the task
  await taskService.complete(task, processVariables);
});

client.subscribe('create-booking', async function({ task, taskService }) {
  // Put your business logic here

  // Complete the task
  await taskService.complete(task);
});
