// Version: 1.0

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