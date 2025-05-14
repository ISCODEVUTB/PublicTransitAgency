import 'package:flutter/material.dart';

class AdminPanel extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Panel del Administrador'),
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
                  'Administrador',
                  style: TextStyle(fontSize: 20, fontWeight: FontWeight.bold),
                ),
                const Divider(),
                ...['Actualizar Flota', 'Agendar Mantenimiento', 'Asignar Ruta Vehículo'].map((title) => ElevatedButton(
                      onPressed: () {},
                      child: Text(title),
                    )),
                const Divider(),
                for (var section in ['Rutas', 'Usuarios', 'Operarios', 'Mantenimiento', 'Supervisores', 'Horario', 'Tarifa'])
                  ExpansionTile(
                    title: Text(section),
                    children: ['Añadir', 'Leer', 'Actualizar', 'Eliminar'].map((action) => ListTile(
                          title: Text('$action $section'),
                          onTap: () {},
                        )).toList(),
                  ),
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
                    'Panel General del Administrador',
                    style: TextStyle(fontSize: 24, fontWeight: FontWeight.bold),
                  ),
                  const SizedBox(height: 20),
                  Wrap(
                    spacing: 20,
                    children: [
                      for (var info in [
                        {'title': 'Total de Vehículos', 'count': '150'},
                        {'title': 'Usuarios Registrados', 'count': '1,245'},
                        {'title': 'Operarios Activos', 'count': '73'},
                        {'title': 'Supervisores', 'count': '15'},
                      ])
                        Card(
                          child: Padding(
                            padding: const EdgeInsets.all(16),
                            child: Column(
                              children: [
                                Text(info['title']!, style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold)),
                                Text(info['count']!, style: TextStyle(fontSize: 16)),
                              ],
                            ),
                          ),
                        ),
                    ],
                  ),
                ],
              ),
            ),
          ),
        ],
      ),
    );
  }
}
