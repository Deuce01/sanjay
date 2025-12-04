# API Documentation

## Overview
The Matrimony Video Generator provides a simple REST API for job management and file processing.

## Base URL
```
http://127.0.0.1:5000
```

## Endpoints

### Upload File and Create Job
```http
POST /
Content-Type: multipart/form-data
```

**Parameters:**
- `file` (required): Excel file (.xlsx)

**Response:**
- Redirects to status page with job ID

**Example:**
```bash
curl -X POST -F "file=@profiles.xlsx" http://127.0.0.1:5000/
```

### Get Job Status
```http
GET /status/{job_id}
```

**Parameters:**
- `job_id` (path): UUID of the job

**Response:**
- HTML page with job status and logs
- Auto-refreshes every 10 seconds during processing

**Example:**
```bash
curl http://127.0.0.1:5000/status/123e4567-e89b-12d3-a456-426614174000
```

### Download Results
```http
GET /download/{job_id}
```

**Parameters:**
- `job_id` (path): UUID of completed job

**Response:**
- ZIP file containing generated videos
- Returns 404 if job not found or not completed

**Example:**
```bash
curl -O http://127.0.0.1:5000/download/123e4567-e89b-12d3-a456-426614174000
```

## Job Status Values

| Status | Description |
|--------|-------------|
| `PENDING` | Job created, waiting for processing |
| `PROCESSING` | Currently being processed |
| `COMPLETED` | Successfully completed, ZIP ready |
| `FAILED` | Processing failed, check logs |

## Error Responses

### 400 Bad Request
```json
{
  "error": "Invalid file path",
  "message": "File path validation failed"
}
```

### 404 Not Found
```json
{
  "error": "Job not found",
  "message": "Job ID does not exist or is not ready"
}
```

### 500 Internal Server Error
```json
{
  "error": "Download failed",
  "message": "File system error occurred"
}
```

## Input File Formats

### Format 1: URL Scraping
```xlsx
| Profile url | Background music URL |
|-------------|---------------------|
| https://... | https://music.mp3   |
```

### Format 2: Direct Data
```xlsx
| Profile Name | Age | Religion | Education | ... |
|-------------|-----|----------|-----------|-----|
| John Doe    | 25  | Hindu    | MBA       | ... |
```

## Response Examples

### Job Status Response (HTML)
```html
<div class="status-container">
  <h2>Processing...</h2>
  <p>Status: <span>PROCESSING</span></p>
  <div class="logs">
    [14:30:25] Started processing job abc123
    [14:30:26] Found 5 profiles to process
    [14:30:27] [1/5] Scraping https://...
    [14:30:30] ✓ Video created for row 0
  </div>
</div>
```

### Download Response
```http
HTTP/1.1 200 OK
Content-Type: application/zip
Content-Disposition: attachment; filename="abc123.zip"
Content-Length: 15728640

[ZIP file binary data]
```

## Rate Limiting
- No explicit rate limiting implemented
- Limited by server resources and FFmpeg processing time
- Recommended: 1 concurrent job per instance

## Authentication
- No authentication required (localhost only)
- For production: implement authentication middleware

## WebSocket Alternative (Future)
For real-time updates without polling:
```javascript
const ws = new WebSocket('ws://127.0.0.1:5000/ws/job/{job_id}');
ws.onmessage = (event) => {
  const log = JSON.parse(event.data);
  console.log(log.message);
};
```

## SDK Example (Python)
```python
import requests
import time

# Upload file
with open('profiles.xlsx', 'rb') as f:
    response = requests.post('http://127.0.0.1:5000/', 
                           files={'file': f})

# Extract job ID from redirect
job_id = response.url.split('/')[-1]

# Poll status
while True:
    status_response = requests.get(f'http://127.0.0.1:5000/status/{job_id}')
    if 'COMPLETED' in status_response.text:
        break
    elif 'FAILED' in status_response.text:
        print("Job failed")
        break
    time.sleep(10)

# Download results
download_response = requests.get(f'http://127.0.0.1:5000/download/{job_id}')
with open(f'{job_id}.zip', 'wb') as f:
    f.write(download_response.content)
```

## Monitoring Endpoints (Future)
```http
GET /health          # Health check
GET /metrics         # Prometheus metrics
GET /jobs            # List all jobs
DELETE /jobs/{id}    # Cancel/delete job
```