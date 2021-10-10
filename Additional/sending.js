const net = require("net"); // import net
const readline = require("readline").createInterface({
    input: process.stdin,
    output: process.stdout
}); // this will be important later

const options = {
    port: 65432,
    host: 'localhost',
};

let client = net.connect(options, () => {
    console.log("connected!");
    client.write('test');
});