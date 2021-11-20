chrome.downloads.onCreated.addListener(function(downloadItem) {
    manageDownload(downloadItem.id, downloadItem.finalUrl, downloadItem.fileSize, downloadItem.startTime, downloadItem.totalBytes, downloadItem.url)
});

function manageDownload(id, finalUrl, fileSize, startTime, totalBytes, url) {
    chrome.downloads.cancel(id)

    sendDownloadInfo(id, finalUrl, fileSize, startTime, totalBytes, url)

    alert(finalUrl)
}

function sendDownloadInfo(id, finalUrl, fileSize, startTime, totalBytes, url) {
    var json = {
        'download_id': id,
        'final_url': finalUrl,
        'file_size': fileSize,
        'start_time': startTime,
        'total_bytes': totalBytes,
        'original_url': url,
    }
    var req = new XMLHttpRequest();
    req.open('POST', 'http://localhost:65432', true);
    req.setRequestHeader('Content-Type', 'application/json');
    req.send(JSON.stringify(json));
    alert(JSON.stringify(json))
}