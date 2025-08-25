// // const hamburger = document.querySelector("#toggle-btn");

// // hamburger.addEventListener("click", function () {
// //     document.querySelector("#sidebar").classList.toggle("expand");
// // });


// document.addEventListener("DOMContentLoaded", function () {
//   const sidebar = document.getElementById("sidebar");
//   const toggleBtn = document.getElementById("toggle-btn");

//   // Load saved state
//   if (localStorage.getItem("sidebarExpanded") === "true") {
//     sidebar.classList.add("expand");
//   }

//   toggleBtn.addEventListener("click", () => {
//     sidebar.classList.toggle("expand");
//     localStorage.setItem("sidebarExpanded", sidebar.classList.contains("expand"));
//   });
// });

// // Disable animation if sidebar already expanded before
// if (localStorage.getItem("sidebarExpanded") === "true") {
//   document.querySelector('.sidebar-logo a').style.animation = "none";
// }