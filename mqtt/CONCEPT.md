# Jellyfin MQTT Bridge - Konzeptdokument

## Übersicht

Die MQTT Bridge verbindet Jellyfin mit Home Assistant über MQTT Discovery.
Sie registriert sich als vollständiges Gerät und publiziert alle relevanten Daten.

---

## 1. Unraid Template - Environment Variables

### Neue Template-Variablen für MQTT

```xml
<!-- MQTT Configuration -->
<Config Name="MQTT Broker Host" Target="MQTT_HOST" Default="" Mode="" Description="MQTT Broker IP/Hostname (z.B. 192.168.1.100)" Type="Variable" Display="always" Required="false" Mask="false"/>

<Config Name="MQTT Broker Port" Target="MQTT_PORT" Default="1883" Mode="" Description="MQTT Broker Port (Standard: 1883)" Type="Variable" Display="always" Required="false" Mask="false"/>

<Config Name="MQTT Username" Target="MQTT_USER" Default="" Mode="" Description="MQTT Benutzername (leer lassen wenn keine Auth)" Type="Variable" Display="always" Required="false" Mask="false"/>

<Config Name="MQTT Password" Target="MQTT_PASSWORD" Default="" Mode="" Description="MQTT Passwort" Type="Variable" Display="always" Required="false" Mask="true"/>

<Config Name="MQTT Base Topic" Target="MQTT_TOPIC" Default="jellyfin" Mode="" Description="MQTT Base Topic (Standard: jellyfin)" Type="Variable" Display="always" Required="false" Mask="false"/>

<Config Name="MQTT Discovery Prefix" Target="MQTT_DISCOVERY_PREFIX" Default="homeassistant" Mode="" Description="Home Assistant Discovery Prefix" Type="Variable" Display="always" Required="false" Mask="false"/>

<Config Name="MQTT Client ID" Target="MQTT_CLIENT_ID" Default="jellyfin-mqtt" Mode="" Description="MQTT Client ID (muss eindeutig sein)" Type="Variable" Display="always" Required="false" Mask="false"/>

<Config Name="MQTT Enable" Target="MQTT_ENABLE" Default="false" Mode="" Description="MQTT Bridge aktivieren (true/false)" Type="Variable" Display="always" Required="false" Mask="false"/>

<Config Name="MQTT Poll Interval" Target="MQTT_POLL_INTERVAL" Default="5" Mode="" Description="API Poll Intervall in Sekunden" Type="Variable" Display="always" Required="false" Mask="false"/>

<Config Name="Jellyfin API Key" Target="JELLYFIN_API_KEY" Default="" Mode="" Description="Jellyfin API Key für MQTT Bridge" Type="Variable" Display="always" Required="false" Mask="true"/>
```

### Environment Variables Übersicht

| Variable | Default | Beschreibung |
|----------|---------|--------------|
| `MQTT_ENABLE` | `false` | MQTT Bridge aktivieren |
| `MQTT_HOST` | - | Broker IP/Hostname (required wenn enabled) |
| `MQTT_PORT` | `1883` | Broker Port |
| `MQTT_USER` | - | Username (optional) |
| `MQTT_PASSWORD` | - | Password (optional) |
| `MQTT_TOPIC` | `jellyfin` | Base Topic |
| `MQTT_DISCOVERY_PREFIX` | `homeassistant` | HA Discovery Prefix |
| `MQTT_CLIENT_ID` | `jellyfin-mqtt` | Client ID |
| `MQTT_POLL_INTERVAL` | `5` | Poll Intervall (Sekunden) |
| `JELLYFIN_API_KEY` | - | Jellyfin API Key (required wenn enabled) |

---

## 2. MQTT Topic Struktur

### Base Topics

