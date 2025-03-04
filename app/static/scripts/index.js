
// Hamburger menu
const hamburger = document.querySelector(".hamburger");
const navLinks = document.querySelector(".nav-links");

hamburger.addEventListener("click", () => {
  hamburger.classList.toggle("active");
  navLinks.classList.toggle("active");
});

// Close menu when clicking a link
navLinks.querySelectorAll("a").forEach((link) => {
  link.addEventListener("click", () => {
    hamburger.classList.remove("active");
    navLinks.classList.remove("active");
  });
});


// Toggle additional fields based on role selection
function toggleAdditionalFields() {
  const role = document.getElementById("role").value;

  const farmerFields = document.getElementById("farmerFields");
  const vetFields = document.getElementById("vetFields");

  // show or hide fields based on role selection
  farmerFields.style.display = role === "farmer" ? "block" : "none";
  vetFields.style.display = role === "vet" ? "block" : "none";

  // enable/disable required attribute
  document
    .querySelectorAll("#farmerFields input, #farmerFields textarea")
    .forEach((field) => {
      if (role === "farmer") {
        field.setAttribute("required", "true");
      } else {
        field.removeAttribute("required");
      }
    });

  document
    .querySelectorAll(
      "#vetFields input, #vetFields select, #vetFields textarea"
    )
    .forEach((field) => {
      if (role === "vet") {
        field.setAttribute("required", "true");
      } else {
        field.removeAttribute("required");
      }
    });
}

// Ensure fields are set correctly when the page loads
window.onload = function () {
  toggleAdditionalFields();
};
