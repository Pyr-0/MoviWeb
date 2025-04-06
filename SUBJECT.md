# MoviWeb App: Flask Web Application Project

## Prologue

Welcome to the MoviWeb App project! Here, you'll transform your static movie application into a full-featured, dynamic web application. Remember that initial movie application you built with a command-line interface? We're going to give it a major upgrade using Flask and user-specific functionalities.

### 🌐 From CLI to the Web
Picture this: your movie application, instead of running through a command line or static HTML pages, is accessible from anywhere on the web. The MoviWeb App allows users to pick their identity and then view, add, update, or delete movies from their personalized favorite movie list. It's an exciting transformation that will truly test your newly acquired Flask skills.

### 👑 New code base
We won't be proceeding with your existing code. Dealing with outdated code can lead to issues since there are numerous sections that are no longer applicable, such as the CLI component. The optimal approach to move forward is by initiating a fresh project, free from any previous code.

### 🗃️ Adding SQLite Support
We've been managing our data using JSON so far, but as our data grows, we'll need a more robust system. In the first stage, we'll implement an SQLite data manager, setting up our database and creating our first tables. This will provide a much more scalable solution for handling our data.

### 💡 Project Scope
In this project, you'll be dealing with a variety of tasks: HTML templating, handling user interactions, managing a database, and more. Above all, you will need to think about how to structure your application to handle user-specific features.

### 🛠️ Embrace the Challenge
The journey might seem challenging, but that's where the fun and learning are. Applying the best software engineering practices, splitting tasks into manageable chunks, and incremental development will help you reach your goal.

Stay focused, enjoy the journey, and let's bring this fantastic project to life! The next sections will guide you through the detailed project structure and the core functionalities required. Happy coding! 🚀

## Step 1: Project Structure and Core Functionalities

This section outlines the structure of your MoviWeb application, and the core functionalities that will be needed to successfully implement the user-specific features. Let's break it down.

### 🧱 Application Structure
The MoviWeb application will consist of several key parts:
- **User Interface (UI)**: An intuitive web interface built using Flask, HTML, and CSS. It will provide forms for adding, updating, and deleting movies, as well as a method to select a user.
- **Data Management**: A Python class to handle operations related to the data source. This class should expose functions for getting all users, getting a user's movies, and updating a user's movie.
- **Database file**: For storing user and movie data. This file can be a .db or .sqlite file.

### 📝 Core Functionalities
The core functionalities of your MoviWeb application will include:
- **User Selection**: The ability for a user to select their identity from a list of users.
- **Movie Management**: After a user is selected, the application will display a list of their favorite movies. From here, users should be able to:
  - Add a movie: Include the movie's name, director, year of release, and rating.
  - Delete a movie: Remove a movie from their list.
  - Update a movie: Modify the information of a movie from their list.
  - List all movies: View all the movies on their list.
- **Data Source Management**: Use your Python class to manage interactions with the database.

The next sections will walk you through how to set up your development environment, how to implement these features step-by-step, and how to test your application to ensure everything works as expected. Let's get started! 💪🚀

## Step 2: Planning Your Database

Before you dive into building the application, let's take some time to design the data structure that will support our app. This can save a lot of time and confusion later.

### User and Movie Information
The MoviWeb app will keep track of different users and their favorite movies. Each user can have multiple movies, and each movie will have its own set of details.

At the very least, each User in our app should have:
- A unique identifier (id)
- A name (name)

Each Movie should have:
- A unique identifier (id)
- The movie's name (name)
- The movie's director (director)
- The year of release (year)
- The rating of the movie (rating)

### Class for Data Management
We need a Python class that will interface with the data. Let's call it DataManager. This class will be responsible for reading the data source, and providing methods to manipulate the data (like adding, updating, or removing movies).

This is just a high-level view. In the next section, we'll start implementing these ideas and gradually bring our MoviWeb App to life. Remember to take small steps and test your code as you go. You've got this! 💪🚀

## Step 3: Implementing the DataManager Class with Interface

Your new task will be to create a data manager to handle the application's data. The key idea is to make this component flexible, so in the future, it can manage different kinds of data sources and different databases.

To achieve this, we will use a principle called polymorphism, which is a Greek word that means "many shapes". In the context of object-oriented programming, polymorphism is the provision of a single interface to represent different types.

In other words, we'll define an interface (a sort of contract) that each DataManager will implement, regardless of the data source it works with. This will make our code more modular and easy to maintain or expand in the future.

### Creating the DataManager Interface
First, we'll define an interface for our DataManager using Python's abc (Abstract Base Classes) module. Our DataManager interface will specify a few methods that every DataManager needs to implement.

```python
from abc import ABC, abstractmethod

class DataManagerInterface(ABC):
    @abstractmethod
    def get_all_users(self):
        pass

    @abstractmethod
    def get_user_movies(self, user_id):
        pass
```

