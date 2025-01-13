document.addEventListener('DOMContentLoaded', function () {
    const uploadForm = document.getElementById('upload-form');
    const apkFileInput = document.getElementById('apk-file');
    const uploadStatus = document.createElement('p');
    uploadForm.appendChild(uploadStatus);

    uploadForm.addEventListener('submit', function (event) {
        const file = apkFileInput.files[0];

        if (!file) {
            uploadStatus.textContent = 'Lütfen bir dosya seçin.';
            uploadStatus.style.color = 'red';
            event.preventDefault();
            return;
        }

        if (!file.name.endsWith('.apk')) {
            uploadStatus.textContent = 'Lütfen geçerli bir APK dosyası seçin.';
            uploadStatus.style.color = 'red';
            event.preventDefault();
            return;
        }

        uploadStatus.textContent = 'APK dosyası analiz ediliyor...';
        uploadStatus.style.color = 'green';
    });
});
