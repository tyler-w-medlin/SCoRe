function sendData(){
    var XHR = new XMLHttpRequest({mozSystem: true});
    var data = { "search" : document.getElementById("searchbar").value };
    var results = document.getElementById("results");
    var searchResults;
    var displayString = "";
    var resultNum;
    var theNode;

    XHR.addEventListener('load', (event)=> {
        console.log("Data sent and response loaded");
    });

    XHR.addEventListener('error', (event)=> {
        alert('Search not sent. Something went wrong.')
    })

    XHR.onreadystatechange = ()=> {
        if(XHR.readyState == 4){
            console.log(XHR.response);
            searchResults = JSON.parse(XHR.response);
            //console.log(searchResults);
            resultNum = 0;
            for (var property in searchResults) {
                if(searchResults.hasOwnProperty(property)) {
                    displayString = displayString + "Result Number: " + resultNum + "\n";
                    displayString = displayString + searchResults[property]["keywords"] + "\n";
                    displayString = displayString + searchResults[property]['raw_code'] + "\n";
                    displayString = displayString + "--------------------------------------------------\n";
                    resultNum++;
                }
            }
            theNode = document.createTextNode(displayString);
            results.appendChild(theNode);
        }
    }

    //console.log(data);

    XHR.open('POST', 'http://localhost:5000/search');

    XHR.setRequestHeader('Content-Type', 'application/json');

    XHR.send(JSON.stringify(data));

    //results.addEventListener("")
}