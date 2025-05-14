import 'package:flutter/material.dart';

class HomePage extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Home'),
      ),
      body: Row(
        children: [
          // Sidebar
          Container(
            width: 200,
            color: Colors.grey[200],
            padding: const EdgeInsets.all(16),
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                const Text(
                  'Public Transit Agency',
                  style: TextStyle(fontSize: 20, fontWeight: FontWeight.bold),
                ),
                const SizedBox(height: 16),
                ElevatedButton(
                  onPressed: () {},
                  child: const Text('Consultar saldo'),
                ),
                const SizedBox(height: 8),
                ElevatedButton(
                  onPressed: () {},
                  child: const Text('Portal de usuario'),
                ),
                const SizedBox(height: 8),
                ElevatedButton(
                  onPressed: () {},
                  child: const Text('Avisos'),
                ),
              ],
            ),
          ),
          // Main content
          Expanded(
            child: Center(
              child: Container(
                padding: const EdgeInsets.all(16),
                margin: const EdgeInsets.all(16),
                decoration: BoxDecoration(
                  color: Colors.white,
                  borderRadius: BorderRadius.circular(10),
                  boxShadow: [
                    BoxShadow(
                      color: Colors.grey.withOpacity(0.3),
                      blurRadius: 5,
                      offset: const Offset(0, 3),
                    ),
                  ],
                ),
                child: Column(
                  mainAxisSize: MainAxisSize.min,
                  children: [
                    const Text(
                      'PORTAL DEL USUARIO',
                      style: TextStyle(fontSize: 24, fontWeight: FontWeight.bold),
                    ),
                    const SizedBox(height: 10),
                    const Text('Consulta tu saldo y gestiona tus viajes'),
                    const SizedBox(height: 20),
                    ElevatedButton(
                      onPressed: () {},
                      child: const Text('Ingresar'),
                    ),
                  ],
                ),
              ),
            ),
          ),
        ],
      ),
    );
  }
}
