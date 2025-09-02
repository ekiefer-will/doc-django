// Enhanced script for ResourceLink admin page to show/hide URL and File fields
// based on the selected Link Type with improved debugging and fallback handling.

(function() {
    'use strict';
    
    // Enhanced debugging function
    function debug(message, data) {
        console.log('[ResourceLink Admin]', message, data || '');
    }
    
    function initializeDynamicFields() {
        debug("Initializing dynamic fields script");
        
        // Try multiple jQuery sources
        let $ = null;
        if (window.django && window.django.jQuery) {
            $ = window.django.jQuery;
            debug("Using django.jQuery");
        } else if (window.jQuery) {
            $ = window.jQuery;
            debug("Using window.jQuery");
        } else if (window.$) {
            $ = window.$;
            debug("Using window.$");
        } else {
            debug("ERROR: jQuery not found!");
            return;
        }
        
        // Wait for DOM to be ready
        $(document).ready(function() {
            debug("DOM ready, searching for elements");
            
            // Try multiple selector strategies for the link type field
            let linkTypeDropdown = $('#id_link_type');
            if (linkTypeDropdown.length === 0) {
                linkTypeDropdown = $('select[name="link_type"]');
                debug("Trying alternative selector for link_type");
            }
            if (linkTypeDropdown.length === 0) {
                linkTypeDropdown = $('select').filter(function() {
                    return $(this).attr('name') && $(this).attr('name').includes('link_type');
                });
                debug("Trying wildcard selector for link_type");
            }
            
            // Try multiple selector strategies for field rows
            let urlFieldRow = $('.form-row.field-url');
            if (urlFieldRow.length === 0) {
                urlFieldRow = $('.field-url');
                debug("Trying alternative selector for url field");
            }
            if (urlFieldRow.length === 0) {
                urlFieldRow = $('div').filter(function() {
                    return $(this).find('input[name*="url"]').length > 0;
                });
                debug("Trying input-based selector for url field");
            }
            
            let fileFieldRow = $('.form-row.field-file');
            if (fileFieldRow.length === 0) {
                fileFieldRow = $('.field-file');
                debug("Trying alternative selector for file field");
            }
            if (fileFieldRow.length === 0) {
                fileFieldRow = $('div').filter(function() {
                    return $(this).find('input[type="file"]').length > 0;
                });
                debug("Trying input-based selector for file field");
            }
            
            // Enhanced debugging
            debug("Link Type Dropdown found:", linkTypeDropdown.length > 0);
            debug("Link Type Dropdown ID:", linkTypeDropdown.attr('id'));
            debug("Link Type Dropdown name:", linkTypeDropdown.attr('name'));
            debug("URL Field Row found:", urlFieldRow.length > 0);
            debug("URL Field Row classes:", urlFieldRow.attr('class'));
            debug("File Field Row found:", fileFieldRow.length > 0);
            debug("File Field Row classes:", fileFieldRow.attr('class'));
            
            // Log all available form elements for debugging
            debug("All select elements:", $('select').map(function() { 
                return $(this).attr('name') || $(this).attr('id'); 
            }).get());
            debug("All form rows:", $('.form-row').map(function() { 
                return $(this).attr('class'); 
            }).get());
            
            // Check if we found the required elements
            if (linkTypeDropdown.length === 0) {
                debug("ERROR: Link type dropdown not found!");
                return;
            }
            
            if (urlFieldRow.length === 0 && fileFieldRow.length === 0) {
                debug("ERROR: Neither URL nor File field rows found!");
                return;
            }
            
            function toggleFields() {
                const selectedType = linkTypeDropdown.val();
                debug("Selected link type:", selectedType);
                debug("Available options:", linkTypeDropdown.find('option').map(function() {
                    return $(this).val() + ': ' + $(this).text();
                }).get());
                
                // Hide both fields initially
                urlFieldRow.hide();
                fileFieldRow.hide();
                
                // Show appropriate field based on selection
                if (selectedType === 'EXTERNAL') {
                    urlFieldRow.show();
                    debug("Showing URL field");
                } else if (selectedType === 'UPLOAD') {
                    fileFieldRow.show();
                    debug("Showing File field");
                } else {
                    debug("No matching type, hiding both fields");
                }
                
                // Force a layout recalculation
                urlFieldRow.trigger('change');
                fileFieldRow.trigger('change');
            }
            
            // Set initial state
            debug("Setting initial field state");
            toggleFields();
            
            // Add event listener
            linkTypeDropdown.on('change', function() {
                debug("Link type changed");
                toggleFields();
            });
            
            debug("Script initialization complete");
        });
    }
    
    // Try to initialize immediately if jQuery is available
    if ((window.django && window.django.jQuery) || window.jQuery || window.$) {
        initializeDynamicFields();
    } else {
        // Fallback: wait for Django admin to load
        debug("jQuery not immediately available, waiting for admin load");
        
        // Check every 100ms for up to 10 seconds
        let attempts = 0;
        const maxAttempts = 100;
        
        const checkForJQuery = setInterval(function() {
            attempts++;
            if ((window.django && window.django.jQuery) || window.jQuery || window.$) {
                clearInterval(checkForJQuery);
                debug("jQuery found after", attempts * 100, "ms");
                initializeDynamicFields();
            } else if (attempts >= maxAttempts) {
                clearInterval(checkForJQuery);
                debug("ERROR: jQuery not found after 10 seconds");
            }
        }, 100);
    }
})();