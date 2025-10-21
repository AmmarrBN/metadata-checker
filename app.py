#!/usr/bin/env python3
"""
Metadata Checker Tool with GUI - Termux Compatible Version with Logging
"""

import os
import sys
import json
import argparse
import subprocess
from pathlib import Path
from datetime import datetime
from flask import Flask, render_template, request, jsonify, send_file
from werkzeug.utils import secure_filename
import mimetypes

app = Flask(__name__, template_folder='templates', static_folder='static')
app.config['MAX_CONTENT_LENGTH'] = 100 * 1024 * 1024  # 100MB max file size untuk Termux
app.config['UPLOAD_FOLDER'] = 'uploads'

# Create uploads folder if it doesn't exist
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

TOOLS_AVAILABLE = {}

def log_message(level, tool, message, file_path=None):
    """Log messages with timestamp and formatting"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    file_info = f" - File: {os.path.basename(file_path)}" if file_path else ""
    print(f"[{timestamp}] [{level}] {tool.upper()}: {message}{file_info}")

def check_tool(tool_name):
    """Check if a tool is installed - Termux compatible"""
    if tool_name in TOOLS_AVAILABLE:
        return TOOLS_AVAILABLE[tool_name]

    try:
        log_message("CHECKING", tool_name, "Checking if tool is available")
        
        if tool_name == 'exiftool':
            subprocess.run(['exiftool', '-ver'], capture_output=True, check=True, timeout=5)
        elif tool_name == 'mediainfo':
            subprocess.run(['mediainfo', '--version'], capture_output=True, check=True, timeout=5)
        elif tool_name == 'ffprobe':
            subprocess.run(['ffprobe', '-version'], capture_output=True, check=True, timeout=5)
        elif tool_name == 'identify':
            subprocess.run(['identify', '-version'], capture_output=True, check=True, timeout=5)
        elif tool_name == 'file':
            subprocess.run(['file', '--version'], capture_output=True, check=True, timeout=5)
        elif tool_name == 'zipinfo':
            subprocess.run(['zipinfo', '-v'], capture_output=True, check=True, timeout=5)
        elif tool_name == 'strings':
            subprocess.run(['strings', '--version'], capture_output=True, check=True, timeout=5)
        
        TOOLS_AVAILABLE[tool_name] = True
        log_message("SUCCESS", tool_name, "Tool is available")
        return True
    except (subprocess.CalledProcessError, FileNotFoundError, subprocess.TimeoutExpired) as e:
        TOOLS_AVAILABLE[tool_name] = False
        log_message("ERROR", tool_name, f"Tool not available: {str(e)}")
        return False

def get_exiftool_metadata(file_path):
    """Extract metadata using exiftool"""
    if not check_tool('exiftool'):
        return {"error": "exiftool not installed"}

    try:
        log_message("RUNNING", "EXIFTOOL", "Extracting metadata", file_path)
        
        result = subprocess.run(
            ['exiftool', '-json', file_path],
            capture_output=True, text=True, check=True, timeout=30
        )
        
        if result.stdout.strip():
            metadata = json.loads(result.stdout)[0]
            log_message("SUCCESS", "EXIFTOOL", f"Extracted {len(metadata)} metadata fields", file_path)
            return metadata
        else:
            log_message("WARNING", "EXIFTOOL", "No metadata found", file_path)
            return {"error": "No metadata found"}
    except Exception as e:
        log_message("ERROR", "EXIFTOOL", f"Failed to extract metadata: {str(e)}", file_path)
        return {"error": str(e)}

def get_mediainfo_metadata(file_path):
    """Extract metadata using mediainfo"""
    if not check_tool('mediainfo'):
        return {"error": "mediainfo not installed"}

    try:
        log_message("RUNNING", "MEDIAINFO", "Extracting media information", file_path)
        
        result = subprocess.run(
            ['mediainfo', '--Output=JSON', file_path],
            capture_output=True, text=True, check=True, timeout=30
        )
        
        if result.stdout.strip():
            metadata = json.loads(result.stdout)
            log_message("SUCCESS", "MEDIAINFO", "Media information extracted successfully", file_path)
            return metadata
        else:
            log_message("WARNING", "MEDIAINFO", "No media information found", file_path)
            return {"error": "No metadata found"}
    except Exception as e:
        log_message("ERROR", "MEDIAINFO", f"Failed to extract media information: {str(e)}", file_path)
        return {"error": str(e)}

def get_ffprobe_metadata(file_path):
    """Extract metadata using ffprobe"""
    if not check_tool('ffprobe'):
        return {"error": "ffprobe not installed"}

    try:
        log_message("RUNNING", "FFPROBE", "Extracting audio/video information", file_path)
        
        result = subprocess.run(
            ['ffprobe', '-v', 'quiet', '-print_format', 'json', '-show_format', '-show_streams', file_path],
            capture_output=True, text=True, check=True, timeout=30
        )
        
        if result.stdout.strip():
            metadata = json.loads(result.stdout)
            log_message("SUCCESS", "FFPROBE", "Audio/video information extracted successfully", file_path)
            return metadata
        else:
            log_message("WARNING", "FFPROBE", "No audio/video information found", file_path)
            return {"error": "No metadata found"}
    except Exception as e:
        log_message("ERROR", "FFPROBE", f"Failed to extract audio/video information: {str(e)}", file_path)
        return {"error": str(e)}

def get_pdf_metadata(file_path):
    """Extract PDF metadata using exiftool (fallback since pdfinfo not available)"""
    log_message("INFO", "PDF", "Using exiftool for PDF metadata extraction", file_path)
    return get_exiftool_metadata(file_path)

def get_identify_metadata(file_path):
    """Extract metadata using ImageMagick identify"""
    if not check_tool('identify'):
        return {"error": "identify not installed"}

    try:
        log_message("RUNNING", "IDENTIFY", "Extracting image information", file_path)
        
        result = subprocess.run(
            ['identify', '-verbose', file_path],
            capture_output=True, text=True, check=True, timeout=30
        )
        
        metadata = {}
        current_section = None
        
        for line in result.stdout.split('\n'):
            line = line.strip()
            if line.endswith(':'):
                current_section = line[:-1]
                metadata[current_section] = {}
            elif ': ' in line and current_section:
                key, value = line.split(': ', 1)
                metadata[current_section][key.strip()] = value.strip()
            elif ':' in line and line:
                key, value = line.split(':', 1)
                metadata[key.strip()] = value.strip()
        
        if metadata:
            log_message("SUCCESS", "IDENTIFY", f"Extracted image information with {len(metadata)} sections", file_path)
        else:
            log_message("WARNING", "IDENTIFY", "No image information found", file_path)
            
        return metadata
    except Exception as e:
        log_message("ERROR", "IDENTIFY", f"Failed to extract image information: {str(e)}", file_path)
        return {"error": str(e)}

def get_file_type_metadata(file_path):
    """Extract metadata using file command"""
    if not check_tool('file'):
        return {"error": "file command not installed"}

    try:
        log_message("RUNNING", "FILE", "Identifying file type", file_path)
        
        result = subprocess.run(
            ['file', '-b', '--mime-type', file_path],
            capture_output=True, text=True, check=True, timeout=10
        )
        mime_type = result.stdout.strip()
        
        result2 = subprocess.run(
            ['file', '-b', file_path],
            capture_output=True, text=True, check=True, timeout=10
        )
        description = result2.stdout.strip()
        
        log_message("SUCCESS", "FILE", f"File type identified: {mime_type}", file_path)
        
        return {
            "mime_type": mime_type,
            "description": description
        }
    except Exception as e:
        log_message("ERROR", "FILE", f"Failed to identify file type: {str(e)}", file_path)
        return {"error": str(e)}

def get_zipinfo_metadata(file_path):
    """Extract metadata using zipinfo"""
    if not check_tool('zipinfo'):
        return {"error": "zipinfo not installed"}

    try:
        log_message("RUNNING", "ZIPINFO", "Extracting archive information", file_path)
        
        result = subprocess.run(
            ['zipinfo', '-l', file_path],
            capture_output=True, text=True, check=True, timeout=30
        )
        
        lines = result.stdout.split('\n')
        metadata = {
            "files": [],
            "summary": ""
        }
        
        for line in lines:
            if line.strip():
                metadata["files"].append(line)
        
        if metadata["files"]:
            log_message("SUCCESS", "ZIPINFO", f"Archive contains {len(metadata['files'])} items", file_path)
        else:
            log_message("WARNING", "ZIPINFO", "No archive information found", file_path)
            
        return metadata
    except Exception as e:
        log_message("ERROR", "ZIPINFO", f"Failed to extract archive information: {str(e)}", file_path)
        return {"error": str(e)}

def get_strings_metadata(file_path):
    """Extract strings from binary files"""
    if not check_tool('strings'):
        return {"error": "strings command not installed"}

    try:
        log_message("RUNNING", "STRINGS", "Extracting strings from binary", file_path)
        
        result = subprocess.run(
            ['strings', '-n', '4', file_path],  # Minimum 4 characters
            capture_output=True, text=True, check=True, timeout=30
        )
        
        strings_list = result.stdout.split('\n')
        
        # Filter for interesting strings
        interesting = []
        for s in strings_list:
            s = s.strip()
            if len(s) >= 4:  # Minimum 4 characters
                s_lower = s.lower()
                if any(keyword in s_lower for keyword in 
                       ['http', 'https', 'ftp', 'www.', 'email', 'mailto:', 
                        'password', 'pwd', 'token', 'api', 'key', 'secret',
                        '@', '://', '.com', '.org', '.net']):
                    interesting.append(s)
        
        log_message("SUCCESS", "STRINGS", f"Found {len(strings_list)} total strings, {len(interesting)} interesting", file_path)
        
        return {
            "total_strings": len(strings_list),
            "interesting_strings": interesting[:30]  # Limit to 30
        }
    except Exception as e:
        log_message("ERROR", "STRINGS", f"Failed to extract strings: {str(e)}", file_path)
        return {"error": str(e)}

def get_file_info(file_path):
    """Get basic file information"""
    try:
        log_message("RUNNING", "FILE_INFO", "Getting file information", file_path)
        
        stat = os.stat(file_path)
        file_name = os.path.basename(file_path)
        file_ext = os.path.splitext(file_name)[1].lower()
        mime_type = mimetypes.guess_type(file_path)[0] or "unknown"

        file_info = {
            "name": file_name,
            "extension": file_ext,
            "mime_type": mime_type,
            "size": stat.st_size,
            "size_formatted": format_size(stat.st_size),
            "created": datetime.fromtimestamp(stat.st_ctime).isoformat(),
            "modified": datetime.fromtimestamp(stat.st_mtime).isoformat(),
            "accessed": datetime.fromtimestamp(stat.st_atime).isoformat(),
        }
        
        log_message("SUCCESS", "FILE_INFO", f"File information collected: {file_info['size_formatted']}", file_path)
        return file_info
    except Exception as e:
        log_message("ERROR", "FILE_INFO", f"Failed to get file information: {str(e)}", file_path)
        return {"error": str(e)}

def format_size(bytes):
    """Format bytes to human readable size"""
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if bytes < 1024.0:
            return f"{bytes:.2f} {unit}"
        bytes /= 1024.0
    return f"{bytes:.2f} PB"

def validate_metadata_key(key):
    """Validate and clean metadata key for exiftool"""
    # Remove spaces and special characters, keep only alphanumeric
    import re
    clean_key = re.sub(r'[^a-zA-Z0-9]', '', key)
    return clean_key

def get_supported_metadata_fields():
    """Get list of supported metadata fields for different file types"""
    return {
        "common": [
            "Title", "Description", "Comment", "Keywords", "Subject",
            "Author", "Creator", "Copyright", "Software", "Rating"
        ],
        "image": [
            "Artist", "Make", "Model", "DateTime", "GPSLatitude", "GPSLongitude",
            "Orientation", "XResolution", "YResolution", "ResolutionUnit"
        ],
        "video": [
            "Title", "Artist", "Album", "Genre", "Year", "Track",
            "Composer", "Director", "Producer", "Show", "Episode"
        ],
        "audio": [
            "Title", "Artist", "Album", "Genre", "Year", "Track",
            "Composer", "Publisher", "BPM", "Lyrics"
        ]
    }

def add_metadata(file_path, metadata_dict):
    """Add metadata to file using exiftool"""
    if not check_tool('exiftool'):
        return {"success": False, "error": "exiftool not installed"}

    try:
        log_message("RUNNING", "EXIFTOOL", f"Adding metadata: {metadata_dict}", file_path)
        
        cmd = ['exiftool', '-overwrite_original']
        for key, value in metadata_dict.items():
            # Clean the key - remove spaces and special characters
            clean_key = validate_metadata_key(key)
            if clean_key:  # Only add if key is not empty
                cmd.append(f'-{clean_key}={value}')
        
        cmd.append(file_path)
        
        log_message("DEBUG", "EXIFTOOL", f"Running command: {' '.join(cmd)}", file_path)
        
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
        
        # Check if command was successful
        if result.returncode == 0:
            log_message("SUCCESS", "EXIFTOOL", "Metadata added successfully", file_path)
            return {"success": True, "message": "Metadata added successfully"}
        else:
            error_msg = result.stderr.strip() if result.stderr else "Unknown error"
            log_message("ERROR", "EXIFTOOL", f"Failed to add metadata: {error_msg}", file_path)
            return {"success": False, "error": f"ExifTool error: {error_msg}"}
            
    except Exception as e:
        log_message("ERROR", "EXIFTOOL", f"Exception while adding metadata: {str(e)}", file_path)
        return {"success": False, "error": str(e)}

@app.route('/')
def index():
    """Main page"""
    log_message("INFO", "WEB", "Homepage accessed")
    tools_status = {
        'exiftool': check_tool('exiftool'),
        'mediainfo': check_tool('mediainfo'),
        'ffprobe': check_tool('ffprobe'),
        'identify': check_tool('identify'),
        'file': check_tool('file'),
        'zipinfo': check_tool('zipinfo'),
        'strings': check_tool('strings'),
    }
    return render_template('index.html', tools_status=tools_status)

@app.route('/api/upload', methods=['POST'])
def upload_file():
    """Handle file upload"""
    if 'file' not in request.files:
        return jsonify({"error": "No file provided"}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No file selected"}), 400

    try:
        filename = secure_filename(file.filename)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_")
        filename = timestamp + filename
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        
        log_message("INFO", "UPLOAD", f"Uploading file: {filename}")
        file.save(filepath)
        
        log_message("SUCCESS", "UPLOAD", f"File saved: {filename}")
        
        file_info = get_file_info(filepath)
        all_metadata = {
            "file_info": file_info,
            "exiftool": get_exiftool_metadata(filepath),
            "mediainfo": get_mediainfo_metadata(filepath),
            "ffprobe": get_ffprobe_metadata(filepath),
            "pdf": get_pdf_metadata(filepath),
            "identify": get_identify_metadata(filepath),
            "file": get_file_type_metadata(filepath),
            "zipinfo": get_zipinfo_metadata(filepath),
            "strings": get_strings_metadata(filepath),
        }
        
        log_message("SUCCESS", "PROCESSING", f"Completed metadata extraction for {filename}")
        
        return jsonify({
            "success": True,
            "file_id": filename,
            "metadata": all_metadata
        })
    except Exception as e:
        log_message("ERROR", "UPLOAD", f"Upload failed: {str(e)}")
        return jsonify({"error": str(e)}), 500

@app.route('/api/metadata/<file_id>', methods=['GET'])
def get_metadata(file_id):
    """Get metadata for uploaded file from all tools"""
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(file_id))

    if not os.path.exists(filepath):
        return jsonify({"error": "File not found"}), 404

    log_message("INFO", "METADATA", f"Fetching metadata for: {file_id}")
    
    file_info = get_file_info(filepath)
    all_metadata = {
        "file_info": file_info,
        "exiftool": get_exiftool_metadata(filepath),
        "mediainfo": get_mediainfo_metadata(filepath),
        "ffprobe": get_ffprobe_metadata(filepath),
        "pdf": get_pdf_metadata(filepath),
        "identify": get_identify_metadata(filepath),
        "file": get_file_type_metadata(filepath),
        "zipinfo": get_zipinfo_metadata(filepath),
        "strings": get_strings_metadata(filepath),
    }
    
    log_message("SUCCESS", "METADATA", f"Metadata retrieved for: {file_id}")
    return jsonify(all_metadata)

@app.route('/api/metadata/<file_id>', methods=['POST'])
def update_metadata(file_id):
    """Update metadata for file"""
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(file_id))

    if not os.path.exists(filepath):
        return jsonify({"error": "File not found"}), 404

    try:
        data = request.get_json()
        metadata_dict = data.get('metadata', {})
        
        log_message("INFO", "UPDATE", f"Updating metadata for: {file_id} with data: {metadata_dict}")
        
        # Clean and validate metadata keys
        clean_metadata = {}
        for key, value in metadata_dict.items():
            clean_key = validate_metadata_key(key)
            if clean_key:
                clean_metadata[clean_key] = value
        
        if not clean_metadata:
            log_message("ERROR", "UPDATE", "No valid metadata fields provided")
            return jsonify({"success": False, "error": "No valid metadata fields provided"}), 400
        
        result = add_metadata(filepath, clean_metadata)
        if result.get('success'):
            # Get updated metadata
            updated_metadata = get_exiftool_metadata(filepath)
            log_message("SUCCESS", "UPDATE", f"Metadata updated successfully for: {file_id}")
            return jsonify({
                "success": True,
                "message": "Metadata updated successfully",
                "metadata": updated_metadata
            })
        else:
            log_message("ERROR", "UPDATE", f"Metadata update failed: {result.get('error')}")
            return jsonify(result), 400
    except Exception as e:
        log_message("ERROR", "UPDATE", f"Metadata update exception: {str(e)}")
        return jsonify({"error": str(e)}), 500

@app.route('/api/download/<file_id>', methods=['GET'])
def download_file(file_id):
    """Download file"""
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(file_id))

    if not os.path.exists(filepath):
        return jsonify({"error": "File not found"}), 404

    log_message("INFO", "DOWNLOAD", f"Downloading file: {file_id}")
    return send_file(filepath, as_attachment=True)

@app.route('/api/delete/<file_id>', methods=['DELETE'])
def delete_file(file_id):
    """Delete uploaded file"""
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(file_id))

    if not os.path.exists(filepath):
        return jsonify({"error": "File not found"}), 404

    try:
        log_message("INFO", "DELETE", f"Deleting file: {file_id}")
        os.remove(filepath)
        log_message("SUCCESS", "DELETE", f"File deleted: {file_id}")
        return jsonify({"success": True, "message": "File deleted successfully"})
    except Exception as e:
        log_message("ERROR", "DELETE", f"File deletion failed: {str(e)}")
        return jsonify({"error": str(e)}), 500

@app.route('/api/tools-status', methods=['GET'])
def tools_status():
    """Get status of all available tools"""
    log_message("INFO", "TOOLS", "Checking tools status")
    status = {
        'exiftool': check_tool('exiftool'),
        'mediainfo': check_tool('mediainfo'),
        'ffprobe': check_tool('ffprobe'),
        'identify': check_tool('identify'),
        'file': check_tool('file'),
        'zipinfo': check_tool('zipinfo'),
        'strings': check_tool('strings'),
    }
    return jsonify(status)

@app.route('/api/supported-fields', methods=['GET'])
def get_supported_fields():
    """Get supported metadata fields"""
    file_type = request.args.get('type', 'common')
    log_message("INFO", "FIELDS", f"Getting supported fields for: {file_type}")
    
    supported = get_supported_metadata_fields()
    
    if file_type in supported:
        return jsonify({"fields": supported[file_type]})
    else:
        return jsonify({"fields": supported["common"]})

def main():
    parser = argparse.ArgumentParser(
        description='Metadata Checker Tool - Termux Compatible Version with Logging',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
Examples:
  python app.py
  python app.py -r 127.0.0.1:8080
        '''
    )

    parser.add_argument(
        '-r', '--run', type=str, default='127.0.0.1:8080',
        help='Run GUI server (default: 127.0.0.1:8080)'
    )
    
    args = parser.parse_args()
    
    if args.run:
        host, port = args.run.split(':')
        port = int(port)
        
        log_message("START", "SYSTEM", "Starting Metadata Checker Tool")
        
        tools = {
            'exiftool': check_tool('exiftool'),
            'mediainfo': check_tool('mediainfo'),
            'ffprobe': check_tool('ffprobe'),
            'identify': check_tool('identify'),
            'file': check_tool('file'),
            'zipinfo': check_tool('zipinfo'),
            'strings': check_tool('strings'),
        }
        
        tools_info = '\n'.join([f"   {'✓' if v else '✗'} {k}" for k, v in tools.items()])
        
        print(f"""
╔════════════════════════════════════════════════════════════╗
║          Metadata Checker Tool - Termux Version           ║
╚════════════════════════════════════════════════════════════╝

🚀 Server running at: http://{host}:{port}
📁 Upload folder: {os.path.abspath(app.config['UPLOAD_FOLDER'])}

📊 Available Tools:
{tools_info}

💡 Note: 
  - Buka browser dan akses URL di atas
  - pdfinfo tidak tersedia, menggunakan exiftool untuk PDF
  - Strings analysis tersedia via binutils
  - Logs akan ditampilkan di console

Press CTRL+C to stop the server
        """)
        
        app.run(host=host, port=port, debug=False)

if __name__ == '__main__':
    main()

