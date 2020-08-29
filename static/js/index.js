var imageInput = document.getElementById("upload-image");
var analyzeBtn = document.querySelector(".analyze-btn");
var result = document.getElementById("result");

imageInput.addEventListener("change", updateImagePreview);
analyzeBtn.addEventListener("click", validateAndSubmit);

function updateImagePreview(e) {
    var previewImage = document.getElementById('preview-image');
    var uploadLabel = document.getElementById('upload-label');
    var imagePath = document.getElementById('upload-image').value;

    // hide result if exists
    result.classList.add("d-none");

    // no files selected
    if (e.target.files.length == 0) {
        previewImage.classList.add("invisible");
        uploadLabel.innerHTML = "No file chosen";
        return
    } 

    // get filename
    var startIndex = (imagePath.indexOf('\\') >= 0 ? imagePath.lastIndexOf('\\') : imagePath.lastIndexOf('/'));
    var filename = imagePath.substring(startIndex);
    if (filename.indexOf('\\') === 0 || filename.indexOf('/') === 0) {
        filename = filename.substring(1);
    }

    //update preview and label
    previewImage.classList.remove("invisible");
    previewImage.src = URL.createObjectURL(e.target.files[0]);
    console.log(previewImage.src)
    uploadLabel.innerText = filename;
}

function validateAndSubmit(event) {
    event.preventDefault();

    console.log("validate")
    var fileInput = document.querySelector("#upload-image").files[0];

    if (fileInput) {
        var url = window.URL || window.webkitURL;
        var image = new Image()

        image.onload = function() {
            var spinner = document.getElementById("analyze-spinner");
            var xhr = new XMLHttpRequest();
            xhr.open("POST", "/", true);

            xhr.onload = function() {
                spinner.classList.add("d-none");
                console.log("added")

                if (this.status == 200) {
                    updateResult(this.responseText);
                } else {
                    updateResult("Failure");
                }
            }

            var formData = new FormData();
            formData.append("upload-image", fileInput);
            xhr.send(formData);
            spinner.classList.remove("d-none");
            console.log("Sending ajax")
        }

        image.onerror = function() {
            alert("Invalid Image");
        }

        console.log(fileInput);
        image.src = url.createObjectURL(fileInput);
    } else {
        alert("Load an image");
    }                
}

function updateResult(message) {
    result.classList.remove("d-none");
    result.innerHTML = message;
}