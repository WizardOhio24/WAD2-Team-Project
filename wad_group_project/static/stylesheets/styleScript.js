
document.addEventListener("DOMContentLoaded", myfunction);

function myfunction(){
    var navBar = document.getElementById('navigationBar');

    var buttons = navBar.getElementsByClassName('Button');
    

    


    for(var i=0;i<buttons.length;i++){
        
        buttons[i].addEventListener("click", callback);
    }  

}


function callBack(){
    var current = document.getElementsById('active');
    current[0].Id = current[0].Id.replace('active', 'notActive');
    this.Id = 'notActive';
}
