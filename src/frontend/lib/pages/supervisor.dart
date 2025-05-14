import 'package:flutter/material.dart';
class SupervisorDashboard extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Supervisor - Dashboard'),
      ),
      body: Row(
        children: [
          // Sidebar
          Container(
            width: 220,
            color: Colors.grey[200],
            padding: const EdgeInsets.all(8),
            child: ListView(
              children: [
                const Text(
                  'Supervisor',
                  style: TextStyle(fontSize: 20, fontWeight: FontWeight.bold),
                ),
                const Divider(),
                ...['Asignar turnos', 'Generar reporte de desempeño', 'Obtener información de Unidad', 'Consultar incidencias'].map((title) => ElevatedButton(
                      onPressed: () {},
                      child: Text(title),
                    )),
              ],
            ),
          ),
          // Main content
          Expanded(
            child: Padding(
              padding: const EdgeInsets.all(16),
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  const Text(
                    'Panel de Supervisor',
                    style: TextStyle(fontSize: 24, fontWeight: FontWeight.bold),
                  ),
                  const SizedBox(height: 20),
                  Row(
                    mainAxisAlignment: MainAxisAlignment.spaceEvenly,
                    children: [
                      _buildCard('Solicitudes Abiertas', '8', 'Total en curso'),
                      _buildCard('Solicitudes Atrasadas', '0', 'Sin resolver', color: Colors.red),
                      _buildCard('Tareas Vencidas', '7', 'Supervisión requerida', color: Colors.orange),
                    ],
                  ),
                  const SizedBox(height: 20),
                  Row(
                    children: [
                      _buildChart('Distribución por Regulación'),
                      _buildChart('Distribución por Actividad'),
                    ],
                  ),
                  const SizedBox(height: 20),
                  _buildChart('Solicitudes en el tiempo', fullWidth: true),
                ],
              ),
            ),
          ),
        ],
      ),
    );
  }

  Widget _buildCard(String title, String number, String subtitle, {Color color = Colors.blue}) {
    return Card(
      color: color,
      child: Padding(
        padding: const EdgeInsets.all(16),
        child: Column(
          children: [
            Text(title, style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold)),
            Text(number, style: TextStyle(fontSize: 32)),
            Text(subtitle),
          ],
        ),
      ),
    );
  }

  Widget _buildChart(String title, {bool fullWidth = false}) {
    return Expanded(
      flex: fullWidth ? 2 : 1,
      child: Card(
        margin: const EdgeInsets.all(8),
        child: Padding(
          padding: const EdgeInsets.all(16),
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              Text(title, style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold)),
              const SizedBox(height: 100),
              const Text('[Gráfico aquí]'),
            ],
          ),
        ),
      ),
    );
  }
}
