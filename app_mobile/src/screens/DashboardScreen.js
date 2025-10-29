/**
 * Dashboard Screen - ManagerSchool Mobile
 */

import React, { useEffect, useState } from 'react';
import {
  View,
  Text,
  ScrollView,
  StyleSheet,
  RefreshControl,
  TouchableOpacity
} from 'react-native';
import { apiClient, API_ENDPOINTS } from '../config/api';

export default function DashboardScreen({ navigation }) {
  const [stats, setStats] = useState(null);
  const [refreshing, setRefreshing] = useState(false);

  const loadStats = async () => {
    try {
      const data = await apiClient.get(API_ENDPOINTS.dashboardStats);
      setStats(data);
    } catch (error) {
      console.error('Errore caricamento stats:', error);
    }
  };

  const onRefresh = async () => {
    setRefreshing(true);
    await loadStats();
    setRefreshing(false);
  };

  useEffect(() => {
    loadStats();
  }, []);

  return (
    <ScrollView
      style={styles.container}
      refreshControl={
        <RefreshControl refreshing={refreshing} onRefresh={onRefresh} />
      }
    >
      <View style={styles.header}>
        <Text style={styles.title}>Dashboard</Text>
      </View>

      {stats && (
        <View style={styles.statsContainer}>
          <StatCard
            title="Studenti"
            value={stats.studenti_totali || 0}
            icon="👥"
            color="#667eea"
          />
          <StatCard
            title="Voti"
            value={stats.voti_totali || 0}
            icon="📊"
            color="#f5576c"
          />
          <StatCard
            title="Classi"
            value={stats.classi_totali || 0}
            icon="🎓"
            color="#4facfe"
          />
          <StatCard
            title="Media"
            value={stats.media_generale?.toFixed(1) || '0.0'}
            icon="⭐"
            color="#43e97b"
          />
        </View>
      )}

      <View style={styles.section}>
        <Text style={styles.sectionTitle}>Azioni Rapide</Text>
        <QuickAction
          title="Inserisci Voto"
          icon="➕"
          onPress={() => navigation.navigate('InserimentoVoti')}
        />
        <QuickAction
          title="Visualizza Voti"
          icon="📚"
          onPress={() => navigation.navigate('Voti')}
        />
        <QuickAction
          title="Report"
          icon="📈"
          onPress={() => navigation.navigate('Report')}
        />
      </View>
    </ScrollView>
  );
}

function StatCard({ title, value, icon, color }) {
  return (
    <View style={[styles.statCard, { borderLeftColor: color }]}>
      <Text style={styles.statIcon}>{icon}</Text>
      <Text style={styles.statValue}>{value}</Text>
      <Text style={styles.statTitle}>{title}</Text>
    </View>
  );
}

function QuickAction({ title, icon, onPress }) {
  return (
    <TouchableOpacity style={styles.actionButton} onPress={onPress}>
      <Text style={styles.actionIcon}>{icon}</Text>
      <Text style={styles.actionTitle}>{title}</Text>
      <Text style={styles.actionArrow}>→</Text>
    </TouchableOpacity>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#f5f5f5'
  },
  header: {
    padding: 20,
    backgroundColor: '#fff',
    borderBottomWidth: 1,
    borderBottomColor: '#eee'
  },
  title: {
    fontSize: 24,
    fontWeight: 'bold',
    color: '#333'
  },
  statsContainer: {
    flexDirection: 'row',
    flexWrap: 'wrap',
    padding: 10
  },
  statCard: {
    width: '48%',
    backgroundColor: '#fff',
    padding: 20,
    margin: '1%',
    borderRadius: 10,
    borderLeftWidth: 4
  },
  statIcon: {
    fontSize: 24,
    marginBottom: 5
  },
  statValue: {
    fontSize: 28,
    fontWeight: 'bold',
    color: '#333',
    marginBottom: 5
  },
  statTitle: {
    fontSize: 14,
    color: '#666'
  },
  section: {
    margin: 20
  },
  sectionTitle: {
    fontSize: 20,
    fontWeight: 'bold',
    color: '#333',
    marginBottom: 15
  },
  actionButton: {
    flexDirection: 'row',
    alignItems: 'center',
    backgroundColor: '#fff',
    padding: 20,
    borderRadius: 10,
    marginBottom: 10
  },
  actionIcon: {
    fontSize: 24,
    marginRight: 15
  },
  actionTitle: {
    flex: 1,
    fontSize: 16,
    color: '#333'
  },
  actionArrow: {
    fontSize: 20,
    color: '#667eea'
  }
});