```
jellyfin/                           # Base Topic
├── status                          # online/offline (LWT)
├── server/
│   ├── info                        # Server-Infos (JSON)
│   ├── version                     # Server-Version
│   └── url                         # Server-URL
├── sessions/
│   ├── count                       # Anzahl aktiver Sessions
│   ├── playing_count               # Anzahl mit aktivem Playback
│   └── {session_id}/
│       ├── state                   # playing/paused/idle
│       ├── user                    # Username
│       ├── client                  # Client Name
│       ├── device                  # Device Name
│       ├── media                   # Now Playing (JSON)
│       ├── progress                # Progress in %
│       ├── position                # Position in Sekunden
│       ├── duration                # Dauer in Sekunden
│       ├── play_method             # DirectPlay/DirectStream/Transcode
│       └── command                 # (Subscribe) Steuerungsbefehle
├── transcoding/
│   ├── active                      # true/false
│   ├── count                       # Anzahl aktiver Transcodes
│   └── sessions                    # Liste der Transcoding-Sessions
├── gpu/
│   ├── name                        # GPU Name
│   ├── utilization                 # GPU Auslastung %
│   ├── memory_used                 # VRAM Used (MB)
│   ├── memory_total                # VRAM Total (MB)
│   ├── memory_percent              # VRAM %
│   ├── temperature                 # Temperatur °C
│   ├── encoder                     # Encoder Auslastung %
│   ├── decoder                     # Decoder Auslastung %
│   └── power                       # Power Draw (W)
├── container/
│   ├── cpu_percent                 # CPU Auslastung %
│   ├── memory_used                 # RAM Used (MB)
│   ├── memory_limit                # RAM Limit (MB)
│   ├── memory_percent              # RAM %
│   ├── network_rx                  # Network RX (Bytes)
│   └── network_tx                  # Network TX (Bytes)
├── library/
│   ├── scan_progress               # Scan Fortschritt %
│   ├── scanning                    # true/false
│   └── command                     # (Subscribe) scan trigger
├── tasks/
│   ├── running_count               # Anzahl laufender Tasks
│   └── {task_id}/
│       ├── state                   # Running/Idle/Completed
│       ├── progress                # Progress %
│       └── command                 # (Subscribe) start/stop
└── command                         # (Subscribe) Globale Befehle
```

---

## 3. Home Assistant MQTT Discovery

### Geräte-Identifier

```json
{
  "identifiers": ["jellyfin_server_{server_id}"],
  "name": "Jellyfin Media Server",
  "model": "Jellyfin 10.11.5",
  "manufacturer": "Jellyfin",
  "sw_version": "MQTT Bridge 1.0",
  "configuration_url": "http://192.168.1.57:8096"
}
```

### Discovery Topics & Payloads

#### 3.1 Server Status (Binary Sensor)
```
Topic: homeassistant/binary_sensor/jellyfin_server_status/config
Payload:
{
  "name": "Server Status",
  "unique_id": "jellyfin_server_status",
  "state_topic": "jellyfin/status",
  "payload_on": "online",
  "payload_off": "offline",
  "device_class": "connectivity",
  "device": { "identifiers": ["jellyfin_server"], "name": "Jellyfin Media Server", ... }
}
```

#### 3.2 Active Sessions (Sensor)
```
Topic: homeassistant/sensor/jellyfin_active_sessions/config
Payload:
{
  "name": "Active Sessions",
  "unique_id": "jellyfin_active_sessions",
  "state_topic": "jellyfin/sessions/count",
  "icon": "mdi:account-multiple",
  "device": { "identifiers": ["jellyfin_server"] }
}
```

#### 3.3 Playing Sessions (Sensor)
```
Topic: homeassistant/sensor/jellyfin_playing_sessions/config
Payload:
{
  "name": "Playing Sessions",
  "unique_id": "jellyfin_playing_sessions",
  "state_topic": "jellyfin/sessions/playing_count",
  "icon": "mdi:play-circle",
  "device": { "identifiers": ["jellyfin_server"] }
}
```

#### 3.4 Transcoding Active (Binary Sensor)
```
Topic: homeassistant/binary_sensor/jellyfin_transcoding/config
Payload:
{
  "name": "Transcoding Active",
  "unique_id": "jellyfin_transcoding_active",
  "state_topic": "jellyfin/transcoding/active",
  "payload_on": "true",
  "payload_off": "false",
  "icon": "mdi:cog-sync",
  "device": { "identifiers": ["jellyfin_server"] }
}
```

#### 3.5 GPU Utilization (Sensor)
```
Topic: homeassistant/sensor/jellyfin_gpu_utilization/config
Payload:
{
  "name": "GPU Utilization",
  "unique_id": "jellyfin_gpu_utilization",
  "state_topic": "jellyfin/gpu/utilization",
  "unit_of_measurement": "%",
  "icon": "mdi:chart-line",
  "device": { "identifiers": ["jellyfin_server"] }
}
```

