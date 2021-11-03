chrome.downloads.onCreated.addListener(function(downloadItem) {
    manageDownload(downloadItem.finalUrl, downloadItem.id)
});

function manageDownload(finalUrl, id) {
    chrome.downloads.cancel(id)

    sendFinalUrl(finalUrl)

    alert(finalUrl)
}

function sendFinalUrl(finalUrl) {
    var req = new XMLHttpRequest();
    req.open("POST", "http://localhost:65432", true);
    req.send(finalUrl);
}

// chrome.downloads.onCreated.addListener(function(downloadItem) {
//     var postUrl = "http://localhost:65432";

//     chrome.downloads.cancel(downloadItem.id)
//     req = new XMLHttpRequest();
//     req.open("POST", postUrl, true);
//     req.send(downloadItem.finalUrl);

//     alert("The download link is: " + downloadItem.finalUrl)
//     console.log(downloadItem.finalUrl)

// })

// const options = {
//     port: 65432,
//     host: 'localhost',
// };

// let client = net.connect(options, () => {
//     console.log("connected!");
//     client.write(e.finalUrl);
// });
// });


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
// };      });
//     }
// };