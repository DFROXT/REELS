from flask import Flask, request, render_template_string, send_file, jsonify
import os
import logging
from main import process_reel

app = Flask(__name__)
logging.basicConfig(level=logging.INFO)

HTML = '''
<!DOCTYPE html>
<html>
<head>
    <title>Viral Reel Editor</title>
    <style>
        body { font-family: Arial; text-align: center; padding: 50px; }
        input[type=url] { width: 400px; padding: 10px; margin: 10px; }
        button { padding: 10px 20px; background: #ff0050; color: white; border: none; cursor: pointer; }
        .loading { display: none; }
    </style>
</head>
<body>
    <h1>🔥 Viral Reel Editor</h1>
    <form method="POST" action="/" onsubmit="showLoading()">
        <input type="url" name="youtube_url" placeholder="Enter YouTube URL" required>
        <button type="submit">Generate Reel</button>
    </form>
    <div class="loading" id="loading">Processing... may take a minute ⏳</div>
    {% if download_link %}
        <h3>✅ Done! <a href="{{ download_link }}">Download Reel</a></h3>
    {% endif %}
    {% if error %}
        <h3 style="color:red">❌ Error: {{ error }}</h3>
    {% endif %}
    <script>
        function showLoading() {
            document.getElementById('loading').style.display = 'block';
        }
    </script>
</body>
</html>
'''

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        url = request.form['youtube_url']
        try:
            output_file = process_reel(url)
            download_link = f'/download/{os.path.basename(output_file)}'
            return render_template_string(HTML, download_link=download_link)
        except Exception as e:
            return render_template_string(HTML, error=str(e))
    return render_template_string(HTML)

@app.route('/download/<filename>')
def download(filename):
    try:
        return send_file(f'output/{filename}', as_attachment=True)
    except Exception as e:
        return f"File not found: {e}", 404

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=False, host='0.0.0.0', port=port)
