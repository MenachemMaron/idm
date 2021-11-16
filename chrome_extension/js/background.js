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