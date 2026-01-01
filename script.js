/* ========================================
   FANCY PORTFOLIO WEBSITE - JAVASCRIPT
   Interactive Features & Animations
   ======================================== */

// ===== DOM ELEMENTS =====
const navbar = document.getElementById('navbar');
const navLinks = document.querySelectorAll('.nav-link');
const menuToggle = document.getElementById('menu-toggle');
const navLinksContainer = document.getElementById('nav-links');
const backToTopBtn = document.getElementById('back-to-top');
const typewriterElement = document.getElementById('typewriter');
const projectFilters = document.querySelectorAll('.filter-btn');
const projectCards = document.querySelectorAll('.project-card');
const contactForm = document.getElementById('contact-form');
const skillItems = document.querySelectorAll('.skill-item');
const hero = document.querySelector('.hero');

// ===== TYPEWRITER EFFECT =====
const typewriterText = "Hi, I'm Zayan Parpia";
let charIndex = 0;

function typeWriter() {
  if (typewriterElement && charIndex < typewriterText.length) {
    typewriterElement.textContent += typewriterText.charAt(charIndex);
    charIndex++;
    setTimeout(typeWriter, 100);
  }
}

// Start typewriter effect when page loads
window.addEventListener('load', () => {
  setTimeout(typeWriter, 500);
});

// ===== NAVBAR SCROLL EFFECT =====
let lastScrollTop = 0;

window.addEventListener('scroll', () => {
  const scrollTop = window.pageYOffset || document.documentElement.scrollTop;

  // Add/remove scrolled class for glassmorphism effect
  if (scrollTop > 100) {
    navbar.classList.add('scrolled');
  } else {
    navbar.classList.remove('scrolled');
  }

  lastScrollTop = scrollTop;
});

// ===== SMOOTH SCROLL & ACTIVE NAVIGATION =====
navLinks.forEach(link => {
  link.addEventListener('click', (e) => {
    // Get targetId
    const targetId = link.getAttribute('href');

    // Only prevent default and smooth scroll for internal links
    if (targetId.startsWith('#')) {
      e.preventDefault();

      // Remove active class from all links
      navLinks.forEach(l => l.classList.remove('active'));

      // Add active class to clicked link
      link.classList.add('active');

      const targetSection = document.querySelector(targetId);

      if (targetSection) {
        // Smooth scroll to section
        const offsetTop = targetSection.offsetTop - 80;
        window.scrollTo({
          top: offsetTop,
          behavior: 'smooth'
        });
      }

      // Close mobile menu if open
      if (navLinksContainer.classList.contains('active')) {
        navLinksContainer.classList.remove('active');
        menuToggle.classList.remove('active');
      }
    }
  });
});

// ===== MOBILE MENU TOGGLE =====
menuToggle.addEventListener('click', () => {
  menuToggle.classList.toggle('active');
  navLinksContainer.classList.toggle('active');
});

// Close mobile menu when clicking outside
document.addEventListener('click', (e) => {
  if (!e.target.closest('.navbar')) {
    navLinksContainer.classList.remove('active');
    menuToggle.classList.remove('active');
  }
});

// ===== ACTIVE SECTION DETECTION ON SCROLL =====
const sections = document.querySelectorAll('.section');

function updateActiveLink() {
  const scrollPosition = window.pageYOffset + 150;

  sections.forEach(section => {
    const sectionTop = section.offsetTop;
    const sectionHeight = section.offsetHeight;
    const sectionId = section.getAttribute('id');

    if (scrollPosition >= sectionTop && scrollPosition < sectionTop + sectionHeight) {
      navLinks.forEach(link => {
        link.classList.remove('active');
        if (link.getAttribute('href') === `#${sectionId}`) {
          link.classList.add('active');
        }
      });
    }
  });
}

window.addEventListener('scroll', updateActiveLink);

// ===== INTERSECTION OBSERVER FOR SCROLL ANIMATIONS =====
const observerOptions = {
  threshold: 0.1,
  rootMargin: '0px 0px -100px 0px'
};

const observer = new IntersectionObserver((entries) => {
  entries.forEach(entry => {
    if (entry.isIntersecting) {
      entry.target.classList.add('visible');

      // Trigger skill bar animations
      if (entry.target.classList.contains('skill-item')) {
        const progressBar = entry.target.querySelector('.skill-progress');
        const progress = progressBar.getAttribute('data-progress');
        progressBar.style.width = progress + '%';
      }
    }
  });
}, observerOptions);

