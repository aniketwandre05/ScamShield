/**
 * ScamShield - Accessible Senior-Friendly Frontend Controller
 * Implements full HCI Usability Checklist:
 * 1. Tab switching & drag-and-drop file preview
 * 2. Form usability: Paste from clipboard and clear input
 * 3. Loading overlay ("Analyzing for scams...") for visibility of system status
 * 4. Text-to-Speech (TTS) audio narration for result accessibility
 * 5. Copy summary & native Web Share API
 * 6. "Was this helpful?" feedback mechanism
 * 7. Dark/Light mode theme switch & Dyslexia / High Contrast accessibility modes
 * 8. Onboarding quick start banner
 * 9. History search & level filter & Print report
 * 10. Learn quiz evaluation
 * 11. Toast notification system
 */

document.addEventListener("DOMContentLoaded", function () {
    // =========================================================================
    // 0. Toast Notification System
    // =========================================================================
    function showToast(message) {
        const container = document.getElementById("toast-container");
        if (!container) return;
        const toast = document.createElement("div");
        toast.className = "toast";
        toast.textContent = message;
        container.appendChild(toast);
        setTimeout(() => {
            toast.style.opacity = "0";
            toast.style.transition = "opacity 0.3s ease";
            setTimeout(() => toast.remove(), 300);
        }, 3500);
    }

    // =========================================================================
    // 1. Tab Switching (Paste Text vs Upload Screenshot)
    // =========================================================================
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

    // =========================================================================
    // 2. File Upload & Drag-and-Drop Handling (Dual "Choose File" & "Take Photo")
    // =========================================================================
    const uploadZones = document.querySelectorAll(".upload-zone");
    uploadZones.forEach(zone => {
        const inputChoose = zone.querySelector(".file-input-choose") || zone.querySelector("input[type='file']:not([capture])");
        const inputCamera = zone.querySelector(".file-input-camera") || zone.querySelector("input[type='file'][capture]");
        const btnChoose = zone.querySelector(".btn-choose-file");
        const btnCamera = zone.querySelector(".btn-take-photo");
        const previewContainer = zone.parentElement ? zone.parentElement.querySelector(".file-preview") : null;
        const form = zone.closest("form");

        function syncFileSelection(sourceInput) {
            if (!sourceInput || !sourceInput.files || !sourceInput.files[0]) return;
            const selectedFile = sourceInput.files[0];
            
            // Ensure the input containing the file has name="screenshot" for submission
            if (sourceInput === inputChoose) {
                inputChoose.name = "screenshot";
                if (inputCamera) inputCamera.name = "";
            } else if (sourceInput === inputCamera) {
                inputCamera.name = "screenshot";
                if (inputChoose) inputChoose.name = "";
                // Attempt to copy to inputChoose via DataTransfer if supported
                try {
                    const dt = new DataTransfer();
                    dt.items.add(selectedFile);
                    if (inputChoose) inputChoose.files = dt.files;
                } catch (err) {
                    // Fallback: inputCamera is named "screenshot"
                }
            }
            updateFilePreview(selectedFile, previewContainer);
        }

        // 1. "Choose File" Button Handler (Android opens Gallery / Files)
        if (btnChoose && inputChoose) {
            btnChoose.addEventListener("click", (e) => {
                e.preventDefault();
                e.stopPropagation();
                inputChoose.name = "screenshot";
                if (inputCamera) inputCamera.name = "";
                inputChoose.click();
            });
        }

        // 2. "Take Photo" Button Handler (Android opens Camera directly)
        if (btnCamera && inputCamera) {
            btnCamera.addEventListener("click", (e) => {
                e.preventDefault();
                e.stopPropagation();
                inputCamera.name = "screenshot";
                if (inputChoose) inputChoose.name = "";
                inputCamera.click();
            });
        }

        // 3. Click anywhere else on zone -> defaults to Choose File
        zone.addEventListener("click", (e) => {
            if (e.target.closest(".btn-browse-file") || e.target.tagName === "INPUT" || e.target.tagName === "BUTTON") {
                return;
            }
            if (inputChoose) {
                inputChoose.name = "screenshot";
                if (inputCamera) inputCamera.name = "";
                inputChoose.click();
            } else if (inputCamera) {
                inputCamera.name = "screenshot";
                inputCamera.click();
            }
        });

        // 4. Change event listeners
        if (inputChoose) {
            inputChoose.addEventListener("change", () => {
                if (inputChoose.files && inputChoose.files[0]) {
                    syncFileSelection(inputChoose);
                }
            });
        }

        if (inputCamera) {
            inputCamera.addEventListener("change", () => {
                if (inputCamera.files && inputCamera.files[0]) {
                    syncFileSelection(inputCamera);
                }
            });
        }

        // 5. Drag & Drop events
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
            const files = dt ? dt.files : null;
            if (files && files.length > 0 && inputChoose) {
                inputChoose.files = files;
                syncFileSelection(inputChoose);
            }
        });

        // 6. Form submit validation for screenshot mode
        if (form) {
            form.addEventListener("submit", (e) => {
                const modeInput = form.querySelector("input[name='input_mode']");
                if (modeInput && modeInput.value === "screenshot") {
                    const hasChooseFile = inputChoose && inputChoose.files && inputChoose.files.length > 0;
                    const hasCameraFile = inputCamera && inputCamera.files && inputCamera.files.length > 0;
                    if (!hasChooseFile && !hasCameraFile) {
                        e.preventDefault();
                        e.stopPropagation();
                        showToast("Please choose a screenshot file or take a photo first.");
                        zone.focus();
                    }
                }
            });
        }
    });

    function updateFilePreview(file, container) {
        if (!container) return;
        const nameEl = container.querySelector(".preview-filename");
        const sizeEl = container.querySelector(".preview-filesize");
        
        if (nameEl) nameEl.textContent = file.name;
        if (sizeEl) sizeEl.textContent = `(${(file.size / 1024).toFixed(1)} KB)`;
        
        container.style.display = "flex";
    }

    // Clear File Buttons
    const clearFileBtns = document.querySelectorAll(".btn-clear-file");
    clearFileBtns.forEach(btn => {
        btn.addEventListener("click", () => {
            const form = btn.closest("form");
            if (form) {
                const fileInputs = form.querySelectorAll("input[type='file']");
                fileInputs.forEach(fi => { fi.value = ""; });
                const inputChoose = form.querySelector(".file-input-choose");
                const inputCamera = form.querySelector(".file-input-camera");
                if (inputChoose) inputChoose.name = "screenshot";
                if (inputCamera) inputCamera.name = "";

                const preview = form.querySelector(".file-preview");
                if (preview) preview.style.display = "none";
                showToast("File removed.");
            }
        });
    });

    // =========================================================================
    // 3. Demo Sample Inserters
    // =========================================================================
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

    // =========================================================================
    // 4. Form Usability: Paste from Clipboard & Clear Input
    // =========================================================================
    document.querySelectorAll(".btn-action-paste").forEach(btn => {
        btn.addEventListener("click", async () => {
            const targetId = btn.getAttribute("data-target");
            const targetEl = document.getElementById(targetId);
            if (!targetEl) return;
            try {
                const text = await navigator.clipboard.readText();
                if (text) {
                    targetEl.value = text;
                    targetEl.focus();
                    showToast("Pasted from clipboard!");
                }
            } catch (err) {
                showToast("Clipboard permission not granted. Use Ctrl+V to paste.");
            }
        });
    });

    document.querySelectorAll(".btn-action-clear").forEach(btn => {
        btn.addEventListener("click", () => {
            const targetId = btn.getAttribute("data-target");
            const targetEl = document.getElementById(targetId);
            if (targetEl) {
                targetEl.value = "";
                targetEl.focus();
                showToast("Input cleared.");
            }
        });
    });


    // =========================================================================
    // 6. Visibility of System Status: Analyzing Loading Overlay
    // =========================================================================
    const overlay = document.getElementById("analyzing-overlay");
    if (overlay) {
        document.querySelectorAll("form").forEach(form => {
            const action = form.getAttribute("action") || "";
            if (action.includes("/analyze/")) {
                form.addEventListener("submit", (e) => {
                    const inputs = form.querySelectorAll("[required]");
                    let isValid = true;
                    inputs.forEach(inp => {
                        if (!inp.value.trim()) isValid = false;
                    });
                    if (isValid) {
                        overlay.style.display = "flex";
                    }
                });
            }
        });
    }

    // =========================================================================
    // 7. Text-to-Speech (TTS) Narration for Results
    // =========================================================================
    const btnReadAloud = document.getElementById("btn-read-aloud");
    if (btnReadAloud && "speechSynthesis" in window) {
        let isPlaying = false;
        btnReadAloud.addEventListener("click", () => {
            if (isPlaying) {
                window.speechSynthesis.cancel();
                isPlaying = false;
                btnReadAloud.classList.remove("active-audio");
                btnReadAloud.textContent = "🔊 Read Aloud";
                return;
            }
            
            const summaryText = document.getElementById("result-summary-text")?.textContent || "";
            const scoreText = document.querySelector(".risk-score-number")?.textContent || "";
            const fullText = `Assessment result: ${scoreText}. ${summaryText}`;
            
            const utterance = new SpeechSynthesisUtterance(fullText);
            const lang = btnReadAloud.getAttribute("data-lang") || "en";
            if (lang === "mr") utterance.lang = "mr-IN";
            else if (lang === "hi") utterance.lang = "hi-IN";
            else utterance.lang = "en-US";
            
            utterance.onend = () => {
                isPlaying = false;
                btnReadAloud.classList.remove("active-audio");
                btnReadAloud.textContent = "🔊 Read Aloud";
            };
            utterance.onerror = () => {
                isPlaying = false;
                btnReadAloud.classList.remove("active-audio");
                btnReadAloud.textContent = "🔊 Read Aloud";
            };
            
            window.speechSynthesis.speak(utterance);
            isPlaying = true;
            btnReadAloud.classList.add("active-audio");
            btnReadAloud.textContent = "⏹️ Stop Audio";
        });
    }

    // =========================================================================
    // 8. Result Actions: Copy Summary & Native Web Share
    // =========================================================================
    const btnCopySummary = document.getElementById("btn-copy-summary");
    if (btnCopySummary) {
        btnCopySummary.addEventListener("click", async () => {
            const summary = document.getElementById("result-summary-text")?.textContent?.trim() || "";
            const score = document.querySelector(".risk-score-number")?.textContent?.trim() || "";
            const shareText = `[ScamShield Result] Safety Score: ${score}\n${summary}\nVerified with ScamShield AI.`;
            try {
                await navigator.clipboard.writeText(shareText);
                showToast("Result summary copied to clipboard!");
            } catch (e) {
                showToast("Could not copy to clipboard.");
            }
        });
    }

    const btnShareWarning = document.getElementById("btn-share-warning");
    if (btnShareWarning) {
        btnShareWarning.addEventListener("click", async () => {
            const summary = document.getElementById("result-summary-text")?.textContent?.trim() || "";
            const score = document.querySelector(".risk-score-number")?.textContent?.trim() || "";
            const shareData = {
                title: "ScamShield Scam Alert",
                text: `⚠️ Security Alert from ScamShield:\nScore: ${score}\n${summary}\nStay safe!`,
                url: window.location.origin
            };
            if (navigator.share) {
                try {
                    await navigator.share(shareData);
                } catch (e) {
                    // user cancelled share
                }
            } else {
                await navigator.clipboard.writeText(`${shareData.text}\n${shareData.url}`);
                showToast("Share text copied to clipboard!");
            }
        });
    }

    // =========================================================================
    // 9. Assessment Feedback: "Was this helpful?"
    // =========================================================================
    document.querySelectorAll(".btn-feedback").forEach(btn => {
        btn.addEventListener("click", async () => {
            const val = btn.getAttribute("data-val");
            const widget = btn.closest(".result-feedback-widget");
            const responseEl = widget.querySelector(".feedback-response");
            const btns = widget.querySelector(".feedback-btns");
            
            try {
                await fetch("/api/feedback", {
                    method: "POST",
                    headers: { "Content-Type": "application/json" },
                    body: JSON.stringify({ helpful: val === "yes", url: window.location.href })
                });
            } catch (e) {
                // Ignore network issues for feedback
            }
            
            if (btns) btns.style.display = "none";
            if (responseEl) responseEl.style.display = "block";
            showToast("Thank you for your feedback!");
        });
    });

    // =========================================================================
    // 10. Dark Mode & Accessibility Modes (localStorage)
    // =========================================================================
    const themeBtn = document.getElementById("theme-toggle-btn");
    const themeIcon = document.getElementById("theme-icon");
    const savedTheme = localStorage.getItem("scamshield_theme");
    if (savedTheme === "dark") {
        document.body.classList.add("theme-dark");
        if (themeIcon) themeIcon.textContent = "☀️";
    }
    if (themeBtn) {
        themeBtn.addEventListener("click", () => {
            document.body.classList.toggle("theme-dark");
            const isDark = document.body.classList.contains("theme-dark");
            localStorage.setItem("scamshield_theme", isDark ? "dark" : "light");
            if (themeIcon) themeIcon.textContent = isDark ? "☀️" : "🌙";
            showToast(isDark ? "Dark mode activated" : "Light mode activated");
        });
    }

    const a11yBtn = document.getElementById("a11y-menu-btn");
    const a11yDropdown = document.getElementById("a11y-dropdown");
    if (a11yBtn && a11yDropdown) {
        a11yBtn.addEventListener("click", (e) => {
            e.stopPropagation();
            const isExpanded = a11yDropdown.classList.toggle("show");
            a11yBtn.setAttribute("aria-expanded", isExpanded);
        });
        document.addEventListener("click", () => {
            a11yDropdown.classList.remove("show");
            a11yBtn.setAttribute("aria-expanded", "false");
        });
    }

    const btnDyslexia = document.getElementById("btn-toggle-dyslexia");
    if (localStorage.getItem("scamshield_dyslexia") === "true") {
        document.body.classList.add("font-dyslexia");
        btnDyslexia?.classList.add("active");
    }
    btnDyslexia?.addEventListener("click", () => {
        document.body.classList.toggle("font-dyslexia");
        const active = document.body.classList.contains("font-dyslexia");
        btnDyslexia.classList.toggle("active", active);
        localStorage.setItem("scamshield_dyslexia", active ? "true" : "false");
        showToast(active ? "Dyslexia-friendly font enabled" : "Standard font restored");
    });

    const btnContrast = document.getElementById("btn-toggle-contrast");
    if (localStorage.getItem("scamshield_contrast") === "true") {
        document.body.classList.add("high-contrast");
        btnContrast?.classList.add("active");
    }
    btnContrast?.addEventListener("click", () => {
        document.body.classList.toggle("high-contrast");
        const active = document.body.classList.contains("high-contrast");
        btnContrast.classList.toggle("active", active);
        localStorage.setItem("scamshield_contrast", active ? "true" : "false");
        showToast(active ? "High contrast mode enabled" : "Standard contrast restored");
    });

    // =========================================================================
    // 11. Onboarding Guide Dismissal (localStorage)
    // =========================================================================
    const onboardingGuide = document.getElementById("onboarding-guide");
    const btnDismissOnboarding = document.getElementById("btn-dismiss-onboarding");
    if (localStorage.getItem("scamshield_onboarding_dismissed") === "true" && onboardingGuide) {
        onboardingGuide.style.display = "none";
    }
    if (btnDismissOnboarding && onboardingGuide) {
        btnDismissOnboarding.addEventListener("click", () => {
            onboardingGuide.style.display = "none";
            localStorage.setItem("scamshield_onboarding_dismissed", "true");
        });
    }

    // =========================================================================
    // 12. History Search & Risk Filter & Print Report
    // =========================================================================
    const historySearch = document.getElementById("history-search");
    const historyFilter = document.getElementById("history-filter-level");
    const historyCards = document.querySelectorAll(".history-item-card");
    const noMatchEl = document.getElementById("history-no-match");
    const btnPrintHistory = document.getElementById("btn-print-history");

    function applyHistoryFilters() {
        if (!historyCards.length) return;
        const q = (historySearch?.value || "").toLowerCase().trim();
        const level = (historyFilter?.value || "all").toLowerCase();
        let visibleCount = 0;

        historyCards.forEach(card => {
            const cardText = card.getAttribute("data-text") || "";
            const cardLevel = card.getAttribute("data-level") || "";
            const matchesQuery = !q || cardText.includes(q);
            const matchesLevel = level === "all" || cardLevel === level;

            if (matchesQuery && matchesLevel) {
                card.style.display = "flex";
                visibleCount++;
            } else {
                card.style.display = "none";
            }
        });

        if (noMatchEl) {
            noMatchEl.style.display = visibleCount === 0 ? "block" : "none";
        }

        const countBadge = document.getElementById("history-count-badge");
        if (countBadge) {
            const templateFilter = countBadge.getAttribute("data-template-filter") || "Showing {visible} of {total} scans";
            const templateAll = countBadge.getAttribute("data-template-all") || "Showing {count} scans";
            if (visibleCount === historyCards.length) {
                countBadge.textContent = templateAll.replace("{count}", visibleCount);
            } else {
                countBadge.textContent = templateFilter.replace("{visible}", visibleCount).replace("{total}", historyCards.length);
            }
        }
    }

    historySearch?.addEventListener("input", applyHistoryFilters);
    historyFilter?.addEventListener("change", applyHistoryFilters);
    btnPrintHistory?.addEventListener("click", () => window.print());

    // =========================================================================
    // 13. Learn Page Quiz Interaction
    // =========================================================================
    document.querySelectorAll(".quiz-card").forEach(card => {
        const buttons = card.querySelectorAll(".btn-quiz-opt");
        const feedbackEl = card.querySelector(".quiz-feedback");
        buttons.forEach(btn => {
            btn.addEventListener("click", () => {
                const isCorrect = btn.getAttribute("data-correct") === "true";
                buttons.forEach(b => {
                    b.disabled = true;
                    if (b.getAttribute("data-correct") === "true") {
                        b.classList.add("opt-correct");
                    }
                });
                const correctMsg = card.getAttribute("data-feedback-correct") || "✅ Correct! Great instincts for spotting fraud traps.";
                const wrongMsg = card.getAttribute("data-feedback-wrong") || "❌ Incorrect. Remember: Official institutions never demand immediate action or secret codes.";
                if (!isCorrect) {
                    btn.classList.add("opt-wrong");
                    if (feedbackEl) {
                        feedbackEl.textContent = wrongMsg;
                        feedbackEl.style.color = "var(--danger-color)";
                        feedbackEl.style.display = "block";
                    }
                } else {
                    if (feedbackEl) {
                        feedbackEl.textContent = correctMsg;
                        feedbackEl.style.color = "var(--safe-color)";
                        feedbackEl.style.display = "block";
                    }
                }
            });
        });
    });

    // =========================================================================
    // 14. Font Size Scaling Controls (ISO 9241 Individualisation & WCAG 1.4.4)
    // =========================================================================
    const btnFontDec = document.getElementById("btn-font-decrease");
    const btnFontReset = document.getElementById("btn-font-reset");
    const btnFontInc = document.getElementById("btn-font-increase");

    const FONT_CLASSES = ["font-size-sm", "font-size-md", "font-size-lg", "font-size-xl"];
    const ZOOM_FACTORS = [0.88, 1.0, 1.18, 1.35];
    const BASE_FONT_SIZES = ["15px", "18px", "21px", "24px"];
    let currentFontIndex = 1; // default md (18px)

    function applyFontSize(index, notify = true) {
        currentFontIndex = Math.max(0, Math.min(FONT_CLASSES.length - 1, index));
        FONT_CLASSES.forEach(cls => document.body.classList.remove(cls));
        const selectedClass = FONT_CLASSES[currentFontIndex];
        document.body.classList.add(selectedClass);
        localStorage.setItem("scamshield_font_size", selectedClass);

        // 1. Direct visual zoom on body (scales all text, cards, buttons proportionally)
        const factor = ZOOM_FACTORS[currentFontIndex];
        document.body.style.zoom = factor;

        // 2. Set root CSS custom property for responsive multipliers
        document.documentElement.style.setProperty("--font-scale", factor);

        // 3. Set base font size on html & body
        const basePx = BASE_FONT_SIZES[currentFontIndex];
        document.documentElement.style.fontSize = basePx;
        document.body.style.fontSize = basePx;

        // Update active button indicators
        [btnFontDec, btnFontReset, btnFontInc].forEach(b => b?.classList.remove("active"));
        if (currentFontIndex === 1) btnFontReset?.classList.add("active");
        else if (currentFontIndex > 1) btnFontInc?.classList.add("active");
        else btnFontDec?.classList.add("active");

        if (notify) {
            const labels = ["Smaller (-12%)", "Standard (Default)", "Large (+18%)", "Extra Large (+35%)"];
            showToast(`Text size: ${labels[currentFontIndex]}`);
        }
    }

    const savedFont = localStorage.getItem("scamshield_font_size");
    if (savedFont && FONT_CLASSES.includes(savedFont)) {
        currentFontIndex = FONT_CLASSES.indexOf(savedFont);
        applyFontSize(currentFontIndex, false);
    } else {
        applyFontSize(1, false);
    }

    btnFontDec?.addEventListener("click", () => applyFontSize(currentFontIndex - 1));
    btnFontReset?.addEventListener("click", () => applyFontSize(1));
    btnFontInc?.addEventListener("click", () => applyFontSize(currentFontIndex + 1));

    // =========================================================================
    // 15. Keyboard Navigation Shortcuts (Shneiderman Rule #2 Shortcuts)
    // =========================================================================
    document.addEventListener("keydown", function (e) {
        // Do not trigger shortcuts when typing inside form inputs
        const activeTag = document.activeElement ? document.activeElement.tagName.toLowerCase() : "";
        if (activeTag === "input" || activeTag === "textarea" || activeTag === "select") {
            return;
        }

        // Close modal on Escape
        if (e.key === "Escape") {
            const modalBackdrop = document.getElementById("accessible-modal-backdrop");
            if (modalBackdrop && modalBackdrop.style.display !== "none") {
                modalBackdrop.style.display = "none";
            }
        }

        // Shortcuts on Home Page
        if (window.location.pathname === "/" || window.location.pathname === "") {
            if (e.key === "1") {
                document.getElementById("card-sms")?.click();
            } else if (e.key === "2") {
                document.getElementById("card-email")?.click();
            } else if (e.key === "3") {
                document.getElementById("card-url")?.click();
            } else if (e.key === "4") {
                document.getElementById("card-phone")?.click();
            }
        }
    });

    // =========================================================================
    // 16. Phone Questionnaire Live Progress Bar (Nielsen Heuristic #1)
    // =========================================================================
    const phoneForm = document.getElementById("phone-form");
    if (phoneForm) {
        const radios = phoneForm.querySelectorAll("input[type='radio']");
        const countEl = document.getElementById("answered-count");
        const percentEl = document.getElementById("answered-percent");
        const fillEl = document.getElementById("phone-progress-fill");

        function updatePhoneProgress() {
            const answeredIds = new Set();
            radios.forEach(r => {
                if (r.checked) answeredIds.add(r.name);
            });
            const count = answeredIds.size;
            const pct = Math.round((count / 10) * 100);

            if (countEl) countEl.textContent = count;
            if (percentEl) percentEl.textContent = `${pct}%`;
            if (fillEl) fillEl.style.width = `${pct}%`;
        }

        radios.forEach(r => r.addEventListener("change", updatePhoneProgress));
        updatePhoneProgress();

        document.getElementById("btn-reset-phone")?.addEventListener("click", () => {
            setTimeout(updatePhoneProgress, 50);
            showToast("All answers have been reset.");
        });
    }

    // =========================================================================
    // 17. Progressive Disclosure Accordion (Hick-Hyman Law)
    // =========================================================================
    const btnToggleDetails = document.getElementById("btn-toggle-details");
    const detailsContent = document.getElementById("result-details-content");

    btnToggleDetails?.addEventListener("click", () => {
        const isExpanded = btnToggleDetails.getAttribute("aria-expanded") === "true";
        if (isExpanded) {
            btnToggleDetails.setAttribute("aria-expanded", "false");
            if (detailsContent) detailsContent.style.display = "none";
            const icon = btnToggleDetails.querySelector(".toggle-icon");
            if (icon) icon.textContent = "▶";
        } else {
            btnToggleDetails.setAttribute("aria-expanded", "true");
            if (detailsContent) detailsContent.style.display = "block";
            const icon = btnToggleDetails.querySelector(".toggle-icon");
            if (icon) icon.textContent = "▼";
        }
    });

    // =========================================================================
    // 18. Accessible Confirmation Modal for Clear History (Shneiderman #5 & #6)
    // =========================================================================
    const btnOpenClearModal = document.getElementById("btn-open-clear-modal");
    const modalBackdrop = document.getElementById("accessible-modal-backdrop");
    const btnModalCancel = document.getElementById("modal-btn-cancel");
    const btnModalConfirm = document.getElementById("modal-btn-confirm");
    const formClearHistory = document.getElementById("form-clear-history");

    if (btnOpenClearModal && modalBackdrop) {
        btnOpenClearModal.addEventListener("click", () => {
            modalBackdrop.style.display = "flex";
            btnModalCancel?.focus();
        });

        btnModalCancel?.addEventListener("click", () => {
            modalBackdrop.style.display = "none";
            btnOpenClearModal.focus();
        });

        btnModalConfirm?.addEventListener("click", () => {
            modalBackdrop.style.display = "none";
            formClearHistory?.submit();
        });
    }

    // =========================================================================
    // 19. Form Reset Helpers & Validation (Shneiderman Rule #6)
    // =========================================================================
    document.querySelectorAll(".btn-reset-form").forEach(btn => {
        btn.addEventListener("click", () => {
            const targetId = btn.getAttribute("data-target");
            const targetEl = document.getElementById(targetId);
            if (targetEl) targetEl.value = "";

            const targetExtra = btn.getAttribute("data-target-extra");
            if (targetExtra) {
                const extraEl = document.getElementById(targetExtra);
                if (extraEl) extraEl.value = "";
            }

            const targetSender = btn.getAttribute("data-target-sender");
            if (targetSender) {
                const senderEl = document.getElementById(targetSender);
                if (senderEl) senderEl.value = "";
            }

            showToast("Form cleared.");
            targetEl?.focus();
        });
    });
});