#### 3.6 GPU Temperature (Sensor)
```
Topic: homeassistant/sensor/jellyfin_gpu_temperature/config
Payload:
{
  "name": "GPU Temperature",
  "unique_id": "jellyfin_gpu_temperature",
  "state_topic": "jellyfin/gpu/temperature",
  "unit_of_measurement": "°C",
  "device_class": "temperature",
  "device": { "identifiers": ["jellyfin_server"] }
}
```

#### 3.7 GPU Memory (Sensor)
```
Topic: homeassistant/sensor/jellyfin_gpu_memory/config
Payload:
{
  "name": "GPU Memory Used",
  "unique_id": "jellyfin_gpu_memory",
  "state_topic": "jellyfin/gpu/memory_percent",
  "unit_of_measurement": "%",
  "icon": "mdi:memory",
  "device": { "identifiers": ["jellyfin_server"] }
}
```

#### 3.8 Container CPU (Sensor)
```
Topic: homeassistant/sensor/jellyfin_container_cpu/config
Payload:
{
  "name": "Container CPU",
  "unique_id": "jellyfin_container_cpu",
  "state_topic": "jellyfin/container/cpu_percent",
  "unit_of_measurement": "%",
  "icon": "mdi:cpu-64-bit",
  "device": { "identifiers": ["jellyfin_server"] }
}
```

#### 3.9 Container Memory (Sensor)
```
Topic: homeassistant/sensor/jellyfin_container_memory/config
Payload:
{
  "name": "Container Memory",
  "unique_id": "jellyfin_container_memory",
  "state_topic": "jellyfin/container/memory_percent",
  "unit_of_measurement": "%",
  "icon": "mdi:memory",
  "device": { "identifiers": ["jellyfin_server"] }
}
```

#### 3.10 Library Scan (Button + Sensor)
```
Topic: homeassistant/button/jellyfin_library_scan/config
Payload:
{
  "name": "Library Scan",
  "unique_id": "jellyfin_library_scan",
  "command_topic": "jellyfin/library/command",
  "payload_press": "scan",
  "icon": "mdi:refresh",
  "device": { "identifiers": ["jellyfin_server"] }
}

Topic: homeassistant/binary_sensor/jellyfin_library_scanning/config
Payload:
{
  "name": "Library Scanning",
  "unique_id": "jellyfin_library_scanning",
  "state_topic": "jellyfin/library/scanning",
  "payload_on": "true",
  "payload_off": "false",
  "icon": "mdi:magnify-scan",
  "device": { "identifiers": ["jellyfin_server"] }
}
```


#### 3.11 Dynamische Session Media Player (pro aktive Session)
```
Topic: homeassistant/media_player/jellyfin_session_{session_id}/config
Payload:
{
  "name": "Jellyfin - {DeviceName}",
  "unique_id": "jellyfin_session_{session_id}",
  "object_id": "jellyfin_{device_name_slug}",
  
  "state_topic": "jellyfin/sessions/{session_id}/state",
  "command_topic": "jellyfin/sessions/{session_id}/command",
  
  "payload_play": "play",
  "payload_pause": "pause",
  "payload_stop": "stop",
  "payload_next": "next",
  "payload_previous": "previous",
  
  "media_title_template": "{{ value_json.title }}",
  "media_artist_template": "{{ value_json.artist }}",
  "media_album_name_template": "{{ value_json.album }}",
  "media_series_title_template": "{{ value_json.series }}",
  "media_season_template": "{{ value_json.season }}",
  "media_episode_template": "{{ value_json.episode }}",
  "media_duration_template": "{{ value_json.duration }}",
  "media_position_template": "{{ value_json.position }}",
  
  "json_attributes_topic": "jellyfin/sessions/{session_id}/media",
  
  "icon": "mdi:plex",
  "device": {
    "identifiers": ["jellyfin_server"],
    "via_device": "jellyfin_server"
  },
  
  "availability": [
    { "topic": "jellyfin/status", "payload_available": "online", "payload_not_available": "offline" }
  ]
}
```

