import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;
import 'dart:convert';
import 'package:flutter/services.dart';
import '../config/config.dart';

class AdminPanel extends StatelessWidget {
  final String token;

  const AdminPanel({Key? key, required this.token}) : super(key: key);

  // Define our color scheme
  static const primaryColor = Color(0xFF1A73E8); // Blue
  static const secondaryColor = Color(0xFF34A853); // Green accent
  static const accentColor = Color(0xFFFBBC05); // Yellow accent
  static const warningColor = Color(0xFFEA4335); // Red for alerts
  static const backgroundColor = Colors.white;
  static const cardColor = Color(0xFFF8F9FA); // Light gray/white

  Future<Map<String, dynamic>> fetchDashboardData() async {
    print('Token enviado: $token');
    final response = await http.get(
      Uri.parse('${AppConfig.baseUrl}/login/dashboard'),
      headers: {
        'Authorization': 'Bearer $token',
        'accept': 'application/json',
      },
    );

    if (response.statusCode == 200) {
      final dashboardData = json.decode(response.body);
      print('Datos del dashboard: $dashboardData');
      return dashboardData;
    } else {
      print('Error al obtener el dashboard: ${response.body}');
      throw Exception('Error al cargar datos del dashboard: ${response.body}');
    }
  }

  Future<List<dynamic>> fetchTransportUnits() async {
    final response = await http.get(
      Uri.parse('${AppConfig.baseUrl}/transport_units/'),
      headers: {
        'Authorization': 'Bearer $token',
        'accept': 'application/json',
      },
    );
    if (response.statusCode == 200) {
      return json.decode(response.body);
    } else {
      throw Exception('Error al cargar unidades de transporte');
    }
  }

  Future<bool> createTransportUnit(Map<String, dynamic> data) async {
    final response = await http.post(
      Uri.parse('${AppConfig.baseUrl}/transport_units/create'),
      headers: {
        'Authorization': 'Bearer $token',
        'accept': 'application/json',
        'Content-Type': 'application/x-www-form-urlencoded',
      },
      body: data,
    );
    return response.statusCode == 200 || response.statusCode == 201;
  }

  Future<bool> updateTransportUnit(Map<String, dynamic> data) async {
    final response = await http.post(
      Uri.parse('${AppConfig.baseUrl}/transport_units/update'),
      headers: {
        'Authorization': 'Bearer $token',
        'accept': 'application/json',
        'Content-Type': 'application/x-www-form-urlencoded',
      },
      body: data,
    );
    return response.statusCode == 200;
  }

