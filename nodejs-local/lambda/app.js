const axios = require("axios");
const faker = require("@faker-js/faker");
const localDep = require("local-dep");

exports.lambdaHandler = async () => {
    const response = await axios("https://api.ipify.org");
    const firstName = faker.faker.person.firstName();

    return {
        "hello": "world",
        "name": firstName,
        "ip": response.data,
        "local": localDep.localDepVariable
    };
};