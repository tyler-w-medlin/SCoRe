var path = 'http://localhost:5000/';

function sendCode(){
    var XHR = new XMLHttpRequest({mozSystem: true});
    var textBox = { "code" : document.getElementById("rawcode").value };
    //var fileInput = document.getElementById("selectfile").files[0];
    var docString = document.getElementById("docstring").value;
    let raw_code = new Object();
    var formData = new FormData();

    console.log(textBox.code);
    console.log(docString);
    console.log(fileInput);
    if (textBox.code !== "" && docString !== ""){
        raw_code["code"] = textBox.code;
        raw_code["docstring"] = docString;
        console.log(raw_code);
    } else if (textBox.code !== "") {
        raw_code = textBox;
        console.log(raw_code);
    }
    // } else if (fileInput.files !== null) {
        
    //     const reader = new FileReader()
    //     reader.readAsText(fileInput);
    //     reader.onload = ()=>{
    //         formData.append("code", new fileInput(reader.result, fileInput));
    //     }
    //     // formData.append("code", new File(fileInput));
    // }

    XHR.addEventListener('load', (event)=> {
        console.log("Code sent and response loaded");
    });

    XHR.addEventListener('error', (event)=> {
        alert('Code not sent. Something went wrong.')
    })

    XHR.onreadystatechange = ()=> {
        if(XHR.readyState == 4){
            console.log('Code submitted successfully.');
        }
    }

    XHR.open('POST', path + "addCode");

    //XHR.setRequestHeader('Content-Type', 'multipart/form-data');
    XHR.setRequestHeader('Content-Type', 'application/json');

    XHR.send(JSON.stringify(raw_code));
    //XHR.send(formData);

    //results.addEventListener("")
}

// function FileUpload(img, file) {
//     const reader = new FileReader();  
//     //this.ctrl = createThrobber(img);
//     const xhr = new XMLHttpRequest();
//     this.xhr = xhr;
    
//     const self = this;
//     this.xhr.upload.addEventListener("progress", function(e) {
//           if (e.lengthComputable) {
//             const percentage = Math.round((e.loaded * 100) / e.total);
//             //self.ctrl.update(percentage);
//           }
//         }, false);
    
//     xhr.upload.addEventListener("load", function(e){
//             //self.ctrl.update(100);
//             //const canvas = self.ctrl.ctx.canvas;
//             canvas.parentNode.removeChild(canvas);
//         }, false);
//     xhr.open("POST", path);
//     xhr.overrideMimeType('text/plain; charset=x-user-defined-binary');
//     reader.onload = function(evt) {
//       xhr.send(evt.target.result);
//     };
//     reader.readAsBinaryString(file);
// }