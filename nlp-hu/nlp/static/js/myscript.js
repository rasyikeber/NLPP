// Function to handle click event for the reject button
function handleRejectClick(event) {
    // Get the group_id from the data-group-id attribute of the clicked button
    const groupId = event.target.dataset.groupId;
    displayConfirmation(groupId);
    sendRejectRequest(groupId);
}
function displayConfirmation(groupId) {
    alert("Are you sure to delete this project with group-id of: " + groupId);
}
function sendRejectRequest(groupId) {
    axios.post('/reject-projectidea', {
        groupId: groupId
    })
    .then(response => {
        console.log("Response from Flask server:", response);
    })
    .catch(error => {
        console.error("Error:", error);
    });
}
document.addEventListener('click', function(event) {
    if (event.target.classList.contains('rejectButton')) {
        handleRejectClick(event);
    }
});
// For Approve
function handleApproveClick(event) {
    const projectId = event.target.dataset.projectid;
    displayConfirmationForA(projectId);
    sendApproveRequest(projectId);
}
function displayConfirmationForA(projectId) {
    alert("Are you sure to approve this project with id of: " + projectId);
}
function sendApproveRequest(projectId) {
    axios.post('/approve-projectidea', {
        projectId: projectId
    })
    .then(response => {
        console.log("project id to approved:"+ projectId)
    })
    .catch(error => {
        console.error("Error approving project:", error);
    });
}
document.addEventListener('click', function(event) {
    if (event.target.classList.contains('approveButton')) {
        handleApproveClick(event);
    }
});