  Future<bool> deleteTransportUnit(String id) async {
    final response = await http.post(
      Uri.parse('${AppConfig.baseUrl}/transport_units/delete'),
      headers: {
        'Authorization': 'Bearer $token',
        'accept': 'application/json',
        'Content-Type': 'application/x-www-form-urlencoded',
      },
      body: {'ID': id},
    );
    return response.statusCode == 200;
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        elevation: 0,
        backgroundColor: primaryColor,
        title: const Text(
          'Panel de Administración',
          style: TextStyle(
            fontWeight: FontWeight.w600,
            fontSize: 20,
          ),
        ),
        actions: [
          IconButton(
            icon: const Icon(Icons.notifications_outlined),
            onPressed: () {},
            tooltip: 'Notificaciones',
          ),
          IconButton(
            icon: const Icon(Icons.settings_outlined),
            onPressed: () {},
            tooltip: 'Configuración',
          ),
          IconButton(
            icon: const Icon(Icons.account_circle_outlined),
            onPressed: () {},
            tooltip: 'Perfil',
          ),
        ],
        systemOverlayStyle: SystemUiOverlayStyle.light,
      ),
      body: FutureBuilder<Map<String, dynamic>>(
        future: fetchDashboardData(),
        builder: (context, snapshot) {
          if (snapshot.connectionState == ConnectionState.waiting) {
            return Center(
              child: Column(
                mainAxisAlignment: MainAxisAlignment.center,
                children: [
                  CircularProgressIndicator(
                    color: primaryColor,
                    strokeWidth: 3,
                  ),
                  const SizedBox(height: 16),
                  const Text(
                    'Cargando información del sistema...',
                    style: TextStyle(
                      color: Color(0xFF5F6368),
                      fontSize: 16,
                    ),
                  ),
                ],
              ),
            );
          } else if (snapshot.hasError) {
            return Center(
              child: Column(
                mainAxisAlignment: MainAxisAlignment.center,
                children: [
                  const Icon(
                    Icons.error_outline,
                    color: Colors.red,
                    size: 60,
                  ),
                  const SizedBox(height: 16),
                  Text(
                    'Error: ${snapshot.error}',
                    style: const TextStyle(color: Colors.red),
                    textAlign: TextAlign.center,
                  ),
                ],
              ),
            );
          } else if (!snapshot.hasData) {
            return const Center(
              child: Text(
                'Sin datos disponibles',
                style: TextStyle(fontSize: 18),
              ),
            );
          }

          final data = snapshot.data!;
          final user = data['user'] ?? {};
          final totalVehiculos = data['total_vehiculos'] ?? 0;
          final totalPasajeros = data['total_passanger'] ?? 0;
          final totalOperarios = data['total_operative'] ?? 0;
          final totalSupervisores = data['total_supervisors'] ?? 0;

          return Row(
            children: [
              // Sidebar
              Container(
                width: 250,
                color: const Color(0xFFF8F9FA),
                child: Column(
                  children: [
                    Container(
                      padding: const EdgeInsets.symmetric(
                          vertical: 24, horizontal: 16),
                      color: primaryColor.withOpacity(0.05),
                      child: Row(
                        children: [
                          CircleAvatar(
                            backgroundColor: primaryColor,
                            radius: 24,
                            child: Text(
                              user['Nombre']?.toString().substring(0, 1) ?? 'A',
                              style: const TextStyle(
                                color: Colors.white,
                                fontWeight: FontWeight.bold,
                                fontSize: 18,
                              ),
                            ),
                          ),
                          const SizedBox(width: 12),
                          Expanded(
                            child: Column(
                              crossAxisAlignment: CrossAxisAlignment.start,
                              children: [
                                Text(
                                  user['Nombre']?.toString() ?? 'Administrador',
                                  style: const TextStyle(
                                    fontWeight: FontWeight.bold,
                                    fontSize: 16,
                                    color: Color(0xFF202124),
                                  ),
                                  overflow: TextOverflow.ellipsis,
                                ),
                                const SizedBox(height: 4),
                                Container(
                                  padding: const EdgeInsets.symmetric(
                                      horizontal: 8, vertical: 2),
                                  decoration: BoxDecoration(
                                    color: primaryColor,
                                    borderRadius: BorderRadius.circular(12),
                                  ),
                                  child: const Text(
                                    'Administrador',
                                    style: TextStyle(
                                      color: Colors.white,
                                      fontSize: 12,
                                      fontWeight: FontWeight.w500,
                                    ),
                                  ),
                                ),
                              ],
                            ),
                          ),
                        ],
                      ),
                    ),
                    const Divider(height: 1),
                    Expanded(
                      child: ListView(
                        padding: EdgeInsets.zero,
                        children: [
                          _buildMenuItem(
                            icon: Icons.dashboard_outlined,
                            title: 'Panel Principal',
                            color: primaryColor,
                            isActive: true,
                          ),
                          _buildMenuItem(
                            icon: Icons.directions_bus,
                            title: 'Actualizar Flota',
                            color: primaryColor,
                          ),
                          _buildMenuItem(
                            icon: Icons.build_circle_outlined,
                            title: 'Agendar Mantenimiento',
                            color: primaryColor,
                            onTap: () {
                              Navigator.push(
                                context,
                                MaterialPageRoute(
                                  builder: (_) =>
                                      AgendarMantenimientoScreen(token: token),
                                ),
                              );
                            },
                          ),
                          _buildMenuItem(
                            icon: Icons.alt_route,
                            title: 'Asignar Ruta Vehículo',
                            color: primaryColor,
                          ),
                          _buildMenuItem(
                            icon: Icons.person_add_alt_1,
                            title: 'Crear Usuario',
                            color: primaryColor,
                          ),
                          _buildMenuItem(
                            icon: Icons.question_answer_outlined,
                            title: 'Gestión de PQR',
                            color: primaryColor,
                          ),
                          _buildMenuItem(
                            icon: Icons.bar_chart_outlined,
                            title: 'Gestión de Rendimiento',
                            color: primaryColor,
                          ),
                          _buildMenuItem(
                            icon: Icons.assignment_turned_in_outlined,
                            title: 'Gestión de Asistencia',
                            color: primaryColor,
                          ),
                          // CRUD: Rutas
                          _buildCrudSection(
                            title: 'Rutas',
                            color: primaryColor,
                            buttons: [
                              _buildCrudButton(
                                '➕ Añadir Ruta',
                                () => showDialog(
                                  context: context,
                                  builder: (_) => Dialog(
                                    child: Padding(
                                      padding: const EdgeInsets.all(24),
                                      child: _RutaFormWidget(
                                        token: token,
                                        mode: RutaFormMode.create,
                                        onSuccess: () => Navigator.pop(context),
                                      ),
                                    ),
                                  ),
                                ),
                              ),
                              _buildCrudButton(
                                '📄 Leer Rutas',
                                () => showDialog(
                                  context: context,
                                  builder: (_) => Dialog(
                                    child: Padding(
                                      padding: const EdgeInsets.all(24),
                                      child: _RutaListWidget(token: token),
                                    ),
                                  ),
                                ),
                              ),
                              _buildCrudButton(
                                '🖊️ Actualizar Ruta',
                                () => showDialog(
                                  context: context,
                                  builder: (_) => Dialog(
                                    child: Padding(
                                      padding: const EdgeInsets.all(24),
                                      child: _RutaFormWidget(
                                        token: token,
                                        mode: RutaFormMode.update,
                                        onSuccess: () => Navigator.pop(context),
                                      ),
                                    ),
                                  ),
                                ),
                              ),
                              _buildCrudButton(
                                '🗑️ Eliminar Ruta',
                                () => showDialog(
                                  context: context,
                                  builder: (_) => Dialog(
                                    child: Padding(
                                      padding: const EdgeInsets.all(24),
                                      child: _RutaDeleteWidget(
                                        token: token,
                                        onSuccess: () => Navigator.pop(context),
                                      ),
                                    ),
                                  ),
                                ),
                              ),
                            ],
                          ),
                          // CRUD: Usuarios
                          _buildCrudSection(
                            title: 'Usuarios',
                            color: primaryColor,
                            buttons: [
                              _buildCrudButton(
                                  '📄 Leer Usuarios',
                                  () => Navigator.pushNamed(
                                      context, '/user/consultar')),
                              _buildCrudButton(
                                  '🖊️ Actualizar Usuario',
                                  () => Navigator.pushNamed(
                                      context, '/user/actualizar')),
                              _buildCrudButton(
                                  '🗑️ Eliminar Usuario',
                                  () => Navigator.pushNamed(
                                      context, '/user/eliminar')),
                            ],
                          ),
                          // CRUD: Operarios
                          _buildCrudSection(
                            title: 'Operarios',
                            color: primaryColor,
                            buttons: [
                              _buildCrudButton(
                                  '📄 Leer Operarios',
                                  () => Navigator.pushNamed(
                                      context, '/user/consultar')),
                              _buildCrudButton(
                                  '🖊️ Actualizar Operarios',
                                  () => Navigator.pushNamed(
                                      context, '/user/actualizar')),
                              _buildCrudButton(
                                  '🗑️ Eliminar Operarios',
                                  () => Navigator.pushNamed(
                                      context, '/user/eliminar')),
                            ],
                          ),
                          // CRUD: Mantenimiento
                          _buildCrudSection(
                            title: 'Mantenimiento',
                            color: primaryColor,
                            buttons: [
                              _buildCrudButton(
                                '➕ Añadir Mantenimiento',
                                () => showDialog(
                                  context: context,
                                  builder: (_) => Dialog(
                                      child: AgendarMantenimientoScreen(
                                          token: token)),
                                ),
                              ),
                              _buildCrudButton(
                                '📄 Leer Mantenimientos',
                                () => showDialog(
                                  context: context,
                                  builder: (_) => Dialog(
                                      child: LeerMantenimientosWidget(
                                          token: token)),
                                ),
                              ),
                              _buildCrudButton(
                                '🖊️ Actualizar Mantenimiento',
                                () => showDialog(
                                  context: context,
                                  builder: (_) => Dialog(
                                      child: ActualizarMantenimientoWidget(
                                          token: token)),
                                ),
                              ),
                              _buildCrudButton(
                                '🗑️ Eliminar Mantenimiento',
                                () => showDialog(
                                  context: context,
                                  builder: (_) => Dialog(
                                      child: EliminarMantenimientoWidget(
                                          token: token)),
                                ),
                              ),
                            ],
                          ),
                          // CRUD: Supervisores
                          _buildCrudSection(
                            title: 'Supervisores',
                            color: primaryColor,
                            buttons: [
                              _buildCrudButton(
                                  '📄 Leer Supervisores',
                                  () => Navigator.pushNamed(
                                      context, '/user/consultar')),
                              _buildCrudButton(
                                  '🖊️ Actualizar Supervisores',
                                  () => Navigator.pushNamed(
                                      context, '/user/actualizar')),
                              _buildCrudButton(
                                  '🗑️ Eliminar Supervisores',
                                  () => Navigator.pushNamed(
                                      context, '/user/eliminar')),
                            ],
                          ),
                          // CRUD: Horario
                          _buildCrudSection(
                            title: 'Horario',
                            color: primaryColor,
                            buttons: [
                              _buildCrudButton(
                                '➕ Añadir horario',
                                () => showDialog(
                                  context: context,
                                  builder: (_) => Dialog(
                                    child: Padding(
                                      padding: const EdgeInsets.all(24),
                                      child: _HorarioFormWidget(
                                        token: token,
                                        mode: HorarioFormMode.create,
                                        onSuccess: () => Navigator.pop(context),
                                      ),
                                    ),
                                  ),
                                ),
                              ),
                              _buildCrudButton(
                                '📄 Leer horario',
                                () => showDialog(
                                  context: context,
                                  builder: (_) => Dialog(
                                    child: Padding(
                                      padding: const EdgeInsets.all(24),
                                      child: _HorarioListWidget(token: token),
                                    ),
                                  ),
                                ),
                              ),
                              _buildCrudButton(
                                '🖊️ Actualizar horario',
                                () => showDialog(
                                  context: context,
                                  builder: (_) => Dialog(
                                    child: Padding(
                                      padding: const EdgeInsets.all(24),
                                      child: _HorarioFormWidget(
                                        token: token,
                                        mode: HorarioFormMode.update,
                                        onSuccess: () => Navigator.pop(context),
                                      ),
                                    ),
                                  ),
                                ),
                              ),
                              _buildCrudButton(
                                '🗑️ Eliminar horario',
                                () => showDialog(
                                  context: context,
                                  builder: (_) => Dialog(
                                    child: Padding(
                                      padding: const EdgeInsets.all(24),
                                      child: _HorarioDeleteWidget(
                                        token: token,
                                        onSuccess: () => Navigator.pop(context),
                                      ),
                                    ),
                                  ),
                                ),
                              ),
                            ],
                          ),
                          // CRUD: Tarifa
                          _buildCrudSection(
                            title: 'Tarifa',
                            color: primaryColor,
                            buttons: [
                              _buildCrudButton(
                                  '➕ Añadir Tarifa',
                                  () => Navigator.pushNamed(
                                      context, '/price/crear')),
                              _buildCrudButton(
                                  '📄 Leer Tarifa',
                                  () => Navigator.pushNamed(
                                      context, '/price/consultar')),
                              _buildCrudButton(
                                  '🖊️ Actualizar Tarifa',
                                  () => Navigator.pushNamed(
                                      context, '/price/actualizar')),
                              _buildCrudButton(
                                  '🗑️ Eliminar Tarifa',
                                  () => Navigator.pushNamed(
                                      context, '/price/eliminar')),
                            ],
                          ),
                          // CRUD: Otros
                          _buildCrudSection(
                            title: 'Otros',
                            color: primaryColor,
                            buttons: [
                              _buildCrudButton(
                                  '📄 Extraer Tipo de Usuario',
                                  () => Navigator.pushNamed(
                                      context, '/roluser/consultar')),
                              _buildCrudButton(
                                  '📄 Extraer Tipo de Movimiento',
                                  () => Navigator.pushNamed(
                                      context, '/typemovement/consultar')),
                              _buildCrudButton(
                                  '📄 Extraer Servicios de Transporte',
                                  () => Navigator.pushNamed(
                                      context, '/typetransport/consultar')),
                            ],
                          ),
                        ],
                      ),
                    ),

                    // Logout Button
                    Container(
                      width: double.infinity,
                      padding: const EdgeInsets.all(16),
                      child: ElevatedButton.icon(
                        onPressed: () {},
                        icon: const Icon(Icons.logout, size: 18),
                        label: const Text('Cerrar Sesión'),
                        style: ElevatedButton.styleFrom(
                          backgroundColor: Colors.white,
                          foregroundColor: primaryColor,
                          elevation: 0,
                          padding: const EdgeInsets.symmetric(vertical: 12),
                          shape: RoundedRectangleBorder(
                            borderRadius: BorderRadius.circular(8),
                            side: BorderSide(color: primaryColor),
                          ),
                        ),
                      ),
                    ),
                  ],
                ),
              ),

              // Main content
              Expanded(
                child: Container(
                  color: const Color(0xFFF5F7FA),
                  child: SingleChildScrollView(
                    padding: const EdgeInsets.all(24),
                    child: Column(
                      crossAxisAlignment: CrossAxisAlignment.start,
                      children: [
                        // Header with date and welcome message
                        Row(
                          mainAxisAlignment: MainAxisAlignment.spaceBetween,
                          children: [
                            Column(
                              crossAxisAlignment: CrossAxisAlignment.start,
                              children: [
                                Row(
                                  children: [
                                    const Icon(
                                      Icons.dashboard_outlined,
                                      color: primaryColor,
                                      size: 28,
                                    ),
                                    const SizedBox(width: 12),
                                    const Text(
                                      'Panel de Control',
                                      style: TextStyle(
                                        fontSize: 24,
                                        fontWeight: FontWeight.bold,
                                        color: Color(0xFF202124),
                                      ),
                                    ),
                                  ],
                                ),
                                const SizedBox(height: 8),
                                Text(
                                  'Bienvenido, ${user['Nombre'] ?? 'Administrador'}. Aquí está el resumen del sistema.',
                                  style: const TextStyle(
                                    fontSize: 16,
                                    color: Color(0xFF5F6368),
                                  ),
                                ),
                              ],
                            ),
                            Container(
                              padding: const EdgeInsets.symmetric(
                                horizontal: 16,
                                vertical: 8,
                              ),
                              decoration: BoxDecoration(
                                color: Colors.white,
                                borderRadius: BorderRadius.circular(8),
                                border: Border.all(
                                  color: const Color(0xFFDFE1E5),
                                  width: 1,
                                ),
                              ),
                              child: Row(
                                children: [
                                  const Icon(
                                    Icons.calendar_today,
                                    size: 18,
                                    color: primaryColor,
                                  ),
                                  const SizedBox(width: 8),
                                  Text(
                                    _getCurrentDate(),
                                    style: const TextStyle(
                                      fontSize: 14,
                                      fontWeight: FontWeight.w500,
                                      color: Color(0xFF202124),
                                    ),
                                  ),
                                ],
                              ),
                            ),
                          ],
                        ),
                        const SizedBox(height: 24),

                        // Stats Overview
                        Row(
                          children: [
                            Expanded(
                              child: _buildStatCard(
                                title: 'Total Vehículos',
                                value: '$totalVehiculos',
                                icon: Icons.directions_bus,
                                color: primaryColor,
                              ),
                            ),
                            const SizedBox(width: 16),
                            Expanded(
                              child: _buildStatCard(
                                title: 'Total Pasajeros',
                                value: '$totalPasajeros',
                                icon: Icons.people,
                                color: secondaryColor,
                              ),
                            ),
                            const SizedBox(width: 16),
                            Expanded(
                              child: _buildStatCard(
                                title: 'Total Operarios',
                                value: '$totalOperarios',
                                icon: Icons.engineering,
                                color: accentColor,
                              ),
                            ),
                            const SizedBox(width: 16),
                            Expanded(
                              child: _buildStatCard(
                                title: 'Total Supervisores',
                                value: '$totalSupervisores',
                                icon: Icons.supervisor_account,
                                color: warningColor,
                              ),
                            ),
                          ],
                        ),
                        const SizedBox(height: 24),

                        // Quick Actions
                        Card(
                          elevation: 0,
                          shape: RoundedRectangleBorder(
                            borderRadius: BorderRadius.circular(12),
                            side: BorderSide(
                              color: primaryColor.withOpacity(0.1),
                              width: 1,
                            ),
                          ),
                          color: cardColor,
                          child: Padding(
                            padding: const EdgeInsets.all(20),
                            child: Column(
                              crossAxisAlignment: CrossAxisAlignment.start,
                              children: [
                                Row(
                                  children: [
                                    Icon(
                                      Icons.flash_on,
                                      color: primaryColor,
                                      size: 22,
                                    ),
                                    const SizedBox(width: 8),
                                    const Text(
                                      'Acciones Rápidas',
                                      style: TextStyle(
                                        fontSize: 18,
                                        fontWeight: FontWeight.bold,
                                        color: Color(0xFF202124),
                                      ),
                                    ),
                                  ],
                                ),
                                const SizedBox(height: 16),
                                const Divider(),
                                const SizedBox(height: 16),
                                GridView.count(
                                  shrinkWrap: true,
                                  physics: const NeverScrollableScrollPhysics(),
                                  crossAxisCount: 2,
                                  crossAxisSpacing: 16,
                                  mainAxisSpacing: 16,
                                  childAspectRatio: 2.5,
                                  children: [
                                    _buildActionButton(
                                      label: 'Añadir Usuario',
                                      icon: Icons.person_add_outlined,
                                      color: primaryColor,
                                    ),
                                    _buildActionButton(
                                      label: 'Añadir Vehículo',
                                      icon: Icons.add_circle_outline,
                                      color: secondaryColor,
                                      onPressed: () => showDialog(
                                        context: context,
                                        builder: (_) => Dialog(
                                          child: CrearUnidadWidget(
                                            token: token,
                                            onCreated: () =>
                                                Navigator.pop(context),
                                          ),
                                        ),
                                      ),
                                    ),
                                    _buildActionButton(
                                      label: 'Generar Reporte',
                                      icon: Icons.assessment_outlined,
                                      color: accentColor,
                                    ),
                                  ],
                                ),
                              ],
                            ),
                          ),
                        ),
                        const SizedBox(height: 24),

                        // Transport Units Management
                        const SizedBox(height: 32),
                        Text('Gestión de Flota',
                            style: TextStyle(
                                fontSize: 22, fontWeight: FontWeight.bold)),
                        const SizedBox(height: 16),
                        Row(
                          children: [
                            ElevatedButton.icon(
                              icon: Icon(Icons.add),
                              label: Text('Añadir Unidad'),
                              style: ElevatedButton.styleFrom(
                                backgroundColor: AdminPanel.primaryColor,
                                foregroundColor: Colors.white,
                              ),
                              onPressed: () {
                                showDialog(
                                  context: context,
                                  builder: (_) => Dialog(
                                    child: CrearUnidadWidget(
                                      token: token,
                                      onCreated: () => Navigator.pop(context),
                                    ),
                                  ),
                                );
                              },
                            ),
                            const SizedBox(width: 16),
                            ElevatedButton.icon(
                              icon: Icon(Icons.refresh),
                              label: Text('Actualizar Tabla'),
                              onPressed: () {
                                (context as Element).markNeedsBuild();
                              },
                            ),
                          ],
                        ),
                        const SizedBox(height: 24),
                        _buildTransportUnitsSection(),
                      ],
                    ),
                  ),
                ),
              ),
            ],
          );
        },
      ),
    );
  }

  Widget _buildTransportUnitsSection() {
    return FutureBuilder<List<dynamic>>(
      future: fetchTransportUnits(),
      builder: (context, snapshot) {
        if (snapshot.connectionState == ConnectionState.waiting) {
          return Center(child: CircularProgressIndicator());
        } else if (snapshot.hasError) {
          return Center(
              child: Text('Error al cargar unidades de transporte'));
        } else if (!snapshot.hasData || snapshot.data!.isEmpty) {
          return Center(child: Text('No hay unidades registradas.'));
        }
        final units = snapshot.data!;
        return DataTable(
          columns: const [
            DataColumn(label: Text('ID')),
            DataColumn(label: Text('Ubicación')),
            DataColumn(label: Text('Capacidad')),
            DataColumn(label: Text('Ruta')),
            DataColumn(label: Text('Tipo')),
            DataColumn(label: Text('Acciones')),
          ],
          rows: units.map<DataRow>((unit) {
            return DataRow(
              cells: [
                DataCell(Text(unit['ID']?.toString() ?? '-')),
                DataCell(Text(unit['Ubicacion']?.toString() ?? '-')),
                DataCell(Text(unit['Capacidad']?.toString() ?? '-')),
                DataCell(Text(unit['IDRuta']?.toString() ?? '-')),
                DataCell(Text(unit['IDTipo']?.toString() ?? '-')),
                DataCell(Row(
                  children: [
                    IconButton(
                      icon: Icon(Icons.edit, color: Colors.blue),
                      tooltip: 'Editar',
                      onPressed: () {
                        showDialog(
                          context: context,
                          builder: (_) => Dialog(
                            child: EditarUnidadWidget(
                              token: token,
                              unidad: unit,
                              onUpdated: () =>
                                  (context as Element).markNeedsBuild(),
                            ),
                          ),
                        );
                      },
                    ),
                    IconButton(
                      icon: Icon(Icons.delete, color: Colors.red),
                      tooltip: 'Eliminar',
                      onPressed: () async {
                        final confirm = await showDialog<bool>(
                          context: context,
                          builder: (_) => AlertDialog(
                            title: Text('Eliminar unidad'),
                            content: Text(
                                '¿Seguro que deseas eliminar esta unidad?'),
                            actions: [
                              TextButton(
                                onPressed: () =>
                                    Navigator.pop(context, false),
                                child: Text('Cancelar'),
                              ),
                              TextButton(
                                onPressed: () =>
                                    Navigator.pop(context, true),
                                child: Text('Eliminar'),
                              ),
                            ],
                          ),
                        );
                        if (confirm == true) {
                          await deleteTransportUnit(unit['ID'].toString());
                          (context as Element).markNeedsBuild();
                        }
                      },
                    ),
                  ],
                )),
              ],
            );
          }).toList(),
        );
      },
    );
  }

  String _getCurrentDate() {
    final now = DateTime.now();
    final months = [
      'Enero',
      'Febrero',
      'Marzo',
      'Abril',
      'Mayo',
      'Junio',
      'Julio',
      'Agosto',
      'Septiembre',
      'Octubre',
      'Noviembre',
      'Diciembre'
    ];
    return '${now.day} de ${months[now.month - 1]}, ${now.year}';
  }

  Widget _buildMenuItem({
    required IconData icon,
    required String title,
    required Color color,
    bool isActive = false,
    VoidCallback? onTap,
  }) {
    return ListTile(
      leading: Icon(
        icon,
        color: isActive ? color : const Color(0xFF5F6368),
      ),
      title: Text(
        title,
        style: TextStyle(
          fontSize: 14,
          fontWeight: isActive ? FontWeight.w600 : FontWeight.w500,
          color: isActive ? color : const Color(0xFF202124),
        ),
      ),
      dense: true,
      horizontalTitleGap: 8,
      onTap: onTap,
      shape: RoundedRectangleBorder(
        borderRadius: BorderRadius.circular(8),
      ),
      tileColor: isActive ? color.withOpacity(0.1) : null,
      hoverColor: color.withOpacity(0.05),
    );
  }

  Widget _buildStatCard({
    required String title,
    required String value,
    required IconData icon,
    required Color color,
  }) {
    return Card(
      elevation: 0,
      shape: RoundedRectangleBorder(
        borderRadius: BorderRadius.circular(12),
        side: BorderSide(
          color: color.withOpacity(0.1),
          width: 1,
        ),
      ),
      color: cardColor,
      child: Padding(
        padding: const EdgeInsets.all(20),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Row(
              mainAxisAlignment: MainAxisAlignment.spaceBetween,
              children: [
                Text(
                  title,
                  style: TextStyle(
                    fontSize: 14,
                    fontWeight: FontWeight.w500,
                    color: color,
                  ),
                ),
                Container(
                  width: 40,
                  height: 40,
                  decoration: BoxDecoration(
                    color: color.withOpacity(0.1),
                    borderRadius: BorderRadius.circular(8),
                  ),
                  child: Icon(
                    icon,
                    color: color,
                    size: 20,
                  ),
                ),
              ],
            ),
            const SizedBox(height: 12),
            Text(
              value,
              style: const TextStyle(
                fontSize: 28,
                fontWeight: FontWeight.bold,
                color: Color(0xFF202124),
              ),
            ),
          ],
        ),
      ),
    );
  }

  Widget _buildActionButton({
    required String label,
    required IconData icon,
    required Color color,
    VoidCallback? onPressed,
  }) {
    return ElevatedButton.icon(
      onPressed: onPressed,
      icon: Icon(icon, size: 18),
      label: Text(label),
      style: ElevatedButton.styleFrom(
        backgroundColor: color,
        foregroundColor: Colors.white,
        padding: const EdgeInsets.symmetric(vertical: 12, horizontal: 16),
        shape: RoundedRectangleBorder(
          borderRadius: BorderRadius.circular(8),
        ),
        elevation: 0,
        alignment: Alignment.centerLeft,
      ),
    );
  }

  Widget _buildCrudSection(
      {required String title,
      required Color color,
      required List<Widget> buttons}) {
    return Padding(
      padding: const EdgeInsets.symmetric(vertical: 8.0, horizontal: 8.0),
      child: Card(
        color: color.withOpacity(0.04),
        elevation: 0,
        shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(8)),
        child: ExpansionTile(
          title: Text(title,
              style: TextStyle(fontWeight: FontWeight.bold, color: color)),
          children: buttons,
        ),
      ),
    );
  }

  Widget _buildCrudButton(String label, VoidCallback onPressed) {
    return Padding(
      padding: const EdgeInsets.symmetric(vertical: 2.0, horizontal: 16.0),
      child: SizedBox(
        width: double.infinity,
        child: OutlinedButton(
          onPressed: onPressed,
          child: Align(
            alignment: Alignment.centerLeft,
            child: Text(label, style: const TextStyle(fontSize: 14)),
          ),
          style: OutlinedButton.styleFrom(
            padding: const EdgeInsets.symmetric(vertical: 10, horizontal: 12),
            side: const BorderSide(color: Color(0xFFDFE1E5)),
            shape:
                RoundedRectangleBorder(borderRadius: BorderRadius.circular(6)),
          ),
        ),
      ),
    );
  }
}