**Session State Topic Payload:**
```json
{
  "state": "playing",
  "title": "Movie Name",
  "artist": "",
  "album": "",
  "series": "Series Name",
  "season": 1,
  "episode": 5,
  "duration": 3600,
  "position": 1234,
  "progress": 34,
  "play_method": "DirectPlay",
  "user": "Username",
  "client": "Jellyfin Web",
  "device": "Chrome Windows"
}
```

---

## 4. Command Topics (Subscribe)

### 4.1 Session Control
```
Topic: jellyfin/sessions/{session_id}/command
Payloads:
  - "play"      → Resume playback
  - "pause"     → Pause playback
  - "stop"      → Stop playback
  - "next"      → Next track/episode
  - "previous"  → Previous track/episode
  - "seek:1234" → Seek to position (seconds)
  - "mute"      → Mute
  - "unmute"    → Unmute
  - "volume:50" → Set volume (0-100)
```

### 4.2 Library Control
```
Topic: jellyfin/library/command
Payloads:
  - "scan"      → Full library scan
```

### 4.3 Global Commands
```
Topic: jellyfin/command
Payloads:
  - "restart"   → Restart Jellyfin server
  - "shutdown"  → Shutdown Jellyfin server
```

---

## 5. Script-Architektur

### Dateistruktur
```
mqtt/
├── mqtt_bridge.py          # Hauptscript
├── config.py               # Konfiguration aus ENV lesen
├── jellyfin_api.py         # Jellyfin REST API Client
├── gpu_monitor.py          # nvidia-smi Wrapper
├── container_stats.py      # Docker Stats (falls verfügbar)
├── discovery.py            # MQTT Discovery Payloads
├── requirements.txt        # Python Dependencies
└── CONCEPT.md              # Dieses Dokument
```

### Ablauf
```
1. Startup
   ├── ENV Variables lesen
   ├── Prüfen ob MQTT_ENABLE=true
   ├── Validieren: MQTT_HOST und JELLYFIN_API_KEY vorhanden
   └── Exit wenn nicht konfiguriert (graceful, kein Error)

2. MQTT Connect
   ├── Verbindung zu MQTT Broker
   ├── LWT setzen: jellyfin/status = "offline"
   └── Bei Erfolg: jellyfin/status = "online" (retain)

3. Discovery senden (einmalig bei Start)
   ├── Alle statischen Sensoren registrieren
   └── retain: true für alle Discovery-Nachrichten

4. Main Loop (alle MQTT_POLL_INTERVAL Sekunden)
   │
   ├── Jellyfin API abfragen
   │   ├── /System/Info
   │   ├── /Sessions
   │   ├── /ScheduledTasks (nur running)
   │   └── /Library/VirtualFolders (scan status)
   │
   ├── GPU Metriken holen
   │   └── nvidia-smi --query-gpu=... --format=csv,noheader
   │
   ├── Sessions verarbeiten
   │   ├── Neue Sessions → Discovery senden
   │   ├── Beendete Sessions → Discovery entfernen (leere Payload)
   │   └── State Updates publishen
   │
   └── Alle Topics publishen

5. Command Handler (Subscribe Callbacks)
   ├── jellyfin/sessions/+/command → Session steuern
   ├── jellyfin/library/command → Library Scan
   └── jellyfin/command → Server Befehle
```

---

## 6. Python Dependencies

### requirements.txt
```
paho-mqtt>=2.0.0
requests>=2.31.0
```

### System-Abhängigkeiten (bereits im Container)
- `nvidia-smi` (für GPU-Metriken)
- `curl` (Fallback für API-Calls)

---

## 7. Startup-Integration

### In run.sh (Container Entrypoint)
```bash
#!/bin/bash

# Start MQTT Bridge wenn aktiviert
if [ "${MQTT_ENABLE}" = "true" ]; then
    echo "Starting MQTT Bridge..."
    
    # Prüfen ob Konfiguration vollständig
    if [ -z "${MQTT_HOST}" ]; then
        echo "WARNING: MQTT_ENABLE=true but MQTT_HOST not set. MQTT Bridge disabled."
    elif [ -z "${JELLYFIN_API_KEY}" ]; then
        echo "WARNING: MQTT_ENABLE=true but JELLYFIN_API_KEY not set. MQTT Bridge disabled."
    else
        # MQTT Bridge im Hintergrund starten
        python3 /usr/local/bin/mqtt/mqtt_bridge.py &
        MQTT_PID=$!
        echo "MQTT Bridge started with PID: $MQTT_PID"
    fi
fi

# Jellyfin starten (Hauptprozess)
exec /jellyfin/jellyfin
```

