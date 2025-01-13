from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from config import Config
import subprocess
import yaml
import os

app = Flask(__name__)
app.config.from_object(Config)  # Lädt alle Konfigurationsvariablen aus config.py
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'  # Dies setzt die Login-Route

# Konfigurationsdaten aus playbooks_config.yaml laden
with open("playbooks_config.yaml", 'r') as config_file:
    config = yaml.safe_load(config_file)
    playbooks = config['playbooks']  # Hier wird die playbooks-Liste aus der YAML-Datei geladen

# Dummy-Benutzer-Daten (In der Produktion solltest du eine Datenbank verwenden)
users = {'admin': 'passwort'}  # Benutzername: Passwort

class User(UserMixin):
    def __init__(self, username):
        self.username = username

    def get_id(self):
        return self.username  # Gibt die Benutzer-ID zurück

@login_manager.user_loader
def load_user(username):
    return User(username)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username in users and users[username] == password:
            user = User(username)
            login_user(user)
            return redirect(url_for('playbooks_view'))  # Auf die Playbook-Liste umleiten
        else:
            flash('Ungültiger Benutzername oder Passwort', 'danger')
    return render_template('login.html')

@app.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/')
def home():
    return render_template('home.html')


@app.route('/playbooks')
@login_required
def playbooks_view():
    return render_template('playbooks.html', playbooks=playbooks)

@app.route('/playbook/<int:playbook_id>/execute', methods=['GET', 'POST'])
@login_required
def execute_playbook(playbook_id):
    # Suche das Playbook basierend auf der ID
    playbook_config = next((p for p in playbooks if p['id'] == playbook_id), None)

    if not playbook_config:
        return "Playbook nicht gefunden", 404

    if request.method == 'POST':
        # Erstelle die Umgebungsvariablen aus den POST-Daten, falls welche vorhanden sind
        playbook_vars = {}
        if 'variables' in playbook_config:
            for var in playbook_config['variables']:
                if var['type'] == 'checkbox':
                    playbook_vars[var['name']] = request.form.get(var['name'], 'false')
                else:
                    playbook_vars[var['name']] = request.form[var['name']]

        # Playbook-Pfad und Verzeichnis festlegen
        playbook_path = playbook_config['path']
        playbook_dir = os.path.dirname(playbook_path)

        # Erstelle den Befehl zum Ausführen des Playbooks
        command = ['ansible-playbook', playbook_path]

        # Füge die Variablen zum Befehl hinzu, falls vorhanden
        for key, value in playbook_vars.items():
            command.append('-e')
            command.append(f"{key}={value}")

        # Debugging-Ausgabe des Befehls
        print("Auszuführender Befehl:", " ".join(command))
        
        # Führe den Befehl aus, ohne dass bei Fehlern eine Exception ausgelöst wird
        result = subprocess.run(command, capture_output=True, text=True, cwd=playbook_dir, check=False)

        # Unabhängig vom Erfolg das Ergebnis und eventuelle Fehler an das Template übergeben
        output = result.stdout
        error = result.stderr

        # Render die execute.html mit der Ausgabe
        return render_template('execute.html', playbook=playbook_config, output=output, error=error)

    # Bei GET-Anfrage zeige das Formular für die Eingabe der Variablen (falls vorhanden)
    return render_template('execute.html', playbook=playbook_config)

if __name__ == '__main__':
    app.run(host=app.config['HOST'], port=app.config['PORT'], debug=app.config['DEBUG'])
