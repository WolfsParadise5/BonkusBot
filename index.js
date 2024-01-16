const express = require('express'); 
  
const app = express(); 
const PORT = 3000;

app.listen(PORT, (error) => {
    if (!error)
        console.log("Server is running successfully on port " + PORT)
    else
        console.log("Server is unable to run, is the port in use?")
})