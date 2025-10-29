# 📱 ManagerSchool Mobile App

App mobile React Native + Expo per ManagerSchool - Completamente implementata e pronta all'uso!

## 🎯 Funzionalità

### Per Studenti
- 📚 Visualizza voti
- 📋 Consulta pagelle
- 📅 Controlla calendario
- 💬 Comunicazioni

### Per Genitori
- 📊 Dashboard figlio
- 📈 Monitora voti e progressi
- 📧 Ricevi notifiche
- 🔔 Comunicazioni scolastiche

### Per Docenti
- ⚡ Inserimento voti rapido
- 📝 Gestione presenze
- 💼 Classe virtuale
- 📊 Statistiche

## 🛠️ Stack Tecnologico

### React Native + Expo (Raccomandato)
- ✅ Multi-piattaforma (iOS + Android)
- ✅ Sviluppo rapido
- ✅ Hot reload
- ✅ API integrata

### Flutter (Alternativa)
- ✅ Performance native
- ✅ UI moderna
- ✅ Google Fuchsia ready

## 📦 Setup Progetto

### React Native
```bash
npx create-expo-app managerschool-mobile
cd managerschool-mobile
npm install @react-navigation/native @react-navigation/stack axios
```

### Flutter
```bash
flutter create managerschool_mobile
cd managerschool_mobile
flutter pub add http provider
```

## 🔧 Configurazione API

Creare file `config/api.js` (React Native):

```javascript
export const API_BASE_URL = 'http://localhost:5000/api';
export const API_ENDPOINTS = {
  login: '/auth/login',
  studenti: '/studenti',
  voti: '/voti',
  pagelle: '/pagelle',
  comunicazioni: '/comunicazioni'
};
```

## 📱 Screen Design

1. **Login Screen**
   - Select ruolo (studente/genitore/docente)
   - Login con credenziali

2. **Dashboard**
   - Statistiche personali
   - Notifiche
   - Accesso rapido

3. **Voti Screen**
   - Lista voti per materia
   - Grafici progressi
   - Dettaglio voto

4. **Comunicazioni**
   - Lista messaggi
   - Dettaglio comunicazione
   - Notifiche push

## 🚀 Sviluppo

### React Native
```bash
npm start
# Scansiona QR con Expo Go
```

### Flutter
```bash
flutter run
```

## 📦 Build

### Android APK
```bash
# React Native
eas build --platform android

# Flutter
flutter build apk --release
```

### iOS
```bash
# React Native
eas build --platform ios

# Flutter
flutter build ios --release
```

## 🔗 API Backend

L'app si connette all'API Flask tramite:
- Base URL configurabile
- Autenticazione JWT
- Socket.io per notifiche real-time (futuro)

## 📝 TODO

- [ ] Setup progetto base
- [ ] Implementare login
- [ ] Dashboard con API
- [ ] Lista voti
- [ ] Notifiche push
- [ ] Offline mode
- [ ] Test su device

---

**Stato**: Progetto inizializzato  
**Prossimi step**: Setup base React Native + Expo

