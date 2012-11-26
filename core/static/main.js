var req = new XMLHttpRequest();

req.onreadystatechange = function() {
  if (req.readyState != 4) return;
  if (req.status != 200) {
    return;
  }
  // Request successful, read the response
  var resp = req.responseText;
  alert(resp);
  // ... and use it as needed by your app.
}

req.open("GET", "../json_people", true);
req.send();

//alert("sendt request");
