chrome.runtime.onInstalled.addListener(() => {
    chrome.contextMenus.create({
      id: "checkFakeNews",
      title: "Check Fake News",
      contexts: ["selection"],
    });
  });
  
  chrome.contextMenus.onClicked.addListener(async (info, tab) => {
    if (info.menuItemId === "checkFakeNews") {
      const selectedText = info.selectionText;
      if (selectedText) {
        try {
          // Send the highlighted text to Flask API for Fake News detection
          const response = await fetch('http://127.0.0.1:5000/detect_fake_news', {
            method: 'POST',
            headers: {
              'Content-Type': 'application/json',
            },
            body: JSON.stringify({ text: selectedText })
          });
  
          const data = await response.json();
  
          // Send the result to popup
          chrome.storage.local.set({ isFake: data.isFake, text: selectedText });
          
          // Open the popup
          chrome.action.openPopup();
        } catch (error) {
          console.error('Error:', error);
          chrome.storage.local.set({ isFake: null, text: 'Error occurred' });
          chrome.action.openPopup();
        }
      }
    }
  });
  