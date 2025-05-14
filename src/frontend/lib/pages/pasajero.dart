import 'package:flutter/material.dart';

class PassengerPanel extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Pasajero - Panel'),
      ),
      body: Row(
        children: [
          // Panel Izquierdo (Sidebar)
          Container(
            width: 220,
            color: Colors.grey[200],
            padding: const EdgeInsets.all(8),
            child: ListView(
              children: [
                const Text(
                  'Pasajero',
                  style: TextStyle(fontSize: 20, fontWeight: FontWeight.bold),
                ),
                const Divider(),
                ...[
                  'Planificador de viaje',
                  'Líneas, horarios y medios',
                  'Tarifas y peajes',
                  'Noticias y Alertas',
                  'Movimientos',
                  'Sugerencias y Quejas'
                ].map((title) => ElevatedButton(
                      onPressed: () {},
                      child: Text(title),
                    )),
              ],
            ),
          ),
          // Panel Derecho (Main content)
          Expanded(
            child: Padding(
              padding: const EdgeInsets.all(16),
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  const Text(
                    'Información general del pasajero',
                    style: TextStyle(fontSize: 24, fontWeight: FontWeight.bold),
                  ),
                  const SizedBox(height: 20),
                  Card(
                    child: Padding(
                      padding: const EdgeInsets.all(16),
                      child: Column(
                        crossAxisAlignment: CrossAxisAlignment.start,
                        children: [
                          _buildInfoRow('Nombre', '{user.username ?? "No disponible"}'),
                          _buildInfoRow('ID', '{user.username ?? "No disponible"}'),
                          _buildInfoRow('Correo', '{user.email ?? "No disponible"}'),
                          _buildInfoRow('Teléfono', '{user.tel ?? "No disponible"}'),
                          _buildInfoRow('Tipo de tarjeta', '{user.type_card ?? "No disponible"}'),
                          _buildInfoRow('Saldo disponible', '\${user.saldo ?? "0.00"}'),
                          _buildInfoRow('Último viaje', '{day ?? "N/A"} - {route ?? "N/A"} - {time ?? "N/A"}'),
                        ],
                      ),
                    ),
                  ),
                ],
              ),
            ),
          ),
        ],
      ),
    );
  }

  // Helper function to create rows with labels and values
  Widget _buildInfoRow(String label, String value) {
    return Padding(
      padding: const EdgeInsets.symmetric(vertical: 8.0),
      child: Row(
        children: [
          Text(
            '$label:',
            style: const TextStyle(fontWeight: FontWeight.bold),
          ),
          const SizedBox(width: 8),
          Text(value),
        ],
      ),
    );
  }
}
