/**
 * ScamShield - Accessible Senior-Friendly Frontend Controller
 * Implements full HCI Usability Checklist:
 * 1. Tab switching & drag-and-drop file preview
 * 2. Form usability: Paste from clipboard, clear input, voice dictation (Web Speech API)
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
    // 2. File Upload & Drag-and-Drop Handling
    // =========================================================================
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

    // Clear File Buttons
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
    // 5. Form Usability: Voice Input Dictation (Web Speech API)
    // =========================================================================
    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
    document.querySelectorAll(".btn-action-voice").forEach(btn => {
        if (!SpeechRecognition) {
            btn.style.display = "none";
            return;
        }
        const targetId = btn.getAttribute("data-target");
        const targetEl = document.getElementById(targetId);
        const langCode = btn.getAttribute("data-lang") || "en";
        
        let recognition = new SpeechRecognition();
        recognition.continuous = false;
        recognition.interimResults = false;
        
        if (langCode === "mr") recognition.lang = "mr-IN";
        else if (langCode === "hi") recognition.lang = "hi-IN";
        else recognition.lang = "en-US";
        
        let isRecording = false;
        btn.addEventListener("click", () => {
            if (isRecording) {
                recognition.stop();
                return;
            }
            try {
                recognition.start();
                isRecording = true;
                btn.classList.add("recording");
                showToast("Listening... please speak clearly.");
            } catch (e) {
                isRecording = false;
                btn.classList.remove("recording");
            }
        });
        
        recognition.onresult = (event) => {
            const transcript = event.results[0][0].transcript;
            if (targetEl) {
                targetEl.value = (targetEl.value ? targetEl.value + " " : "") + transcript;
                targetEl.focus();
            }
            showToast("Speech recognized!");
        };
        recognition.onerror = () => {
            isRecording = false;
            btn.classList.remove("recording");
            showToast("Could not recognize speech. Please try again.");
        };
        recognition.onend = () => {
            isRecording = false;
            btn.classList.remove("recording");
        };
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
                if (!isCorrect) {
                    btn.classList.add("opt-wrong");
                    if (feedbackEl) {
                        feedbackEl.textContent = "❌ Incorrect. Remember: Official institutions never demand immediate action or secret codes.";
                        feedbackEl.style.color = "var(--danger-color)";
                        feedbackEl.style.display = "block";
                    }
                } else {
                    if (feedbackEl) {
                        feedbackEl.textContent = "✅ Correct! Great instincts for spotting fraud traps.";
                        feedbackEl.style.color = "var(--safe-color)";
                        feedbackEl.style.display = "block";
                    }
                }
            });
        });
    });
});
