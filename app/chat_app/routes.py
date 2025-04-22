# chat_app/routes.py

from flask import render_template, session, redirect, url_for
from . import chat_app_bp

@chat_app_bp.route('/')
def chat_app():
    """
    Render the chat application page.
    
    This function handles the rendering of the chat application page.
    It checks if the user is logged in and renders the appropriate template.
    
    Returns:
        str: Rendered HTML template for the chat application page.
    """
    # Check if user is logged in
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))

    return render_template('chat_app.html', username=session['username'])