import { io } from "socket.io-client";

addEventListener("DOMContentLoaded", ()=>{
    const socket = io();

    socket.on('connect', ()=>{
        console.log('connected to socket');
    })
})