// Agrego la pantalla para agendar mantenimiento
class AgendarMantenimientoScreen extends StatefulWidget {
  final String token;
  const AgendarMantenimientoScreen({Key? key, required this.token})
      : super(key: key);

  static const primaryColor = Color(0xFF1A73E8);

  @override
  State<AgendarMantenimientoScreen> createState() =>
      _AgendarMantenimientoScreenState();
}

class _AgendarMantenimientoScreenState
    extends State<AgendarMantenimientoScreen> {
  final _formKey = GlobalKey<FormState>();
  final TextEditingController _idController = TextEditingController();
  final TextEditingController _idStatusController = TextEditingController();
  final TextEditingController _typeController = TextEditingController();
  final TextEditingController _fechaController = TextEditingController();
  final TextEditingController _idUnidadController = TextEditingController();
  bool _loading = false;
  String? _response;
  String? _error;

  Future<void> _agendarMantenimiento() async {
    if (!_formKey.currentState!.validate()) return;
    setState(() {
      _loading = true;
      _response = null;
      _error = null;
    });
    try {
      final response = await http.post(
        Uri.parse('${AppConfig.baseUrl}/maintainance/create'),
        headers: {
          'Authorization': 'Bearer ${widget.token}',
          'accept': 'application/json',
          'Content-Type': 'application/x-www-form-urlencoded',
        },
        body: {
          'ID': _idController.text.trim(),
          'id_status': _idStatusController.text.trim(),
          'type': _typeController.text.trim(),
          'fecha': _fechaController.text.trim(),
          'idunidad': _idUnidadController.text.trim(),
        },
      );
      if (response.statusCode == 200 || response.statusCode == 201) {
        setState(() {
          _response = 'Mantenimiento agendado exitosamente.';
        });
      } else {
        setState(() {
          _error = 'No se pudo agendar el mantenimiento. (${response.body})';
        });
      }
    } catch (e) {
      setState(() {
        _error = 'Error de conexión.';
      });
    } finally {
      setState(() {
        _loading = false;
      });
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Agendar Mantenimiento'),
        backgroundColor: AgendarMantenimientoScreen.primaryColor,
      ),
      body: SingleChildScrollView(
        padding: const EdgeInsets.all(24.0),
        child: Form(
          key: _formKey,
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              Text('Complete los datos para agendar un mantenimiento:',
                  style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold)),
              const SizedBox(height: 24),
              TextFormField(
                controller: _idController,
                keyboardType: TextInputType.number,
                decoration: InputDecoration(
                  labelText: 'ID',
                  border: OutlineInputBorder(),
                  prefixIcon: Icon(Icons.confirmation_number),
                ),
                validator: (value) =>
                    value == null || value.isEmpty ? 'Ingrese el ID' : null,
              ),
              const SizedBox(height: 16),
              TextFormField(
                controller: _idStatusController,
                keyboardType: TextInputType.number,
                decoration: InputDecoration(
                  labelText: 'ID Status',
                  border: OutlineInputBorder(),
                  prefixIcon: Icon(Icons.info_outline),
                ),
                validator: (value) => value == null || value.isEmpty
                    ? 'Ingrese el ID Status'
                    : null,
              ),
              const SizedBox(height: 16),
              TextFormField(
                controller: _typeController,
                decoration: InputDecoration(
                  labelText: 'Tipo de Mantenimiento',
                  border: OutlineInputBorder(),
                  prefixIcon: Icon(Icons.build),
                ),
                validator: (value) =>
                    value == null || value.isEmpty ? 'Ingrese el tipo' : null,
              ),
              const SizedBox(height: 16),
              TextFormField(
                controller: _fechaController,
                decoration: InputDecoration(
                  labelText: 'Fecha (YYYY-MM-DD HH:MM:SS)',
                  border: OutlineInputBorder(),
                  prefixIcon: Icon(Icons.date_range),
                ),
                validator: (value) =>
                    value == null || value.isEmpty ? 'Ingrese la fecha' : null,
              ),
              const SizedBox(height: 16),
              TextFormField(
                controller: _idUnidadController,
                keyboardType: TextInputType.number,
                decoration: InputDecoration(
                  labelText: 'ID Unidad',
                  border: OutlineInputBorder(),
                  prefixIcon: Icon(Icons.directions_bus),
                ),
                validator: (value) => value == null || value.isEmpty
                    ? 'Ingrese el ID Unidad'
                    : null,
              ),
              const SizedBox(height: 24),
              SizedBox(
                width: double.infinity,
                child: ElevatedButton(
                  onPressed: _loading ? null : _agendarMantenimiento,
                  child: _loading
                      ? SizedBox(
                          width: 20,
                          height: 20,
                          child: CircularProgressIndicator(
                              strokeWidth: 2, color: Colors.white),
                        )
                      : Text('Agendar Mantenimiento'),
                  style: ElevatedButton.styleFrom(
                    backgroundColor: AgendarMantenimientoScreen.primaryColor,
                    foregroundColor: Colors.white,
                    padding: EdgeInsets.symmetric(vertical: 14),
                    shape: RoundedRectangleBorder(
                      borderRadius: BorderRadius.circular(12),
                    ),
                  ),
                ),
              ),
              if (_response != null) ...[
                const SizedBox(height: 24),
                Card(
                  color: Colors.green[50],
                  elevation: 0,
                  shape: RoundedRectangleBorder(
                    borderRadius: BorderRadius.circular(12),
                  ),
                  child: Padding(
                    padding: const EdgeInsets.all(16.0),
                    child: Row(
                      children: [
                        Icon(Icons.check_circle, color: Colors.green[700]),
                        const SizedBox(width: 12),
                        Expanded(
                            child: Text(_response!,
                                style: TextStyle(
                                    color: Colors.green[900],
                                    fontWeight: FontWeight.bold))),
                      ],
                    ),
                  ),
                ),
              ],
              if (_error != null) ...[
                const SizedBox(height: 24),
                Card(
                  color: Colors.red[50],
                  elevation: 0,
                  shape: RoundedRectangleBorder(
                    borderRadius: BorderRadius.circular(12),
                  ),
                  child: Padding(
                    padding: const EdgeInsets.all(16.0),
                    child: Row(
                      children: [
                        Icon(Icons.error, color: Colors.red[700]),
                        const SizedBox(width: 12),
                        Expanded(
                            child: Text(_error!,
                                style: TextStyle(
                                    color: Colors.red[900],
                                    fontWeight: FontWeight.bold))),
                      ],
                    ),
                  ),
                ),
              ],
            ],
          ),
        ),
      ),
    );
  }
}

