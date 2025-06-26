  function loadPage(sectionName) {
    // Convert to lowercase and build the URL
    const url = '/' + sectionName.toLowerCase();

    // Make an AJAX GET request to the server
    fetch(url)
      .then(response => {
        if (!response.ok) {
          throw new Error(`Page not found: ${url}`);
        }
        return response.text();
      })
      .then(html => {
        // Inject the returned HTML into the content div
        document.querySelector('.content').innerHTML = html;
      })
      .catch(error => {
        document.querySelector('.content').innerHTML = `<p>Error loading page: ${error.message}</p>`;
      });
  }