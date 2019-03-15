function sendData(){
    var XHR = new XMLHttpRequest();
    var urlEncodedData = "";
    var urlEncodedDataPairs = [];
    var name;
    var data = document.getElementById("searchbar").value;

    /*for(name in data){
        urlEncodedDataPairs.push(encodeURIComponent(name) + "=" + encodeURIComponent(data[name]));
    }*/

    //urlEncodedData = urlEncodedDataPairs.join('&').replace(/%20/g, '+');

    XHR.addEventListener('load', (event)=> {
        console.log("Data sent and response loaded");
    });

    XHR.addEventListener('error', (event)=> {
        alert('Search not sent. Something went wrong.')
    })

    /*for(entry in urlEncodedData){
        console.log(entry);
    }*/

    console.log(data);

    //XHR.open('POST', 'https://ourdatabase.com');

    //XHR.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');

    //XHR.send(urlEncodedData);
}