// Nueva pantalla para leer mantenimientos
class LeerMantenimientosWidget extends StatefulWidget {
  final String token;
  const LeerMantenimientosWidget({Key? key, required this.token})
      : super(key: key);
  @override
  State<LeerMantenimientosWidget> createState() =>
      _LeerMantenimientosWidgetState();
}

class _LeerMantenimientosWidgetState extends State<LeerMantenimientosWidget> {
  bool _loading = true;
  String? _error;
  List<dynamic> _mantenimientos = [];
  @override
  void initState() {
    super.initState();
    _fetch();
  }

  Future<void> _fetch() async {
    setState(() {
      _loading = true;
      _error = null;
    });
    try {
      final response = await http.get(
        Uri.parse('${AppConfig.baseUrl}/maintainance/listar'),
        headers: {
          'Authorization': 'Bearer ${widget.token}',
          'accept': 'application/json'
        },
      );
      if (response.statusCode == 200) {
        setState(() {
          _mantenimientos = json.decode(response.body);
        });
      } else {
        setState(() {
          _error = 'No se pudo obtener la lista.';
        });
      }
    } catch (e) {
      setState(() {
        _error = 'Error de conexión.';
      });
    } finally {
      setState(() {
        _loading = false;
      });
    }
  }

  @override
  Widget build(BuildContext context) {
    return SizedBox(
      width: 500,
      child: Padding(
        padding: const EdgeInsets.all(24),
        child: _loading
            ? Center(child: CircularProgressIndicator())
            : _error != null
                ? Center(
                    child: Text(_error!, style: TextStyle(color: Colors.red)))
                : _mantenimientos.isEmpty
                    ? const Center(child: Text('No hay mantenimientos.'))
                    : ListView.separated(
                        shrinkWrap: true,
                        itemCount: _mantenimientos.length,
                        separatorBuilder: (_, __) => Divider(),
                        itemBuilder: (_, i) {
                          final m = _mantenimientos[i];
                          return ListTile(
                            title:
                                Text('ID: \\${m['ID']} - Tipo: \\${m['type']}'),
                            subtitle: Text(
                                'Fecha: \\${m['fecha']} | Unidad: \\${m['idunidad']} | Estado: \\${m['id_status']}'),
                          );
                        },
                      ),
      ),
    );
  }
}

