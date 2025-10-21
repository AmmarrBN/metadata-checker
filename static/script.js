let currentFileId = null;

// Initialize
document.addEventListener("DOMContentLoaded", () => {
    initializeToolsStatus();
    setupUploadArea();
    setupEventListeners();
    loadSupportedFields('common'); // Load common fields by default
});

function initializeToolsStatus() {
    const statusEl = document.getElementById("exiftoolStatus");
    fetch("/api/tools-status")
        .then(res => res.json())
        .then(data => {
            const availableTools = Object.entries(data).filter(([_, available]) => available).length;
            statusEl.textContent = `Tools Available: ${availableTools}/7`;
            statusEl.classList.remove("error");
        })
        .catch(() => {
            statusEl.textContent = "Unable to check tools status";
            statusEl.classList.add("error");
        });
}

function setupUploadArea() {
    const uploadArea = document.getElementById("uploadArea");
    const fileInput = document.getElementById("fileInput");

    uploadArea.addEventListener("click", () => fileInput.click());

    uploadArea.addEventListener("dragover", (e) => {
        e.preventDefault();
        uploadArea.classList.add("dragover");
    });

    uploadArea.addEventListener("dragleave", () => {
        uploadArea.classList.remove("dragover");
    });

    uploadArea.addEventListener("drop", (e) => {
        e.preventDefault();
        uploadArea.classList.remove("dragover");
        if (e.dataTransfer.files.length) {
            handleFileUpload(e.dataTransfer.files[0]);
        }
    });

    fileInput.addEventListener("change", (e) => {
        if (e.target.files.length) {
            handleFileUpload(e.target.files[0]);
        }
    });
}

function setupEventListeners() {
    document.getElementById("addMetadataBtn").addEventListener("click", () => {
        document.getElementById("addMetadataForm").style.display = "block";
    });

    document.getElementById("cancelAddMetadataBtn").addEventListener("click", () => {
        document.getElementById("addMetadataForm").style.display = "none";
        document.getElementById("newMetadataKey").value = "";
        document.getElementById("newMetadataValue").value = "";
        document.getElementById("fieldPreset").value = "";
        document.getElementById("fieldType").value = "common";
        handleFieldTypeChange();
    });

    document.getElementById("saveNewMetadataBtn").addEventListener("click", saveNewMetadata);

    document.getElementById("downloadBtn").addEventListener("click", downloadFile);
    document.getElementById("deleteBtn").addEventListener("click", deleteFile);
    document.getElementById("uploadNewBtn").addEventListener("click", resetUpload);

    document.getElementById("searchMetadata").addEventListener("input", filterMetadata);
    
    document.getElementById("fieldType").addEventListener("change", handleFieldTypeChange);
    document.getElementById("fieldPreset").addEventListener("change", handleFieldPresetChange);
}

function handleFieldTypeChange() {
    const fieldType = document.getElementById("fieldType").value;
    const fieldPreset = document.getElementById("fieldPreset");
    const customField = document.getElementById("newMetadataKey");
    
    if (fieldType === "custom") {
        fieldPreset.style.display = "none";
        customField.style.display = "block";
        customField.value = "";
    } else {
        fieldPreset.style.display = "block";
        customField.style.display = "none";
        loadSupportedFields(fieldType);
    }
}

function handleFieldPresetChange() {
    const selectedField = document.getElementById("fieldPreset").value;
    if (selectedField) {
        // You can add auto-suggested values here if needed
    }
}

function loadSupportedFields(type) {
    fetch(`/api/supported-fields?type=${type}`)
        .then(res => res.json())
        .then(data => {
            const fieldPreset = document.getElementById("fieldPreset");
            fieldPreset.innerHTML = '<option value="">Select a field...</option>';
            
            data.fields.forEach(field => {
                const option = document.createElement("option");
                option.value = field;
                option.textContent = field;
                fieldPreset.appendChild(option);
            });
        })
        .catch(err => {
            console.error("Failed to load supported fields:", err);
        });
}

function handleFileUpload(file) {
    showSpinner(true);

    const formData = new FormData();
    formData.append("file", file);

    fetch("/api/upload", {
        method: "POST",
        body: formData,
    })
    .then((res) => res.json())
    .then((data) => {
        if (data.success) {
            currentFileId = data.file_id;
            displayFileInfo(data.metadata.file_info);
            displayAllMetadata(data.metadata);
            showToast("File uploaded successfully", "success");
        } else {
            showToast(data.error || "Upload failed", "error");
        }
    })
    .catch((err) => {
        showToast("Upload error: " + err.message, "error");
    })
    .finally(() => showSpinner(false));
}

function displayFileInfo(fileInfo) {
    const fileInfoSection = document.getElementById("fileInfoSection");
    const fileInfoDiv = document.getElementById("fileInfo");

    const html = `
        <div class="file-info-item">
            <span class="file-info-label">Name</span>
            <span class="file-info-value">${escapeHtml(fileInfo.name)}</span>
        </div>
        <div class="file-info-item">
            <span class="file-info-label">Type</span>
            <span class="file-info-value">${escapeHtml(fileInfo.mime_type)}</span>
        </div>
        <div class="file-info-item">
            <span class="file-info-label">Size</span>
            <span class="file-info-value">${escapeHtml(fileInfo.size_formatted)}</span>
        </div>
        <div class="file-info-item">
            <span class="file-info-label">Modified</span>
            <span class="file-info-value">${new Date(fileInfo.modified).toLocaleString()}</span>
        </div>
    `;

    fileInfoDiv.innerHTML = html;
    fileInfoSection.style.display = "block";
}

