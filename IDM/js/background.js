chrome.downloads.onCreated.addListener(function(e) {
        chrome.downloads.cancel(e.id)

        const req = new XMLHttpRequest();
        const postUrl = "http://localhost:65432";
        req.open("POST", postUrl, true);
        req.send(e.finalUrl);

        req.onreadystatechange = function() { // Call a function when the state changes.
            if (this.readyState === XMLHttpRequest.DONE && this.status === 200) {
                console.log("Got response 200!");
            }
        }
    })
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