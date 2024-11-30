// Select buttons for switching themes
const lightThemeBtn = document.getElementById('light-theme');
const darkThemeBtn = document.getElementById('dark-theme');

// Apply saved theme on page load
document.addEventListener('DOMContentLoaded', () => {
  const savedTheme = localStorage.getItem('theme');
  if (savedTheme === null || savedTheme === 'light-mode') {
    // If no theme is saved or "light-mode" is saved, apply light mode by default
    document.documentElement.className = 'light-mode';
    localStorage.setItem('theme', 'light-mode');
  } else {
    // Apply dark mode if dark mode is saved
    document.documentElement.className = 'dark-mode';
  }
});

// Event listeners for changing themes and saving to localStorage
lightThemeBtn.addEventListener('click', () => {
  document.documentElement.className = 'light-mode'; // Apply light mode
  localStorage.setItem('theme', 'light-mode'); // Save light mode
});

darkThemeBtn.addEventListener('click', () => {
  document.documentElement.className = 'dark-mode'; // Apply dark mode
  localStorage.setItem('theme', 'dark-mode'); // Save dark mode
});
