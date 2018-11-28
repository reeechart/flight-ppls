const axios = require('axios')
const http = require('http');
const uuidv4 = require('uuid/v4');
const EasySoap = require('easysoap');
const { Client, logger, Variables } = require('camunda-external-task-client-js');
const parseString = require('xml2js').parseString;

const config = { baseUrl: 'http://localhost:8080/engine-rest', use: logger };

const params = {
  host: '167.205.35.211:8080',
  path: '/easypay/PaymentService',
  wsdl: '/easypay/PaymentService?wsdl',
 }

const hotelParams = {
  host: '167.205.35.216:8081',
  path: '/',
  wsdl: '/?wsdl'
}

/*
* create the client
*/
const soapClient = new EasySoap(params)
const hotelSoapClient = new EasySoap(hotelParams)
 
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
  const eventId = task.variables.get('event_id');
  
  let passengers = task.variables.get('passengers');
  if(typeof(passengers) == 'string') {
    passengers = jsonParser(passengers)
  }
  const processVariables = new Variables();
  processVariables.set('passengers', passengers)
  const bookingNumber = task.id;
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

  processVariables.set('event_id', eventId);
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
  const processVariables = new Variables();
  try {
    let response = await soapClient.call({
      method    : 'beginPayment',
      params: {
        paymentMethodId: 'bank',
        amount: task.variables.get('totalPrice')
      }
    })
    
    processVariables.set('paymentId',response.data.return);

  } catch(error) {
    console.log(error)

  }
  await taskService.complete(task, processVariables);
});


client.subscribe('book-check-payment-status', async function({ task, taskService }) {
  const processVariables = new Variables();
  const paymentId = task.variables.get('paymentId');
  console.log(paymentId);
  try {
    var status = ''
    soapClient.call({
      method: 'getPaymentEvents',
      params: {
        paymentId: paymentId,
      }
    }).then((res) => {
        let data = res.response.body;
        let tIndex = data.search('type="');
        data = data.substring(tIndex)
        data = data.substring(data.search("\""));
        data = data.substring(1);
        // console.log(data)
        data = data.substring(0,data.search("\""));
        status = data;
      }).catch((err) => {
      console.log(err)
    })  
    let  response = status === 'SUCCESS';
    console.log("Payment valid? "+ response);
    processVariables.set('paid', response)

  } catch(error) {
    console.log(error)

  }
  await taskService.complete(task, processVariables);
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

client.subscribe('book-book-event', async function({task, taskService}) {
  const eventId = task.variables.get('event_id');
  const username = task.variables.get('username');
  let userId = 0;

  if (eventId != null) {
    try {
      await axios.get(BASE_URL+'users/'+username+'/');
      userId = response.data.id;
    } catch(error) {
      console.log(error);
    }

    try {
      hotelSoapClient.call({
        method: 'bookTicket',
        params: {
          eventId: eventId,
          userId: userId,
          sectionsId: '[1]'
        }
      })
    } catch(error) {
      console.log(error);
    }
  }
});

client.subscribe('cancel-cancel-booking', async function({ task, taskService }) {
  const bookingNumber = task.variables.get('booking_number');
  const processVariables = new Variables();

  try {
    console.log(bookingNumber)
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
    console.log(error);
  }
  await taskService.complete(task, processVariables);
});

client.subscribe('reschedule-get-credentials', async function({ task, taskService}) {
  const bookingNumber = task.variables.get('booking_number');
  const newFlightNumber = task.variables.get('flight_number');
  const processVariables = new Variables();

  try {
    let response = await axios.get(BASE_URL+'bookings/'+bookingNumber+'/');
    passengers = response.data.passengers
    username = response.data.user
    processVariables.set('passengers', passengers);
    processVariables.set('username', username);
  } catch(error) {
    console.log(error);
  }
  await taskService.complete(task, processVariables);
});