// Nueva pantalla para actualizar mantenimiento
class ActualizarMantenimientoWidget extends StatefulWidget {
  final String token;
  const ActualizarMantenimientoWidget({Key? key, required this.token})
      : super(key: key);
  @override
  State<ActualizarMantenimientoWidget> createState() =>
      _ActualizarMantenimientoWidgetState();
}

class _ActualizarMantenimientoWidgetState
    extends State<ActualizarMantenimientoWidget> {
  final _formKey = GlobalKey<FormState>();
  final _idController = TextEditingController();
  final _idStatusController = TextEditingController();
  final _typeController = TextEditingController();
  final _fechaController = TextEditingController();
  final _idUnidadController = TextEditingController();
  bool _loading = false;
  String? _response;
  String? _error;
  Future<void> _actualizar() async {
    if (!_formKey.currentState!.validate()) return;
    setState(() {
      _loading = true;
      _response = null;
      _error = null;
    });
    try {
      final response = await http.post(
        Uri.parse('${AppConfig.baseUrl}/maintainance/update'),
        headers: {
          'Authorization': 'Bearer ${widget.token}',
          'accept': 'application/json',
          'Content-Type': 'application/x-www-form-urlencoded'
        },
        body: {
          'ID': _idController.text.trim(),
          'id_status': _idStatusController.text.trim(),
          'type': _typeController.text.trim(),
          'fecha': _fechaController.text.trim(),
          'idunidad': _idUnidadController.text.trim(),
        },
      );
      if (response.statusCode == 200) {
        setState(() {
          _response = 'Mantenimiento actualizado exitosamente.';
        });
      } else {
        setState(() {
          _error = 'No se pudo actualizar. (${response.body})';
        });
      }
    } catch (e) {
      setState(() {
        _error = 'Error de conexión.';
      });
    } finally {
      setState(() {
        _loading = false;
      });
    }
  }

  @override
  Widget build(BuildContext context) {
    return SizedBox(
      width: 400,
      child: Padding(
        padding: const EdgeInsets.all(24),
        child: Form(
          key: _formKey,
          child: Column(
            mainAxisSize: MainAxisSize.min,
            children: [
              Text('Actualizar Mantenimiento',
                  style: TextStyle(fontWeight: FontWeight.bold, fontSize: 18)),
              const SizedBox(height: 16),
              TextFormField(
                controller: _idController,
                keyboardType: TextInputType.number,
                decoration: InputDecoration(labelText: 'ID'),
                validator: (v) =>
                    v == null || v.isEmpty ? 'Ingrese el ID' : null,
              ),
              const SizedBox(height: 8),
              TextFormField(
                controller: _idStatusController,
                keyboardType: TextInputType.number,
                decoration: InputDecoration(labelText: 'ID Status'),
                validator: (v) =>
                    v == null || v.isEmpty ? 'Ingrese el ID Status' : null,
              ),
              const SizedBox(height: 8),
              TextFormField(
                controller: _typeController,
                decoration: InputDecoration(labelText: 'Tipo de Mantenimiento'),
                validator: (v) =>
                    v == null || v.isEmpty ? 'Ingrese el tipo' : null,
              ),
              const SizedBox(height: 8),
              TextFormField(
                controller: _fechaController,
                decoration:
                    InputDecoration(labelText: 'Fecha (YYYY-MM-DD HH:MM:SS)'),
                validator: (v) =>
                    v == null || v.isEmpty ? 'Ingrese la fecha' : null,
              ),
              const SizedBox(height: 8),
              TextFormField(
                controller: _idUnidadController,
                keyboardType: TextInputType.number,
                decoration: InputDecoration(labelText: 'ID Unidad'),
                validator: (v) =>
                    v == null || v.isEmpty ? 'Ingrese el ID Unidad' : null,
              ),
              const SizedBox(height: 16),
              SizedBox(
                width: double.infinity,
                child: ElevatedButton(
                  onPressed: _loading ? null : _actualizar,
                  child: _loading
                      ? SizedBox(
                          width: 20,
                          height: 20,
                          child: CircularProgressIndicator(
                              strokeWidth: 2, color: Colors.white))
                      : Text('Actualizar'),
                ),
              ),
              if (_response != null) ...[
                const SizedBox(height: 16),
                Text(_response!, style: TextStyle(color: Colors.green)),
              ],
              if (_error != null) ...[
                const SizedBox(height: 16),
                Text(_error!, style: TextStyle(color: Colors.red)),
              ],
            ],
          ),
        ),
      ),
    );
  }
}

// Nueva pantalla para eliminar mantenimiento
class EliminarMantenimientoWidget extends StatefulWidget {
  final String token;
  const EliminarMantenimientoWidget({Key? key, required this.token})
      : super(key: key);
  @override
  State<EliminarMantenimientoWidget> createState() =>
      _EliminarMantenimientoWidgetState();
}

