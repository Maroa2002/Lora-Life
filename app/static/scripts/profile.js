document.addEventListener("DOMContentLoaded", function () {
    const searchInput = document.getElementById("search-input");
    const appointmentRows = document.querySelectorAll("tbody tr");
    
    searchInput.addEventListener("input", function () {
        const searchTerm = searchInput.value.toLowerCase();
        appointmentRows.forEach(row => {
            const name = row.querySelector("td:first-child").textContent.toLowerCase();
            const lastName = row.querySelector("td:nth-child(2)").textContent.toLowerCase();
            const phone = row.querySelector("td:nth-child(3)").textContent.toLowerCase();
            
            if (name.includes(searchTerm) || lastName.includes(searchTerm) || phone.includes(searchTerm)) {
                row.style.display = "table-row";
            } else {
                row.style.display = "none";
            }
        });
    });

    const statusButtons = document.querySelectorAll(".status");
    statusButtons.forEach(button => {
        button.addEventListener("click", function () {
            const currentStatus = this.textContent.trim().toLowerCase();
            let newStatus;
            
            if (currentStatus === "open") {
                newStatus = "Pending";
                this.classList.remove("open");
                this.classList.add("pending");
            } else if (currentStatus === "pending") {
                newStatus = "Completed";
                this.classList.remove("pending");
                this.classList.add("completed");
            } else {
                newStatus = "Open";
                this.classList.remove("completed");
                this.classList.add("open");
            }
            
            this.textContent = newStatus;
        });
    });

    const deleteButtons = document.querySelectorAll(".delete");
    deleteButtons.forEach(button => {
        button.addEventListener("click", function () {
            const row = this.closest("tr");
            row.remove();
        });
    });
});