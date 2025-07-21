from dash import Input, Output, State, ctx, html, dcc
import dash
import requests

def register_callbacks(app: dash.Dash):

    # Load chat history when active session changes
    @app.callback(
        Output("chat-history", "data", allow_duplicate=True),
        Input("active-session", "data"),
        prevent_initial_call=True
    )
    def load_chat_history(session_id):
        if not session_id:
            return []
        try:
            resp = requests.get(f"http://localhost:8000/sessions/{session_id}/chat")
            if resp.status_code == 200:
                chat_data = resp.json()
                return chat_data
            else:
                return []
        except Exception:
            return []
    # Login callback
    @app.callback(
        Output("user-store", "data"),
        Output("login-status", "children"),
        Output("session-refresh-interval", "n_intervals"),
        Input("login-btn", "n_clicks"),
        State("username", "value"),
        State("password", "value"),
        State("session-refresh-interval", "n_intervals"),
        prevent_initial_call=True
    )
    def login_user(n_clicks, username, password, n_intervals):
        if not username or not password:
            return dash.no_update, "Please enter username and password.", dash.no_update
        try:
            resp = requests.post("http://localhost:8000/login", json={"username": username, "password": password})
            if resp.status_code == 200:
                user = resp.json()
                # increment n_intervals to trigger session list update
                return user, "Login successful.", (n_intervals or 0) + 1
            else:
                return None, "Invalid login.", dash.no_update
        except Exception:
            return None, "Login failed. Backend not reachable.", dash.no_update
    # Chat logic: send question, update chat-history, display chat, clear input
    @app.callback(
        Output("chat-history", "data", allow_duplicate=True),
        Output("chat-input", "value", allow_duplicate=True),
        Input("send-button", "n_clicks"),
        State("chat-input", "value"),
        State("active-session", "data"),
        State("chat-history", "data"),
        prevent_initial_call=True
    )
    def send_chat(n_clicks, message, session_id, chat_data):
        if not message or not session_id:
            return dash.no_update, ""
        try:
            resp = requests.post("http://localhost:8000/query", json={"session_id": session_id, "question": message})
            if resp.status_code == 200:
                answer = resp.json().get("answer", "No answer.")
                new_entry = {"question": message, "answer": answer}
                chat_data = (chat_data or []) + [new_entry]
                return chat_data, ""
            else:
                return chat_data, ""
        except Exception:
            return chat_data, ""

    @app.callback(
        Output("chat-display", "children"),
        Input("chat-history", "data"),
        prevent_initial_call=True
    )
    def display_chat(chat_data):
        if not chat_data:
            return ["Chat history will appear here."]
        items = []
        for entry in chat_data:
            # User message
            items.append(html.Div([
                html.Div("You:", style={"fontWeight": "bold"}),
                html.Div(entry["question"])
            ], style={"marginBottom": "0.5em"}))
            # Bot response
            answer = entry["answer"]
            bot_parts = [html.Div("Bot:", style={"fontWeight": "bold"})]
            if isinstance(answer, dict) and "events" in answer:
                for event in answer["events"]:
                    if event["type"] == "text":
                        bot_parts.append(html.Pre(event["content"]))
                    elif event["type"] == "plot":
                        bot_parts.append(html.Img(src=event["content"], style={"maxWidth": "400px", "marginTop": "1em"}))
            elif isinstance(answer, dict):
                bot_parts.append(html.Pre(answer.get("text", "")))
                for img_data in answer.get("plots", []):
                    bot_parts.append(html.Img(src=img_data, style={"maxWidth": "400px", "marginTop": "1em"}))
            else:
                bot_parts.append(html.Pre(str(answer)))
            items.append(html.Div(bot_parts, style={"marginBottom": "1.5em"}))
        return items


