// Version: 2.0

AlertsAutoDismissal("auto-dismiss", 2000); // auto dismiss alerts after 2 seconds

/**
 * This function set a timer to close and remove alerts from DOM
 * @param {string} autoCloseClass - The class of the alert to be closed
 * @param {number} timeInterval - The time interval in milliseconds
 *
 */
function AlertsAutoDismissal(autoCloseClass, timeInterval) {
  document.addEventListener("DOMContentLoaded", function () {
    const autoCloseAlerts = document.querySelectorAll("." + autoCloseClass);

    autoCloseAlerts.forEach(function (alert) {
      setTimeout(function () {
        alert.classList.add("hide");

        alert.addEventListener("transitionend", function () {
          alert.remove(); // Remove after the transition ends
        });
      }, timeInterval);
    });
  });
}

/**
 * This function toggles the visibility of some data from a queryset
 * the toggled data are determined by the query parameter `all` in the view function
 * only 1 of this toggle can exist in a page
 */

function toggleAllQueryset() {
  const url = new URL(window.location.href);
  const allParam = url.searchParams.get("all");
  const icon = document.getElementById("showall");

  if (allParam === "true") {
    url.searchParams.set("all", "false");
  } else {
    url.searchParams.set("all", "true");
  }

  window.location.href = url.toString();
}

/**
 * This function is used in conjunction with the toggleAllQueryset function
 * It updates the class of the button icon on page load
 */
function updateButtonClassOnLoad() {
  const url = new URL(window.location.href);
  const allParam = url.searchParams.get("all");
  const icon = document.getElementById("showall");

  if (allParam === "true") {
    icon.classList.add("bi-toggle2-on");
    icon.classList.remove("bi-toggle2-off");
  } else {
    icon.classList.add("bi-toggle2-off");
    icon.classList.remove("bi-toggle2-on");
  }
}

/**
 * Add event listeners to the page so the above 2 functions can work
 */
window.addEventListener("load", updateButtonClassOnLoad);
document.getElementById("showall").addEventListener("click", toggleAllQueryset);
