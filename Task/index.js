const axios = require('axios')
const http = require('http');
const uuidv4 = require('uuid/v4');

const { Client, logger, Variables } = require('camunda-external-task-client-js');


const config = { baseUrl: 'http://localhost:8080/engine-rest', use: logger };


const client = new Client(config);
const baseUrl = "http://localhost:8080/engine-rest" 
const BASE_URL = "http://localhost:8000/"

const jsonParser = data => {
  let result = []
  let idx = data.search('{')
  while( idx != -1) {
      let first_name_idx = data.search("first_name=")+"first_name=".length;
      let comma_idx = data.search(',');
      let first_name = data.substring(first_name_idx, comma_idx)
      data = data.substring(comma_idx+1)
      let closetag_idx = data.search('}')
      let last_name = data.substring(" last_name=".length, closetag_idx)
      result.push({
          first_name: first_name,
          last_name: last_name
      })
      data = data.substring(closetag_idx+2)
      idx = data.search("{")
  }
  return result
}

client.subscribe('book-create-booking', async function({ task, taskService }) {
  const flightNumber = task.variables.get('flight_number');
  const username = task.variables.get('username');
  const passengers = jsonParser(task.variables.get('passengers'));
  const processVariables = new Variables();
  processVariables.set('passengers', passengers)
  const bookingNumber = uuidv4();
  try {
    let response = await axios.get(BASE_URL+'flights/'+flightNumber+'/');
    let totalPrice = passengers.length * response.data.price;
    processVariables.set('totalPrice', totalPrice)
    response  = await axios.post(BASE_URL+'bookings/', {
      user: username,
      flight: flightNumber,
      passengers: passengers,
      number: bookingNumber,
      status: 'pending'
    });
    processVariables.set('booking_number', bookingNumber);
    processVariables.set('created', true);
  } catch(error) {
    console.log("Error!")
    console.log(error)
    processVariables.set('created', false);
  }
  await taskService.complete(task, processVariables);
});

client.subscribe('book-create-invoice', async function({ task, taskService }) {
  const username = task.variables.get('username');
  const bookingNumber = task.variables.get('booking_number');
  const totalPrice = task.variables.get('totalPrice');
  try {
    let response = await axios.post(BASE_URL+'invoices/', {
      user: username,
      booking: bookingNumber,
      price: totalPrice
    });
  } catch(error) {
    
  }
  await taskService.complete(task);
});

client.subscribe('book-notify-payment-gateway', async function({ task, taskService }) {
  const paymentGateWayUrl = "http://localhost:8000/mock/payment"
  try {
    let response = await axios.post(paymentGateWayUrl, {
        callback_url: baseUrl+"/message/",
        callback_body: {
          messageName: "PaymentGateway",
          processInstanceId: task.id
        }
    });
    console.log(response.status)

  } catch(error) {
    console.log(error)

  }
  await taskService.complete(task);
});

client.subscribe('book-issue-ticket', async function({ task, taskService }) {
  const flightNumber = task.variables.get('flight_number');
  const username = task.variables.get('username');
  const passengers = task.variables.get('passengers');
  try {
    for(let i=0;i<passengers.length;i++) {
      await axios.post(BASE_URL+'tickets/', {
        flight: flightNumber,
        user: username,
        first_name: passengers[i].first_name,
        last_name: passengers[i].last_name
      })
    }
  } catch(error) {
  }
  await taskService.complete(task);
});

client.subscribe('book-finish-booking', async function({ task, taskService }) {
  const bookingNumber = task.variables.get('booking_number');
  try {
    await axios.patch(BASE_URL+'bookings/'+bookingNumber+'/', {
      status: 'paid'
    });
  } catch(error ){
    
  }
  await taskService.complete(task);
});

client.subscribe('cancel-cancel-booking', async function({ task, taskService }) {
  const bookingNumber = task.variables.get('booking_number');
  const processVariables = new Variables();

  try {
    let response = await axios.get(BASE_URL+'bookings/'+bookingNumber+'/');
    bookingDetail = response.data
    if (bookingDetail.status === 'paid') {
      processVariables.set('paid', true);
    } else {
      processVariables.set('paid', false);
    }
    await axios.patch(BASE_URL+'bookings/'+bookingNumber+'/', {
      status: 'canceled'
    });
  } catch(error) {
    console.log(error)
  }
  await taskService.complete(task, processVariables);
});
