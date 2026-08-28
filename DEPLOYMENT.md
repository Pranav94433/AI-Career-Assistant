# Deploying the AI Career Assistant

## AI provider

The app uses Groq hosted models and automatically selects an available supported model. No local Ollama installation is required.

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

## Current web results

The app uses the `ddgs` package to search public web results when a user asks a
question. No additional API key is required. The sidebar checkbox can disable
live search, and the assistant continues using the local knowledge base if web
search is unavailable. Verify job listings and other time-sensitive details
because search snippets can become outdated.

## ATS resume generation

Users can generate an ATS-friendly resume from an uploaded resume, typed details,
or both. The output is available as TXT and DOCX. The generator preserves only
supplied facts, so users should review placeholders and every claim before
applying.

## Public reviews

The feedback form asks for a name and displays submitted ratings and comments
under **See what others reviewed**. Reviews are stored in
`career_assistant_reviews.json`, which is created automatically and should not
be committed to GitHub if it contains personal information. Streamlit Community
Cloud storage can be reset when the app restarts, so use a hosted database for
permanent cross-user reviews. A **Delete my review** button is shown only to the
browser session that submitted that review; reviews created before this feature
will not have a delete button.

## Security

Never upload `secrets.toml` to GitHub. If an app password has ever been shared or committed, revoke it in Google Account settings and create a new one.
