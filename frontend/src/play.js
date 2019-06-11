const axios = require('axios');


const GenerateAPI = "http://localhost:8003/api/generate/";

axios.get(GenerateAPI).then((response) => {
    console.log(response.data);
});