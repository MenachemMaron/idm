(async() => {
    const src = chrome.extension.getURL('js/background.js');
    const contentScript = await
    import (src);
    contentScript.main( /* chrome: no need to pass it */ );
})();