class _EliminarMantenimientoWidgetState
    extends State<EliminarMantenimientoWidget> {
  final _formKey = GlobalKey<FormState>();
  final _idController = TextEditingController();
  bool _loading = false;
  String? _response;
  String? _error;
  Future<void> _eliminar() async {
    if (!_formKey.currentState!.validate()) return;
    setState(() {
      _loading = true;
      _response = null;
      _error = null;
    });
    try {
      final response = await http.post(
        Uri.parse('${AppConfig.baseUrl}/maintainance/delete'),
        headers: {
          'Authorization': 'Bearer ${widget.token}',
          'accept': 'application/json',
          'Content-Type': 'application/x-www-form-urlencoded'
        },
        body: {'ID': _idController.text.trim()},
      );
      if (response.statusCode == 200) {
        setState(() {
          _response = 'Mantenimiento eliminado exitosamente.';
        });
      } else {
        setState(() {
          _error = 'No se pudo eliminar. (${response.body})';
        });
      }
    } catch (e) {
      setState(() {
        _error = 'Error de conexión.';
      });
    } finally {
      setState(() {
        _loading = false;
      });
    }
  }

  @override
  Widget build(BuildContext context) {
    return SizedBox(
      width: 350,
      child: Padding(
        padding: const EdgeInsets.all(24),
        child: Form(
          key: _formKey,
          child: Column(
            mainAxisSize: MainAxisSize.min,
            children: [
              Text('Eliminar Mantenimiento',
                  style: TextStyle(fontWeight: FontWeight.bold, fontSize: 18)),
              const SizedBox(height: 16),
              TextFormField(
                controller: _idController,
                keyboardType: TextInputType.number,
                decoration: InputDecoration(labelText: 'ID'),
                validator: (v) =>
                    v == null || v.isEmpty ? 'Ingrese el ID' : null,
              ),
              const SizedBox(height: 16),
              SizedBox(
                width: double.infinity,
                child: ElevatedButton(
                  onPressed: _loading ? null : _eliminar,
                  child: _loading
                      ? SizedBox(
                          width: 20,
                          height: 20,
                          child: CircularProgressIndicator(
                              strokeWidth: 2, color: Colors.white))
                      : Text('Eliminar'),
                  style: ElevatedButton.styleFrom(backgroundColor: Colors.red),
                ),
              ),
              if (_response != null) ...[
                const SizedBox(height: 16),
                Text(_response!, style: TextStyle(color: Colors.green)),
              ],
              if (_error != null) ...[
                const SizedBox(height: 16),
                Text(_error!, style: TextStyle(color: Colors.red)),
              ],
            ],
          ),
        ),
      ),
    );
  }
}

// Widget para crear unidad de transporte
class CrearUnidadWidget extends StatefulWidget {
  final String token;
  final VoidCallback onCreated;
  const CrearUnidadWidget({required this.token, required this.onCreated, Key? key}) : super(key: key);

  @override
  State<CrearUnidadWidget> createState() => _CrearUnidadWidgetState();
}

class _CrearUnidadWidgetState extends State<CrearUnidadWidget> {
  final _formKey = GlobalKey<FormState>();
  final _idController = TextEditingController(); // <-- Nuevo controlador para ID
  final _ubicacionController = TextEditingController();
  final _capacidadController = TextEditingController();
  final _rutaController = TextEditingController();
  final _tipoController = TextEditingController();
  bool _loading = false;
  String? _error;

  Future<void> _submit() async {
    if (!_formKey.currentState!.validate()) return;
    setState(() => _loading = true);
    final data = {
      'ID': _idController.text.trim(), // <-- Incluye el ID manual
      'Ubicacion': _ubicacionController.text.trim(),
      'Capacidad': _capacidadController.text.trim(),
      'IDRuta': _rutaController.text.trim(),
      'IDTipo': _tipoController.text.trim(),
    };
    final response = await http.post(
      Uri.parse('${AppConfig.baseUrl}/transport_units/create'),
      headers: {
        'Authorization': 'Bearer ${widget.token}',
        'accept': 'application/json',
        'Content-Type': 'application/x-www-form-urlencoded',
      },
      body: data,
    );
    setState(() => _loading = false);
    if (response.statusCode == 200 || response.statusCode == 201) {
      widget.onCreated();
    } else {
      setState(() => _error = 'No se pudo crear la unidad.');
    }
  }

  @override
  Widget build(BuildContext context) {
    return Padding(
      padding: const EdgeInsets.all(24),
      child: Form(
        key: _formKey,
        child: Column(
          mainAxisSize: MainAxisSize.min,
          children: [
            Text('Crear Unidad de Transporte', style: TextStyle(fontWeight: FontWeight.bold, fontSize: 18)),
            const SizedBox(height: 16),
            TextFormField(
              controller: _idController,
              decoration: InputDecoration(labelText: 'ID'),
              keyboardType: TextInputType.number,
              validator: (v) => v == null || v.isEmpty ? 'Ingrese el ID' : null,
            ),
            const SizedBox(height: 8),
            TextFormField(
              controller: _ubicacionController,
              decoration: InputDecoration(labelText: 'Ubicación'),
              validator: (v) => v == null || v.isEmpty ? 'Ingrese la ubicación' : null,
            ),
            const SizedBox(height: 8),
            TextFormField(
              controller: _capacidadController,
              decoration: InputDecoration(labelText: 'Capacidad'),
              keyboardType: TextInputType.number,
              validator: (v) => v == null || v.isEmpty ? 'Ingrese la capacidad' : null,
            ),
            const SizedBox(height: 8),
            TextFormField(
              controller: _rutaController,
              decoration: InputDecoration(labelText: 'ID Ruta'),
              keyboardType: TextInputType.number,
              validator: (v) => v == null || v.isEmpty ? 'Ingrese el ID de ruta' : null,
            ),
            const SizedBox(height: 8),
            TextFormField(
              controller: _tipoController,
              decoration: InputDecoration(labelText: 'ID Tipo'),
              keyboardType: TextInputType.number,
              validator: (v) => v == null || v.isEmpty ? 'Ingrese el ID de tipo' : null,
            ),
            const SizedBox(height: 16),
            SizedBox(
              width: double.infinity,
              child: ElevatedButton(
                onPressed: _loading ? null : _submit,
                child: _loading
                    ? SizedBox(width: 20, height: 20, child: CircularProgressIndicator(strokeWidth: 2, color: Colors.white))
                    : Text('Crear'),
              ),
            ),
            if (_error != null) ...[
              const SizedBox(height: 8),
              Text(_error!, style: TextStyle(color: Colors.red)),
            ],
          ],
        ),
      ),
    );
  }
}

// Widget para editar unidad de transporte
class EditarUnidadWidget extends StatefulWidget {
  final String token;
  final Map<String, dynamic> unidad;
  final VoidCallback onUpdated;
  const EditarUnidadWidget({required this.token, required this.unidad, required this.onUpdated, Key? key}) : super(key: key);

  @override
  State<EditarUnidadWidget> createState() => _EditarUnidadWidgetState();
}

class _EditarUnidadWidgetState extends State<EditarUnidadWidget> {
  final _formKey = GlobalKey<FormState>();
  late TextEditingController _idController;
  late TextEditingController _ubicacionController;
  late TextEditingController _capacidadController;
  late TextEditingController _rutaController;
  late TextEditingController _tipoController;
  bool _loading = false;
  String? _error;

  @override
  void initState() {
    super.initState();
    _idController = TextEditingController(text: widget.unidad['ID']?.toString() ?? '');
    _ubicacionController = TextEditingController(text: widget.unidad['Ubicacion']?.toString() ?? '');
    _capacidadController = TextEditingController(text: widget.unidad['Capacidad']?.toString() ?? '');
    _rutaController = TextEditingController(text: widget.unidad['IDRuta']?.toString() ?? '');
    _tipoController = TextEditingController(text: widget.unidad['IDTipo']?.toString() ?? '');
  }

  Future<void> _submit() async {
    if (!_formKey.currentState!.validate()) return;
    setState(() => _loading = true);
    final data = {
      'ID': _idController.text.trim(),
      'Ubicacion': _ubicacionController.text.trim(),
      'Capacidad': _capacidadController.text.trim(),
      'IDRuta': _rutaController.text.trim(),
      'IDTipo': _tipoController.text.trim(),
    };
    final response = await http.post(
      Uri.parse('${AppConfig.baseUrl}/transport_units/update'),
      headers: {
        'Authorization': 'Bearer ${widget.token}',
        'accept': 'application/json',
        'Content-Type': 'application/x-www-form-urlencoded',
      },
      body: data,
    );
    setState(() => _loading = false);
    if (response.statusCode == 200) {
      widget.onUpdated();
      Navigator.pop(context);
    } else {
      setState(() => _error = 'No se pudo actualizar la unidad.');
    }
  }

