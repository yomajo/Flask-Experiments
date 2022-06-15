from app import celery_in, create_app

app = create_app()
app.app_context().push()