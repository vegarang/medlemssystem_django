var req = new XMLHttpRequest();

req.onreadystatechange = function() {
    if (req.readyState != 4) return;
    if (req.status != 200) {
        return;
    }
    // Request successful, read the response
    var resp = req.responseText;
    var obj=jQuery.parseJSON(resp);

    for (var i=0; i<obj.length; i++){
        document.write(obj[i].name);
    }
}

req.open("GET", "../json_people", true);
req.send();

//alert("sendt request");