As you work through this project, you might find you need more methods. When this happens, think about whether each new method is specific to one kind of DataManager (e.g., SQLite, JSON, CSV, etc.) or whether it should be added to the interface.

Here are a few things to consider:
- If the method involves a task that all DataManagers must perform, then it should be added to the interface.
- If the method's task is specific to a certain type of DataManager (like reading or writing to a JSON file), then it should not be added to the interface.

Remember, the purpose of an interface is to specify a set of common methods that different classes will implement in their own way. So keep your interface lean and generic, and put specific operations in the individual DataManager classes.

## Step 4: SQLiteDataManager

After designing and implementing your database schema, and creating the abstract DataManager, now it's time to create a SQLiteDataManager class to work with your new schema. In this section, you're going to implement the methods for interacting with your database.

### 🏗️ Basic Setup
Now that you've decided how to interact with the database, let's talk about implementing the SQLiteDataManager.

The SQLiteDataManager will be a new implementation of the DataManagerInterface. This class will use SQLAlchemy to interact with a SQLite database.

Here's how you might set up the SQLiteDataManager class:
```python
from flask_sqlalchemy import SQLAlchemy
from data_manager_interface import DataManagerInterface

class SQLiteDataManager(DataManagerInterface):
    def __init__(self, db_file_name):
        self.db = SQLAlchemy(db_file_name)
```

You'll need to fill out the rest of the class by implementing all the methods required by DataManagerInterface, using either SQLAlchemy ORM or raw SQL depending on your earlier choice.

Remember to update the DataManagerInterface if you realize that more methods are needed. This might happen as you start to implement the CRUD operations.

### 🏋️‍♀️ Implement SQLiteDataManager
Note that in this section we present the default CRUD methods that we presented in the previous MovieApp projects. Of course, if you used other methods in your DataManager interface, implement these too.

1. **Initialization**: Create a constructor for SQLiteDataManager, that should get the database file name as a parameter. Don't forget to set up the engine, session, and other necessary SQLAlchemy components if you need to.

2. **Get All Users**: Implement the method get_all_users(). This should return a list of all users in your database. If you're using ORM, you can use a simple query on your User model. If you're using raw SQL, you will need to write a SELECT statement.

3. **Get User Movies**: Implement the method get_user_movies(user_id). This should return a list of all movies of a specific user. Again, if you're using ORM, this should be a simple query.

4. **Add User**: Implement the method add_user(user). This should add a new user to your database. If you're using ORM, you can create a new instance of your User model and add it to your session. If you're using raw SQL, you'll need an INSERT statement.

5. **Add Movie**: Implement the method add_movie(movie). This should add a new movie to your database. The process should be similar to adding a new user.

6. **Update Movie**: Implement the method update_movie(movie). This should update the details of a specific movie in your database.

7. **Delete Movie**: Implement the method delete_movie(movie_id). This should delete a specific movie from your database.

Take your time to get this right! Remember to test each method thoroughly to make sure it's working as expected. Don't forget to commit your changes if you're using ORM!

Once you've finished implementing the SQLiteDataManager, you're ready to update your Flask application to use it. Keep going, you're doing great! 🚀

## Step 5: Setting Up Your Flask Application

Having our DataManager ready to go, it's time to start building our Flask application! This will be the server side of our MovieWeb App, and it's the part that will be interacting with our DataManager to perform all CRUD operations.

In this section, we're going to establish the foundations of our application.

### 📁 Organizing Your Project
To start, let's create a new Python file for your Flask application and call it app.py. Project organization is key for code maintenance and readability, so let's try to keep a neat structure. Here's a recommended way to organize your files:

```
MoviWebApp/
|-- app.py
|-- datamanager/
|   |-- __init__.py
|   |-- data_manager_interface.py
|   |-- sqlite_data_manager.py
|-- static/
|-- templates/
```

In Python, a directory must contain a file named __init__.py for Python to recognize it as a package. This file can be empty, but it can also contain code. Its purpose is to include any initialization code that needs to run when the package is imported. In our case, the datamanager directory contains an __init__.py file to make it a package.

The static directory is used to store static files like CSS and JavaScript files. The templates directory, on the other hand, is used to store HTML templates. We'll talk more about these later.

In the app.py file, import Flask and create a new Flask application:
```python
from flask import Flask

app = Flask(__name__)
```

### 🌐 Setting Up Routes
Your Flask application will work with routes to decide what action to perform based on the URL a user visits. For instance, if a user goes to http://yourapp.com/users, your app might display a list of all users.

Let's create a single route for testing. We'll have it return a simple message:
```python
@app.route('/')
def home():
    return "Welcome to MovieWeb App!"
```

To run your Flask application, add these lines at the end of app.py:
```python
if __name__ == '__main__':
    app.run(debug=True)
```

