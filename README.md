# **Currency App API**

---

Welcome to the Currency App API project! This application is designed to provide currency conversion functionalities, fetch daily currency rates, and send email notifications to users with the latest currency rates using Celery workers. Below you'll find instructions on how to set up and use the application effectively.

### Features:

1. **Currency Conversion:**
    - Convert currency from one to another based on the latest exchange rates.
    - Supports a wide range of currencies.

2. **Daily Currency Rate:**
    - Fetches the latest daily currency rates from a reliable API source.

3. **Email Notifications:**
    - Sends daily currency rate updates to users via email using Celery workers to handle asynchronous tasks efficiently.

### Setup Instructions:

1. **Clone the Repository:**
    ```
    git clone https://github.com/Dave1607/currency_app.git
    cd currency_app
    ```

2. **Install Dependencies:**
    ```
    pip install -r requirements.txt
    ```

3. **Configuration:**
    - Set up your environment variables for API keys, email configurations, and any other sensitive information required.
    
4. **Run Migrations:**
    ```
    python manage.py migrate
    ```

5. **Run Celery Worker:**
    ```
    celery -A currency_app worker --loglevel=info
    ```

6. **Start the Server:**
    ```
    python manage.py runserver
    ```

### API Endpoints:

- **Currency Conversion:**
    - Endpoint: `/convert`
    - Method: POST
    - Parameters: `amount`, `from_currency`, `to_currency`
    - Example: `curl -X POST http://localhost:8000/convert -d "amount=100&from_currency=USD&to_currency=EUR"`

- **Daily Currency Rate:**
    - Endpoint: `/rate-reminder/`
    - Method: POST
    - Parameters: 'name', 'email, 'currency_code'
    - Example: `curl http://localhost:8000/rate-reminder -d "name=dave&email=email@gmail.com&currency_code=EUR"`
`

### Email Notifications:

- Ensure that Celery worker is running to handle background tasks.
- Users will receive daily currency rate updates via email as configured in the application settings.

### Contributing:

Contributions are welcome! If you have any suggestions, bug reports, or would like to contribute to the project, please feel free to open an issue or submit a pull request.

Thank you for using the Currency App API! If you have any questions or need further assistance, feel free to contact us. Happy coding! 🚀
