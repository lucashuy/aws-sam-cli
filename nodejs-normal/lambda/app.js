const axios = require("axios");
const faker = require("@faker-js/faker");

exports.lambdaHandler = async () => {
    const firstName = faker.faker.person.firstName();

    return {
        "hello": "world",
        "name": firstName
    };
};