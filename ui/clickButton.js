$(window).on("load", function() {
    document.addEventListener('click', (event)=> {
        if      (event.target.id == 'searchbtn') sendData();
        else if (event.target.id == 'viewbtn') changeView('submit');
        else if (event.target.id == 'backbtn') changeView('search');
        else if (event.target.id == 'sendcode') sendCode();
    });
});