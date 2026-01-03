# Quick Start: PythonAnywhere Deployment

This is a condensed version of the deployment setup. For detailed instructions, see [DEPLOYMENT.md](DEPLOYMENT.md).

## Prerequisites

- PythonAnywhere account
- GitHub account with repository access
- Basic terminal/command line knowledge

## Setup Steps (30 minutes)

### 1. PythonAnywhere Initial Setup (15 min)

1. **Sign up** at [PythonAnywhere](https://www.pythonanywhere.com/)
2. **Generate API Token**: Account → API token → Create
3. **Clone repository** in Bash console:
   ```bash
   git clone https://github.com/K-s-c49/django-ecommerce-project.git
   cd django-ecommerce-project
   ```
4. **Create virtual environment**:
   ```bash
   mkvirtualenv --python=/usr/bin/python3.10 django-ecommerce-env
   pip install -r requirements.txt
   ```
5. **Create web app**: Web tab → Add new web app → Manual configuration → Python 3.10

### 2. Configure Web App (10 min)

1. **Set virtual environment path**:
   ```
   /home/yourusername/.virtualenvs/django-ecommerce-env
   ```

2. **Configure WSGI file** (click the link in Code section):
   ```python
   import os
   import sys
   
   path = '/home/yourusername/django-ecommerce-project'
   if path not in sys.path:
       sys.path.insert(0, path)
   
   os.environ['DJANGO_SETTINGS_MODULE'] = 'ec.settings'
   
   from django.core.wsgi import get_wsgi_application
   application = get_wsgi_application()
   ```

3. **Configure static files** in Web tab:
   - URL: `/static/` → Directory: `/home/yourusername/django-ecommerce-project/staticfiles`
   - URL: `/media/` → Directory: `/home/yourusername/django-ecommerce-project/media`

4. **Set environment variables** (create .env file in project root):
   ```bash
   cd ~/django-ecommerce-project
   nano .env
   ```
   Add:
   ```
   DJANGO_SECRET_KEY=generate-new-secret-key
   DJANGO_DEBUG=False
   DJANGO_ALLOWED_HOSTS=yourusername.pythonanywhere.com
   DJANGO_CSRF_TRUSTED_ORIGINS=https://yourusername.pythonanywhere.com
   ```

5. **Run initial commands**:
   ```bash
   workon django-ecommerce-env
   cd ~/django-ecommerce-project
   python manage.py migrate
   python manage.py collectstatic --noinput
   python manage.py createsuperuser
   ```

6. **Reload web app**: Click green Reload button in Web tab

### 3. GitHub Secrets Setup (5 min)

Go to GitHub repository → Settings → Secrets and variables → Actions → New repository secret

Add these 6 secrets:

| Secret Name | Value Example |
|------------|---------------|
| `PYTHONANYWHERE_USERNAME` | `yourusername` |
| `PYTHONANYWHERE_PASSWORD` | Your SSH password |
| `PYTHONANYWHERE_API_TOKEN` | Your API token |
| `PYTHONANYWHERE_PROJECT_DIR` | `/home/yourusername/django-ecommerce-project` |
| `PYTHONANYWHERE_VENV_DIR` | `/home/yourusername/.virtualenvs/django-ecommerce-env` |
| `PYTHONANYWHERE_WEBAPP_NAME` | `yourusername.pythonanywhere.com` |

## Usage

After setup, deployment is automatic:

```bash
git add .
git commit -m "Your changes"
git push origin master
```

GitHub Actions will automatically deploy to PythonAnywhere!

## Verify Deployment

1. Check GitHub Actions tab for workflow status
2. Visit your site: `https://yourusername.pythonanywhere.com`
3. Check PythonAnywhere error log if issues occur

## Common Issues

| Issue | Solution |
|-------|----------|
| Import errors | Run `pip install -r requirements.txt` in console |
| Static files not loading | Run `python manage.py collectstatic --noinput` |
| Changes not showing | Click Reload button in Web tab |
| GitHub Actions failing | Check all secrets are set correctly |

## Need Help?

See detailed documentation: [DEPLOYMENT.md](DEPLOYMENT.md)

---

**Pro Tip**: Always test changes locally before pushing to master!
