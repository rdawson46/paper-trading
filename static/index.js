addEventListener("DOMContentLoaded", ()=>{
    const socket = io();
    
    let buttons = document.querySelectorAll('button')

    buttons.forEach(element => {
        let text = element.innerText;

        if(text == 'Buy'){
            element.addEventListener('click', (event)=>{
                console.log('clicked')
                let stock = event.target.dataset.stock
                
                socket.emit('price', {'stock': stock});
            });
        }
        
        else{
            element.addEventListener('click', ()=> {
                // emit for selling
            });
        }
    });
    
    socket.on('connect', ()=>{
        console.log('connected to socket');

    });
    
    socket.on('priceReturn', (data)=>{
        // add pop up window for dollar amount
        let value = data.value;

        console.log(value);
    });
});