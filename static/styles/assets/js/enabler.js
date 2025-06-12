function passenable(){
    alert ('hello');
    if (getElementById('pass').value == true){
        document.getElementById('pass-no').disabled = true;
        document.getElementById('place-of-issue').disabled = true;
        document.getElementById('date-of-issue').disabled = true;
        document.getElementById('valid-date').disabled = true;
    }
    else {
        document.getElementById('pass-no').disabled = false;
        document.getElementById('place-of-issue').disabled = false;
        document.getElementById('date-of-issue').disabled = false;
        document.getElementById('valid-date').disabled = false;
    }
}