  @override
  Widget build(BuildContext context) {
    return Padding(
      padding: const EdgeInsets.all(24),
      child: Form(
        key: _formKey,
        child: Column(
          mainAxisSize: MainAxisSize.min,
          children: [
            Text('Editar Unidad de Transporte', style: TextStyle(fontWeight: FontWeight.bold, fontSize: 18)),
            const SizedBox(height: 16),
            TextFormField(
              controller: _idController,
              decoration: InputDecoration(labelText: 'ID'),
              enabled: false,
            ),
            const SizedBox(height: 8),
            TextFormField(
              controller: _ubicacionController,
              decoration: InputDecoration(labelText: 'Ubicación'),
              validator: (v) => v == null || v.isEmpty ? 'Ingrese la ubicación' : null,
            ),
            const SizedBox(height: 8),
            TextFormField(
              controller: _capacidadController,
              decoration: InputDecoration(labelText: 'Capacidad'),
              keyboardType: TextInputType.number,
              validator: (v) => v == null || v.isEmpty ? 'Ingrese la capacidad' : null,
            ),
            const SizedBox(height: 8),
            TextFormField(
              controller: _rutaController,
              decoration: InputDecoration(labelText: 'ID Ruta'),
              keyboardType: TextInputType.number,
              validator: (v) => v == null || v.isEmpty ? 'Ingrese el ID de ruta' : null,
            ),
            const SizedBox(height: 8),
            TextFormField(
              controller: _tipoController,
              decoration: InputDecoration(labelText: 'ID Tipo'),
              keyboardType: TextInputType.number,
              validator: (v) => v == null || v.isEmpty ? 'Ingrese el ID de tipo' : null,
            ),
            const SizedBox(height: 16),
            SizedBox(
              width: double.infinity,
              child: ElevatedButton(
                onPressed: _loading ? null : _submit,
                child: _loading
                    ? SizedBox(width: 20, height: 20, child: CircularProgressIndicator(strokeWidth: 2, color: Colors.white))
                    : Text('Actualizar'),
              ),
            ),
            if (_error != null) ...[
              const SizedBox(height: 8),
              Text(_error!, style: TextStyle(color: Colors.red)),
            ],
          ],
        ),
      ),
    );
  }
}

// Widgets auxiliares para CRUD de Horarios

enum HorarioFormMode { create, update }

class _HorarioFormWidget extends StatefulWidget {
  final String token;
  final HorarioFormMode mode;
  final VoidCallback onSuccess;
  const _HorarioFormWidget({
    required this.token,
    required this.mode,
    required this.onSuccess,
    Key? key,
  }) : super(key: key);

  @override
  State<_HorarioFormWidget> createState() => _HorarioFormWidgetState();
}

class _HorarioFormWidgetState extends State<_HorarioFormWidget> {
  final _formKey = GlobalKey<FormState>();
  final _idController = TextEditingController();
  final _llegadaController = TextEditingController();
  final _salidaController = TextEditingController();
  bool _loading = false;
  String? _error;
  String? _success;

  Future<void> _submit() async {
    if (!_formKey.currentState!.validate()) return;
    setState(() {
      _loading = true;
      _error = null;
      _success = null;
    });
    final data = {
      'id': _idController.text.trim(),
      'Llegada': _llegadaController.text.trim(),
      'Salida': _salidaController.text.trim(),
    };
    final url = widget.mode == HorarioFormMode.create
        ? '${AppConfig.baseUrl}/schedules/create'
        : '${AppConfig.baseUrl}/schedules/update';
    final response = await http.post(
      Uri.parse(url),
      headers: {
        'Authorization': 'Bearer ${widget.token}',
        'accept': 'application/json',
        'Content-Type': 'application/x-www-form-urlencoded',
      },
      body: data,
    );
    setState(() => _loading = false);
    if (response.statusCode == 200 || response.statusCode == 201) {
      setState(() => _success = widget.mode == HorarioFormMode.create
          ? 'Horario creado exitosamente.'
          : 'Horario actualizado exitosamente.');
      widget.onSuccess();
    } else {
      setState(() => _error = 'Error: ${response.body}');
    }
  }

  @override
  Widget build(BuildContext context) {
    return SizedBox(
      width: 350,
      child: Form(
        key: _formKey,
        child: Column(
          mainAxisSize: MainAxisSize.min,
          children: [
            Text(
              widget.mode == HorarioFormMode.create
                  ? 'Añadir Horario'
                  : 'Actualizar Horario',
              style: TextStyle(fontWeight: FontWeight.bold, fontSize: 18),
            ),
            const SizedBox(height: 16),
            TextFormField(
              controller: _idController,
              decoration: InputDecoration(labelText: 'ID'),
              keyboardType: TextInputType.number,
              validator: (v) =>
                  v == null || v.isEmpty ? 'Ingrese el ID' : null,
              enabled: widget.mode == HorarioFormMode.create,
            ),
            const SizedBox(height: 8),
            TextFormField(
              controller: _llegadaController,
              decoration: InputDecoration(labelText: 'Llegada'),
              validator: (v) =>
                  v == null || v.isEmpty ? 'Ingrese la llegada' : null,
            ),
            const SizedBox(height: 8),
            TextFormField(
              controller: _salidaController,
              decoration: InputDecoration(labelText: 'Salida'),
              validator: (v) =>
                  v == null || v.isEmpty ? 'Ingrese la salida' : null,
            ),
            const SizedBox(height: 16),
            SizedBox(
              width: double.infinity,
              child: ElevatedButton(
                onPressed: _loading ? null : _submit,
                child: _loading
                    ? SizedBox(
                        width: 20,
                        height: 20,
                        child: CircularProgressIndicator(
                            strokeWidth: 2, color: Colors.white))
                    : Text(widget.mode == HorarioFormMode.create
                        ? 'Crear'
                        : 'Actualizar'),
              ),
            ),
            if (_success != null) ...[
              const SizedBox(height: 8),
              Text(_success!, style: TextStyle(color: Colors.green)),
            ],
            if (_error != null) ...[
              const SizedBox(height: 8),
              Text(_error!, style: TextStyle(color: Colors.red)),
            ],
          ],
        ),
      ),
    );
  }
}

class _HorarioListWidget extends StatelessWidget {
  final String token;
  const _HorarioListWidget({required this.token, Key? key}) : super(key: key);

  Future<List<dynamic>> fetchHorarios() async {
    final response = await http.get(
      Uri.parse('${AppConfig.baseUrl}/schedules/'),
      headers: {
        'Authorization': 'Bearer $token',
        'accept': 'application/json',
      },
    );
    if (response.statusCode == 200) {
      return json.decode(response.body);
    } else {
      throw Exception('Error al cargar horarios');
    }
  }

  @override
  Widget build(BuildContext context) {
    return SizedBox(
      width: 400,
      child: FutureBuilder<List<dynamic>>(
        future: fetchHorarios(),
        builder: (context, snapshot) {
          if (snapshot.connectionState == ConnectionState.waiting) {
            return Center(child: CircularProgressIndicator());
          } else if (snapshot.hasError) {
            return Center(child: Text('Error al cargar horarios'));
          } else if (!snapshot.hasData || snapshot.data!.isEmpty) {
            return Center(child: Text('No hay horarios registrados.'));
          }
          final horarios = snapshot.data!;
          return ListView.separated(
            shrinkWrap: true,
            itemCount: horarios.length,
            separatorBuilder: (_, __) => Divider(),
            itemBuilder: (_, i) {
              final h = horarios[i];
              return ListTile(
                title: Text('ID: ${h['ID']}'),
                subtitle: Text('Llegada: ${h['Llegada']} | Salida: ${h['Salida']}'),
              );
            },
          );
        },
      ),
    );
  }
}

class _HorarioDeleteWidget extends StatefulWidget {
  final String token;
  final VoidCallback onSuccess;
  const _HorarioDeleteWidget({required this.token, required this.onSuccess, Key? key}) : super(key: key);

  @override
  State<_HorarioDeleteWidget> createState() => _HorarioDeleteWidgetState();
}

class _HorarioDeleteWidgetState extends State<_HorarioDeleteWidget> {
  final _formKey = GlobalKey<FormState>();
  final _idController = TextEditingController();
  bool _loading = false;
  String? _error;
  String? _success;

  Future<void> _delete() async {
    if (!_formKey.currentState!.validate()) return;
    setState(() {
      _loading = true;
      _error = null;
      _success = null;
    });
    final response = await http.post(
      Uri.parse('${AppConfig.baseUrl}/schedules/delete'),
      headers: {
        'Authorization': 'Bearer ${widget.token}',
        'accept': 'application/json',
        'Content-Type': 'application/x-www-form-urlencoded',
      },
      body: {'id': _idController.text.trim()},
    );
    setState(() => _loading = false);
    if (response.statusCode == 200) {
      setState(() => _success = 'Horario eliminado exitosamente.');
      widget.onSuccess();
    } else {
      setState(() => _error = 'Error: ${response.body}');
    }
  }

