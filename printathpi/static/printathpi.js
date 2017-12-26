/* Print a document at the Hasso-Plattner-Institute in Potsdam.
 *
 *    printathpi({"document.pdf": "... content ..."}, username, password, onPrint, onError);
 *    printathpi({"document.pdf": "... content ..."}, null, null, onPrint, onError);
 *    printathpi({"document.pdf": "... content ..."});
 */

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
  
  if (username && password) {
    // Basic auth see https://stackoverflow.com/a/5507289/1320237
    XHR.setRequestHeader ("Authorization", "Basic " + btoa(username + ":" + password));
  }

  // Send our FormData object; HTTP headers are set automatically
  XHR.send(formData);
} 

var PRINT_AT_HPI_ENDPOINT = "https://printathpi.quelltext.eu/print";
