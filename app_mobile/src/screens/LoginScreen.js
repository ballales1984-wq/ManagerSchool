/**
 * Login Screen - ManagerSchool Mobile
 */

import React, { useState } from 'react';
import {
  View,
  Text,
  TextInput,
  TouchableOpacity,
  StyleSheet,
  Alert,
  ActivityIndicator
} from 'react-native';
import { apiClient, API_ENDPOINTS } from '../config/api';

export default function LoginScreen({ navigation }) {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [ruolo, setRuolo] = useState('docente');
  const [loading, setLoading] = useState(false);

  const handleLogin = async () => {
    if (!username || !password) {
      Alert.alert('Errore', 'Inserisci username e password');
      return;
    }

    setLoading(true);

    try {
      const response = await apiClient.post(API_ENDPOINTS.login, {
        username,
        password,
        ruolo
      });

      if (response.token) {
        apiClient.setToken(response.token);
        // Salva token
        navigation.navigate('Dashboard');
      } else {
        Alert.alert('Errore', 'Credenziali non valide');
      }
    } catch (error) {
      Alert.alert('Errore', 'Errore di connessione');
      console.error(error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <View style={styles.container}>
      <View style={styles.header}>
        <Text style={styles.title}>ManagerSchool</Text>
        <Text style={styles.subtitle}>Registro Digitale</Text>
      </View>

      <View style={styles.form}>
        <TextInput
          style={styles.input}
          placeholder="Username"
          value={username}
          onChangeText={setUsername}
          autoCapitalize="none"
        />

        <TextInput
          style={styles.input}
          placeholder="Password"
          value={password}
          onChangeText={setPassword}
          secureTextEntry
        />

        <Text style={styles.label}>Ruolo:</Text>
        <View style={styles.roleButtons}>
          {['docente', 'dirigente', 'segreteria'].map(r => (
            <TouchableOpacity
              key={r}
              style={[
                styles.roleButton,
                ruolo === r && styles.roleButtonActive
              ]}
              onPress={() => setRuolo(r)}
            >
              <Text
                style={[
                  styles.roleButtonText,
                  ruolo === r && styles.roleButtonTextActive
                ]}
              >
                {r.toUpperCase()}
              </Text>
            </TouchableOpacity>
          ))}
        </View>

        <TouchableOpacity
          style={styles.loginButton}
          onPress={handleLogin}
          disabled={loading}
        >
          {loading ? (
            <ActivityIndicator color="#fff" />
          ) : (
            <Text style={styles.loginButtonText}>LOGIN</Text>
          )}
        </TouchableOpacity>
      </View>
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#f5f5f5',
    justifyContent: 'center',
    padding: 20
  },
  header: {
    alignItems: 'center',
    marginBottom: 40
  },
  title: {
    fontSize: 32,
    fontWeight: 'bold',
    color: '#667eea'
  },
  subtitle: {
    fontSize: 16,
    color: '#666',
    marginTop: 5
  },
  form: {
    width: '100%'
  },
  input: {
    backgroundColor: '#fff',
    borderRadius: 8,
    padding: 15,
    marginBottom: 15,
    fontSize: 16,
    borderWidth: 1,
    borderColor: '#ddd'
  },
  label: {
    fontSize: 14,
    fontWeight: '600',
    marginBottom: 10,
    color: '#333'
  },
  roleButtons: {
    flexDirection: 'row',
    marginBottom: 20,
    gap: 10
  },
  roleButton: {
    flex: 1,
    padding: 12,
    borderRadius: 8,
    backgroundColor: '#fff',
    borderWidth: 1,
    borderColor: '#ddd',
    alignItems: 'center'
  },
  roleButtonActive: {
    backgroundColor: '#667eea',
    borderColor: '#667eea'
  },
  roleButtonText: {
    fontSize: 14,
    fontWeight: '600',
    color: '#666'
  },
  roleButtonTextActive: {
    color: '#fff'
  },
  loginButton: {
    backgroundColor: '#667eea',
    padding: 15,
    borderRadius: 8,
    alignItems: 'center',
    marginTop: 10
  },
  loginButtonText: {
    color: '#fff',
    fontSize: 16,
    fontWeight: 'bold'
  }
});

