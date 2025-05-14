import 'package:flutter/material.dart';

class OperarioPanel extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Panel del Operario'),
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
                  'Operario',
                  style: TextStyle(fontSize: 20, fontWeight: FontWeight.bold),
                ),
                const Divider(),
                ...['Reportar Incidencia', 'Reporte de fallas', 'Alertas', 'Comunicacion con el centro de control'].map((title) => ElevatedButton(
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
                    'Información General',
                    style: TextStyle(fontSize: 24, fontWeight: FontWeight.bold),
                  ),
                  const SizedBox(height: 20),
                  Wrap(
                    spacing: 20,
                    children: [
                      for (var info in [
                        {'title': 'Nombre', 'value': '{nombre}'},
                        {'title': 'Turno', 'value': '{turno}'},
                        {'title': 'Horario', 'value': '{hora:entrada} AM - {hora:salida} PM'},
                        {'title': 'Ruta Asignada', 'value': '{ruta}'},
                        {'title': 'Zona', 'value': '{zona (opcional)}'},
                      ])
                        Card(
                          child: Padding(
                            padding: const EdgeInsets.all(16),
                            child: Column(
                              children: [
                                Text(info['title']!, style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold)),
                                Text(info['value']!, style: TextStyle(fontSize: 16)),
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