// Observe all fade-in elements
const fadeElements = document.querySelectorAll('.fade-in');
fadeElements.forEach(el => observer.observe(el));

// Observe skill items for animation
skillItems.forEach(item => observer.observe(item));

// ===== PROJECT FILTERING =====
projectFilters.forEach(filter => {
  filter.addEventListener('click', () => {
    // Remove active class from all filters
    projectFilters.forEach(f => f.classList.remove('active'));

    // Add active class to clicked filter
    filter.classList.add('active');

    // Get filter value
    const filterValue = filter.getAttribute('data-filter');

    // Filter projects
    projectCards.forEach(card => {
      const category = card.getAttribute('data-category');

      if (filterValue === 'all' || category === filterValue) {
        card.style.display = 'block';
        // Trigger animation
        setTimeout(() => {
          card.style.opacity = '1';
          card.style.transform = 'translateY(0)';
        }, 10);
      } else {
        card.style.opacity = '0';
        card.style.transform = 'translateY(20px)';
        setTimeout(() => {
          card.style.display = 'none';
        }, 300);
      }
    });
  });
});

// ===== CONTACT FORM VALIDATION =====
if (contactForm) {
  contactForm.addEventListener('submit', (e) => {
    e.preventDefault();

    // Get form fields
    const nameInput = document.getElementById('name');
    const emailInput = document.getElementById('email');
    const subjectInput = document.getElementById('subject');
    const messageInput = document.getElementById('message');

    // Validation flags
    let isValid = true;

    // Validate name
    if (nameInput.value.trim() === '') {
      showError(nameInput);
      isValid = false;
    } else {
      removeError(nameInput);
    }

    // Validate email
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    if (!emailRegex.test(emailInput.value.trim())) {
      showError(emailInput);
      isValid = false;
    } else {
      removeError(emailInput);
    }

    // Validate subject
    if (subjectInput.value.trim() === '') {
      showError(subjectInput);
      isValid = false;
    } else {
      removeError(subjectInput);
    }

    // Validate message
    if (messageInput.value.trim() === '') {
      showError(messageInput);
      isValid = false;
    } else {
      removeError(messageInput);
    }

    // If form is valid, show success message
    if (isValid) {
      // Show success feedback
      const submitBtn = contactForm.querySelector('.submit-btn');
      const originalText = submitBtn.textContent;
      submitBtn.textContent = '✓ Message Sent!';
      submitBtn.style.background = 'linear-gradient(135deg, #00d9ff, #00ff88)';

      // Reset form
      contactForm.reset();

      // Reset button after 3 seconds
      setTimeout(() => {
        submitBtn.textContent = originalText;
        submitBtn.style.background = '';
      }, 3000);
    }
  });
}

// Helper function to show error
function showError(input) {
  const formGroup = input.parentElement;
  formGroup.classList.add('error');
}

// Helper function to remove error
function removeError(input) {
  const formGroup = input.parentElement;
  formGroup.classList.remove('error');
}

// Remove error on input
const formInputs = document.querySelectorAll('.contact-form input, .contact-form textarea');
formInputs.forEach(input => {
  input.addEventListener('input', () => {
    removeError(input);
  });
});

// ===== BACK TO TOP BUTTON =====
window.addEventListener('scroll', () => {
  if (window.pageYOffset > 500) {
    backToTopBtn.classList.add('visible');
  } else {
    backToTopBtn.classList.remove('visible');
  }
});

backToTopBtn.addEventListener('click', () => {
  window.scrollTo({
    top: 0,
    behavior: 'smooth'
  });
});

// ===== STAGGERED ANIMATION FOR PROJECT CARDS =====
window.addEventListener('load', () => {
  projectCards.forEach((card, index) => {
    setTimeout(() => {
      card.style.opacity = '1';
      card.style.transform = 'translateY(0)';
    }, index * 100);
  });
});

// ===== PARALLAX EFFECT FOR HERO SECTION (Optional Enhancement) =====
window.addEventListener('scroll', () => {
  const scrolled = window.pageYOffset;
  if (hero && scrolled < window.innerHeight) {
    hero.style.transform = `translateY(${scrolled * 0.5}px)`;
  }
});

