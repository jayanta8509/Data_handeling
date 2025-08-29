# CSV Data Processor API

A production-ready FastAPI application for processing Excel and WooCommerce data, comparing CSV files, and identifying unique items. This API automates the workflow of downloading data from multiple sources, converting them to CSV format, and performing efficient comparisons.

## 🚀 Features

- **Excel Processing**: Downloads Excel files from URLs and converts them to CSV format
- **WooCommerce Integration**: Fetches data from WooCommerce API endpoints and saves to CSV
- **Smart Comparison**: Uses vectorized operations to efficiently compare large CSV files
- **Production Ready**: Includes health checks, logging, CORS middleware, and error handling
- **Performance Optimized**: Multiple comparison algorithms for different use cases

## 📁 Project Structure

```
Data_handeling/
├── app.py                 # Main FastAPI application
├── Woocommerce.py         # WooCommerce API integration
├── exl_file.py           # Excel file processing utilities
├── compare.py            # CSV comparison algorithms
├── requirements.txt      # Python dependencies
├── upload/              # Generated CSV files storage
└── README.md           # This file
```

## 🛠️ Core Components

### 1. Main Application (`app.py`)
- FastAPI server with production configuration
- Main `/process` endpoint orchestrating the entire workflow
- Health check endpoint for monitoring
- Comprehensive error handling and logging

### 2. WooCommerce Integration (`Woocommerce.py`)
- Fetches data from WooCommerce API endpoints
- Extracts ID and name fields
- Automatically generates dated CSV filenames
- Handles API errors gracefully

### 3. Excel Processing (`exl_file.py`)
- Downloads Excel files from URLs
- Extracts ARTIST and TITLE columns
- Combines data into "ARTIST - TITLE" format
- Removes duplicates and saves to CSV

### 4. CSV Comparison (`compare.py`)
- **Efficient Set-based**: O(n+m) complexity with set lookups
- **Vectorized**: Ultra-fast pandas operations for large datasets
- **Memory-efficient**: Chunked processing for very large files

## 🚀 Quick Start

### Prerequisites
- Python 3.10+
- Virtual environment (recommended)

### Installation

1. **Clone and navigate to the project directory:**
   ```bash
   cd Data_handeling
   ```

2. **Create and activate virtual environment:**
   ```bash
   python -m venv env
   # On Windows:
   env\Scripts\activate
   # On macOS/Linux:
   source env/bin/activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the application:**
   ```bash
   python app.py
   ```

The API will be available at `http://localhost:8000`

## 📚 API Endpoints

### Health Check
```http
GET /health
```
Returns application status and version information.

### Process Data
```http
GET /process
```
Main endpoint that executes the complete data processing workflow:
1. Downloads and processes Excel file
2. Fetches WooCommerce data
3. Compares both datasets
4. Returns unique items

**Response:**
```json
{
  "status": 200,
  "message": "Data processing completed successfully",
  "unique_ids": [123, 456, 789],
  "unique_count": 3,
  "processing_time": 2.345
}
```

## 🔧 Configuration

### Environment Variables
The application uses the following external URLs (configure as needed):
- **Excel Source**: `https://www.cobraside.com/catalog/instock/STK_With_QTY.xlsx`
- **WooCommerce API**: `https://workflows.poptechstudio.ai/webhook/get-woo-data`

### CORS Settings
Currently configured to allow all origins (`*`). For production, restrict to specific domains.

## 📊 Data Flow

1. **Excel Processing**: Downloads Excel file → extracts ARTIST/TITLE → creates CSV with "ARTIST - TITLE" format
2. **WooCommerce**: Calls API → extracts ID/name → saves to CSV
3. **Comparison**: Loads both CSVs → normalizes text → finds unique names → returns IDs

## 🚀 Performance Features

- **Vectorized Operations**: Uses pandas for fast data processing
- **Memory Management**: Chunked processing for large files
- **Efficient Lookups**: Set-based comparisons for O(1) performance
- **Background Processing**: Supports async operations

## 📝 Logging

The application includes comprehensive logging:
- Processing start/completion times
- File generation status
- Comparison results
- Error details

## 🔒 Security Considerations

- SSL verification disabled for Excel downloads (configure as needed)
- CORS middleware for cross-origin requests
- Input validation with Pydantic models
- Error handling without exposing sensitive information

## 🧪 Testing

Test the API endpoints:
- **Health Check**: `http://localhost:8000/health`
- **API Documentation**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`

## 📦 Dependencies

Key dependencies include:
- **FastAPI**: Modern web framework for building APIs
- **Pandas**: Data manipulation and analysis
- **OpenPyXL**: Excel file processing
- **Requests**: HTTP library for API calls
- **Uvicorn**: ASGI server for production deployment

## 🚀 Deployment

### Production Settings
- Set `reload=False` in uvicorn configuration
- Configure appropriate `workers` based on CPU cores
- Restrict CORS origins for security
- Enable SSL verification for external requests

### Docker (Optional)
```dockerfile
FROM python:3.10-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["python", "app.py"]
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📄 License

This project is open source and available under the [MIT License](LICENSE).

## 🆘 Support

For issues and questions:
1. Check the API documentation at `/docs`
2. Review the logs for error details
3. Ensure all dependencies are properly installed
4. Verify external API endpoints are accessible

---

**Note**: This API is designed for production use with proper error handling, logging, and performance optimization. The comparison algorithms are optimized for large datasets and can handle millions of records efficiently.