  @override
  Widget build(BuildContext context) {
    return SizedBox(
      width: 300,
      child: Form(
        key: _formKey,
        child: Column(
          mainAxisSize: MainAxisSize.min,
          children: [
            Text('Eliminar Horario', style: TextStyle(fontWeight: FontWeight.bold, fontSize: 18)),
            const SizedBox(height: 16),
            TextFormField(
              controller: _idController,
              decoration: InputDecoration(labelText: 'ID'),
              keyboardType: TextInputType.number,
              validator: (v) => v == null || v.isEmpty ? 'Ingrese el ID' : null,
            ),
            const SizedBox(height: 16),
            SizedBox(
              width: double.infinity,
              child: ElevatedButton(
                onPressed: _loading ? null : _delete,
                child: _loading
                    ? SizedBox(width: 20, height: 20, child: CircularProgressIndicator(strokeWidth: 2, color: Colors.white))
                    : Text('Eliminar'),
                style: ElevatedButton.styleFrom(backgroundColor: Colors.red),
              ),
            ),
            if (_success != null) ...[
              const SizedBox(height: 8),
              Text(_success!, style: TextStyle(color: Colors.green)),
            ],
            if (_error != null) ...[
              const SizedBox(height: 8),
              Text(_error!, style: TextStyle(color: Colors.red)),
            ],
          ],
        ),
      ),
    );
  }
}

// Widgets auxiliares para CRUD de Rutas

enum RutaFormMode { create, update }

class _RutaFormWidget extends StatefulWidget {
  final String token;
  final RutaFormMode mode;
  final VoidCallback onSuccess;
  const _RutaFormWidget({
    required this.token,
    required this.mode,
    required this.onSuccess,
    Key? key,
  }) : super(key: key);

  @override
  State<_RutaFormWidget> createState() => _RutaFormWidgetState();
}

class _RutaFormWidgetState extends State<_RutaFormWidget> {
  final _formKey = GlobalKey<FormState>();
  final _idController = TextEditingController();
  final _idHorarioController = TextEditingController();
  final _nombreController = TextEditingController();
  bool _loading = false;
  String? _error;
  String? _success;

  Future<void> _submit() async {
    if (!_formKey.currentState!.validate()) return;
    setState(() {
      _loading = true;
      _error = null;
      _success = null;
    });
    final data = {
      'ID': _idController.text.trim(),
      'IDHorario': _idHorarioController.text.trim(),
      'Nombre': _nombreController.text.trim(),
    };
    final url = widget.mode == RutaFormMode.create
        ? '${AppConfig.baseUrl}/routes/create'
        : '${AppConfig.baseUrl}/routes/update';
    final response = await http.post(
      Uri.parse(url),
      headers: {
        'Authorization': 'Bearer ${widget.token}',
        'accept': 'application/json',
        'Content-Type': 'application/x-www-form-urlencoded',
      },
      body: data,
    );
    setState(() => _loading = false);
    if (response.statusCode == 200 || response.statusCode == 201) {
      setState(() => _success = widget.mode == RutaFormMode.create
          ? 'Ruta creada exitosamente.'
          : 'Ruta actualizada exitosamente.');
      widget.onSuccess();
    } else {
      setState(() => _error = 'Error: ${response.body}');
    }
  }

  @override
  Widget build(BuildContext context) {
    return SizedBox(
      width: 350,
      child: Form(
        key: _formKey,
        child: Column(
          mainAxisSize: MainAxisSize.min,
          children: [
            Text(
              widget.mode == RutaFormMode.create
                  ? 'Añadir Ruta'
                  : 'Actualizar Ruta',
              style: TextStyle(fontWeight: FontWeight.bold, fontSize: 18),
            ),
            const SizedBox(height: 16),
            TextFormField(
              controller: _idController,
              decoration: InputDecoration(labelText: 'ID'),
              keyboardType: TextInputType.number,
              validator: (v) =>
                  v == null || v.isEmpty ? 'Ingrese el ID' : null,
              enabled: widget.mode == RutaFormMode.create,
            ),
            const SizedBox(height: 8),
            TextFormField(
              controller: _idHorarioController,
              decoration: InputDecoration(labelText: 'ID Horario'),
              keyboardType: TextInputType.number,
              validator: (v) =>
                  v == null || v.isEmpty ? 'Ingrese el ID Horario' : null,
            ),
            const SizedBox(height: 8),
            TextFormField(
              controller: _nombreController,
              decoration: InputDecoration(labelText: 'Nombre'),
              validator: (v) =>
                  v == null || v.isEmpty ? 'Ingrese el nombre' : null,
            ),
            const SizedBox(height: 16),
            SizedBox(
              width: double.infinity,
              child: ElevatedButton(
                onPressed: _loading ? null : _submit,
                child: _loading
                    ? SizedBox(
                        width: 20,
                        height: 20,
                        child: CircularProgressIndicator(
                            strokeWidth: 2, color: Colors.white))
                    : Text(widget.mode == RutaFormMode.create
                        ? 'Crear'
                        : 'Actualizar'),
              ),
            ),
            if (_success != null) ...[
              const SizedBox(height: 8),
              Text(_success!, style: TextStyle(color: Colors.green)),
            ],
            if (_error != null) ...[
              const SizedBox(height: 8),
              Text(_error!, style: TextStyle(color: Colors.red)),
            ],
          ],
        ),
      ),
    );
  }
}

class _RutaListWidget extends StatelessWidget {
  final String token;
  const _RutaListWidget({required this.token, Key? key}) : super(key: key);

  Future<List<dynamic>> fetchRutas() async {
    final response = await http.get(
      Uri.parse('${AppConfig.baseUrl}/routes/'),
      headers: {
        'Authorization': 'Bearer $token',
        'accept': 'application/json',
      },
    );
    if (response.statusCode == 200) {
      return json.decode(response.body);
    } else {
      throw Exception('Error al cargar rutas');
    }
  }

  @override
  Widget build(BuildContext context) {
    return SizedBox(
      width: 400,
      child: FutureBuilder<List<dynamic>>(
        future: fetchRutas(),
        builder: (context, snapshot) {
          if (snapshot.connectionState == ConnectionState.waiting) {
            return Center(child: CircularProgressIndicator());
          } else if (snapshot.hasError) {
            return Center(child: Text('Error al cargar rutas'));
          } else if (!snapshot.hasData || snapshot.data!.isEmpty) {
            return Center(child: Text('No hay rutas registradas.'));
          }
          final rutas = snapshot.data!;
          return ListView.separated(
            shrinkWrap: true,
            itemCount: rutas.length,
            separatorBuilder: (_, __) => Divider(),
            itemBuilder: (_, i) {
              final r = rutas[i];
              return ListTile(
                title: Text('ID: ${r['ID']}'),
                subtitle: Text('Horario: ${r['IDHorario']} | Nombre: ${r['Nombre']}'),
              );
            },
          );
        },
      ),
    );
  }
}

class _RutaDeleteWidget extends StatefulWidget {
  final String token;
  final VoidCallback onSuccess;
  const _RutaDeleteWidget({required this.token, required this.onSuccess, Key? key}) : super(key: key);

  @override
  State<_RutaDeleteWidget> createState() => _RutaDeleteWidgetState();
}

class _RutaDeleteWidgetState extends State<_RutaDeleteWidget> {
  final _formKey = GlobalKey<FormState>();
  final _idController = TextEditingController();
  bool _loading = false;
  String? _error;
  String? _success;

  Future<void> _delete() async {
    if (!_formKey.currentState!.validate()) return;
    setState(() {
      _loading = true;
      _error = null;
      _success = null;
    });
    final response = await http.post(
      Uri.parse('${AppConfig.baseUrl}/routes/delete'),
      headers: {
        'Authorization': 'Bearer ${widget.token}',
        'accept': 'application/json',
        'Content-Type': 'application/x-www-form-urlencoded',
      },
      body: {'ID': _idController.text.trim()},
    );
    setState(() => _loading = false);
    if (response.statusCode == 200) {
      setState(() => _success = 'Ruta eliminada exitosamente.');
      widget.onSuccess();
    } else {
      setState(() => _error = 'Error: ${response.body}');
    }
  }

  @override
  Widget build(BuildContext context) {
    return SizedBox(
      width: 300,
      child: Form(
        key: _formKey,
        child: Column(
          mainAxisSize: MainAxisSize.min,
          children: [
            Text('Eliminar Ruta', style: TextStyle(fontWeight: FontWeight.bold, fontSize: 18)),
            const SizedBox(height: 16),
            TextFormField(
              controller: _idController,
              decoration: InputDecoration(labelText: 'ID'),
              keyboardType: TextInputType.number,
              validator: (v) => v == null || v.isEmpty ? 'Ingrese el ID' : null,
            ),
            const SizedBox(height: 16),
            SizedBox(
              width: double.infinity,
              child: ElevatedButton(
                onPressed: _loading ? null : _delete,
                child: _loading
                    ? SizedBox(width: 20, height: 20, child: CircularProgressIndicator(strokeWidth: 2, color: Colors.white))
                    : Text('Eliminar'),
                style: ElevatedButton.styleFrom(backgroundColor: Colors.red),
              ),
            ),
            if (_success != null) ...[
              const SizedBox(height: 8),
              Text(_success!, style: TextStyle(color: Colors.green)),
            ],
            if (_error != null) ...[
              const SizedBox(height: 8),
              Text(_error!, style: TextStyle(color: Colors.red)),
            ],
          ],
        ),
      ),
    );
  }
}
