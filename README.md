# Marstek CT Meter Integration für Home Assistant

Diese Integration bindet Marstek CT Smart Meter (z.B. CT002/CT003) direkt in Home Assistant ein und ermöglicht die Konfiguration über die Benutzeroberfläche. Sie nutzt eine lokale Polling-Methode, um Daten direkt vom Gerät abzurufen, ohne auf eine Cloud angewiesen zu sein.

## Features

- **Lokale Datenabfrage:** Ruft Daten per UDP direkt von deinem CT-Meter ab.
- **UI-Konfiguration:** Einfaches Hinzufügen und Konfigurieren über die Home Assistant-Benutzeroberfläche. Kein Bearbeiten von YAML für die Zugangsdaten nötig.
- **Automatische Geräteerstellung:** Legt automatisch ein Gerät in Home Assistant an und ordnet alle Sensoren diesem Gerät zu.
- **Vielfältige Sensoren:** Erstellt Sensoren für Gesamtleistung, Lade-/Entladeleistung, Phasen-Details, Energie und WLAN-Signalstärke.

## Installation

### Manuelle Installation

1.  Erstelle im `config`-Verzeichnis deines Home Assistant ein Verzeichnis `custom_components`, falls es nicht existiert.
2.  Erstelle darin einen Ordner namens `marstek_ct`. Der vollständige Pfad lautet dann `/config/custom_components/marstek_ct/`.
3.  Kopiere alle `.py`- und `.json`-Dateien dieser Integration in den `marstek_ct`-Ordner.
4.  Starte Home Assistant neu.

### HACS

Diese Integration ist derzeit nicht im HACS-Standard-Repository.

## Konfiguration

1.  Gehe in Home Assistant zu **Einstellungen > Geräte & Dienste**.
2.  Klicke unten rechts auf **+ INTEGRATION HINZUFÜGEN**.
3.  Suche nach **"Marstek CT Meter"** und wähle die Integration aus.
4.  Gib die IP-Adresse und die MAC-Adressen deines Geräts ein, wie im Dialogfeld beschrieben. Die Daten findest du in deiner Marstek-App.

## Sensoren

Die Integration erstellt unter anderem die folgenden Sensoren:

- Gesamtleistung (W)
- Ladeleistung (W)
- Entladeleistung (W)
- Gesamt geladene Energie (kWh)
- Leistung der Phasen A, B, C (W)
- WLAN RSSI (dBm)

## Danksagung

Diese Integration basiert auf der Analyse und dem Python-Skript von R. Weijnen, zu finden unter [marstek-venus-e-firmware-notes](https://github.com/rweijnen/marstek-venus-e-firmware-notes/).
