function sendData(){
    var XHR = new XMLHttpRequest({mozSystem: true});
    var data = { "search" : document.getElementById("searchbar").value };
    var results = document.getElementById("results");
    var searchResults;
    var displayString = "";
    var resultNum;
    var theNode;
    var resultsList;

    while (results.firstChild){
        results.removeChild(results.firstChild);
    }

    XHR.addEventListener('load', (event)=> {
        console.log("Data sent and response loaded");
    });

    XHR.addEventListener('error', (event)=> {
        alert('Search not sent. Something went wrong.')
    })

    XHR.onreadystatechange = ()=> {
        if(XHR.readyState == 4){
            //console.log(XHR.response);
            searchResults = JSON.parse(XHR.response);
            //console.log(searchResults);
            resultNum = 0;
            resultsList = new Array();
            var i = 0;
            for (var property in searchResults) {
                resultsList.push(searchResults[property]);
                resultsList[i].keywords = resultsList[i].keywords.split(" ");
                i++;
            }

            //sorts by number of keywords
            resultsList.sort((a, b)=>{
                return b.relevancy - a.relevancy;
            })


            resultsList.forEach(result => {
                displayString = displayString + "Result Number: " + resultNum + "\n"; //resultnumber
                displayString = displayString + "Keywords: ";
                result.keywords.forEach(keyword =>{
                    displayString +=  keyword + " "; //keyword
                })
                displayString = displayString + "\nCode:\n";
                displayString = displayString + "--------------------------------------------------\n";
                displayString = displayString + result.raw_code + "\n"; //raw_code
                displayString = displayString + "--------------------------------------------------\n";
                displayString = displayString + "--------------------------------------------------\n";
                resultNum++;
            });

            theNode = document.createTextNode(displayString);
            results.appendChild(theNode);
        }
    }

    //console.log(data);

    XHR.open('POST', 'http://10.13.1.207:5000/search');

    XHR.setRequestHeader('Content-Type', 'application/json');

    XHR.send(JSON.stringify(data));

    //results.addEventListener("")
}