document.addEventListener('DOMContentLoaded', function () {
    // Retrieve the data stored in chrome.storage
    chrome.storage.local.get(['isFake', 'text'], function(data) {
      const newsText = data.text;
      const resultMessage = document.getElementById('resultMessage');
      
      if (newsText) {
        document.getElementById('newsText').textContent = `News: ${newsText}`;
        
        if (data.isFake === null) {
          resultMessage.textContent = "Error occurred while checking news.";
          resultMessage.className = "message";
        } else if (data.isFake) {
          resultMessage.textContent = "This News Could be Fake";
          resultMessage.className = "message fake";
        } else {
          resultMessage.textContent = "This Seems like a Genuine News ";
          resultMessage.className = "message genuine";
        }
      } else {
        resultMessage.textContent = "No text selected.";
        resultMessage.className = "message";
      }
    });
  });
  