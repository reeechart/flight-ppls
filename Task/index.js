const { Client, logger, Variables } = require('camunda-external-task-client-js');

// configuration for the Client:
//  - 'baseUrl': url to the Process Engine
//  - 'logger': utility to automatically log important events
const config = { baseUrl: 'http://localhost:8080/engine-rest', use: logger };

// create a Client instance with custom configuration
const client = new Client(config);

client.subscribe('book-create-booking', async function({ task, taskService }) {
    const processVariables = new Variables();
    processVariables.set('created', true);
    await taskService.complete(task, processVariables);
});

client.subscribe('book-create-invoice', async function({ task, taskService }) {
  await taskService.complete(task);
});

client.subscribe('book-notify-payment-gateway', async function({ task, taskService }) {
  await taskService.complete(task);
});

client.subscribe('book-cancel-booking', async function({ task, taskService }) {
  await taskService.complete(task);
});
  
  