const mongoose = require("mongoose")
mongoose.connect("mongodb+srv://firstTime:<password>@cluster0.wnym4e2.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")

.then(()=>{
    console.log("Mongodb connected")
})

.catch(()=>{
    console.log("Failed to connect")
})

const loginSchema = new mongoose.Schema({
    name: {
        type: String,
        required: true
    },

    password:{
        type: String,
        required: true
    }
})

