# SSL configuration for Supabase compatibility
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'your_db_name',
        'USER': 'your_user',
        'PASSWORD': 'your_password',
        'HOST': 'your_host',
        'PORT': 'your_port',
        'OPTIONS': {'sslmode': 'require'},  # Updated SSL configuration
    }
}