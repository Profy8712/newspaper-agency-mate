# newspaper-agency-mate

[Newspaper Agency deployed to render](https://newspaper-agency-mate-dllr.onrender.com/newspaper//)

A Django-based system for managing newspapers, topics and redactors with beautiful frontend.

## Installation

Python3 must be already installed

1. Clone the repository:
git clone https://github.com/yourusername/newspaper-agency.git
cd newspaper-agency
2. Create and activate virtual environment:
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate    # Windows
3. Install dependencies:
pip install -r requirements.txt
4. Apply migrations:
python manage.py migrate
5. Create superuser:
python manage.py createsuperuser
6. Run development server:
python manage.py runserver
7. Access the admin panel at http://localhost:8000/admin/

## Features

- Custom user model (Redactor)
- CRUD operations for all entities
- Search and filtering
- Pagination
- Authentication system
- Modern Bootstrap 5 UI
- Crispy Forms for beautiful forms
- Responsive design
- Smooth animations
- 
## Demo

![Website Interface](demo.png)
