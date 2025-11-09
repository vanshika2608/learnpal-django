# LearnPal — Personal Learning Assistant

LearnPal is a Django-based web application that helps students plan, manage, and track their learning goals.  
It includes a simple machine learning–based recommender system that suggests useful learning resources based on user goals.

## Features

- User authentication (login and signup)
- Add, edit, and delete learning goals
- Track goal progress and completion
- View progress analytics on a dashboard
- Get smart resource recommendations using TF-IDF and cosine similarity
- Add and manage study resources linked to goals
- Dark-themed modern UI
- Built with responsive design for desktop and mobile

## Tools and Technologies Used

| Category | Tools/Technologies |
|-----------|--------------------|
| Frontend | HTML, CSS, JavaScript, Bootstrap |
| Backend | Django (Python) |
| Database | SQLite3 |
| Machine Learning | scikit-learn |
| Version Control | Git, GitHub |
| IDE | VS Code / PyCharm |

## Installation & Setup

### 1. Clone the repository
```bash
git clone https://github.com/vanshika2608/learnpal-django.git
cd learnpal-django
```

### 2. Create and activate a virtual environment
```bash
python3 -m venv venv
source venv/bin/activate   # macOS/Linux
venv\Scripts\activate      # Windows
```

### 3. Install required dependencies
```bash
pip install -r requirements.txt
```

### 4. Apply migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

### 5. Run the server
```bash
python manage.py runserver
```

Then open your browser and go to:
```
http://127.0.0.1:8000/
```

## Machine Learning Recommender

The recommender system uses:
- **TF-IDF Vectorizer** to convert text (learning goals) into feature vectors.
- **Cosine Similarity** to find and suggest similar learning topics.

This provides personalized learning resource recommendations based on user goals.

### Example:
If your recent goal is:
> “Learn Python for Data Science”

The system might recommend:
> “Statistics Basics”, “Pandas and NumPy”, “Data Visualization with Matplotlib”, etc.

## Example Workflow

1. Log in or create an account  
2. Add your learning goals (e.g., “Learn Python”, “Study Machine Learning”)  
3. View your dashboard to track progress and see upcoming deadlines  
4. Get recommended topics and resources automatically  
5. Add or remove learning materials as needed  

## Testing & Version Control

- Integration and regression testing using Django’s test framework  
- Git and GitHub used for version control  
- Local deployment testing for stable builds  

## Future Enhancements

- Collaborative filtering for advanced recommendations  
- Email or notification reminders  
- Export progress reports as PDFs  
- Cloud data sync  
- Enhanced analytics with charts  

## Author

**Vanshika Deswal**  
B.Tech Computer Science and Engineering  
India  
[GitHub Profile](https://github.com/vanshika2608)