### Alternativ: Supervisord
```ini
[program:mqtt-bridge]
command=python3 /usr/local/bin/mqtt/mqtt_bridge.py
autostart=%(ENV_MQTT_ENABLE)s
autorestart=true
stdout_logfile=/config/logs/mqtt-bridge.log
stderr_logfile=/config/logs/mqtt-bridge-error.log
environment=MQTT_HOST="%(ENV_MQTT_HOST)s",MQTT_PORT="%(ENV_MQTT_PORT)s",...
```


---

## 8. Home Assistant Integration

### Automatisch erkannte Entities (nach MQTT Discovery)

**Binary Sensors:**
- `binary_sensor.jellyfin_server_status` - Online/Offline
- `binary_sensor.jellyfin_transcoding_active` - Transcoding läuft
- `binary_sensor.jellyfin_library_scanning` - Library Scan läuft

**Sensors:**
- `sensor.jellyfin_active_sessions` - Anzahl Sessions
- `sensor.jellyfin_playing_sessions` - Anzahl spielend
- `sensor.jellyfin_gpu_utilization` - GPU %
- `sensor.jellyfin_gpu_temperature` - GPU °C
- `sensor.jellyfin_gpu_memory` - VRAM %
- `sensor.jellyfin_container_cpu` - Container CPU %
- `sensor.jellyfin_container_memory` - Container RAM %

**Buttons:**
- `button.jellyfin_library_scan` - Library Scan starten

**Media Players (dynamisch):**
- `media_player.jellyfin_{device_name}` - Pro aktive Session

### Beispiel Dashboard Card
```yaml
type: entities
title: Jellyfin Server
entities:
  - entity: binary_sensor.jellyfin_server_status
    name: Status
  - entity: sensor.jellyfin_active_sessions
    name: Aktive Sessions
  - entity: sensor.jellyfin_playing_sessions
    name: Wiedergabe aktiv
  - entity: binary_sensor.jellyfin_transcoding_active
    name: Transcoding
  - type: section
    label: GPU Statistiken
  - entity: sensor.jellyfin_gpu_utilization
    name: GPU Auslastung
  - entity: sensor.jellyfin_gpu_temperature
    name: GPU Temperatur
  - entity: sensor.jellyfin_gpu_memory
    name: GPU Speicher
  - type: section
    label: Container
  - entity: sensor.jellyfin_container_cpu
    name: CPU
  - entity: sensor.jellyfin_container_memory
    name: RAM
  - type: section
    label: Aktionen
  - entity: button.jellyfin_library_scan
    name: Library scannen
```

### Beispiel Automation
```yaml
automation:
  - alias: "Jellyfin - Licht dimmen bei Wiedergabe"
    trigger:
      - platform: state
        entity_id: sensor.jellyfin_playing_sessions
        from: "0"
    condition:
      - condition: time
        after: "18:00:00"
        before: "23:00:00"
    action:
      - service: light.turn_on
        target:
          entity_id: light.wohnzimmer
        data:
          brightness_pct: 20

  - alias: "Jellyfin - Notification bei Transcoding"
    trigger:
      - platform: state
        entity_id: binary_sensor.jellyfin_transcoding_active
        to: "on"
        for:
          minutes: 5
    action:
      - service: notify.mobile_app
        data:
          title: "Jellyfin Transcoding"
          message: "Transcoding läuft seit 5 Minuten. GPU: {{ states('sensor.jellyfin_gpu_utilization') }}%"
```

---

## 9. Unraid Template Update

### Vollständiges Template mit MQTT Sektion

