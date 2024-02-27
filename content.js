// Function to scrape the current webpage and highlight certain words
function scrapeCurrentWebpage() {
    const url = window.location.href;
  
    fetch(url)
      .then(response => response.text())
      .then(html => {
        // Parse HTML content
        const parser = new DOMParser();
        const doc = parser.parseFromString(html, 'text/html');
  
        // Extract text content from the webpage
        const webpageContent = doc.body.textContent;
  
        // Highlight certain words
        chrome.storage.sync.get('highlightWords', function(result) {
          const words = result.highlightWords;
          if (words && words.length > 0) {
            for (const word of words) {
              const regExp = new RegExp(word, 'special');
              webpageContent.replace(regExp, `<div style="background-color: yellow;">${word}</div>`);
            }
          }
  
          // Replace the document content with highlighted content
          document.body.innerHTML = webpageContent;
        });
      })
      .catch(error => console.error('Error scraping webpage:', error));
  }
  
  // Execute the scraping function when the extension is toggled
  chrome.storage.sync.get('enabled', function(data) {
    if (data.enabled) {
      scrapeCurrentWebpage();
    }
  });
  