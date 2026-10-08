// Main Javascript controller for PEIS UI

let debounceTimer = null;
let currentSuggestedCategory = null;
let currentSuggestedMethod = "manual";

function openAddModal() {
    const modal = document.getElementById("addTransactionModal");
    if (modal) {
        modal.classList.add("active");
        const descInput = document.getElementById("tx-description");
        if (descInput) {
            setTimeout(() => descInput.focus(), 100);
        }
    }
}

function closeAddModal() {
    const modal = document.getElementById("addTransactionModal");
    if (modal) {
        modal.classList.remove("active");
    }
}

// Close modal on background click or ESC key
window.addEventListener("click", function(event) {
    const addModal = document.getElementById("addTransactionModal");
    if (event.target === addModal) {
        closeAddModal();
    }
});

window.addEventListener("keydown", function(event) {
    if (event.key === "Escape") {
        closeAddModal();
    }
});

function toggleType(type) {
    // If needed, filter category dropdown options based on type
    const categorySelect = document.getElementById("tx-category");
    if (!categorySelect) return;
    
    // Suggest relevant default if switching to income
    if (type === "income" && (!categorySelect.value || categorySelect.value === "Food & Dining")) {
        categorySelect.value = "Salary";
    }
}

// Real-time Intelligence: Auto-Categorize as user types
function handleDescriptionInput(text) {
    clearTimeout(debounceTimer);
    const box = document.getElementById("auto-cat-box");
    if (!box) return;

    if (!text || text.trim().length < 3) {
        box.classList.remove("visible");
        return;
    }

    debounceTimer = setTimeout(() => {
        fetch("/api/intelligence/categorize", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ description: text })
        })
        .then(res => res.json())
        .then(data => {
            if (data.success && data.category && data.category !== "Miscellaneous") {
                currentSuggestedCategory = data.category;
                currentSuggestedMethod = data.method;

                const nameEl = document.getElementById("auto-cat-name");
                const metaEl = document.getElementById("auto-cat-meta");
                
                if (nameEl) nameEl.textContent = data.category;
                if (metaEl) {
                    const confPct = Math.round(data.confidence * 100);
                    metaEl.textContent = `${data.explanation} (${confPct}% confidence)`;
                }

                box.classList.add("visible");

                // If category is not selected yet, auto select it directly
                const categorySelect = document.getElementById("tx-category");
                if (categorySelect && (!categorySelect.value || categorySelect.value === "Miscellaneous")) {
                    categorySelect.value = data.category;
                    const methodInput = document.getElementById("tx-categorization-method");
                    if (methodInput) methodInput.value = data.method;
                }
            } else {
                box.classList.remove("visible");
            }
        })
        .catch(err => {
            console.error("Categorize error:", err);
            box.classList.remove("visible");
        });
    }, 280); // 280ms debounce
}

function acceptSuggestedCategory() {
    if (!currentSuggestedCategory) return;
    const categorySelect = document.getElementById("tx-category");
    const methodInput = document.getElementById("tx-categorization-method");
    const box = document.getElementById("auto-cat-box");

    if (categorySelect) categorySelect.value = currentSuggestedCategory;
    if (methodInput) methodInput.value = currentSuggestedMethod;
    if (box) box.classList.remove("visible");
}
