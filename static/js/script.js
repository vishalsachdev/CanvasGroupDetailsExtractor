document.addEventListener('DOMContentLoaded', function() {
    const extractForm = document.getElementById('extractForm');
    const loading = document.getElementById('loading');
    const error = document.getElementById('error');
    const exportBtn = document.getElementById('exportBtn');

    if (extractForm) {
        extractForm.addEventListener('submit', function(e) {
            e.preventDefault();
            loading.style.display = 'block';
            error.style.display = 'none';

            const formData = new FormData(extractForm);
            const courseUrl = formData.get('course_url');

            // Extract base URL and course ID
            try {
                const url = new URL(courseUrl);
                const baseUrl = `${url.protocol}//${url.hostname}`;
                const courseId = url.pathname.split('/').pop();

                formData.set('base_url', baseUrl);
                formData.set('course_id', courseId);
                formData.delete('course_url');
            } catch (err) {
                error.textContent = 'Invalid course URL. Please provide a valid Canvas course URL.';
                error.style.display = 'block';
                loading.style.display = 'none';
                return;
            }

            fetch('/extract', {
                method: 'POST',
                body: formData
            })
            .then(response => {
                if (!response.ok) {
                    return response.json().then(err => {
                        throw new Error(err.error || 'Network response was not ok');
                    });
                }
                return response.text();
            })
            .then(html => {
                document.body.innerHTML = html;
                // Re-attach event listener for export button after DOM update
                attachExportButtonListener();
            })
            .catch(err => {
                console.error('Error:', err);
                error.textContent = 'An error occurred: ' + err.message;
                error.style.display = 'block';
            })
            .finally(() => {
                loading.style.display = 'none';
            });
        });
    }

    // Function to attach event listener to export button
    function attachExportButtonListener() {
        const exportBtn = document.getElementById('exportBtn');
        const exportLoading = document.getElementById('exportLoading');
        const exportError = document.getElementById('exportError');

        if (exportBtn) {
            exportBtn.addEventListener('click', function() {
                exportLoading.style.display = 'block';
                exportError.style.display = 'none';
                exportBtn.disabled = true;

                const data = {
                    students: Array.from(document.querySelectorAll('table:first-of-type tbody tr')).map(row => ({
                        id: row.cells[0].textContent,
                        name: row.cells[1].textContent,
                        email: row.cells[2].textContent,
                        groups: row.cells[3].textContent.split(', ').filter(g => g !== 'No Group')
                    })),
                    groups: Array.from(document.querySelectorAll('table:last-of-type tbody tr')).map(row => ({
                        id: row.cells[0].textContent,
                        name: row.cells[1].textContent,
                        members_count: parseInt(row.cells[2].textContent)
                    }))
                };

                fetch('/export', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify(data)
                })
                .then(response => {
                    if (!response.ok) {
                        return response.json().then(err => {
                            throw new Error(err.error || 'Export failed');
                        });
                    }
                    return response.blob();
                })
                .then(blob => {
                    const url = window.URL.createObjectURL(blob);
                    const a = document.createElement('a');
                    a.style.display = 'none';
                    a.href = url;
                    a.download = 'canvas_course_data.csv';
                    document.body.appendChild(a);
                    a.click();
                    window.URL.revokeObjectURL(url);
                })
                .catch(err => {
                    console.error('Export failed:', err);
                    exportError.textContent = 'Export failed: ' + err.message;
                    exportError.style.display = 'block';
                })
                .finally(() => {
                    exportLoading.style.display = 'none';
                    exportBtn.disabled = false;
                });
            });
        }
    }

    // Attach event listener for export button on initial page load
    attachExportButtonListener();
});
