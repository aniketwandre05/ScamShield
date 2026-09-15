/**
 * ScamShield - Senior-Friendly Frontend Controller
 * Handles accessible tab switching, file previews, demo sample filling, and font sizing.
 */

document.addEventListener("DOMContentLoaded", function () {
    // 1. Tab Switching (Paste Text vs Upload Screenshot)
    const tabButtons = document.querySelectorAll(".tab-btn");
    const tabPanels = document.querySelectorAll(".tab-panel");

    tabButtons.forEach(button => {
        button.addEventListener("click", () => {
            const targetId = button.getAttribute("data-tab");
            
            tabButtons.forEach(btn => {
                btn.classList.remove("active");
                btn.setAttribute("aria-selected", "false");
            });
            tabPanels.forEach(panel => {
                panel.style.display = "none";
            });

            button.classList.add("active");
            button.setAttribute("aria-selected", "true");
            
            const activePanel = document.getElementById(targetId);
            if (activePanel) {
                activePanel.style.display = "block";
            }
        });
    });

    // 3. File Upload & Drag-and-Drop Handling
    const uploadZones = document.querySelectorAll(".upload-zone");
    uploadZones.forEach(zone => {
        const fileInput = zone.querySelector("input[type='file']");
        const previewContainer = zone.parentElement.querySelector(".file-preview");

        if (!fileInput) return;

        zone.addEventListener("click", (e) => {
            if (e.target !== fileInput) {
                fileInput.click();
            }
        });

        // Drag & Drop events
        ['dragenter', 'dragover'].forEach(eventName => {
            zone.addEventListener(eventName, (e) => {
                e.preventDefault();
                e.stopPropagation();
                zone.classList.add("dragover");
            }, false);
        });

        ['dragleave', 'drop'].forEach(eventName => {
            zone.addEventListener(eventName, (e) => {
                e.preventDefault();
                e.stopPropagation();
                zone.classList.remove("dragover");
            }, false);
        });

        zone.addEventListener("drop", (e) => {
            const dt = e.dataTransfer;
            const files = dt.files;
            if (files && files.length > 0) {
                fileInput.files = files;
                updateFilePreview(files[0], previewContainer);
            }
        });

        fileInput.addEventListener("change", () => {
            if (fileInput.files && fileInput.files[0]) {
                updateFilePreview(fileInput.files[0], previewContainer);
            }
        });
    });

    function updateFilePreview(file, container) {
        if (!container) return;
        const nameEl = container.querySelector(".preview-filename");
        const sizeEl = container.querySelector(".preview-filesize");
        
        if (nameEl) nameEl.textContent = file.name;
        if (sizeEl) sizeEl.textContent = `(${(file.size / 1024).toFixed(1)} KB)`;
        
        container.style.display = "flex";
    }

    // 4. Clear File Buttons
    const clearFileBtns = document.querySelectorAll(".btn-clear-file");
    clearFileBtns.forEach(btn => {
        btn.addEventListener("click", () => {
            const form = btn.closest("form");
            if (form) {
                const fileInput = form.querySelector("input[type='file']");
                if (fileInput) fileInput.value = "";
                const preview = form.querySelector(".file-preview");
                if (preview) preview.style.display = "none";
            }
        });
    });

    // 5. Demo Sample Inserters
    const demoBtns = document.querySelectorAll(".btn-demo");
    demoBtns.forEach(btn => {
        btn.addEventListener("click", () => {
            const targetFieldId = btn.getAttribute("data-target");
            const sampleText = btn.getAttribute("data-text");
            const targetField = document.getElementById(targetFieldId);
            
            if (targetField && sampleText) {
                targetField.value = sampleText;
                targetField.focus();
            }

            // Fill extra fields if provided (e.g. subject/sender for email)
            const extraTarget = btn.getAttribute("data-target-extra");
            const extraText = btn.getAttribute("data-text-extra");
            if (extraTarget && extraText) {
                const extraField = document.getElementById(extraTarget);
                if (extraField) extraField.value = extraText;
            }
            
            const senderTarget = btn.getAttribute("data-target-sender");
            const senderText = btn.getAttribute("data-text-sender");
            if (senderTarget && senderText) {
                const senderField = document.getElementById(senderTarget);
                if (senderField) senderField.value = senderText;
            }
        });
    });
});
