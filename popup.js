window.onload = function() {
var lastUpdateTime;
var feed;

chrome.extension.getBackgroundPage().console.log("test1");
chrome.storage.sync.get("lastUpdate", function(data){
    chrome.extension.getBackgroundPage().console.log("test 1.5: ", data['lastUpdate']);

    if(chrome.runtime.lastError || data == undefined || typeof data['lastUpdate'] != "number"){
        chrome.extension.getBackgroundPage().console.log("test2");
        var setvar = Date.now()/1000 - 361;
        chrome.storage.sync.set({'lastUpdate': setvar}, function(){
            console.log("type: ", typeof data);
            if(lastUpdateTime <= Date.now()/1000 - 3*60){
                chrome.extension.getBackgroundPage().console.log("entered");
                var xhr = new XMLHttpRequest();
                var url =  "https://news-alert-scraper.herokuapp.com/feed";
                var params = JSON.stringify({'sites': ['reddit', 'cbc', 'globe-and-mail-canada'], 'keywords': [], 'urgency': 0});

                xhr.open("POST", url, true);
                xhr.setRequestHeader("Content-type", "application/json");

                xhr.onload = function (e) {
                    if(xhr.readyState === 4){
                        if (xhr.status === 200){
                            feed = JSON.parse(xhr.responseText);
                            chrome.extension.getBackgroundPage().console.log(feed);
                            chrome.storage.sync.set({'feed': feed});
                            chrome.storage.sync.set({'lastUpdate': Date.now()/1000});

                            displayFeed(feed['feed']['feed']);

                            chrome.storage.sync.get('lastUpdate', function(data){console.log("last: ", data);})
                            chrome.storage.sync.get('feed', function(data){console.log("feed: ", data);})
                        } 
                    }
                };
                xhr.onerror = function (e) {
                  console.error(xhr.statusText);
                };
                xhr.send(params);
            }

        });
        lastUpdateTime = setvar;
    } else {
        chrome.extension.getBackgroundPage().console.log("test 3:", data);
        lastUpdateTime = data['lastUpdate'];
        chrome.extension.getBackgroundPage().console.log("data: ", data);

        chrome.extension.getBackgroundPage().console.log("before display");
        chrome.storage.sync.get('feed', function(data){
            feed = data['feed']['feed']
            chrome.extension.getBackgroundPage().console.log("just before display: ", feed);
            displayFeed(feed)
        });
        console.log("type: ", typeof data);
        if(lastUpdateTime <= Date.now()/1000 - 3*60){
            chrome.extension.getBackgroundPage().console.log("entered2");
            var xhr = new XMLHttpRequest();
            var url = "https://news-alert-scraper.herokuapp.com/feed";
            var params = JSON.stringify({'sites': ['reddit', 'cbc', 'globe-and-mail-canada'], 'keywords': [], 'urgency': 0});

            xhr.open("POST", url, true);
            xhr.setRequestHeader("Content-type", "application/json");

            console.log("1");
            xhr.onload = function (e) {
                console.log("2");
                console.log("readstage: ", xhr.readyState);
                if(xhr.readyState === 4){
                    console.log("3");
                    if (xhr.status === 200){

                        feed = JSON.parse(xhr.responseText);
                        chrome.extension.getBackgroundPage().console.log(feed);
                        chrome.storage.sync.set({'feed': feed});
                        chrome.storage.sync.set({'lastUpdate': Date.now()/1000});

                        console.log("ACUTAL FEED: ", feed);
                        displayFeed(feed['feed']['feed']);

                        chrome.storage.sync.get('lastUpdate', function(data){console.log("last: ", data);})
                        chrome.storage.sync.get('feed', function(data){console.log("feed: ", data);})
                    } 
                }
            };
            xhr.onerror = function (e) {
              console.error(xhr.statusText);
            };
            xhr.send(params);
        }

        
    }
});

function displayFeed(feed){
    if(feed != undefined && feed != null){
        chrome.extension.getBackgroundPage().console.log("DISPLAYING!");
        document.getElementById('container').innerHTML = "";
        
        var i;
        chrome.extension.getBackgroundPage().console.log(feed);
        for(i=0; i<feed.length; i++){
            chrome.extension.getBackgroundPage().console.log(feed[i]);
            chrome.extension.getBackgroundPage().console.log(feed[i].title);
            document.getElementById('container').innerHTML += "<a class='articleLink' target=\"_blank\" style='display:block;' href='" + feed[i].url + "'><div class='story' id='article" +(i.toString()) +"' >" +
            "<h3 class='articleTitle'>" + feed[i].title + "</h3>" +
            "<span class='articleInfo'> Posted: "+ new Date(feed[i].time).toLocaleString() + "</span>"+
            "<span class='articleInfo' style='float: right'>"+ feed[i].source +"</span>"+
            "</div></a>"
            console.log(feed[i].url);
            document.getElementById("article"+(i.toString())).addEventListener('click', function(){
                console.log("CLICK");
            });
            if(i != feed.length-1){
                document.getElementById('container').innerHTML += "<hr>"
            }
        }   
        
    }
}
}

