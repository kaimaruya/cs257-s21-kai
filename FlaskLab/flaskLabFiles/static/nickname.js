function displayTextBox() {
    var checkbox = document.getElementById('nickname');
    var element = document.getElementById('nicknameInfo');
    if (checkbox.checked == true) {
        element.style.display = 'nicknameInfo';
    } else {
        element.style.display = 'none';
    }

}