$(document).ready(function(){
    console.log('this is working');

    const socket = io();

    socket.on('connect', ()=>{
        console.log('Connected to socket');
    });

    document.querySelectorAll('#delete-button').forEach(element => {
        element.addEventListener('click', (event)=>{
            const user = event.currentTarget.dataset.user;
            const email = event.currentTarget.dataset.email

            socket.emit('delete', {'user':user, 'email':email}, (res)=>{
                console.log(res);
                location.reload();
            });
        });
    });
});