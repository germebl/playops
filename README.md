
# PlayOps

PlayOps ist eine einfache Webanwendung zum Ausführen von Ansible-Playbooks über eine Web-UI. Diese App ermöglicht es dir, Playbooks einfach und schnell per Mausklick auszuführen. Alle Variablen und Einstellungen lassen sich bequem über Umgebungsvariablen steuern.

## Features

- **Ansible-Integration**: Auswahl und Ausführung von Ansible-Playbooks mit nur wenigen Klicks.
- **Benutzerfreundliche Oberfläche**: Simples Web-Interface, das keine tiefgehenden Kenntnisse erfordert.
- **Umgebungsvariablen**: Einstellungen lassen sich über Umgebungsvariablen steuern und anpassen.

## Installation

### Voraussetzungen

- Python 3.7+
- [Ansible](https://docs.ansible.com/ansible/latest/installation_guide/intro_installation.html)
- Virtuelle Umgebung für Python (optional, aber empfohlen)
- Flask für die Web-App
- Playbook muss per Umgebungsvariablen steuerbar sein

### Schritte

1. **Repository klonen**
   ```bash
   git clone https://github.com/your-username/PlayOps.git
   cd PlayOps
   ```

2. **Virtuelle Umgebung einrichten**
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Abhängigkeiten installieren**
   ```bash
   pip install -r requirements.txt
   ```

4. **Server starten**
   ```bash
   flask run
   ```

   Die Anwendung wird standardmäßig unter `http://127.0.0.1:5000` laufen.

## Zugangsdaten WebUI
Aktuell noch in der app.py wird der Benutzer und das Passwort definiert. Das könnte auf jeden Fall noch optimiert werden.

## Playbook Anbindung
Um ein neues Playbook anzubinden, benötigst du nur die `playbooks_config.yaml` editieren. Dort ist bereits unter der `ID 1` ein Test Playbook vorhanden, um die Funktionsweise der Konfiguration zu erklären und aufzuzeigen.

Das Playbook muss nicht zwingend im selben Verzeichnis liegen! Ein vollständiger Pfad zur `main.yaml` des Playbooks reicht aus.

# Inventory und andere Ansible Einstellungen
Um ein Inventory oder andere Ansible Einstellungen zu konfigurieren, einfach die passende ansible.cfg im Playbook Verzeichnis haben, sodass beim Ausführen des Playbooks diese automatisch geladen werden können und nicht an den Befehl angehängt werden müssen.

Hier ein Beispiel einer ansible.cfg die innerhalb des Playbook Verzeichnis liegt:
```
[defaults]
inventory = hosts.ini
host_key_checking = False
remote_user = ansible
ask_pass = False
ask_become_pass = False
private_key_file = ~/.ssh/id_ansible
remote_port = 22
timeout = 30
roles_path = roles/
display_skipped_hosts = false
```

## Nutzung

1. **Login**: Melde dich über das Login-Formular an.
2. **Playbook-Auswahl**: Wähle ein Playbook aus der Liste und fülle die benötigten Variablen aus.
3. **Ausführung starten**: Starte das Playbook und überprüfe den Output.

## Lizenz

Dieses Projekt ist unter der MIT-Lizenz lizenziert. Siehe die [LICENSE-Datei](LICENSE) für Details.

---

**PlayOps** – Für alle, die eine simple Lösung suchen, um Playbooks per Webinterface auszuführen.
