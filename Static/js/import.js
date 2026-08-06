/**
 * Medicine Import Handler
 * MediTracker
 *
 * Handles bulk medicine import through CSV/Excel files with progress UI
 */

document.addEventListener("DOMContentLoaded", function () {

    const importForm = document.getElementById("importForm");
    const fileInput = document.getElementById("medicineFile") || document.querySelector("input[type='file'][name='csv_file']");
    const uploadBtn = document.getElementById("uploadBtn") || document.querySelector("button[type='submit']");

    if (!importForm || !fileInput) {
        return;
    }

    importForm.addEventListener("submit", async function (event) {
        event.preventDefault();

        if (!fileInput.files || !fileInput.files.length) {
            showMessage("Please select a file to import first.", "danger");
            return;
        }

        const file = fileInput.files[0];

        if (!validateFile(file)) {
            showMessage("Only .csv, .xlsx, or .xls files are supported.", "danger");
            return;
        }

        const formData = new FormData();
        formData.append("csv_file", file);
        formData.append("file", file);

        const originalBtnText = uploadBtn ? uploadBtn.innerText : "Import Medicines";
        let progressInterval = null;

        try {
            if (uploadBtn) {
                uploadBtn.disabled = true;
                uploadBtn.innerHTML = `<i class="fa-solid fa-spinner fa-spin me-1"></i> Uploading...`;
            }

            progressInterval = showProgress();

            const targetUrl = importForm.getAttribute("action") || "/import-csv";

            const response = await fetch(targetUrl, {
                method: "POST",
                body: formData
            });

            const contentType = response.headers.get("content-type");
            let result = {};

            if (contentType && contentType.includes("application/json")) {
                result = await response.json();
            }

            if (response.ok) {
                showMessage(
                    result.message || "Medicine import completed successfully!",
                    "success"
                );
                resetProgress(progressInterval);
                importForm.reset();
            } else {
                clearInterval(progressInterval);
                showMessage(
                    result.error || result.message || "Import failed. Please verify file format and columns.",
                    "danger"
                );
            }

        } catch (error) {
            if (progressInterval) clearInterval(progressInterval);
            console.error("Medicine import error:", error);
            showMessage("Server communication error. Please check your network and try again.", "danger");
        } finally {
            if (uploadBtn) {
                uploadBtn.disabled = false;
                uploadBtn.innerText = originalBtnText;
            }
        }
    });

});

/**
 * Validate uploaded file extensions
 */
function validateFile(file) {
    if (!file || !file.name) return false;

    const allowedExtensions = ["csv", "xlsx", "xls"];
    const extension = file.name.split(".").pop().toLowerCase();

    return allowedExtensions.includes(extension);
}

/**
 * Display status alert messages
 */
function showMessage(message, type) {
    const messageBox = document.getElementById("importMessage");

    if (!messageBox) {
        alert(message);
        return;
    }

    messageBox.innerText = message;
    
    // Normalize type for Bootstrap styling
    const alertType = type === "error" ? "danger" : type;
    messageBox.className = `alert alert-${alertType} alert-dismissible fade show mt-3 mb-0`;
    messageBox.setAttribute("role", "alert");
}

/**
 * Progress bar animation generator
 */
function showProgress() {
    const progressBar = document.getElementById("progressBar");

    if (!progressBar) return null;

    progressBar.style.width = "0%";
    let width = 0;

    const interval = setInterval(function () {
        if (width >= 90) {
            clearInterval(interval);
        } else {
            width += 10;
            progressBar.style.width = width + "%";
        }
    }, 200);

    return interval;
}

/**
 * Complete and reset progress bar state
 */
function resetProgress(intervalToClear) {
    if (intervalToClear) clearInterval(intervalToClear);

    const progressBar = document.getElementById("progressBar");

    if (progressBar) {
        progressBar.style.width = "100%";

        setTimeout(function () {
            progressBar.style.width = "0%";
        }, 1000);
    }
}