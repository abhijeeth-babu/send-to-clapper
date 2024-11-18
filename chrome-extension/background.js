// Create a context menu item for YouTube links
chrome.runtime.onInstalled.addListener(() => {
  chrome.contextMenus.create({
    id: "sendToClapper",
    title: "Send to Clapper",
    contexts: ["link"],
    targetUrlPatterns: ["*://*.youtube.com/watch*", "*://*.youtube.com/shorts/*"]
  });
});

// Listen for context menu clicks
chrome.contextMenus.onClicked.addListener((info) => {
  if (info.menuItemId === "sendToClapper") {
    const videoLink = normalizeYouTubeLink(info.linkUrl);
    openClapper(videoLink);
  }
});

// Handle extension icon click
chrome.action.onClicked.addListener(async (tab) => {
  const url = tab.url;

  if ( !(url.includes("youtube.com/watch") || url.includes("youtube.com/shorts/")) ) {
    showNotification("Not a YouTube video", "This page is not a YouTube video.");
    return;
  }

  const videoLink = normalizeYouTubeLink(url);

  if (!videoLink) {
    showNotification("Invalid YouTube Link", "Could not process this link.");
    return;
  }


  chrome.scripting.executeScript({
    target: { tabId: tab.id },
    func: () => {
      const video = document.querySelector('video[src^="blob:"]');
      if (video) video.pause();
    },
  });

  openClapper(videoLink);
});

// Normalize YouTube links to standard format
function normalizeYouTubeLink(url) {
  const shortsRegex = /https?:\/\/(?:www\.)?youtube\.com\/shorts\/([a-zA-Z0-9_-]+)/;
  const watchRegex = /https?:\/\/(?:www\.)?youtube\.com\/watch\?v=([a-zA-Z0-9_-]+)/;

  if (shortsRegex.test(url)) {
    const videoId = url.match(shortsRegex)[1];
    return `https://www.youtube.com/watch?v=${videoId}`;
  } else if (watchRegex.test(url)) {
    return url; // Already in the correct format
  }
  return url; // Return as-is for unsupported formats
}

// Open Clapper with the given video link
function openClapper(videoLink) {
  chrome.runtime.sendNativeMessage(
    "com.example.clapper",
    { link: videoLink },
    (response) => {
      if (chrome.runtime.lastError || !response) {
        showNotification(
          "Error sending to Clapper",
          chrome.runtime.lastError?.message || "No response from Clapper."
        );
      }
    }
  );
}

// Show a notification
function showNotification(title, message) {
  chrome.notifications.create({
    type: "basic",
    iconUrl: "icons/icon128.png",
    title: title,
    message: message,
  });
}

