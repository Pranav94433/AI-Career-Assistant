# Deploying the AI Career Assistant

## Important: Ollama hosting

This app currently uses Ollama through `ollama.chat()`. Local Ollama works on your computer, but Streamlit Community Cloud cannot connect to your computer's Ollama service.

The app now supports `OLLAMA_HOST`. The simplest production setup is one Ubuntu VPS running both Ollama and Streamlit. Do not expose Ollama's port directly to the public internet.

## Ubuntu VPS setup

On a fresh Ubuntu 22.04/24.04 server, run:

```bash
curl -fsSL https://ollama.com/install.sh | sh
ollama pull llama3.2:1b
sudo apt update && sudo apt install -y python3-venv git
git clone YOUR_GITHUB_REPOSITORY_URL AI-Career-Assistant
cd AI-Career-Assistant
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
streamlit run app.py --server.address 0.0.0.0 --server.port 8501
```

Open the server address in your browser. The app uses local Ollama automatically when `OLLAMA_HOST` is not set.

For a separate app server, add this to `.streamlit/secrets.toml`:

```toml
OLLAMA_HOST = "http://YOUR_PRIVATE_OLLAMA_SERVER:11434"
```

Use a private network or VPN between servers. Ollama should listen on localhost unless a protected private network is configured.

Before deploying publicly, choose one of these options:

- Deploy Ollama on a server with a public/private reachable URL and configure the Ollama client to use it.
- Replace the Ollama call with a hosted model provider such as OpenAI, Groq, or OpenRouter.
- Run the app on your own computer or a server where Ollama is installed.

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
