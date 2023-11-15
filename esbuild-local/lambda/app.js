const axios = require("axios");
const faker = require("@faker-js/faker");
const localDep = require("localDep");

exports.lambdaHandler = async () => {
    const response = await axios("https://api.ipify.org");
    const firstName = faker.faker.name.firstName();

    return {
        "hello": "world",
        "ip": response.data,
        "name": firstName,
        "localdep": localDep.localDepVariable
    };
};