```xml
<?xml version="1.0"?>
<Container version="2">
  <Name>jellyfin-nvidia-cuda12</Name>
  <Repository>drshyper/jellyfin-nvidia-cuda12:latest</Repository>
  <Registry>https://hub.docker.com/r/drshyper/jellyfin-nvidia-cuda12</Registry>
  <Network>bridge</Network>
  <Privileged>false</Privileged>
  <Support>https://github.com/drshyper/jellyfin-nvidia-cuda12</Support>
  <Project>https://jellyfin.org/</Project>
  <Overview>Jellyfin Media Server with NVIDIA CUDA 12 hardware transcoding support and optional MQTT integration for Home Assistant.</Overview>
  <Category>MediaServer:Video MediaServer:Music</Category>
  <WebUI>http://[IP]:[PORT:8096]</WebUI>
  <TemplateURL>https://raw.githubusercontent.com/drshyper/jellyfin-nvidia-cuda12/main/unraid-template.xml</TemplateURL>
  <Icon>https://raw.githubusercontent.com/jellyfin/jellyfin-ux/master/branding/SVG/icon-transparent.svg</Icon>
  <ExtraParams>--runtime=nvidia --gpus all</ExtraParams>
  <DateInstalled></DateInstalled>
  
  <!-- Standard Jellyfin Config -->
  <Config Name="Web UI Port" Target="8096" Default="8096" Mode="tcp" Description="Web interface port" Type="Port" Display="always" Required="true" Mask="false">8096</Config>
  
  <Config Name="Config Path" Target="/config" Default="/mnt/user/appdata/jellyfin-nvidia" Mode="rw" Description="Jellyfin config folder" Type="Path" Display="always" Required="true" Mask="false">/mnt/user/appdata/jellyfin-nvidia</Config>
  
  <Config Name="Cache Path" Target="/cache" Default="/mnt/user/appdata/jellyfin-nvidia/cache" Mode="rw" Description="Jellyfin cache/transcoding folder" Type="Path" Display="always" Required="true" Mask="false">/mnt/user/appdata/jellyfin-nvidia/cache</Config>
  
  <Config Name="Media Path" Target="/media" Default="/mnt/user/media" Mode="ro" Description="Media library path" Type="Path" Display="always" Required="true" Mask="false">/mnt/user/media</Config>
  
  <Config Name="NVIDIA_VISIBLE_DEVICES" Target="NVIDIA_VISIBLE_DEVICES" Default="all" Mode="" Description="Which GPUs to expose" Type="Variable" Display="advanced" Required="false" Mask="false">all</Config>
  
  <Config Name="NVIDIA_DRIVER_CAPABILITIES" Target="NVIDIA_DRIVER_CAPABILITIES" Default="all" Mode="" Description="Driver capabilities" Type="Variable" Display="advanced" Required="false" Mask="false">all</Config>
  
  <!-- ============================================ -->
  <!-- MQTT Configuration (Home Assistant Bridge)  -->
  <!-- ============================================ -->
  
  <Config Name="MQTT aktivieren" Target="MQTT_ENABLE" Default="false" Mode="" Description="MQTT Bridge für Home Assistant aktivieren (true/false)" Type="Variable" Display="always" Required="false" Mask="false">false</Config>
  
  <Config Name="MQTT Broker Host" Target="MQTT_HOST" Default="" Mode="" Description="MQTT Broker IP oder Hostname (z.B. 192.168.1.100 oder mqtt.local)" Type="Variable" Display="always" Required="false" Mask="false"></Config>
  
  <Config Name="MQTT Broker Port" Target="MQTT_PORT" Default="1883" Mode="" Description="MQTT Broker Port (Standard: 1883, SSL: 8883)" Type="Variable" Display="always" Required="false" Mask="false">1883</Config>
  
  <Config Name="MQTT Benutzername" Target="MQTT_USER" Default="" Mode="" Description="MQTT Benutzername (leer wenn keine Authentifizierung)" Type="Variable" Display="always" Required="false" Mask="false"></Config>
  
  <Config Name="MQTT Passwort" Target="MQTT_PASSWORD" Default="" Mode="" Description="MQTT Passwort" Type="Variable" Display="always" Required="false" Mask="true"></Config>
  
  <Config Name="MQTT Base Topic" Target="MQTT_TOPIC" Default="jellyfin" Mode="" Description="MQTT Base Topic - alle Nachrichten werden unter diesem Topic gesendet" Type="Variable" Display="advanced" Required="false" Mask="false">jellyfin</Config>
  
  <Config Name="MQTT Discovery Prefix" Target="MQTT_DISCOVERY_PREFIX" Default="homeassistant" Mode="" Description="Home Assistant MQTT Discovery Prefix (Standard: homeassistant)" Type="Variable" Display="advanced" Required="false" Mask="false">homeassistant</Config>
  
  <Config Name="MQTT Client ID" Target="MQTT_CLIENT_ID" Default="jellyfin-mqtt" Mode="" Description="MQTT Client ID - muss im Netzwerk eindeutig sein" Type="Variable" Display="advanced" Required="false" Mask="false">jellyfin-mqtt</Config>
  
  <Config Name="MQTT Poll Intervall" Target="MQTT_POLL_INTERVAL" Default="5" Mode="" Description="Wie oft Jellyfin API abgefragt wird (in Sekunden)" Type="Variable" Display="advanced" Required="false" Mask="false">5</Config>
  
  <Config Name="Jellyfin API Key" Target="JELLYFIN_API_KEY" Default="" Mode="" Description="Jellyfin API Key für MQTT Bridge (Dashboard → API Keys → Erstellen)" Type="Variable" Display="always" Required="false" Mask="true"></Config>

</Container>
```