Now you can start your application and navigate to http://localhost:5000 on your web browser. You should see the message: "Welcome to MovieWeb App!"

In the next section, we'll be integrating our DataManager with our Flask application to start building more complex routes. Buckle up, it's about to get interesting! 🚀

## Step 6: Integrating DataManager with Flask App

Now that we've laid the groundwork for our Flask application, it's time to integrate our DataManager class. Remember, the purpose of the DataManager is to interact with our data source. The Flask application will use the DataManager to perform operations based on the requests it receives.

In this section, we're going to show how to create an instance of our SQLiteDataManager in the Flask app and use it to create a more meaningful route.

### 📝 Integrating DataManager
In the app.py file, import the SQLiteDataManager class and instantiate it:
```python
from flask import Flask
from datamanager.sqlite_data_manager import SQLiteDataManager

app = Flask(__name__)
data_manager = SQLiteDataManager('moviwebapp.db')  # Use the appropriate path to your Database
```

Now that we have a data_manager object, we can use it to interact with our data.

### 🌐 Creating a Meaningful Route
Let's create a new route in our Flask application that lists all users:
```python
@app.route('/users')
def list_users():
    users = data_manager.get_all_users()
    return str(users)  # Temporarily returning users as a string
```

Now, when you navigate to http://localhost:5000/users, you should see a list of all users. Remember, we're temporarily returning the users as a string for simplicity, but in a real application, you'll likely want to return a nicely formatted HTML page or a JSON response.

In the upcoming sections, we'll learn how to use Flask's templating engine to return HTML pages that are dynamic and interactive. We'll also delve into how to handle form data and user input.

Keep up the good work, you're making great progress! 🚀

## Step 7: Planning Your Routes

Before diving into writing code for our MovieWeb App, it's paramount to first plan out the different routes our application will encompass. Laying out this roadmap will provide a clear structure for our app and guide us as we implement its functionality.

### 🗺 Route Map
Here's the planned blueprint for our MovieWeb App:

1. **Home (/)**:
   - This will be the home page of our application.
   - You have the creative liberty to design this as a simple welcome screen or a more elaborate dashboard.

2. **Users List (/users)**:
   - This route will present a list of all users registered in our MovieWeb App.

3. **User Movies (/users/<user_id>)**:
   - This route will exhibit a specific user's list of favorite movies.
   - We will use the <user_id> in the route to fetch the appropriate user's movies.

4. **Add User (/add_user)**:
   - This route will present a form that enables the addition of a new user to our MovieWeb App.

5. **Add Movie (/users/<user_id>/add_movie)**:
   - This route will display a form to add a new movie to a user's list of favorite movies.

6. **Update Movie (/users/<user_id>/update_movie/<movie_id>)**:
   - This route will display a form allowing for the updating of details of a specific movie in a user's list.

7. **Delete Movie (/users/<user_id>/delete_movie/<movie_id>)**:
   - Upon visiting this route, a specific movie will be removed from a user's favorite movie list.

### 🚧 Starting the Implementation
With our route map in place, we can now begin the implementation of these routes in our Flask app.

We'll start with the Users List route. In the upcoming section, we'll guide you on implementing this route and utilizing Flask's built-in templating engine to return an HTML page that dynamically displays our users.

By mapping our routes first, we've set a sturdy foundation for our app. Let's get building! 🚀

## Step 8: Implementing the User List Page

Now that we have our routes planned, it's time to begin implementing them. We'll start with the Users List route. This route will display all the users registered in our MovieWeb App.

### 🎨 Creating the Template
First, let's create an HTML template for the Users List page.

Your task is to create an HTML file in the templates directory of your Flask application. You can name it users.html.

This HTML file should be structured to:
- Include a title in the `<head>` section. The title should be "Users - MovieWeb App".
- In the `<body>` section, include a header (h1) with the text "Users".
- Under the header, include a list (ul) that will be filled dynamically with the list of users.
- Each user should be presented as a link that navigates to their favorite movies page (/users/<user_id>).

Remember to use Jinja2's `{% for %}` statement to iterate over the list of users and the `{{ }}` syntax to output each user's name and create the link.

### 🚀 Implementing the Route
With the template created, let's now implement the route in our Flask application.

To do this, you'll need to modify the app.py file and create a new function called list_users. This function should use the DataManager class to fetch the list of users, and then pass this list to the users.html template using the render_template function.

The code to render the template will look something like this:
```python
@app.route('/users')
def list_users():
    users = data_manager.list_all_users()
    return render_template('users.html', users=users)
```

Don't forget to add the `@app.route('/users')` decorator above the list_users function to map it to the /users route.

Once you've implemented this route, run your Flask application and navigate to http://localhost:5000/users on your web browser. If everything's set up correctly, you should see a list of users displayed on the page, each as a link that leads to their favorite movies page.

