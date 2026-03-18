let capsules = JSON.parse(localStorage.getItem("capsules")) || [];

displayCapsules();

function addMessage() {
    let message = document.getElementById("message").value;
    let date = document.getElementById("date").value;

    if (message === "" || date === "") {
        alert("Please fill all fields!");
        return;
    }

    let capsule = {
        id: Date.now(),
        message: message,
        date: date
    };

    capsules.push(capsule);
    saveData();
    displayCapsules();
}

function displayCapsules() {
    let container = document.getElementById("capsules");
    container.innerHTML = "";

    capsules.forEach(c => {
        let today = new Date().toISOString().split('T')[0];
        let locked = today < c.date;

        let div = document.createElement("div");
        div.className = "capsule";

        div.innerHTML = `
            <p>${locked ? "🔒 Locked" : c.message}</p>
            <p>Open on: ${c.date}</p>
            <button onclick="editCapsule(${c.id})">Edit</button>
            <button onclick="deleteCapsule(${c.id})">Delete</button>
        `;

        container.appendChild(div);
    });
}

function deleteCapsule(id) {
    capsules = capsules.filter(c => c.id !== id);
    saveData();
    displayCapsules();
}

function saveData() {
    localStorage.setItem("capsules", JSON.stringify(capsules));
}
function editCapsule(id) {
    let capsule = capsules.find(c => c.id === id);

    let newMessage = prompt("Edit your message:", capsule.message);
    let newDate = prompt("Edit date (YYYY-MM-DD):", capsule.date);

    if (newMessage && newDate) {
        capsule.message = newMessage;
        capsule.date = newDate;

        saveData();
        displayCapsules();
    }
}