function displayAllMetadata(metadata) {
    const metadataSection = document.getElementById("metadataSection");
    const metadataList = document.getElementById("metadataList");
    const emptyState = document.getElementById("emptyState");

    let html = '';

    // Display metadata from all tools
    Object.entries(metadata).forEach(([toolName, toolData]) => {
        if (toolData && typeof toolData === 'object') {
            if (toolData.error) {
                html += `<div class="metadata-tool-section">
                            <h3>${escapeHtml(toolName.toUpperCase())}</h3>
                            <div class="metadata-item">
                                <div class="metadata-value error">${escapeHtml(toolData.error)}</div>
                            </div>
                         </div>`;
            } else if (Object.keys(toolData).length > 0) {
                html += `<div class="metadata-tool-section">
                            <h3>${escapeHtml(toolName.toUpperCase())}</h3>
                            ${displayMetadataObject(toolData, toolName)}
                         </div>`;
            }
        }
    });

    metadataList.innerHTML = html || '<div class="metadata-item"><div class="metadata-value">No metadata found</div></div>';
    metadataSection.style.display = "block";
    emptyState.style.display = "none";
}

function displayMetadataObject(obj, prefix = '') {
    let html = '';
    Object.entries(obj).forEach(([key, value]) => {
        if (value && typeof value === 'object' && !Array.isArray(value)) {
            html += displayMetadataObject(value, `${prefix}_${key}`);
        } else if (Array.isArray(value)) {
            html += `
                <div class="metadata-item">
                    <div class="metadata-key">${escapeHtml(key)}</div>
                    <div class="metadata-value">${escapeHtml(JSON.stringify(value, null, 2))}</div>
                </div>
            `;
        } else if (value !== null && value !== undefined) {
            const displayKey = key.replace(/([A-Z])/g, ' $1').replace(/^./, str => str.toUpperCase());
            html += `
                <div class="metadata-item">
                    <div class="metadata-key">${escapeHtml(displayKey)}</div>
                    <div class="metadata-value">${escapeHtml(String(value))}</div>
                </div>
            `;
        }
    });
    return html;
}

function saveNewMetadata() {
    const fieldType = document.getElementById("fieldType").value;
    let key;
    
    if (fieldType === "custom") {
        key = document.getElementById("newMetadataKey").value.trim();
    } else {
        key = document.getElementById("fieldPreset").value.trim();
    }
    
    const value = document.getElementById("newMetadataValue").value.trim();

    if (!key || !value) {
        showToast("Please fill in all fields", "error");
        return;
    }

    // Clean the key - remove spaces
    key = key.replace(/\s/g, '');

    if (!/^[a-zA-Z0-9]+$/.test(key)) {
        showToast("Invalid field name. Use only letters and numbers.", "error");
        return;
    }

    if (!currentFileId) {
        showToast("No file selected", "error");
        return;
    }

    showSpinner(true);

    fetch(`/api/metadata/${currentFileId}`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ metadata: { [key]: value } }),
    })
    .then((res) => res.json())
    .then((data) => {
        if (data.success) {
            fetch(`/api/metadata/${currentFileId}`)
                .then(res => res.json())
                .then(metadata => {
                    displayAllMetadata(metadata);
                    document.getElementById("addMetadataForm").style.display = "none";
                    document.getElementById("newMetadataKey").value = "";
                    document.getElementById("newMetadataValue").value = "";
                    document.getElementById("fieldPreset").value = "";
                    document.getElementById("fieldType").value = "common";
                    handleFieldTypeChange();
                    showToast("Metadata added successfully", "success");
                });
        } else {
            showToast(data.error || "Failed to add metadata", "error");
        }
    })
    .catch((err) => showToast("Error: " + err.message, "error"))
    .finally(() => showSpinner(false));
}

function filterMetadata() {
    const searchTerm = document.getElementById("searchMetadata").value.toLowerCase();
    const items = document.querySelectorAll(".metadata-item");

    items.forEach((item) => {
        const key = item.querySelector(".metadata-key").textContent.toLowerCase();
        const value = item.querySelector(".metadata-value").textContent.toLowerCase();
        item.style.display = key.includes(searchTerm) || value.includes(searchTerm) ? "block" : "none";
    });
}

function downloadFile() {
    if (!currentFileId) return;
    window.location.href = `/api/download/${currentFileId}`;
    showToast("Download started", "success");
}

function deleteFile() {
    if (!currentFileId) return;

    if (!confirm("Are you sure you want to delete this file?")) return;

    showSpinner(true);

    fetch(`/api/delete/${currentFileId}`, { method: "DELETE" })
    .then((res) => res.json())
    .then((data) => {
        if (data.success) {
            resetUpload();
            showToast("File deleted successfully", "success");
        } else {
            showToast(data.error || "Delete failed", "error");
        }
    })
    .catch((err) => showToast("Error: " + err.message, "error"))
    .finally(() => showSpinner(false));
}

function resetUpload() {
    currentFileId = null;
    document.getElementById("fileInput").value = "";
    document.getElementById("fileInfoSection").style.display = "none";
    document.getElementById("metadataSection").style.display = "none";
    document.getElementById("emptyState").style.display = "flex";
    document.getElementById("addMetadataForm").style.display = "none";
    document.getElementById("searchMetadata").value = "";
}

function showSpinner(show) {
    document.getElementById("spinner").style.display = show ? "block" : "none";
}

function showToast(message, type = "info") {
    const toast = document.getElementById("toast");
    toast.textContent = message;
    toast.className = `toast show ${type}`;
    setTimeout(() => toast.classList.remove("show"), 3000);
}

function escapeHtml(text) {
    const div = document.createElement("div");
    div.textContent = text;
    return div.innerHTML;
}
