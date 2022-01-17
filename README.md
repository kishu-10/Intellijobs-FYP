# IntelliJobs

- For development environment:

    ```
    - Setup .env for virtual env as following:
    DEBUG=1
    SECRET_KEY=i5zzwf7(t9yne1reo=br%ce(cd2v%pa)nbm1)$g%gdck=8_*b^
    ENVIRONMENT=development

    DB_ENGINE=django.db.backends.postgresql
    DB_NAME=dbname
    DB_USER=postgres
    DB_PASSWORD=postgres
    DB_HOST=localhost
    DB_PORT=5432

    EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
    EMAIL_HOST=smtp.gmail.com
    EMAIL_USE_TLS=True
    EMAIL_USE_SSL=True
    EMAIL_PORT=587
    EMAIL_HOST_USER=yourmail@gmail.com
    EMAIL_HOST_PASSWORD=password
    ```