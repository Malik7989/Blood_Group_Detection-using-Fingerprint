// Show the login form and hide the signup form
function showLogin() {
  document.getElementById("login-form").classList.add("active");
  document.getElementById("signup-form").classList.remove("active");
  document.getElementById("show-signup-btn").classList.remove("hidden");
  document.getElementById("show-login-btn").classList.add("hidden");
}

// Show the signup form and hide the login form
function showSignup() {
  document.getElementById("signup-form").classList.add("active");
  document.getElementById("login-form").classList.remove("active");
  document.getElementById("show-signup-btn").classList.add("hidden");
  document.getElementById("show-login-btn").classList.remove("hidden");
}

// navbar code

function toggleMenu() {
  const navLinks = document.querySelector(".nav-links");
  navLinks.classList.toggle("active");
}


// Validate reCAPTCHA before form submission
// function validateCaptcha() {
//   const response = grecaptcha.getResponse();
//   if (response.length === 0) {
//     alert("Please complete the reCAPTCHA!");
//     return false;
//   }
//   return true;
// }
