<!DOCTYPE html>
<html lang="id">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Pencarian Data Artikel Ilmiah</title>
    
    <link href="https://fonts.googleapis.com/css2?family=Roboto:wght@400;500;700&display=swap" rel="stylesheet"> 
    <link rel="stylesheet" href="assets/style.css">
</head>
<body>

<div class="container">
    <h1>PENCARIAN DATA ARTIKEL ILMIAH</h1>

    <div class="search-panel">
        <div class="form-group">
            <label>Input Nama Penulis :</label>
            <input type="text" id="author" placeholder="Contoh: Andrew Ng">
        </div>

        <div class="form-group">
            <label>Input Keyword Artikel :</label>
            <input type="text" id="keyword" placeholder="Contoh: Machine Learning">
        </div>

        <div class="form-group">
            <label>Jumlah data :</label>
            <input type="number" id="limit" value="10" min="1" max="20">
        </div>

        <button onclick="searchScholar()" id="btn-search">Search</button>
    </div>

    <div id="loading" class="loading hidden">
        <p>Sedang mengambil data dari Google Scholar & Menghitung Similaritas...</p>
        <p><small>(Mohon Menunggu)</small></p>
    </div>

    <div id="results-area" class="results-container"></div>
</div>

<script>
    async function searchScholar() {
        const author = document.getElementById('author').value;
        const keyword = document.getElementById('keyword').value;
        const limit = document.getElementById('limit').value;
        
        const resultsArea = document.getElementById('results-area');
        const loading = document.getElementById('loading');
        const btn = document.getElementById('btn-search');

        // Validasi
        if (!author && !keyword) {
            alert("Harap isi setidaknya Nama Penulis atau Keyword Artikel!");
            return;
        }

        // Reset UI
        resultsArea.innerHTML = '';
        loading.classList.remove('hidden');
        btn.disabled = true;
        btn.innerText = "Processing...";

        try {
            const response = await fetch('php/controller.php', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ 
                    author: author, 
                    keyword: keyword,
                    limit: limit 
                })
            });

            const data = await response.json();

            loading.classList.add('hidden');
            btn.disabled = false;
            btn.innerText = "Search";

            if (data.error) {
                resultsArea.innerHTML = `<div class="error-msg">⚠️ Terjadi Kesalahan: ${data.error}</div>`;
            } else if (!data.papers || data.papers.length === 0) {
                resultsArea.innerHTML = `<div class="empty-msg">Tidak ada data ditemukan.</div>`;
            } else {
                // RENDER TABEL
                let tableHtml = `
                    <table>
                        <thead>
                            <tr>
                                <th>Judul Artikel</th>
                                <th>Penulis</th>
                                <th class="center-align">Tanggal Rilis</th>
                                <th>Nama Jurnal</th>
                                <th class="center-align">Jumlah Sitasi</th>
                                <th>Link Jurnal</th>
                                <th class="center-align">Nilai Similaritas</th>
                            </tr>
                        </thead>
                        <tbody>
                `;

                data.papers.forEach(paper => {
                    tableHtml += `
                        <tr>
                            <td class="col-title">${paper.title}</td>
                            <td>${paper.authors}</td>
                            <td class="center-align">${paper.year}</td>
                            <td>${paper.journal}</td>
                            <td class="center-align">${paper.citations}</td>
                            <td class="col-link"><a href="${paper.link}" target="_blank">Buka Link</a></td>
                            <td class="col-sim center-align">${paper.similarity.toFixed(10)}</td>
                        </tr>
                    `;
                });

                tableHtml += `</tbody></table>`;
                resultsArea.innerHTML = tableHtml;
            }

        } catch (error) {
            loading.classList.add('hidden');
            btn.disabled = false;
            btn.innerText = "Search";
            resultsArea.innerHTML = `<div class="error-msg">❌ Gagal terhubung ke server. Pastikan Python sudah terinstall dengan benar.</div>`;
            console.error(error);
        }
    }
</script>

</body>
</html>