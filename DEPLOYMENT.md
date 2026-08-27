# Deploying the AI Career Assistant

## AI provider

The app uses Groq's hosted `llama-3.3-70b-versatile` model. No local Ollama installation is required.

Create a Groq API key at https://console.groq.com/keys. Groq provides a free developer tier with usage limits.

In Streamlit Cloud, open **Settings > Secrets** and add:

```toml
GROQ_API_KEY = "your-groq-api-key"
```

## Streamlit Community Cloud

1. Create a GitHub account at https://github.com if needed.
2. Create a new GitHub repository.
3. Upload these files:
   - `app.py`
   - `requirements.txt`
   - `universal_ai_career_assistant_knowledge_base.txt`
4. Do not upload `.streamlit/secrets.toml`, `venv/`, or `__pycache__/`.
5. Open https://share.streamlit.io.
6. Select **Deploy an app**.
7. Choose your repository, branch, and `app.py` as the main file.
8. Deploy the app.
9. In the deployed app settings, open **Secrets** and add:

```toml
SMTP_USER = "your-sender@gmail.com"
SMTP_PASSWORD = "your-gmail-app-password"
SMTP_HOST = "smtp.gmail.com"
SMTP_PORT = "465"
```

The feedback recipient is already set in `app.py` to `pranavkumar86530@gmail.com`.

## Security

Never upload `secrets.toml` to GitHub. If an app password has ever been shared or committed, revoke it in Google Account settings and create a new one.
