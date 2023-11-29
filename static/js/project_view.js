document.getElementById("pt")?.addEventListener("click", project);
document.getElementById("st")?.addEventListener("click", statistic);
document.getElementById("create_t")?.addEventListener("click", create);
document.getElementById("create_s")?.addEventListener("click", stage);


function statistic() {
    document.getElementById("task-details-container").classList.remove("show");
    document.getElementById("kanban-board").classList.remove("show");
    document.getElementById("stats").classList.remove("hidden");
    document.getElementById("create").classList.remove("show");
    document.getElementById("create_2").classList.remove("show");

    document.getElementById("task-details-container").classList.add("hidden");
    document.getElementById("create_2").classList.add("hidden");
    document.getElementById("kanban-board").classList.add("hidden");
    document.getElementById("stats").classList.add("show");
    document.getElementById("create").classList.add("hidden");
}

function project() {
    document.getElementById("task-details-container").classList.remove("show");
    document.getElementById("kanban-board").classList.remove("hidden");
    document.getElementById("stats").classList.remove("show");
    document.getElementById("create").classList.remove("show");
    document.getElementById("create_2").classList.remove("show");

    document.getElementById("task-details-container").classList.add("hidden");
    document.getElementById("create_2").classList.add("hidden");
    document.getElementById("kanban-board").classList.add("show");
    document.getElementById("stats").classList.add("hidden");
    document.getElementById("create").classList.add("hidden");
}

function create() {
    document.getElementById("task-details-container").classList.remove("show");
    document.getElementById("kanban-board").classList.remove("show");
    document.getElementById("stats").classList.remove("show");
    document.getElementById("create").classList.remove("hidden");
    document.getElementById("create_2").classList.remove("show");

    document.getElementById("task-details-container").classList.add("hidden");
    document.getElementById("create_2").classList.add("hidden");
    document.getElementById("kanban-board").classList.add("hidden");
    document.getElementById("stats").classList.add("hidden");
    document.getElementById("create").classList.add("show");
}

function stage() {
    document.getElementById("task-details-container").classList.remove("show");
    document.getElementById("kanban-board").classList.remove("show");
    document.getElementById('form-t').classList.remove("show");
    document.getElementById("create_2").classList.remove("hidden");
    document.getElementById("stats").classList.remove("show");
    document.getElementById("create").classList.remove("show");

    document.getElementById("task-details-container").classList.add("hidden");
    document.getElementById("kanban-board").classList.add("hidden");
    document.getElementById("stats").classList.add("hidden");
    document.getElementById("create").classList.add("hidden");
}


function drag(ev) {
    ev.dataTransfer.setData("text", ev.target.id);
}

function allowDrop(ev) {
    ev.preventDefault();
}

function drop(ev) {
    ev.preventDefault();
    var data = ev.dataTransfer.getData("text");
    ev.currentTarget.appendChild(document.getElementById(data));
}

// const element = document.getElementById('form-t');
// element?.remove();