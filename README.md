#  Social_Media_Friends_recomendation_system

 A web-based application that suggests potential friends to users based on their interests and interactions. Utilizing machine learning algorithms, the system analyzes user data to provide personalized friend recommendations.

## Algorithm: Jaccard Similarity

The recommendation engine is powered by the Jaccard Similarity algorithm. It measures similarity between two sets (in this case, sets of user interests andd mutual relationship ) as follows:
Jaccard Similarity (A, B)= ∣A∪B∣ / ∣A∩B∣

Where
- A and B are sets of interests of two users.

- The result is a value between 0 and 1 indicating how similar the users are.

- A higher value means more shared interests → higher recommendation priority.

## Features

- **User Registration & Authentication**: Secure sign-up and login functionalities.

- **Interest Profiling**: Users can select and update their interests.

- **Friend Recommendations**: Personalized suggestions based on shared interests and user behavior.

- **Interactive UI**: Responsive design for seamless user experience.

## Tech Stack

- **Frontend**: HTML, CSS
- **Backend**: Python (Flask)
- **Database**: SQLite
- **Machine Learning**: Scikit-learn

## Prerequisites

Before running the project, make sure you have the following installed:

- Python 3.7 or higher
- Flask
- SQLite (or another supported database)


To install the required Python packages, run:

1. **Clone the Repository:**
   
   ```bash
   git clone https://github.com/Rahul23ship/Friends_recomendation_system.git
   cd Friends_recomendation_system
   ```
2. **Create a virtual environment:**
 
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
   
3. **Run the application:**
 
   ```bash
   python app.py
   ```
   
Access the app at http://localhost:5000.
   
## Project Structure

   ```cpp
   Friends_recomendation_system/
├── app.py
├── templates/
│   ├── index.html
│   └── ...
├── static/
│   ├── Styles.css/   
├── instance/
│   └── database.db
├── requirements.txt
└── README.md
```

##  Contribution

This project was developed as a collaborative effort by a team of four members, each contributing to different aspects such as data collection, feature engineering, model development, and web integration. 
By combining our individual strengths in data science, software development, and design, we successfully built a functional and user-friendly friends recommendation system. 
Teamwork, continuous feedback, and shared learning were key to the successful execution of this project.

##  Acknowledgements

We would like to thank everyone who supported and guided us throughout this project.
Special thanks to our mentors and instructors for their valuable feedback and encouragement.
Thanks also to the open-source community for the tools and libraries that made this project possible. 

Finally, we sincerely thank each team member for their unwavering dedication, collaborative spirit, and consistent efforts in bringing this project to fruition.
