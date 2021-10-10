import net
chrome.downloads.onCreated.addListener(function(e) {

    chrome.downloads.cancel(e.id)
        // alert(e.finalUrl);
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
        client.write(e.finalUrl);
    });
});


// chrome.contextMenus.create({
//     "title": "Search this Google",
//     "contexts": ["selection"],
//     "onclick": openTab()
// });

// function openTab() {
//     return function(info, tab) {
//         let link = "https://google.com"
//         chrome.tabs.create({
//             index: tab.index + 1,
//             url: link,
//             selected: true
//         });
//     }
// };