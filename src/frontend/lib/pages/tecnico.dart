import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;
import 'dart:convert';
import 'package:flutter/services.dart';
import '../config/config.dart';

class TecnicoPanel extends StatelessWidget {
  final String token;

  const TecnicoPanel({Key? key, required this.token}) : super(key: key);

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

  Future<List<Map<String, dynamic>>> fetchItinerario() async {
    final response = await http.get(
      Uri.parse('${AppConfig.baseUrl}/schedules/'),
      headers: {
        'Authorization': 'Bearer $token',
        'accept': 'application/json',
      },
    );
    if (response.statusCode == 200) {
      final data = json.decode(response.body);
      if (data is List) {
        return List<Map<String, dynamic>>.from(data);
      }
      return [];
    } else {
      throw Exception('Error al cargar itinerario: ${response.body}');
    }
  }

  @override
  Widget build(BuildContext context) {
    // Estado para la sección seleccionada
    final ValueNotifier<String> selectedSection = ValueNotifier('dashboard');
    final ValueNotifier<List<List<dynamic>>> mantenimientosAtrasados =
        ValueNotifier([]);
    final ValueNotifier<List<List<dynamic>>> mantenimientosProximos =
        ValueNotifier([]);
    final ValueNotifier<bool> loadingAlertas = ValueNotifier(false);
    final ValueNotifier<String?> errorAlertas = ValueNotifier(null);

    void fetchAlertas() async {
      loadingAlertas.value = true;
      errorAlertas.value = null;
      try {
        final response = await http.get(
          Uri.parse('${AppConfig.baseUrl}/reporte/alert-tec'),
          headers: {
            'Authorization': 'Bearer $token',
            'accept': 'application/json',
          },
        );
        if (response.statusCode == 200) {
          final data = json.decode(response.body);
          // Adaptar para aceptar lista plana o lista de listas
          final atrasadosRaw = data['mantenimientos_atrasados'] as List?;
          final proximosRaw = data['mantenimientos_proximos'] as List?;
          if (atrasadosRaw != null &&
              atrasadosRaw.isNotEmpty &&
              atrasadosRaw[0] is! List) {
            mantenimientosAtrasados.value = [List<dynamic>.from(atrasadosRaw)];
          } else if (atrasadosRaw != null) {
            mantenimientosAtrasados.value = atrasadosRaw
                .map<List<dynamic>>((e) => List<dynamic>.from(e))
                .toList();
          } else {
            mantenimientosAtrasados.value = [];
          }
          if (proximosRaw != null &&
              proximosRaw.isNotEmpty &&
              proximosRaw[0] is! List) {
            mantenimientosProximos.value = [List<dynamic>.from(proximosRaw)];
          } else if (proximosRaw != null) {
            mantenimientosProximos.value = proximosRaw
                .map<List<dynamic>>((e) => List<dynamic>.from(e))
                .toList();
          } else {
            mantenimientosProximos.value = [];
          }
        } else {
          errorAlertas.value = 'No se pudo obtener las alertas.';
        }
      } catch (e) {
        errorAlertas.value = 'Error de conexión.';
      } finally {
        loadingAlertas.value = false;
      }
    }

    return Scaffold(
      appBar: AppBar(
        elevation: 0,
        backgroundColor: primaryColor,
        title: const Text('Panel de Técnico',
            style: TextStyle(fontWeight: FontWeight.w600)),
        actions: [
          IconButton(
              icon: const Icon(Icons.notifications_outlined), onPressed: () {}),
          IconButton(
              icon: const Icon(Icons.account_circle_outlined),
              onPressed: () {}),
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
                  CircularProgressIndicator(color: primaryColor),
                  const SizedBox(height: 16),
                  const Text('Cargando información...',
                      style: TextStyle(color: Color(0xFF5F6368))),
                ],
              ),
            );
          } else if (snapshot.hasError) {
            return Center(
              child: Column(
                mainAxisAlignment: MainAxisAlignment.center,
                children: [
                  const Icon(Icons.error_outline, color: Colors.red, size: 60),
                  const SizedBox(height: 16),
                  Text('Error: ${snapshot.error}',
                      style: const TextStyle(color: Colors.red)),
                ],
              ),
            );
          } else if (!snapshot.hasData) {
            return const Center(child: Text('Sin datos disponibles'));
          }

