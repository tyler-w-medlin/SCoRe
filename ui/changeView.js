function changeView(changeTo){
    let submit = document.getElementById("submitcode");
    let search = document.getElementById("searchcode");

    if (changeTo === 'submit'){
        showAndHideElements(submit, search);
    } else if(changeTo === 'search') {
        showAndHideElements(search, submit);
    }
}

function showAndHideElements(show, hide) {
    // TODO: Hide the element "hide" and show the element "show"
    show.classList.remove("hidden");
    hide.classList.add("hidden");
}