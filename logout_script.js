// Run this in your browser console to log out and see the landing page
// Press F12, go to Console tab, paste this, and press Enter

localStorage.removeItem('token');
localStorage.removeItem('auth_token');
localStorage.removeItem('user');
location.reload();

console.log('✅ Logged out! Landing page will appear after reload.');
