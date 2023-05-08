addEventListener("DOMContentLoaded", ()=>{
    const socket = io();

    socket.on('connect', ()=>{
        console.log('connected to socket');
    })
})