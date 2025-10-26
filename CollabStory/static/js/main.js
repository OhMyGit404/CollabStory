// Main JavaScript for CollabStory

document.addEventListener('DOMContentLoaded', function() {
    // Initialize tooltips
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });

    // Initialize popovers
    var popoverTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="popover"]'));
    var popoverList = popoverTriggerList.map(function (popoverTriggerEl) {
        return new bootstrap.Popover(popoverTriggerEl);
    });

    // Auto-hide alerts after 5 seconds
    setTimeout(function() {
        var alerts = document.querySelectorAll('.alert:not(.alert-permanent)');
        alerts.forEach(function(alert) {
            var bsAlert = new bootstrap.Alert(alert);
            bsAlert.close();
        });
    }, 5000);

    // Add loading states to forms
    var forms = document.querySelectorAll('form');
    forms.forEach(function(form) {
        form.addEventListener('submit', function() {
            var submitBtn = form.querySelector('button[type="submit"]');
            if (submitBtn) {
                submitBtn.disabled = true;
                submitBtn.innerHTML = '<span class="spinner-border spinner-border-sm me-2"></span>Processing...';
            }
        });
    });

    // Initialize word count for textareas
    var textareas = document.querySelectorAll('textarea[data-word-count]');
    textareas.forEach(function(textarea) {
        var counter = document.createElement('div');
        counter.className = 'form-text text-end word-count';
        counter.innerHTML = '<span class="word-count-number">0</span> words';
        textarea.parentNode.appendChild(counter);

        function updateWordCount() {
            var words = textarea.value.trim().split(/\s+/).filter(function(word) {
                return word.length > 0;
            }).length;
            
            var wordCountElement = counter.querySelector('.word-count-number');
            wordCountElement.textContent = words;
            
            // Add warning classes based on word count
            counter.className = 'form-text text-end word-count';
            if (words > 1000) {
                counter.classList.add('danger');
            } else if (words > 500) {
                counter.classList.add('warning');
            }
        }

        textarea.addEventListener('input', updateWordCount);
        updateWordCount();
    });

    // Initialize character count for textareas
    var textareasWithCharCount = document.querySelectorAll('textarea[data-char-count]');
    textareasWithCharCount.forEach(function(textarea) {
        var counter = document.createElement('div');
        counter.className = 'form-text text-end';
        counter.innerHTML = '<span class="char-count-number">0</span> characters';
        textarea.parentNode.appendChild(counter);

        function updateCharCount() {
            var chars = textarea.value.length;
            counter.querySelector('.char-count-number').textContent = chars;
        }

        textarea.addEventListener('input', updateCharCount);
        updateCharCount();
    });

    // Initialize image preview for file inputs
    var imageInputs = document.querySelectorAll('input[type="file"][accept*="image"]');
    imageInputs.forEach(function(input) {
        input.addEventListener('change', function(e) {
            var file = e.target.files[0];
            if (file) {
                var reader = new FileReader();
                reader.onload = function(e) {
                    var preview = document.createElement('img');
                    preview.src = e.target.result;
                    preview.className = 'img-thumbnail mt-2';
                    preview.style.maxWidth = '200px';
                    preview.style.maxHeight = '200px';
                    
                    // Remove existing preview
                    var existingPreview = input.parentNode.querySelector('.img-thumbnail');
                    if (existingPreview) {
                        existingPreview.remove();
                    }
                    
                    input.parentNode.appendChild(preview);
                };
                reader.readAsDataURL(file);
            }
        });
    });

    // Initialize search functionality
    var searchInputs = document.querySelectorAll('input[type="search"], input[name="search"]');
    searchInputs.forEach(function(input) {
        var timeout;
        input.addEventListener('input', function() {
            clearTimeout(timeout);
            timeout = setTimeout(function() {
                // Auto-submit search after 500ms of no typing
                var form = input.closest('form');
                if (form) {
                    form.submit();
                }
            }, 500);
        });
    });

    // Initialize HTMX indicators
    document.body.addEventListener('htmx:beforeRequest', function(e) {
        var target = e.target;
        target.classList.add('loading');
        
        // Show loading spinner
        var spinner = document.createElement('span');
        spinner.className = 'spinner-border spinner-border-sm me-2';
        spinner.setAttribute('data-loading-spinner', 'true');
        
        var button = target.querySelector('button');
        if (button) {
            button.appendChild(spinner);
            button.disabled = true;
        }
    });

    document.body.addEventListener('htmx:afterRequest', function(e) {
        var target = e.target;
        target.classList.remove('loading');
        
        // Remove loading spinner
        var spinner = target.querySelector('[data-loading-spinner]');
        if (spinner) {
            spinner.remove();
        }
        
        var button = target.querySelector('button');
        if (button) {
            button.disabled = false;
        }
    });

    // Initialize notification system
    window.showNotification = function(message, type = 'info', duration = 3000) {
        var alertClass = 'alert-' + type;
        var notification = document.createElement('div');
        notification.className = 'alert ' + alertClass + ' alert-dismissible fade show notification';
        notification.innerHTML = message + '<button type="button" class="btn-close" data-bs-dismiss="alert"></button>';
        
        document.body.appendChild(notification);
        
        setTimeout(function() {
            if (notification.parentNode) {
                notification.remove();
            }
        }, duration);
    };

    // Initialize connection status indicator
    function updateConnectionStatus() {
        var statusElement = document.getElementById('connection-status');
        if (statusElement) {
            if (navigator.onLine) {
                statusElement.className = 'connection-status connected';
                statusElement.textContent = 'Connected';
            } else {
                statusElement.className = 'connection-status disconnected';
                statusElement.textContent = 'Offline';
            }
        }
    }

    window.addEventListener('online', updateConnectionStatus);
    window.addEventListener('offline', updateConnectionStatus);
    updateConnectionStatus();

    // Initialize keyboard shortcuts
    document.addEventListener('keydown', function(e) {
        // Ctrl/Cmd + Enter to submit forms
        if ((e.ctrlKey || e.metaKey) && e.key === 'Enter') {
            var form = e.target.closest('form');
            if (form) {
                e.preventDefault();
                form.submit();
            }
        }
        
        // Escape to close modals
        if (e.key === 'Escape') {
            var modals = document.querySelectorAll('.modal.show');
            modals.forEach(function(modal) {
                var bsModal = bootstrap.Modal.getInstance(modal);
                if (bsModal) {
                    bsModal.hide();
                }
            });
        }
    });

    // Initialize auto-save for forms
    var autoSaveForms = document.querySelectorAll('form[data-auto-save]');
    autoSaveForms.forEach(function(form) {
        var inputs = form.querySelectorAll('input, textarea, select');
        var saveTimeout;
        
        inputs.forEach(function(input) {
            input.addEventListener('input', function() {
                clearTimeout(saveTimeout);
                saveTimeout = setTimeout(function() {
                    // Auto-save logic would go here
                    console.log('Auto-saving form...');
                }, 2000);
            });
        });
    });

    // Initialize smooth scrolling for anchor links
    var anchorLinks = document.querySelectorAll('a[href^="#"]');
    anchorLinks.forEach(function(link) {
        link.addEventListener('click', function(e) {
            var targetId = this.getAttribute('href').substring(1);
            var targetElement = document.getElementById(targetId);
            
            if (targetElement) {
                e.preventDefault();
                targetElement.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });

    // Initialize lazy loading for images
    var images = document.querySelectorAll('img[data-src]');
    var imageObserver = new IntersectionObserver(function(entries, observer) {
        entries.forEach(function(entry) {
            if (entry.isIntersecting) {
                var img = entry.target;
                img.src = img.dataset.src;
                img.classList.remove('lazy');
                imageObserver.unobserve(img);
            }
        });
    });

    images.forEach(function(img) {
        imageObserver.observe(img);
    });

    // Initialize copy to clipboard functionality
    var copyButtons = document.querySelectorAll('[data-copy]');
    copyButtons.forEach(function(button) {
        button.addEventListener('click', function() {
            var text = this.dataset.copy;
            navigator.clipboard.writeText(text).then(function() {
                showNotification('Copied to clipboard!', 'success', 2000);
            }).catch(function() {
                showNotification('Failed to copy to clipboard', 'danger', 3000);
            });
        });
    });

    console.log('CollabStory initialized successfully!');
});
