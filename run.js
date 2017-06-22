var system = require('system');
var page = require('webpage').create();
var url = system.args[1];
var timeout = 4000;


page.onNavigationRequested = function(url, type, willNavigate, main) {
    //console.log("[URL] URL="+url);
};

page.settings.resourceTimeout = timeout;

page.onResourceTimeout = function(e) {
    setTimeout(function(){
     //   console.log("[INFO] Timeout")
        phantom.exit();
    }, 1);
};

page.open(url, function(status) {
    ///console.log("[INFO] rendered page");
//console.log(page.content);
    setTimeout(function(){
        phantom.exit();
    }, 1);
});

