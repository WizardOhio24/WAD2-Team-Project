document.addEventListener("DOMContentLoaded", navButton);

function navButton(){
    navigationButtons = document.getElementsByClassName("navButton");

    curURL = document.URL; //window.location.href is the same thing

    for(var i = 0;i<navigationButtons.length;i++){

        if(navigationButtons[i].href == curURL){
          // Then we mush be on that page, so add 'current' class to the nav button
          navigationButtons[0].className="navButton";
          navigationButtons[i].className = "navButton Current";
          
        }
    }
}