          final data = snapshot.data!;
          final user = data['user'] ?? {};
          final registrosMantenimiento =
              data['registros_mantenimiento']?.toString() ?? '0';
          final busesMantenimiento =
              data['buses_mantenimiento']?.toString() ?? '0';
          final proximoMantenimiento =
              data['proximo_mantenimiento']?.toString() ?? 'No disponible';

          return Row(
            children: [
              // Sidebar
              Container(
                width: 250,
                color: const Color(0xFFF8F9FA),
                child: Column(
                  children: [
                    // User profile section
                    Container(
                      padding: const EdgeInsets.symmetric(
                          vertical: 24, horizontal: 16),
                      color: primaryColor.withOpacity(0.05),
                      child: Row(
                        children: [
                          CircleAvatar(
                            backgroundColor: secondaryColor,
                            radius: 24,
                            child: Text(
                              user['Nombre']?.toString().substring(0, 1) ?? 'T',
                              style: const TextStyle(
                                  color: Colors.white,
                                  fontWeight: FontWeight.bold),
                            ),
                          ),
                          const SizedBox(width: 12),
                          Expanded(
                            child: Column(
                              crossAxisAlignment: CrossAxisAlignment.start,
                              children: [
                                Text(
                                  user['Nombre']?.toString() ?? 'Técnico',
                                  style: const TextStyle(
                                      fontWeight: FontWeight.bold,
                                      fontSize: 16),
                                  overflow: TextOverflow.ellipsis,
                                ),
                                const SizedBox(height: 4),
                                Container(
                                  padding: const EdgeInsets.symmetric(
                                      horizontal: 8, vertical: 2),
                                  decoration: BoxDecoration(
                                    color: secondaryColor,
                                    borderRadius: BorderRadius.circular(12),
                                  ),
                                  child: const Text('Técnico de Mantenimiento',
                                      style: TextStyle(
                                          color: Colors.white,
                                          fontSize: 10,
                                          fontWeight: FontWeight.w500)),
                                ),
                              ],
                            ),
                          ),
                        ],
                      ),
                    ),
                    const Divider(height: 1),
                    // Menu items
                    Expanded(
                      child: ValueListenableBuilder<String>(
                        valueListenable: selectedSection,
                        builder: (context, section, _) {
                          return ListView(
                            padding: EdgeInsets.zero,
                            children: [
                              _buildMenuItem(
                                icon: Icons.history,
                                title: 'Consultar historial de bus',
                                isActive: section == 'historial',
                                onTap: () =>
                                    selectedSection.value = 'historial',
                              ),
                              _buildMenuItem(
                                icon: Icons.event,
                                title: 'Itinerario',
                                isActive: section == 'itinerario',
                                onTap: () =>
                                    selectedSection.value = 'itinerario',
                              ),
                              _buildMenuItem(
                                icon: Icons.build_circle_outlined,
                                title: 'Registrar mantenimiento',
                                isActive: section == 'registrar',
                                onTap: () =>
                                    selectedSection.value = 'registrar',
                              ),
                              _buildMenuItem(
                                icon: Icons.warning_amber_outlined,
                                title: 'Alertas',
                                isActive: section == 'alertas',
                                onTap: () {
                                  selectedSection.value = 'alertas';
                                  fetchAlertas();
                                },
                              ),
                              _buildMenuItem(
                                icon: Icons.assignment_turned_in_outlined,
                                title: 'Marcar asistencia',
                                isActive: section == 'asistencia',
                                onTap: () =>
                                    selectedSection.value = 'asistencia',
                              ),
                            ],
                          );
                        },
                      ),
                    ),
                  ],
                ),
              ),
              // Main content
              Expanded(
                child: ValueListenableBuilder<String>(
                  valueListenable: selectedSection,
                  builder: (context, section, _) {
                    if (section == 'itinerario') {
                      // ITINERARIO: Mostrar los schedules
                      return FutureBuilder<List<Map<String, dynamic>>>(
                        future: fetchItinerario(),
                        builder: (context, snapshot) {
                          if (snapshot.connectionState == ConnectionState.waiting) {
                            return const Center(
                              child: CircularProgressIndicator(),
                            );
                          } else if (snapshot.hasError) {
                            return Center(
                              child: Text(
                                'Error al cargar el itinerario: ${snapshot.error}',
                                style: const TextStyle(color: Colors.red),
                              ),
                            );
                          } else if (!snapshot.hasData || snapshot.data!.isEmpty) {
                            return const Center(
                              child: Text('No hay itinerarios disponibles.'),
                            );
                          }
                          final itinerarios = snapshot.data!;
                          return SingleChildScrollView(
                            padding: const EdgeInsets.all(24),
                            child: Column(
                              crossAxisAlignment: CrossAxisAlignment.start,
                              children: [
                                const Text(
                                  'Itinerario de Buses',
                                  style: TextStyle(
                                    fontSize: 22,
                                    fontWeight: FontWeight.bold,
                                  ),
                                ),
                                const SizedBox(height: 24),
                                Container(
                                  decoration: BoxDecoration(
                                    color: Colors.white,
                                    borderRadius: BorderRadius.circular(16),
                                    boxShadow: [
                                      BoxShadow(
                                        color: Colors.black12,
                                        blurRadius: 8,
                                        offset: Offset(0, 2),
                                      ),
                                    ],
                                  ),
                                  child: DataTable(
                                    headingRowColor: MaterialStateProperty.all(
                                        primaryColor.withOpacity(0.1)),
                                    columns: const [
                                      DataColumn(label: Text('ID')),
                                      DataColumn(label: Text('Unidad')),
                                      DataColumn(label: Text('Ruta')),
                                      DataColumn(label: Text('Parada')),
                                      DataColumn(label: Text('Llegada')),
                                      DataColumn(label: Text('Salida')),
                                    ],
                                    rows: itinerarios.map((item) {
                                      return DataRow(
                                        cells: [
                                          DataCell(Text(item['ID']?.toString() ?? '-')),
                                          DataCell(Text(item['IDUnidad']?.toString() ?? '-')),
                                          DataCell(Text(item['IDRuta']?.toString() ?? '-')),
                                          DataCell(Text(item['IDParada']?.toString() ?? '-')),
                                          DataCell(Text(item['Llegada']?.toString() ?? '-')),
                                          DataCell(Text(item['Salida']?.toString() ?? '-')),
                                        ],
                                      );
                                    }).toList(),
                                  ),
                                ),
                              ],
                            ),
                          );
                        },
                      );
                    } else if (section == 'alertas') {
                      return ValueListenableBuilder<bool>(
                        valueListenable: loadingAlertas,
                        builder: (context, loading, _) {
                          if (loading) {
                            return const Center(
                                child: CircularProgressIndicator());
                          }
                          return ValueListenableBuilder<String?>(
                            valueListenable: errorAlertas,
                            builder: (context, error, _) {
                              if (error != null) {
                                return Center(
                                    child: Text(error,
                                        style: const TextStyle(
                                            color: Colors.red)));
                              }
                              return ValueListenableBuilder<
                                  List<List<dynamic>>>(
                                valueListenable: mantenimientosAtrasados,
                                builder: (context, atrasados, _) {
                                  return ValueListenableBuilder<
                                      List<List<dynamic>>>(
                                    valueListenable: mantenimientosProximos,
                                    builder: (context, proximos, _) {
                                      return buildAlertasSection(
                                          atrasados, proximos);
                                    },
                                  );
                                },
                              );
                            },
                          );
                        },
                      );
                    } else if (section == 'registrar') {
                      // Formulario de registrar mantenimiento (igual a admin)
                      return AgendarMantenimientoScreen(token: token);
                    } else {
                      // Dashboard por defecto
                      return SingleChildScrollView(
                        padding: const EdgeInsets.all(24),
                        child: Column(
                          crossAxisAlignment: CrossAxisAlignment.start,
                          children: [
                            // Header
                            Row(
                              children: [
                                const Icon(Icons.build,
                                    color: secondaryColor, size: 28),
                                const SizedBox(width: 12),
                                const Text('Panel de Mantenimiento',
                                    style: TextStyle(
                                        fontSize: 24,
                                        fontWeight: FontWeight.bold,
                                        color: Color(0xFF202124))),
                              ],
                            ),
                            const SizedBox(height: 8),
                            Text(
                                'Bienvenido, ${user['Nombre'] ?? 'Técnico'}. Aquí está el resumen de mantenimiento.',
                                style: const TextStyle(
                                    fontSize: 16, color: Color(0xFF5F6368))),
                            const SizedBox(height: 24),
                            // Stats cards
                            Row(
                              children: [
                                Expanded(
                                  child: _buildStatCard(
                                    title: 'Registros de Mantenimiento',
                                    value: '$registrosMantenimiento',
                                    icon: Icons.assignment,
                                    color: primaryColor,
                                  ),
                                ),
                                const SizedBox(width: 16),
                                Expanded(
                                  child: _buildStatCard(
                                    title: 'Buses en Mantenimiento',
                                    value: '$busesMantenimiento',
                                    icon: Icons.directions_bus,
                                    color: warningColor,
                                  ),
                                ),
                                const SizedBox(width: 16),
                                Expanded(
                                  child: _buildStatCard(
                                    title: 'Próximo Mantenimiento',
                                    value: proximoMantenimiento,
                                    icon: Icons.event,
                                    color: accentColor,
                                  ),
                                ),
                              ],
                            ),
                            const SizedBox(height: 24),
                          ],
                        ),
                      );
                    }
                  },
                ),
              ),
            ],
          );
        },
      ),
    );
  }

  Widget _buildMenuItem({
    required IconData icon,
    required String title,
    bool isActive = false,
    VoidCallback? onTap,
  }) {
    return ListTile(
      leading: Icon(icon,
          color: isActive ? secondaryColor : const Color(0xFF5F6368)),
      title: Text(
        title,
        style: TextStyle(
          fontSize: 14,
          fontWeight: isActive ? FontWeight.w600 : FontWeight.w500,
          color: isActive ? secondaryColor : const Color(0xFF202124),
        ),
      ),
      dense: true,
      horizontalTitleGap: 8,
      onTap: onTap,
      tileColor: isActive ? secondaryColor.withOpacity(0.1) : null,
      shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(8)),
    );
  }

  Widget buildAlertasSection(
      List<List<dynamic>> atrasados, List<List<dynamic>> proximos) {
    return SingleChildScrollView(
      padding: const EdgeInsets.all(24),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          const Text('Alertas de Mantenimiento',
              style: TextStyle(fontSize: 22, fontWeight: FontWeight.bold)),
          const SizedBox(height: 24),
          Card(
            color: warningColor.withOpacity(0.1),
            shape:
                RoundedRectangleBorder(borderRadius: BorderRadius.circular(12)),
            child: Padding(
              padding: const EdgeInsets.all(20),
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  const Text('Mantenimientos Atrasados',
                      style: TextStyle(
                          fontWeight: FontWeight.bold,
                          fontSize: 18,
                          color: warningColor)),
                  const SizedBox(height: 12),
                  if (atrasados.isEmpty)
                    const Text('No hay mantenimientos atrasados.')
                  else
                    ...atrasados.map((m) => Padding(
                          padding: const EdgeInsets.symmetric(vertical: 6.0),
                          child: Column(
                            crossAxisAlignment: CrossAxisAlignment.start,
                            children: [
                              Text(
                                  'ID: ${m[0]} | Unidad: ${m[1]} | Desc: ${m[2]} | Fecha: ${m[3]} | Técnico: ${m[4]}'),
                            ],
                          ),
                        )),
                ],
              ),
            ),
          ),
          const SizedBox(height: 16),
          Card(
            color: accentColor.withOpacity(0.1),
            shape:
                RoundedRectangleBorder(borderRadius: BorderRadius.circular(12)),
            child: Padding(
              padding: const EdgeInsets.all(20),
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  const Text('Mantenimientos Próximos',
                      style: TextStyle(
                          fontWeight: FontWeight.bold,
                          fontSize: 18,
                          color: accentColor)),
                  const SizedBox(height: 12),
                  if (proximos.isEmpty)
                    const Text('No hay mantenimientos próximos.')
                  else
                    ...proximos.map((m) => Padding(
                          padding: const EdgeInsets.symmetric(vertical: 6.0),
                          child: Column(
                            crossAxisAlignment: CrossAxisAlignment.start,
                            children: [
                              Text(
                                  'ID: ${m[0]} | Unidad: ${m[1]} | Desc: ${m[2]} | Fecha: ${m[3]} | Técnico: ${m[4]}'),
                            ],
                          ),
                        )),
                ],
              ),
            ),
          ),
        ],
      ),
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
        side: BorderSide(color: color.withOpacity(0.1)),
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
                Text(title,
                    style: TextStyle(
                        fontSize: 14,
                        fontWeight: FontWeight.w500,
                        color: color)),
                Container(
                  width: 40,
                  height: 40,
                  decoration: BoxDecoration(
                    color: color.withOpacity(0.1),
                    borderRadius: BorderRadius.circular(8),
                  ),
                  child: Icon(icon, color: color, size: 20),
                ),
              ],
            ),
            const SizedBox(height: 12),
            Text(
              value,
              style: const TextStyle(
                  fontSize: 24,
                  fontWeight: FontWeight.bold,
                  color: Color(0xFF202124)),
            ),
          ],
        ),
      ),
    );
  }
}

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