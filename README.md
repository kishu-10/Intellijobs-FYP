# IntelliJobs

- For development environment:
    ```
    - Setup .env for non-docker as following:
    ```
    ```
    DEBUG=1
    ENVIRONMENT=development
    SECRET_KEY=foo
    DJANGO_ALLOWED_HOSTS=localhost 127.0.0.1 [::1]
    
    SQL_ENGINE=django.db.backends.postgresql
    SQL_DATABASE=nepal_police_db
    SQL_USER=admin
    SQL_PASSWORD=admin
    SQL_PORT=5432
    SQL_HOST=127.0.0.1

    EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
    EMAIL_HOST=smtp.gmail.com
    EMAIL_HOST_USER=yourmail@gmail.com
    EMAIL_HOST_PASSWORD=password
    EMAIL_PORT=587
    EMAIL_USE_TLS=True
    CONTACT_EMAIL='yourmail@gmail.com'
    ```
    ```
    # celery
    CELERY_BROKER_URL = amqp://localhost
    SESSION_TIMEOUT_SECONDS=300
    ```