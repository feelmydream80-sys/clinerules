document.addEventListener('DOMContentLoaded', function() {
    highlightActiveNavLink();
    setupUserMenu();
});

function highlightActiveNavLink() {
    const links = document.querySelectorAll('a.nav-link');
    const currentPath = window.location.pathname;

    let bestMatch = null;
    let exactMatch = null;

    // Find an exact match first
    links.forEach(link => {
        if (link.pathname === currentPath) {
            exactMatch = link;
        }
    });

    if (exactMatch) {
        bestMatch = exactMatch;
    } else {
        // If no exact match, find the best partial match (longest path)
        links.forEach(link => {
            if (link.pathname !== '/' && currentPath.startsWith(link.pathname)) {
                if (!bestMatch || link.pathname.length > bestMatch.pathname.length) {
                    bestMatch = link;
                }
            }
        });
    }
    
    // Fallback to root if no other match is found
    if (!bestMatch && currentPath === '/') {
        bestMatch = document.querySelector('a.nav-link[href="/"]');
    }

    // Remove active class from all links first
    links.forEach(link => {
        link.classList.remove('bg-blue-900');
        link.classList.add('hover:bg-blue-700');
    });

    // Apply active class to the best match
    if (bestMatch) {
        bestMatch.classList.add('bg-blue-900');
        bestMatch.classList.remove('hover:bg-blue-700');
    }
}

function setupUserMenu() {
    const userMenuButton = document.getElementById('user-menu-button');
    const userMenu = document.getElementById('user-menu');
    const userMenuContainer = document.getElementById('user-menu-container');

    if (userMenuButton && userMenu && userMenuContainer) {
        userMenuButton.addEventListener('click', (event) => {
            event.stopPropagation();
            userMenu.classList.toggle('hidden');
        });

        document.addEventListener('click', (event) => {
            if (!userMenuContainer.contains(event.target)) {
                userMenu.classList.add('hidden');
            }
        });
    }
}
