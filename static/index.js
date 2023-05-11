"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
var socket_io_client_1 = require("socket.io-client");
addEventListener("DOMContentLoaded", function () {
    var socket = (0, socket_io_client_1.io)();
    socket.on('connect', function () {
        console.log('connected to socket');
    });
});
