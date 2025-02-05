# Business Valuation Tool

A web application that provides free business valuation services. Users can input their business metrics or upload tax returns to get an automated valuation of their business.

## Features

- User authentication (register/login)
- Business metrics input form
- Tax return PDF upload with automatic data extraction
- Multiple valuation methods (Enterprise Value, Equity Value, DCF)
- Modern, responsive UI
- Secure data handling

## Setup

1. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the application:
```bash
python app.py
```

The application will be available at `http://localhost:5000`

## Tech Stack

- Backend: Python Flask
- Database: SQLite with SQLAlchemy
- Frontend: HTML5, CSS3, JavaScript
- UI Framework: Bootstrap 5
- PDF Processing: pdfplumber
- Authentication: Flask-Login

## Security Notes

- Never store sensitive information like API keys directly in the code
- All passwords are hashed before storage
- File uploads are validated and restricted to PDFs
- CSRF protection is enabled by default

## Development

To contribute to this project:

1. Fork the repository
2. Create a new branch for your feature
3. Make your changes
4. Submit a pull request

## License

MIT License
