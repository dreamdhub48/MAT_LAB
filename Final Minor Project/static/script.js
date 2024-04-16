// document.getElementById('upload-form').addEventListener('submit', function(event) {
//     event.preventDefault();
//     const fileUpload = document.getElementById('file-upload');
//     const file = fileUpload.files[0];
//     const formData = new FormData();
//     formData.append('file', file);
//     fetch('/analyze', {
//         method: 'POST',
//         body: formData
//     })
//     .then(response => response.json())
//     .then(data => {
//         const report = document.getElementById('report');
//         report.innerHTML = `<h2>Analysis Report</h2><p>File Type: ${data.file_type}</p><p>Static Analysis: ${data.static_analysis}</p><p>Dynamic Analysis: ${data.dynamic_analysis}</p>`;
//     })
//     .catch(error => {
//         console.error('Error:', error);
//     });
// });