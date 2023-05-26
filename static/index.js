addEventListener("DOMContentLoaded", ()=>{
    const socket = io();

    socket.on('connect', ()=>{
        console.log('connected to socket');

        let buttons = document.querySelectorAll('button')

        buttons.forEach(element => {
            let text = element.innerText;

            if(text == 'Buy'){
                element.addEventListener('click', (event)=>{
                    
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
    });
    
    socket.on('priceReturn', (data)=>{
        // add pop up window for dollar amount
        let value = data.value;

        console.log(value);
    });
});