// ===== DEBOUNCE UTILITY FOR PERFORMANCE =====
function debounce(func, wait = 20) {
  let timeout;
  return function executedFunction(...args) {
    const later = () => {
      clearTimeout(timeout);
      func(...args);
    };
    clearTimeout(timeout);
    timeout = setTimeout(later, wait);
  };
}

// Apply debounce to scroll handlers for better performance
const debouncedScrollHandler = debounce(() => {
  updateActiveLink();
}, 50);

window.addEventListener('scroll', debouncedScrollHandler);

// ===== CONSOLE MESSAGE =====
console.log('%c👋 Welcome to my Portfolio! ', 'color: #00d9ff; font-size: 20px; font-weight: bold;');
console.log('%cInterested in the code? Check out the source or reach out!', 'color: #888; font-size: 14px;');


// ===== UTILITY FUNCTIONS FOR NEW FEATURES =====
function copyCode() {
  const codeBlock = document.querySelector('.project-script code');
  if (codeBlock) {
    const text = codeBlock.textContent;
    navigator.clipboard.writeText(text).then(() => {
      const copyBtn = document.querySelector('.copy-btn');
      const originalText = copyBtn.innerHTML;
      copyBtn.innerHTML = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="20 6 9 17 4 12"></polyline></svg> Copied!';
      copyBtn.style.background = 'var(--color-accent)';

      setTimeout(() => {
        copyBtn.innerHTML = originalText;
        copyBtn.style.background = '';
      }, 2000);
    });
  }
}

function toggleDocumentation() {
  const content = document.getElementById('doc-content');
  const chevron = document.getElementById('doc-chevron');
  if (content && chevron) {
    if (content.classList.contains('expanded')) {
      content.classList.remove('expanded');
      chevron.style.transform = 'rotate(0deg)';
    } else {
      content.classList.add('expanded');
      chevron.style.transform = 'rotate(180deg)';
    }
  }
}

function toggleSecurityPractices() {
  const content = document.getElementById('sec-content');
  const chevron = document.getElementById('sec-chevron');
  if (content && chevron) {
    if (content.classList.contains('expanded')) {
      content.classList.remove('expanded');
      chevron.style.transform = 'rotate(0deg)';
    } else {
      content.classList.add('expanded');
      chevron.style.transform = 'rotate(180deg)';
    }
  }
}

function toggleWhatILearned() {
  const content = document.getElementById('learn-content');
  const chevron = document.getElementById('learn-chevron');
  if (content && chevron) {
    if (content.classList.contains('expanded')) {
      content.classList.remove('expanded');
      chevron.style.transform = 'rotate(0deg)';
    } else {
      content.classList.add('expanded');
      chevron.style.transform = 'rotate(180deg)';
    }
  }
}

// ===== FULLSCREEN IMAGE MODAL LOGIC =====
function initImageModal() {
  console.log('Initializing Image Modal...');
  const modal = document.getElementById('imageModal');
  const modalImg = document.getElementById('fullImage');
  const captionText = document.getElementById('caption');
  const closeBtn = document.getElementById('closeModal');
  const zoomableImages = document.querySelectorAll('.zoom-img');

  console.log('Found zoomable images:', zoomableImages.length);

  if (modal && modalImg && closeBtn) {
    // Open modal on image click
    zoomableImages.forEach(img => {
      img.addEventListener('click', function () {
        modal.classList.add('active');
        modalImg.src = this.src;
        captionText.innerHTML = this.alt;
        document.body.style.overflow = 'hidden';
      });
    });

    // Close modal on X click
    closeBtn.onclick = function () {
      modal.classList.remove('active');
      document.body.style.overflow = 'auto';
    };

    // Close modal on background click (BUT NOT the image itself)
    modal.onclick = function (e) {
      if (e.target === modal) {
        modal.classList.remove('active');
        document.body.style.overflow = 'auto';
      }
    };

    // Close on Escape key
    document.addEventListener('keydown', (e) => {
      if (e.key === 'Escape' && modal.classList.contains('active')) {
        modal.classList.remove('active');
        document.body.style.overflow = 'auto';
      }
    });
  }
}

// Initialize on DOMContentLoaded and also immediately if already loaded
if (document.readyState === 'loading') {
  document.addEventListener('DOMContentLoaded', initImageModal);
} else {
  initImageModal();
}
