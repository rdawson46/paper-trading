// let stock;

// addEventListener("DOMContentLoaded", ()=>{
//     const socket = io();

//     socket.on('connect', ()=>{
//         console.log('connected to socket');
    
//     });
    

//     // setup

//     let buttons = document.querySelectorAll('button')

//     buttons.forEach(element => {
//         let text = element.innerText;

//         if(text == 'Buy' && element.dataset.stock){
//             element.addEventListener('click', (event)=>{
//                 let stock = event.target.dataset.stock;
                
//                 socket.emit('price', {'stock': stock, 'method': 'buy'});
//             });
//         }
        
//         else if(text == 'Sell' && element.dataset.stock){
//             element.addEventListener('click', (event)=> {
//                 // emit for selling
//                 let stock = event.target.dataset.stock;

//                 socket.emit('price', {'stock':stock, 'method': 'sell'})
//             });
//         }
//     });

//     let cancel_button = document.querySelectorAll('.cancel-button');

//     cancel_button.forEach(element => {
//         element.addEventListener('click', (event=>{
//             if(document.getElementById('buy').open){
//                 document.getElementById('buy').close();
//             }
//             else{
//                 document.getElementById('sell').close();
//             }
//         }))
//     });

//     let buy_button = document.querySelectorAll('.buy-button');

//     buy_button.forEach(element=>{
//         element.addEventListener('click', event=>{
//             console.log('buy')
            
//             // need stock and amount of money
//             // get money from input and stock from ?
//             let amount = document.getElementById('buy-amount').value;
//             document.getElementById('buy-amount').value = '';

//             amount = parseFloat(amount)

//             if(!isNaN(amount)){
//                 console.log(`amount: ${amount}`)
//                 console.log(`stock: ${stock}`)

//                 socket.emit('buy', {'stock': stock, 'amount': amount})
//             }
            
//         });
//     });

//     let sell_button = document.querySelectorAll('.sell-button');

//     sell_button.forEach(element=>{
//         element.addEventListener('click', event=>{
//             console.log('sell')
            
//             // find a way to get data to emit
//             // need stock and # of shares
//             // get share # from input and stock from ?
//             let amount = document.getElementById('sell-amount').value;
//             document.getElementById('sell-amount').value = ''

//             if(!isNaN(amount)){
//                 socket.emit('sell', {'stock': stock, 'shares': amount})
//             }
//         });
//     });
    

//     // socket functions

//     socket.on('priceReturn', (data)=>{
//         // add pop up window for dollar amount
//         let value = data.value;
//         let method = data.method;
//         stock = data.stock;

//         if(method == 'buy'){
//             document.getElementById('buy-text').innerText = `Buy ${stock} for ${value} per share`
    
//             document.getElementById('buy').showModal();
//         }

//         else{
//             document.getElementById('sell-text').innerText = `Sell ${stock} for ${value} per share`
    
//             document.getElementById('sell').showModal();
//         }
//     });

//     socket.on('returnBuy', (data)=>{
//         let shares = data.shares;
//         let sharePrice = data.sharePrice;

//         document.getElementById('buy').close()

//         document.getElementById('resultWindow').showModal();
//         document.getElementById('resultText').innerHTML = `<b>Shares: </b>${shares}<br><b>Price: </b>${sharePrice}`;

//     })

//     socket.on('returnSell', (data)=>{
//         let amount = data.amount;
//         let sharePrice = data.sharePrice;

//         console.log(`Amount: ${amount}`)
//         console.log(`SharePrice: ${sharePrice}`)
//     })
// });

let stock;

const socket = io();

socket.on('connect', ()=>{
    console.log('connected to socket');
});


function buyInfoButtonFunc(event){
    let stock = event.target.dataset.stock;

    socket.emit('price', {'stock':stock, 'method': 'buy'});
}

function sellInfoButtonFunc(event){
    let stock = event.target.dataset.stock;

    socket.emit('price', {'stock':stock, 'method': 'sell'});
}

function cancelButtonFunc(event){
    document.getElementById('buy').open ? document.getElementById('buy').close() : document.getElementById('sell').close();
}

function buyButtonFunc(event){
    let amount = document.getElementById('buy-amount').ariaValueMax;
    document.getElementById('buy-amount').value = '';

    amount = parseFloat(amount)

    if(!isNaN(amount)){
        console.log('BUY')

        socket.emit('buy', {'stock': stock, 'amount': amount})
    }
}

function sellButtonFunc(event){
    let amount = document.getElementById('sell-amount').value;
    document.getElementById('sell-amount').value = '';
    
    if(!isNaN(amount)){
        console.log('SELL');
        
        socket.emit('sell', {'stock': stock, 'shares': amount})
    }
}

// socket methods

socket.on('priceReturn', (data)=>{
    let value = data.value;
    let method = data.method;
    stock = data.stock;

    if(method == 'buy'){
        document.getElementById('buy-text').innerText = `Buy ${stock} for ${value} per share`;

        document.getElementById('buy').showModal();
    }
    else{
        document.getElementById('sell-text').innerText = `Sell ${stock} for ${value} per share`;

        document.getElementById('sell').showModal();
    }
});

socket.on('returnBuy', (data)=>{
    let shares = data.shares;
    let sharePrice = data.sharePrice;

    document.getElementById('buy').close()

    document.getElementById('resultWindow').showModal();
    document.getElementById('resultText').innerHTML = `<b>Shares: </b>${shares}<br><b>Price: </b>${sharePrice}`;
});

socket.on('returnSell', (data)=>{
         let amount = data.amount;
         let sharePrice = data.sharePrice;

         console.log(`Amount: ${amount}`)
         console.log(`SharePrice: ${sharePrice}`)
});

const buyInfo = document.querySelectorAll('.buy-info');
const sellInfo = document.querySelectorAll('.sell-info');
const cancel_button = document.querySelectorAll('.cancel-button');
const buy_button = document.querySelectorAll('.buy-button');
const sell_button = document.querySelectorAll('.sell-button');

buyInfo.forEach(button =>{
    button.onclick = buyInfoButtonFunc;
});

sellInfo.forEach(button =>{
    button.onclick = sellInfoButtonFunc;
});

cancel_button.forEach(button =>{
    button.onclick = cancelButtonFunc;
});

buy_button.forEach(button =>{
    button.onclick = buyButtonFunc;
});

sell_button.forEach(button =>{
    button.onclick = sellButtonFunc;
});
