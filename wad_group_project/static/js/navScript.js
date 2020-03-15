document.addEventListener("DOMContentLoaded", navButton);

function navButton(){
    navigationButtons = document.getElementsByClassName("navButton");
    
    for(var i = 0;i<navigationButtons.length;i++){
      
        navigationButtons[i].addEventListener("click", function(){  
            
            document.getElementsByClassName("navButton Current")[0].className="navButton";
            this.className = "navButton Current";
        
        })
    }
}
