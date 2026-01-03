# PythonAnywhere Deployment Guide

This guide provides step-by-step instructions for setting up automatic deployment from GitHub to PythonAnywhere for the Django e-commerce project.

## Table of Contents

- [Prerequisites](#prerequisites)
- [PythonAnywhere Setup](#pythonanywhere-setup)
- [GitHub Repository Setup](#github-repository-setup)
- [GitHub Secrets Configuration](#github-secrets-configuration)
- [Environment Variables](#environment-variables)
- [Manual Deployment](#manual-deployment)
- [Troubleshooting](#troubleshooting)
- [Additional Resources](#additional-resources)

## Prerequisites

Before you begin, ensure you have:

- A PythonAnywhere account (free or paid tier)
- A GitHub account with this repository
- Git installed on your local machine
- Basic knowledge of Django and shell commands

## PythonAnywhere Setup

### 1. Create a PythonAnywhere Account

1. Go to [PythonAnywhere](https://www.pythonanywhere.com/) and sign up for an account
2. Choose a username (this will be part of your web app URL)
3. Verify your email address

### 2. Generate API Token

1. Log in to PythonAnywhere
2. Go to **Account** → **API token**
3. Click **Create a new API token**
4. Copy and save this token securely (you'll need it for GitHub Secrets)

### 3. Set Up SSH Access (for GitHub Actions)

1. In PythonAnywhere, open a **Bash console**
2. Generate an SSH key pair (if not already exists):
   ```bash
   ssh-keygen -t rsa -b 4096 -C "your_email@example.com"
   ```
3. Press Enter to accept default file location
4. Set a password for the SSH key
5. Save this password securely (needed for GitHub Secrets)

### 4. Clone Your Repository

1. Open a **Bash console** in PythonAnywhere
2. Clone your repository:
   ```bash
   cd ~
   git clone https://github.com/K-s-c49/django-ecommerce-project.git
   cd django-ecommerce-project
   ```

### 5. Create Virtual Environment

1. In the Bash console, create a virtual environment:
   ```bash
   mkvirtualenv --python=/usr/bin/python3.10 django-ecommerce-env
   ```
2. Activate the virtual environment:
   ```bash
   workon django-ecommerce-env
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

### 6. Configure Web App

1. Go to **Web** tab in PythonAnywhere dashboard
2. Click **Add a new web app**
3. Choose **Manual configuration** (not Django wizard)
4. Select Python version (3.10 or later)
5. Click **Next**

### 7. Configure WSGI File

1. In the **Web** tab, find the **Code** section
2. Click on the WSGI configuration file link
3. Delete the default content and replace with:
   ```python
   import os
   import sys
   
   # Add your project directory to the sys.path
   path = '/home/yourusername/django-ecommerce-project'
   if path not in sys.path:
       sys.path.insert(0, path)
   
   # Set environment variable for Django settings
   os.environ['DJANGO_SETTINGS_MODULE'] = 'ec.settings'
   
   # Activate virtual environment
   activate_this = '/home/yourusername/.virtualenvs/django-ecommerce-env/bin/activate_this.py'
   exec(open(activate_this).read(), {'__file__': activate_this})
   
   # Import Django application
   from django.core.wsgi import get_wsgi_application
   application = get_wsgi_application()
   ```
4. Replace `yourusername` with your actual PythonAnywhere username
5. Click **Save**

### 8. Configure Virtual Environment Path

1. Still in the **Web** tab, find the **Virtualenv** section
2. Enter the path to your virtual environment:
   ```
   /home/yourusername/.virtualenvs/django-ecommerce-env
   ```
3. Replace `yourusername` with your actual username

### 9. Configure Static Files

1. In the **Web** tab, scroll to **Static files** section
2. Add the following mappings:

   | URL           | Directory                                                    |
   |---------------|--------------------------------------------------------------|
   | /static/      | /home/yourusername/django-ecommerce-project/staticfiles     |
   | /media/       | /home/yourusername/django-ecommerce-project/media           |

3. Replace `yourusername` with your actual username

### 10. Set Environment Variables

1. In the **Web** tab, scroll to **Environment variables** section (if available) or use .env file
2. Add the following environment variables:
   ```
   DJANGO_DEBUG=False
   DJANGO_SECRET_KEY=your-secure-secret-key-here
   DJANGO_ALLOWED_HOSTS=yourusername.pythonanywhere.com
   DJANGO_CSRF_TRUSTED_ORIGINS=https://yourusername.pythonanywhere.com
   RAZOR_KEY_ID=your-razorpay-key-id
   RAZOR_KEY_SECRET=your-razorpay-secret
   ```

3. For secret key, generate a secure one using:
   ```bash
   python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())'
   ```

### 11. Run Initial Setup Commands

1. Open a Bash console and activate your virtual environment:
   ```bash
   workon django-ecommerce-env
   cd ~/django-ecommerce-project
   ```

2. Run migrations:
   ```bash
   python manage.py migrate
   ```

3. Collect static files:
   ```bash
   python manage.py collectstatic --noinput
   ```

4. Create a superuser:
   ```bash
   python manage.py createsuperuser
   ```

### 12. Reload Web App

1. Go back to the **Web** tab
2. Click the green **Reload** button
3. Click on your web app URL to verify it's working

## GitHub Repository Setup

### 1. Enable GitHub Actions

1. Go to your GitHub repository
2. Click on **Settings** → **Actions** → **General**
3. Under **Actions permissions**, ensure "Allow all actions and reusable workflows" is selected
4. Click **Save**

## GitHub Secrets Configuration

To enable automatic deployment, you need to configure the following secrets in your GitHub repository:

1. Go to your GitHub repository
2. Click **Settings** → **Secrets and variables** → **Actions**
3. Click **New repository secret** for each of the following:

### Required Secrets

| Secret Name                    | Description                                          | Example Value                                          |
|--------------------------------|------------------------------------------------------|--------------------------------------------------------|
| `PYTHONANYWHERE_USERNAME`      | Your PythonAnywhere username                         | `yourusername`                                         |
| `PYTHONANYWHERE_PASSWORD`      | SSH password you set when creating SSH key           | `your-ssh-password`                                    |
| `PYTHONANYWHERE_API_TOKEN`     | API token from PythonAnywhere                        | `a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6q7r8s9t0`            |
| `PYTHONANYWHERE_PROJECT_DIR`   | Full path to your project on PythonAnywhere          | `/home/yourusername/django-ecommerce-project`          |
| `PYTHONANYWHERE_VENV_DIR`      | Full path to your virtual environment                | `/home/yourusername/.virtualenvs/django-ecommerce-env` |
| `PYTHONANYWHERE_WEBAPP_NAME`   | Your web app domain name                             | `yourusername.pythonanywhere.com`                      |

### How to Add Secrets

For each secret:
1. Click **New repository secret**
2. Enter the **Name** (exactly as shown in the table above)
3. Enter the **Value**
4. Click **Add secret**

## Environment Variables

The following environment variables should be configured in PythonAnywhere:

### Required Environment Variables

| Variable                      | Description                                    | Example Value                              |
|-------------------------------|------------------------------------------------|--------------------------------------------|
| `DJANGO_SECRET_KEY`           | Django secret key for production               | Generate using Django utility              |
| `DJANGO_DEBUG`                | Debug mode (should be False in production)     | `False`                                    |
| `DJANGO_ALLOWED_HOSTS`        | Comma-separated list of allowed hosts          | `yourusername.pythonanywhere.com`          |
| `DJANGO_CSRF_TRUSTED_ORIGINS` | Comma-separated list of trusted origins        | `https://yourusername.pythonanywhere.com`  |

### Optional Environment Variables

| Variable                | Description                          | Example Value              |
|-------------------------|--------------------------------------|----------------------------|
| `RAZOR_KEY_ID`          | Razorpay API Key ID                  | `rzp_test_xxxxxxxxxxxxx`   |
| `RAZOR_KEY_SECRET`      | Razorpay API Secret                  | `xxxxxxxxxxxxxxxxxxxxxxxx` |
| `DATABASE_URL`          | Database connection string           | SQLite by default          |

### Setting Environment Variables in PythonAnywhere

**Method 1: Web Interface (if available on your plan)**
1. Go to **Web** tab
2. Scroll to **Environment variables** section
3. Add variables one by one

**Method 2: Using .env file**
1. Create a `.env` file in your project root:
   ```bash
   cd ~/django-ecommerce-project
   nano .env
   ```

2. Add your environment variables:
   ```
   DJANGO_SECRET_KEY=your-secret-key-here
   DJANGO_DEBUG=False
   DJANGO_ALLOWED_HOSTS=yourusername.pythonanywhere.com
   DJANGO_CSRF_TRUSTED_ORIGINS=https://yourusername.pythonanywhere.com
   RAZOR_KEY_ID=your-razorpay-key-id
   RAZOR_KEY_SECRET=your-razorpay-secret
   ```

3. Install python-dotenv if not already in requirements.txt:
   ```bash
   pip install python-dotenv
   ```

4. Update your settings.py to load .env file (if not already configured)

## Manual Deployment

If you need to deploy manually without using GitHub Actions:

1. SSH into PythonAnywhere or use a Bash console
2. Navigate to your project directory:
   ```bash
   cd ~/django-ecommerce-project
   ```

3. Make the deployment script executable:
   ```bash
   chmod +x deploy_to_pythonanywhere.sh
   ```

4. Set required environment variables:
   ```bash
   export PYTHONANYWHERE_API_TOKEN="your-api-token"
   export PYTHONANYWHERE_USERNAME="yourusername"
   export PYTHONANYWHERE_PROJECT_DIR="/home/yourusername/django-ecommerce-project"
   export PYTHONANYWHERE_VENV_DIR="/home/yourusername/.virtualenvs/django-ecommerce-env"
   export PYTHONANYWHERE_WEBAPP_NAME="yourusername.pythonanywhere.com"
   ```

5. Run the deployment script:
   ```bash
   ./deploy_to_pythonanywhere.sh
   ```

## Troubleshooting

### Common Issues and Solutions

#### 1. Import Errors After Deployment

**Symptom:** `ImportError` or `ModuleNotFoundError` in error logs

**Solution:**
- Ensure virtual environment is activated
- Verify all dependencies are installed: `pip install -r requirements.txt`
- Check WSGI file configuration
- Verify Python version matches between local and PythonAnywhere

#### 2. Static Files Not Loading

**Symptom:** CSS/JS files return 404 errors

**Solution:**
- Run `python manage.py collectstatic --noinput`
- Verify static files mappings in Web tab
- Check `STATIC_ROOT` and `STATIC_URL` in settings.py
- Ensure WhiteNoise is installed and configured

#### 3. Database Errors

**Symptom:** Database connection errors or missing tables

**Solution:**
- Run migrations: `python manage.py migrate`
- Check database file permissions
- Verify `DATABASE_URL` or database settings

#### 4. Permission Denied Errors

**Symptom:** Permission errors when running deployment script

**Solution:**
- Make script executable: `chmod +x deploy_to_pythonanywhere.sh`
- Check file/directory ownership
- Verify you're in the correct directory

#### 5. GitHub Actions Deployment Fails

**Symptom:** Deployment workflow fails in GitHub Actions

**Solution:**
- Verify all GitHub Secrets are correctly set
- Check SSH password is correct
- Ensure deployment script exists in repository
- Review workflow logs for specific error messages

#### 6. Web App Not Reloading

**Symptom:** Changes not reflected after deployment

**Solution:**
- Manually reload from Web tab
- Verify API token is correct
- Check API endpoint URL format
- Use the reload button in PythonAnywhere dashboard

#### 7. Environment Variables Not Working

**Symptom:** Default values being used instead of configured values

**Solution:**
- Verify environment variables are set in PythonAnywhere
- Check variable names match exactly (case-sensitive)
- Restart web app after setting new variables
- Use .env file as alternative

#### 8. CSRF or CORS Errors

**Symptom:** CSRF verification failed or CORS errors

**Solution:**
- Add your domain to `DJANGO_ALLOWED_HOSTS`
- Add your domain with https:// to `DJANGO_CSRF_TRUSTED_ORIGINS`
- Reload web app after changes

### Viewing Logs

To debug issues, check the following logs:

1. **Error Log** (in Web tab):
   - Contains Python exceptions and errors
   - Most useful for debugging

2. **Server Log** (in Web tab):
   - Contains request/response information
   - Useful for tracking requests

3. **Access Log** (in Web tab):
   - Contains all HTTP requests
   - Useful for monitoring traffic

### Getting Help

If you're still experiencing issues:

1. Check PythonAnywhere [Help Pages](https://help.pythonanywhere.com/)
2. Visit PythonAnywhere [Forums](https://www.pythonanywhere.com/forums/)
3. Check Django [Documentation](https://docs.djangoproject.com/)
4. Review GitHub Actions [Documentation](https://docs.github.com/en/actions)

## Additional Resources

- [PythonAnywhere Django Tutorial](https://help.pythonanywhere.com/pages/DeployExistingDjangoProject/)
- [Django Deployment Checklist](https://docs.djangoproject.com/en/stable/howto/deployment/checklist/)
- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [Django Static Files](https://docs.djangoproject.com/en/stable/howto/static-files/)
- [PythonAnywhere API Documentation](https://help.pythonanywhere.com/pages/API/)

## Security Best Practices

1. **Never commit sensitive information** to the repository
2. **Always use environment variables** for secrets
3. **Keep DEBUG=False** in production
4. **Use strong SECRET_KEY** generated specifically for production
5. **Regularly update dependencies** to patch security vulnerabilities
6. **Use HTTPS** for all production traffic
7. **Regularly rotate API tokens** and passwords
8. **Review and limit** ALLOWED_HOSTS to only necessary domains

## Maintenance

### Regular Tasks

1. **Monitor error logs** regularly for issues
2. **Update dependencies** monthly or when security patches are released
3. **Backup database** before major updates
4. **Test deployment** in development before pushing to master
5. **Review and rotate secrets** quarterly

### Updating the Application

1. Make changes in a feature branch
2. Test locally
3. Merge to master branch
4. GitHub Actions will automatically deploy
5. Monitor deployment logs
6. Test production site after deployment

---

**Last Updated:** 2026-01-03

For questions or issues, please open an issue on GitHub or contact the project maintainer.
