// Initialize Material Components
document.addEventListener('DOMContentLoaded', function() {
    if (typeof mdc !== 'undefined') {
        mdc.autoInit();

        // Initialize all buttons
        document.querySelectorAll('.mdc-button').forEach(function(buttonEl) {
            new mdc.ripple.MDCRipple(buttonEl);
        });
    }

    // Products dropdown functionality
    const productsButton = document.getElementById('products-menu-button');
    const productsDropdown = document.getElementById('products-dropdown');

    if (productsButton && productsDropdown) {
        productsButton.addEventListener('click', function(e) {
            e.stopPropagation();
            const isExpanded = productsButton.getAttribute('aria-expanded') === 'true';
            productsButton.setAttribute('aria-expanded', !isExpanded);
            productsDropdown.classList.toggle('hidden');
            
            // Rotate the arrow icon
            const icon = productsButton.querySelector('.material-icons');
            if (icon) {
                icon.style.transform = isExpanded ? 'rotate(0deg)' : 'rotate(180deg)';
                icon.style.transition = 'transform 0.3s ease';
            }
        });

        // Close dropdown when clicking outside
        document.addEventListener('click', function(e) {
            if (!productsButton.contains(e.target) && !productsDropdown.contains(e.target)) {
                productsButton.setAttribute('aria-expanded', 'false');
                productsDropdown.classList.add('hidden');
                const icon = productsButton.querySelector('.material-icons');
                if (icon) {
                    icon.style.transform = 'rotate(0deg)';
                }
            }
        });
    }

    // Mobile menu functionality
    const mobileMenuButton = document.getElementById('mobile-menu-button');
    const mobileMenu = document.getElementById('mobile-menu');
    const mobileMenuOverlay = document.getElementById('mobile-menu-overlay');
    const mobileMenuClose = document.getElementById('mobile-menu-close');
    const mobileProductsButton = document.getElementById('mobile-products-menu-button');
    const mobileProductsSubmenu = document.getElementById('mobile-products-submenu');

    function toggleMobileMenu() {
        if (mobileMenu && mobileMenuOverlay) {
            mobileMenu.classList.toggle('active');
            mobileMenuOverlay.classList.toggle('active');
            document.body.style.overflow = mobileMenu.classList.contains('active') ? 'hidden' : '';
        }
    }

    if (mobileMenuButton) mobileMenuButton.addEventListener('click', toggleMobileMenu);
    if (mobileMenuClose) mobileMenuClose.addEventListener('click', toggleMobileMenu);
    if (mobileMenuOverlay) mobileMenuOverlay.addEventListener('click', toggleMobileMenu);

    if (mobileProductsButton && mobileProductsSubmenu) {
        mobileProductsButton.addEventListener('click', function() {
            const icon = this.querySelector('.material-icons');
            if (icon) {
                icon.textContent = icon.textContent === 'expand_more' ? 'expand_less' : 'expand_more';
            }
            mobileProductsSubmenu.classList.toggle('hidden');
        });
    }

    // Close mobile menu on window resize if it's open
    window.addEventListener('resize', function() {
        if (window.innerWidth >= 768 && mobileMenu && mobileMenu.classList.contains('active')) {
            toggleMobileMenu();
        }
    });

    // Back to top functionality
    const backToTopButton = document.getElementById('back-to-top');
    if (backToTopButton) {
        window.addEventListener('scroll', () => {
            if (window.pageYOffset > 300) {
                backToTopButton.classList.remove('hidden');
            } else {
                backToTopButton.classList.add('hidden');
            }
        });

        backToTopButton.addEventListener('click', () => {
            window.scrollTo({
                top: 0,
                behavior: 'smooth'
            });
        });
    }

    // Notification system
    const notification = document.getElementById('notification');
    const notificationMessage = document.getElementById('notification-message');

    window.showNotification = function(message) {
        if (notification && notificationMessage) {
            notificationMessage.textContent = message;
            notification.style.transform = 'translateX(0)';
            setTimeout(() => {
                notification.style.transform = 'translateX(100%)';
            }, 3000);
        }
    };

    // Cart and wishlist functionality
    const cartCount = document.getElementById('cart-count');
    const cartCountMobile = document.getElementById('cart-count-mobile');
    const wishlistCount = document.getElementById('wishlist-count');
    const wishlistCountMobile = document.getElementById('wishlist-count-mobile');

    function updateCartCount(count) {
        if (cartCount && cartCountMobile) {
            cartCount.textContent = count;
            cartCountMobile.textContent = count;
            cartCount.style.display = count === 0 ? 'none' : 'flex';
            cartCountMobile.style.display = count === 0 ? 'none' : 'flex';
        }
    }

    function updateWishlistCount(count) {
        if (wishlistCount && wishlistCountMobile) {
            wishlistCount.textContent = count;
            wishlistCountMobile.textContent = count;
            wishlistCount.style.display = count === 0 ? 'none' : 'flex';
            wishlistCountMobile.style.display = count === 0 ? 'none' : 'flex';
        }
    }

    // Add to cart functionality
    document.body.addEventListener('submit', function(e) {
        if (e.target.classList.contains('add-to-cart-form')) {
            e.preventDefault();
            fetch(e.target.action, {
                method: 'POST',
                body: new FormData(e.target),
                headers: {
                    'X-Requested-With': 'XMLHttpRequest',
                }
            })
            .then(response => response.json())
            .then(data => {
                updateCartCount(data.cart_total);
                showNotification('Item added to cart successfully!');
            })
            .catch(error => {
                console.error('Error:', error);
                showNotification('Failed to add item to cart. Please try again.');
            });
        }
    });

    // Add to wishlist functionality
    document.body.addEventListener('submit', function(e) {
        if (e.target.classList.contains('add-to-wishlist-form')) {
            e.preventDefault();
            fetch(e.target.action, {
                method: 'POST',
                body: new FormData(e.target),
                headers: {
                    'X-Requested-With': 'XMLHttpRequest',
                }
            })
            .then(response => response.json())
            .then(data => {
                updateWishlistCount(data.wishlist_total);
                showNotification('Item added to wishlist successfully!');
            })
            .catch(error => {
                console.error('Error:', error);
                showNotification('Failed to add item to wishlist. Please try again.');
            });
        }
    });

    // Initial cart and wishlist count update
    fetch('/cart/count/')
        .then(response => response.json())
        .then(data => updateCartCount(data.count))
        .catch(error => console.error('Error fetching cart count:', error));

    const wishlistCountUrl = document.querySelector('meta[name="wishlist-count-url"]')?.content;
    if (wishlistCountUrl) {
        fetch(wishlistCountUrl)
            .then(response => response.json())
            .then(data => updateWishlistCount(data.count))
            .catch(error => console.error('Error fetching wishlist count:', error));
    }
});