Great job, you've just implemented the first page of your MovieWeb App! 🚀

In the next section, we'll tackle the implementation of the User Movies route.

## Step 9: Building the Other Routes

With the User List page successfully implemented, it's time to move on to the other routes we've planned. Remember, the aim here is not to spoon-feed you every step of the way, but rather to guide you as you learn to implement these features independently.

### 📍 What We're Building
Here's a quick recap of the other routes you'll need to implement:

1. **User Movies (/users/<user_id>)**:
   - This page should display a list of the selected user's favorite movies.
   - Each movie should have options to edit and delete it.

2. **Add User (/add_user)**:
   - This page should display a form allowing a new user to be added to the MovieWeb App.

3. **Add Movie (/users/<user_id>/add_movie)**:
   - This page should display a form allowing a new movie to be added to the user's list of favorite movies.

4. **Update Movie (/users/<user_id>/update_movie/<movie_id>)**:
   - This page should display a form pre-filled with the current details of the selected movie.
   - Any changes made here should be reflected in the user's list of movies.

5. **Delete Movie (/users/<user_id>/delete_movie/<movie_id>)**:
   - Visiting this route should delete the selected movie from the user's list of favorite movies.

### 🎞️ OMDb API
As in the previous parts of the project, when a movie is added to your application, fetch the relevant movie details from OMDb API.

On movie update, the user can edit the information that was fetched from OMDb. For example, the user can edit the title or the rating manually and override the results that were retrieved from OMDB.

### 📝 Considerations
As you build out these routes, remember these key points:

1. **Templates**:
   - Each page will need a corresponding HTML template in the templates directory.
   - Think about how these templates can be structured and how data can be passed to them from the Flask app.

2. **Data Management**:
   - All interactions with the underlying data should go through the DataManager class.
   - When adding, editing, or deleting movies, remember to call the appropriate DataManager methods.

3. **Route Parameters**:
   - Pay attention to how <user_id> and <movie_id> are used in the routes.
   - These are variable parts of the URL, and their values can be accessed within your route functions.

4. **Form Handling**:
   - The 'Add User', 'Add Movie', and 'Update Movie' routes will involve forms.
   - Recall how to handle form data in Flask and how to use this data to update the state of your application.

### Same Route, Different Methods
Hint: We can use the same route to both display the form for adding a user and handle the form submission. This works by distinguishing between GET and POST requests.

Recall that GET requests are used to retrieve and display data, while POST requests are used to submit data. Similar logic can apply for other functionalities such as adding a movie.

### 🚀 Moving Forward
Implementing these routes will involve a good amount of problem-solving and perhaps a bit of trial and error. But don't be discouraged. Each challenge you encounter is an opportunity to learn and grow as a software engineer.

Remember to refer back to your notes, use online resources, and ask for help when you need it. With perseverance and a positive mindset, you'll be able to bring your MovieWeb App to life.

On your mark, get set, code! 🚀

## Step 10: Error Handling

Creating a robust application is not just about building features. It's also about anticipating potential problems and handling them gracefully. This process is often known as error handling. Even though your MovieWeb App might not be dealing with significant risks, it's important to understand and practice good error handling.

### 🌐 HTTP Errors
In the context of web applications, one common form of error handling involves HTTP status codes. There are several HTTP status codes that represent specific types of errors:

1. **4xx codes** represent client errors:
   - The most well-known is probably 404 Not Found, which is returned when the client requests a resource that does not exist.

2. **5xx codes** represent server errors:
   - For example, 500 Internal Server Error indicates an error on the server that is not the client's fault.

In Flask, you can define error handlers for these status codes. Here's how you can create a simple error handler for 404 Not Found:
```python
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404
```

With this error handler, whenever a 404 Not Found error occurs, Flask will render a 404.html template. You can create this template and customize it to fit your app's look and feel.

### 🐞 Exceptions
In Python, when an error occurs, an exception is raised. If this exception is not caught and handled, it will propagate up the call stack and might cause your program to terminate.

In your MovieWeb App, you should anticipate and handle exceptions that might occur. For example:
- What happens if there's an error reading or writing to the database?
- Or what if a function receives an argument of an unexpected type?

Here's how you can handle exceptions in Python:
```python
try:
    # Code that might raise an exception
    data = load_data()
except IOError as e:
    # Code to handle the exception
    print("An IOError occurred: ", str(e))
```

With this try/except block, if an IOError is raised when calling load_data(), the error will be caught and handled by the except block.

### 🚀 Going Forward
As you continue developing your MovieWeb App, consider where errors might occur and how you can handle them. This could involve:
- Returning informative error messages
- Redirecting to a different page
- Logging the error for future investigation

Error handling is an essential part of developing robust, reliable software. So while it might seem like extra work, remember that it's an investment in the quality and stability of your app. Good luck! 