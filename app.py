from flask import Flask, render_template, request, jsonify
import yt_dlp

app = Flask(__name__)

def get_video_info(url):
    ydl_opts = {
        'format': 'best',
        'quiet': True,
        'no_warnings': True,
        # Menggunakan user agent generik agar tidak diblokir FB
        'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    }
    
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            return {
                "title": info.get('title', 'Video Facebook'),
                "url": info.get('url'),
                "thumbnail": info.get('thumbnail'),
                "duration": info.get('duration_string'),
                "success": True
            }
    except Exception as e:
        return {"success": False, "error": str(e)}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/download', methods=['POST'])
def download():
    data = request.get_json()
    video_url = data.get('url')
    
    if not video_url:
        return jsonify({"success": False, "error": "URL tidak valid"})
    
    result = get_video_info(video_url)
    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True, port=5000)
