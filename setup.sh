mkdir -p ~/.streamlit/
echo "\
[server]\n\
headless = true\n\
port = $PORT\n\
enableCORS = false\n\
\n\
" > ~/.streamlit/config.toml

mkdir -p ~/.binder/
echo "\
"--server.enableWebsocketCompression=false",\n\
"--server.enableXsrfProtection=false",\n\
" > ~/.binder/streamlit_call.py
