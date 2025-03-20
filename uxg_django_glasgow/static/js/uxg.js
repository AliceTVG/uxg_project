function redirectTocreatenewpost() {
    window.location.href = create_new_post;
}

function redirectToProfile() {
    window.location.href = profile;
}

function editBio() {
    const bio_text = document.getElementById("bio_text").innerText;
    document.getElementById("bio_text_editer").value = bio_text;
    document.getElementById("bio_dialog_overlay").style.display = "flex";
}

function bioSaveText() {
    const new_bio_text = document.getElementById("bio_text_editer").value;
    document.getElementById("bio_text").innerText = new_bio_text;
    document.getElementById("bio_dialog_overlay").style.display = "none";
}

function bioCloseDialog() {
    document.getElementById("bio_dialog_overlay").style.display = "none";
}