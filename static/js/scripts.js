// Version: 3.0

AlertsAutoDismissal("auto-dismiss", 2000); // auto dismiss alerts after 2 seconds

/**
 * Load remote HTML into a Bootstrap modal via fetch (replaces htmx modal pattern)
 * Usage: <a data-modal-url="/some/url/" data-bs-toggle="modal" data-bs-target="#modal-box">
 * Optional: data-modal-confirm="Are you sure?" to show a confirmation dialog first
 */
document.addEventListener("click", function (e) {
  const trigger = e.target.closest("[data-modal-url]");
  if (!trigger) return;

  const confirmMsg = trigger.getAttribute("data-modal-confirm");
  if (confirmMsg && !confirm(confirmMsg)) {
    e.preventDefault();
    e.stopPropagation();
    return;
  }

  const url = trigger.getAttribute("data-modal-url");
  const targetSel = trigger.getAttribute("data-bs-target");
  const container = document.querySelector(targetSel + " .modal-content");

  fetch(url)
    .then(function (r) { return r.text(); })
    .then(function (html) { container.innerHTML = html; });
});

/**
 * Inline POST + swap (replaces htmx schedule action pattern)
 * Usage: <a data-post-url="/url/" data-target="#element-id" data-swap="outerHTML"
 *           data-csrf="TOKEN" data-confirm="Action this?">
 */
document.addEventListener("click", function (e) {
  const trigger = e.target.closest("[data-post-url]");
  if (!trigger) return;
  e.preventDefault();

  const confirmMsg = trigger.getAttribute("data-confirm");
  if (confirmMsg && !confirm(confirmMsg)) return;

  const url = trigger.getAttribute("data-post-url");
  const targetSel = trigger.getAttribute("data-target");
  const swap = trigger.getAttribute("data-swap") || "innerHTML";
  const csrf = trigger.getAttribute("data-csrf");

  fetch(url, {
    method: "POST",
    headers: { "X-CSRFToken": csrf, "X-Requested-With": "XMLHttpRequest" },
  })
    .then(function (r) { return r.text(); })
    .then(function (html) {
      var target = document.querySelector(targetSel);
      if (!target) return;
      if (swap === "outerHTML") {
        target.outerHTML = html;
      } else {
        target.innerHTML = html;
      }
    });
});

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
  const icon = document.getElementById("showall");
  if (!icon) return;

  const url = new URL(window.location.href);
  const allParam = url.searchParams.get("all");

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
const showallBtn = document.getElementById("showall");
if (showallBtn) {
  showallBtn.addEventListener("click", toggleAllQueryset);
}
