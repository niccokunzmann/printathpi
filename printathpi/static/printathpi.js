/* Print a document at the Hasso-Plattner-Institute in Potsdam.
 *
 *    printathpi({"document.pdf": "... content ..."}, username, password, onPrint, onError);
 *    printathpi({"document.pdf": "... content ..."}, null, null, onPrint, onError);
 *    printathpi({"document.pdf": "... content ..."});
 */

var SAVED_CREDENTIALS = {};

function printathpi(documents, username, password, onprint, onerror) {
  // see https://developer.mozilla.org/en-US/docs/Web/API/FormData
  var formData = new FormData();
  for (var property in documents) {
    // see https://stackoverflow.com/a/16735184/1320237
    if (documents.hasOwnProperty(property)) {
       // see https://developer.mozilla.org/en-US/docs/Web/API/Blob/Blob
       var blob = new Blob([documents[property]]);
       // see https://developer.mozilla.org/en-US/docs/Web/API/FormData/append
       formData.append("files[]", blob, property);
    }
  }
  function sendRequest(username, password){
    // see https://developer.mozilla.org/en-US/docs/Learn/HTML/Forms/Sending_forms_through_JavaScript 
    var XHR = new XMLHttpRequest();
    // Define what happens on successful data submission
    XHR.addEventListener('load', function(event) {
    if (event.target.status == 200) {
      if (onprint) {
        onprint(event);
      }
    } else {
      if (onerror) {
        onerror(event);
      }
    }
    });

    // Define what happens in case of error
    XHR.addEventListener('error', function(event) {
    if (onerror) {
      onerror(event);
    }
    });

    // Set up our request
    XHR.open('POST', PRINT_AT_HPI_ENDPOINT);
    // Basic auth see https://stackoverflow.com/a/5507289/1320237
    XHR.setRequestHeader ("Authorization", "Basic " + btoa(username + ":" + password));

    // Send our FormData object; HTTP headers are set automatically
    XHR.send(formData);
  }
  if (username && password) {
    return sendRequest(username, password);
  }
  function done() {
    sendRequest(usernameInput.value, passwordInput.value);
    abort();
    return false;
  }
  function abort() {
    SAVED_CREDENTIALS.username = usernameInput.value;
    SAVED_CREDENTIALS.password = passwordInput.value;
    document.body.removeChild(dialog);
  }
  
  var dialog = document.createElement("div");
  dialog.style.width = "200px";
  dialog.style.padding = "20px";
  dialog.style.backgroundColor = "gray";    
  dialog.style.position = "absolute";
  dialog.style.top = "100px";
  dialog.style.left = "100px";
  dialog.innerHTML = "HPI E-Mail und Passwort:"
  dialog.onsubmit = done;
  
  var usernameInput = document.createElement("input");
  usernameInput.type = "text";
  usernameInput.id = "hpi-email";
  usernameInput.placeholder = "Alice.XY@student.hpi.de"
  if (username) {
    usernameInput.value = username;
  } else if (SAVED_CREDENTIALS.username) {
    usernameInput.value = SAVED_CREDENTIALS.username;
  }
  dialog.appendChild(usernameInput);
  
  var passwordInput = document.createElement("input");
  passwordInput.type = "password";
  passwordInput.id = "hpi-password";
  if (password) {
    passwordInput.value = password;
  } else if (SAVED_CREDENTIALS.password) {
    passwordInput.value = SAVED_CREDENTIALS.password;
  }
  dialog.appendChild(passwordInput);

  var button = document.createElement("input");
  button.type = "button";
  button.value = "Drucken";
  button.onclick = done;
  dialog.appendChild(button);

  var button2 = document.createElement("input");
  button2.type = "button";
  button2.value = "Abbrechen";
  button2.onclick = abort;
  dialog.appendChild(button2);

  document.body.appendChild(dialog);
}

var PRINT_AT_HPI_ENDPOINT = "https://printathpi.quelltext.eu/print";