---

## 10. Implementierungsplan

### Phase 1: Basis-Framework
- [ ] `config.py` - ENV-Variablen lesen und validieren
- [ ] `mqtt_bridge.py` - MQTT Verbindung, LWT, Main Loop Struktur
- [ ] `discovery.py` - Statische Discovery Payloads generieren
- [ ] Integration in `run.sh`

### Phase 2: Jellyfin API Integration
- [ ] `jellyfin_api.py` - REST Client mit Auth
- [ ] Sessions abrufen und verarbeiten
- [ ] Transcoding-Status erkennen
- [ ] Dynamische Session-Discovery

### Phase 3: System-Metriken
- [ ] `gpu_monitor.py` - nvidia-smi Wrapper
- [ ] Container-Stats (falls Docker Socket verfügbar)
- [ ] Fehlerbehandlung bei fehlenden Metriken

### Phase 4: Befehle & Steuerung
- [ ] Subscribe auf Command-Topics
- [ ] Session-Steuerung implementieren
- [ ] Library-Scan auslösen
- [ ] Server-Befehle (Restart/Shutdown)

### Phase 5: Testing & Dokumentation
- [ ] Tests mit Home Assistant
- [ ] README.md dokumentieren
- [ ] Unraid Template finalisieren
- [ ] Error Handling verbessern

---

## 11. Fehlerbehandlung

### Graceful Degradation
- MQTT nicht erreichbar → Retry mit Backoff, weiter versuchen
- API Key ungültig → Log Error, keine Crashes
- nvidia-smi fehlt → GPU-Metriken auslassen
- Session verschwindet → Discovery sauber entfernen

### Logging
```python
import logging
logging.basicConfig(
    level=logging.INFO,
    format='[MQTT Bridge] %(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler('/config/logs/mqtt-bridge.log')
    ]
)
```

---

## 12. Sicherheitshinweise

1. **API Key schützen**: Mask="true" im Template, nie in Logs ausgeben
2. **MQTT Credentials**: Ebenfalls maskiert, TLS empfohlen
3. **Keine sensiblen Daten**: Keine User-Passwörter, keine internen IPs
4. **Rate Limiting**: Nicht häufiger als nötig pollen (Default: 5s)

---

## Zusammenfassung

Die MQTT Bridge ermöglicht volle Integration von Jellyfin in Home Assistant:

**Monitoring:**
- Server-Status (Online/Offline)
- Aktive Sessions und Playback
- Transcoding-Status
- GPU-Metriken (Auslastung, Temperatur, VRAM)
- Container-Ressourcen (CPU, RAM)
- Library-Scan Status

**Steuerung:**
- Playback Control (Play/Pause/Stop/Seek)
- Library Scan auslösen
- Server Restart/Shutdown

**Konfiguration:**
- Vollständig über Unraid Template
- Keine manuelle Datei-Bearbeitung nötig
- Deaktiviert wenn MQTT_ENABLE=false
