import 'dart:math' as math;
import 'dart:async';
import 'dart:convert';

import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;
import 'package:audioplayers/audioplayers.dart';

import 'app_shell.dart';

import 'package:http/http.dart' as http;


void main() {
  runApp(const QuakeShieldApp());
}

class QuakeShieldApp extends StatelessWidget {
  const QuakeShieldApp({super.key});
  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      debugShowCheckedModeBanner: false,
      title: 'QuakeShield',
      theme: ThemeData.dark(),
      home: const AppShell(),
    );_MonitorScreenState
  }
}

class MonitorScreen extends StatefulWidget {
  const MonitorScreen({super.key});
  @override
  State<MonitorScreen> createState() => _MonitorScreenState();
}

class _MonitorScreenState extends State<MonitorScreen>
    with SingleTickerProviderStateMixin {
  late final AnimationController _waveController;
    Timer? _alertChecker;
  bool _alertAlreadyShown = false;
 @override
void initState() {
  super.initState();

  _waveController = AnimationController(
    vsync: this,
    duration: const Duration(seconds: 3),
  )..repeat();

  _alertChecker = Timer.periodic(
    const Duration(seconds: 2),
    (_) => _checkForAlert(),
  );
}bool _checkingBackend = false;

static const String backendUrl = 'http://10.0.2.2:8000';

Future<void> _checkForAlert() async {
  if (_checkingBackend || !mounted) return;

  _checkingBackend = true;

  try {
    final response = await http
        .get(Uri.parse('$backendUrl/latest-event'))
        .timeout(const Duration(seconds: 3));

    if (!mounted || response.statusCode != 200) return;

    final data = jsonDecode(response.body) as Map<String, dynamic>;
    final hasAlert = data['alert'] == true;

    if (!hasAlert) {
      _alertAlreadyShown = false;
      return;
    }

    if (_alertAlreadyShown) return;

    _alertAlreadyShown = true;

    await Navigator.push(
      context,
      MaterialPageRoute(
        builder: (_) => const AlertScreen(),
      ),
    );
  } catch (e) {
    debugPrint('Backend connection error: $e');
  } finally {
    _checkingBackend = false;
  }
}
 @override
void dispose() {
  _alertChecker?.cancel();
  _waveController.dispose();
  super.dispose();
}

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: const Color(0xFF101820),
      appBar: AppBar(
        backgroundColor: const Color(0xFF101820),
        title: const Text(
          'QUAKESHIELD',
          style: TextStyle(fontWeight: FontWeight.bold, letterSpacing: 2),
        ),
        actions: const [
          Padding(
            padding: EdgeInsets.all(16),
            child: Icon(Icons.shield, color: Colors.greenAccent),
          ),
        ],
      ),
      body: SingleChildScrollView(
        padding: const EdgeInsets.all(20),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            const Text(
              'EARTHQUAKE MONITOR',
              style: TextStyle(color: Colors.white70),
            ),
            const SizedBox(height: 18),
            // System status
            Container(
              width: double.infinity,
              padding: const EdgeInsets.all(22),
              decoration: BoxDecoration(
                color: const Color(0xFF1D2A35),
                borderRadius: BorderRadius.circular(18),
              ),
              child: const Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Icon(Icons.sensors, size: 42, color: Colors.greenAccent),
                  SizedBox(height: 14),
                  Text(
                    'SYSTEM STATUS',
                    style: TextStyle(color: Colors.white70),
                  ),
                  SizedBox(height: 8),
                  Text(
                    'DEMO MONITORING',
                    style: TextStyle(
                      fontSize: 23,
                      fontWeight: FontWeight.bold,
                      color: Colors.greenAccent,
                    ),
                  ),
                  SizedBox(height: 8),
                  Text(
                    'No live seismic sensor connected.',
                    style: TextStyle(color: Colors.white60),
                  ),
                ],
              ),
            ),
            const SizedBox(height: 16),
            // Sensor information
            const Row(
              children: [
                Expanded(
                  child: InfoCard(
                    icon: Icons.waves,
                    title: 'P-WAVES',
                    value: 'STANDBY',
                  ),
                ),
                SizedBox(width: 12),
                Expanded(
                  child: InfoCard(
                    icon: Icons.location_on,
                    title: 'LOCATION',
                    value: 'Mizoram',
                  ),
                ),
              ],
            ),
            const SizedBox(height: 22),
            // Seismic waveform panel
            Container(
              width: double.infinity,
              padding: const EdgeInsets.all(16),
              decoration: BoxDecoration(
                color: const Color(0xFF1D2A35),
                borderRadius: BorderRadius.circular(18),
                border: Border.all(
                  color: Colors.cyanAccent.withValues(alpha: 0.25),
                ),
              ),
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  const Row(
                    children: [
                      Icon(Icons.multiline_chart, color: Colors.cyanAccent),
                      SizedBox(width: 10),
                      Expanded(
                        child: Text(
                          'SEISMIC WAVEFORM',
                          style: TextStyle(
                            fontWeight: FontWeight.bold,
                            letterSpacing: 1,
                          ),
                        ),
                      ),
                      Text(
                        'SIMULATED',
                        style: TextStyle(
                          color: Colors.orangeAccent,
                          fontSize: 11,
                          fontWeight: FontWeight.bold,
                        ),
                      ),
                    ],
                  ),
                  const SizedBox(height: 6),
                  const Text(
                    'Illustrative signal • Not real sensor data',
                    style: TextStyle(color: Colors.white54, fontSize: 12),
                  ),
                  const SizedBox(height: 14),
                  SizedBox(
                    height: 130,
                    width: double.infinity,
                    child: AnimatedBuilder(
                      animation: _waveController,
                      builder: (context, child) {
                        return CustomPaint(
                          painter: WaveformPainter(
                            progress: _waveController.value,
                          ),
                        );
                      },
                    ),
                  ),
                  const SizedBox(height: 12),
                  const Row(
                    mainAxisAlignment: MainAxisAlignment.spaceBetween,
                    children: [
                      Text(
                        'SIGNAL',
                        style: TextStyle(color: Colors.white54, fontSize: 11),
                      ),
                      Text(
                        'DEMO SIGNAL ONLY',
                        style: TextStyle(
                          color: Colors.cyanAccent,
                          fontSize: 11,
                          fontWeight: FontWeight.bold,
                        ),
                      ),
                    ],
                  ),
                ],
              ),
            ),
            const SizedBox(height: 16),
            // Demo sensor activity
            Container(
              padding: const EdgeInsets.all(18),
              decoration: BoxDecoration(
                color: const Color(0xFF1D2A35),
                borderRadius: BorderRadius.circular(16),
              ),
              child: const Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Text(
                    'SENSOR NETWORK',
                    style: TextStyle(
                      fontWeight: FontWeight.bold,
                      letterSpacing: 1,
                    ),
                  ),
                  SizedBox(height: 16),
                  Row(
                    children: [
                      Icon(Icons.circle, color: Colors.orangeAccent, size: 12),
                      SizedBox(width: 10),
                      Expanded(child: Text('Physical sensor')),
                      Text(
                        'NOT CONNECTED',
                        style: TextStyle(
                          color: Colors.orangeAccent,
                          fontSize: 10,
                          fontWeight: FontWeight.bold,
                        ),
                      ),
                    ],
                  ),
                  SizedBox(height: 12),
                  Row(
                    children: [
                      Icon(
                        Icons.play_circle_outline,
                        color: Colors.cyanAccent,
                        size: 18,
                      ),
                      SizedBox(width: 10),
                      Expanded(child: Text('Waveform animation')),
                      Text(
                        'DEMO',
                        style: TextStyle(
                          color: Colors.cyanAccent,
                          fontSize: 11,
                          fontWeight: FontWeight.bold,
                        ),
                      ),
                    ],
                  ),
                ],
              ),
            ),
            const SizedBox(height: 24),
            // Simulated alert button
            SizedBox(
              width: double.infinity,
              height: 55,
              child: ElevatedButton.icon(
                style: ElevatedButton.styleFrom(
                  backgroundColor: Colors.redAccent,
                  foregroundColor: Colors.white,
                  shape: RoundedRectangleBorder(
                    borderRadius: BorderRadius.circular(12),
                  ),
                ),
                icon: const Icon(Icons.warning_amber),
                label: const Text(
                  'TEST SIMULATED ALERT',
                  style: TextStyle(fontWeight: FontWeight.bold),
                ),
                onPressed: () async {
  try {
    final response = await http
        .get(Uri.parse('$backendUrl/test-alert'))
        .timeout(const Duration(seconds: 5));

    if (response.statusCode == 200 && mounted) {
      await _checkForAlert();
    } else if (mounted) {
      ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(content: Text('Backend did not respond')),
      );
    }
  } catch (e) {
    if (mounted) {
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(content: Text('Connection failed: $e')),
      );
    }
  }
},
              ),
            ),
            const SizedBox(height: 16),
            const Center(
              child: Text(
                'QUAKESHIELD • PROTOTYPE',
                style: TextStyle(color: Colors.white38, letterSpacing: 1),
              ),
            ),
          ],
        ),
      ),
    );
  }
}

class WaveformPainter extends CustomPainter {
  final double progress;
  WaveformPainter({required this.progress});
  @override
  void paint(Canvas canvas, Size size) {
    final gridPaint = Paint()
      ..color = Colors.white.withValues(alpha: 0.08)
      ..strokeWidth = 1;
    for (int i = 0; i <= 4; i++) {
      final y = size.height * i / 4;
      canvas.drawLine(Offset(0, y), Offset(size.width, y), gridPaint);
    }
    for (int i = 0; i <= 8; i++) {
      final x = size.width * i / 8;
      canvas.drawLine(Offset(x, 0), Offset(x, size.height), gridPaint);
    }
    final centerY = size.height / 2;
    final path = Path();
    for (double x = 0; x <= size.width; x++) {
      final t = x / size.width;
      final phase = t * math.pi * 12 - progress * math.pi * 2;
      final smallWave = math.sin(phase) * 5;
      final mediumWave = math.sin(phase * 2.2) * 3;
      // Synthetic variations for a visual demonstration only.
      final burst =
          math.exp(-math.pow((t - 0.65) / 0.09, 2)) * math.sin(phase * 3) * 30;
      final y = centerY + smallWave + mediumWave + burst;
      if (x == 0) {
        path.moveTo(x, y);
      } else {
        path.lineTo(x, y);
      }
    }
    final wavePaint = Paint()
      ..color = Colors.cyanAccent
      ..strokeWidth = 2
      ..style = PaintingStyle.stroke
      ..strokeCap = StrokeCap.round;
    canvas.drawPath(path, wavePaint);
  }

  @override
  bool shouldRepaint(covariant WaveformPainter oldDelegate) {
    return oldDelegate.progress != progress;
  }
}

class InfoCard extends StatelessWidget {
  final IconData icon;
  final String title;
  final String value;
  const InfoCard({
    super.key,
    required this.icon,
    required this.title,
    required this.value,
  });
  @override
  Widget build(BuildContext context) {
    return Container(
      padding: const EdgeInsets.all(16),
      decoration: BoxDecoration(
        color: const Color(0xFF1D2A35),
        borderRadius: BorderRadius.circular(15),
      ),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Icon(icon, color: Colors.cyanAccent, size: 28),
          const SizedBox(height: 12),
          Text(title, style: const TextStyle(color: Colors.white60)),
          const SizedBox(height: 6),
          Text(value, style: const TextStyle(fontWeight: FontWeight.bold)),
        ],
      ),
    );
  }
}

class AlertScreen extends StatefulWidget {
  const AlertScreen({super.key});
  @override
  State<AlertScreen> createState() => _AlertScreenState();
}

class _AlertScreenState extends State<AlertScreen> {
  static const int initialSeconds = 12;
  int secondsRemaining = initialSeconds;
  Timer? countdownTimer;
  final AudioPlayer alarmPlayer = AudioPlayer();
  StreamSubscription<void>? alarmCompletionSubscription;

  @override
  void initState() {
    super.initState();

    alarmCompletionSubscription = alarmPlayer.onPlayerComplete.listen((_) {
      if (mounted) {
        startAlarm();
      }
    });

    startAlarm();

    countdownTimer = Timer.periodic(const Duration(seconds: 1), (timer) {
      if (!mounted) {
        timer.cancel();
        return;
      }

      if (secondsRemaining > 0) {
        setState(() {
          secondsRemaining--;
        });
      } else {
        timer.cancel();
      }
    });
  }

  Future<void> startAlarm() async {
    try {
      await alarmPlayer.setReleaseMode(ReleaseMode.stop);
      await alarmPlayer.play(AssetSource('sounds/earthquake_alarm.mp3'));
    } catch (e) {
      debugPrint('Alarm playback failed: $e');
    }
  }

  Future<void> stopAlarm() async {
    try {
      await alarmPlayer.stop();
    } catch (e) {
      debugPrint('Alarm stop failed: $e');
    }
  }

  Future<void> goBack() async {
    countdownTimer?.cancel();
    await stopAlarm();
    if (mounted) {
      Navigator.pop(context);
    }
  }

  @override
  void dispose() {
    countdownTimer?.cancel();
    alarmCompletionSubscription?.cancel();
    alarmPlayer.stop();
    alarmPlayer.dispose();
    super.dispose();
  }

  Widget infoCard({
    required IconData icon,
    required String title,
    required String value,
    required String subtitle,
  }) {
    return Expanded(
      child: Container(
        padding: const EdgeInsets.symmetric(vertical: 18, horizontal: 10),
        decoration: BoxDecoration(
          color: Colors.white.withValues(alpha: 0.09),
          borderRadius: BorderRadius.circular(16),
          border: Border.all(color: Colors.white24),
        ),
        child: Column(
          children: [
            Icon(icon, color: Colors.orangeAccent, size: 30),
            const SizedBox(height: 10),
            Text(
              title,
              textAlign: TextAlign.center,
              style: const TextStyle(color: Colors.white70, fontSize: 12),
            ),
            const SizedBox(height: 8),
            Text(
              value,
              textAlign: TextAlign.center,
              style: const TextStyle(
                color: Colors.white,
                fontSize: 25,
                fontWeight: FontWeight.w900,
              ),
            ),
            const SizedBox(height: 5),
            Text(
              subtitle,
              textAlign: TextAlign.center,
              style: const TextStyle(color: Colors.white70, fontSize: 11),
            ),
          ],
        ),
      ),
    );
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: const Color(0xFF650B12),
      body: SafeArea(
        child: SingleChildScrollView(
          padding: const EdgeInsets.all(22),
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.stretch,
            children: [
              const SizedBox(height: 12),
              const Row(
                mainAxisAlignment: MainAxisAlignment.center,
                children: [
                  Icon(
                    Icons.warning_amber_rounded,
                    color: Colors.white,
                    size: 30,
                  ),
                  SizedBox(width: 10),
                  Text(
                    'QUAKESHIELD ALERT',
                    style: TextStyle(
                      color: Colors.white,
                      fontWeight: FontWeight.w900,
                      letterSpacing: 1.3,
                      fontSize: 19,
                    ),
                  ),
                ],
              ),
              const SizedBox(height: 28),
              Container(
                padding: const EdgeInsets.all(24),
                decoration: BoxDecoration(
                  color: Colors.white.withValues(alpha: 0.08),
                  shape: BoxShape.circle,
                ),
                child: const Icon(
                  Icons.crisis_alert_rounded,
                  color: Colors.white,
                  size: 76,
                ),
              ),
              const SizedBox(height: 24),
              const Text(
                'DROP. COVER. HOLD ON.',
                textAlign: TextAlign.center,
                style: TextStyle(
                  color: Colors.white,
                  fontSize: 27,
                  fontWeight: FontWeight.w900,
                  height: 1.2,
                ),
              ),
              const SizedBox(height: 12),
              const Text(
                'Protect yourself during earthquake shaking.',
                textAlign: TextAlign.center,
                style: TextStyle(color: Color(0xFFFFDCDD), fontSize: 15),
              ),
              const SizedBox(height: 24),
              const Text(
                'SIMULATED EARTHQUAKE DATA',
                textAlign: TextAlign.center,
                style: TextStyle(
                  color: Colors.orangeAccent,
                  fontWeight: FontWeight.bold,
                  letterSpacing: 1,
                  fontSize: 12,
                ),
              ),
              const SizedBox(height: 12),
              Row(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  infoCard(
                    icon: Icons.location_on_rounded,
                    title: 'Source distance',
                    value: '25 km',
                    subtitle: 'Demo estimate',
                  ),
                  const SizedBox(width: 12),
                  infoCard(
                    icon: Icons.timer_rounded,
                    title: 'Demo countdown',
                    value: secondsRemaining > 0
                        ? '$secondsRemaining s'
                        : '00 s',
                    subtitle: secondsRemaining > 0 ? 'Simulated' : 'Demo ended',
                  ),
                ],
              ),
              const SizedBox(height: 12),
              const Text(
                'These values are examples only. The countdown does not predict when an actual earthquake will strike.',
                textAlign: TextAlign.center,
                style: TextStyle(
                  color: Colors.white70,
                  fontSize: 11,
                  height: 1.5,
                ),
              ),
              const SizedBox(height: 28),
              const SafetyStep(
                number: '1',
                title: 'DROP',
                description: 'Get down onto your hands and knees.',
                icon: Icons.accessibility_new,
              ),
              const SizedBox(height: 12),
              const SafetyStep(
                number: '2',
                title: 'COVER',
                description: 'Get under sturdy furniture if possible. Protect your head and neck.',
                icon: Icons.table_restaurant,
              ),
              const SizedBox(height: 12),
              const SafetyStep(
                number: '3',
                title: 'HOLD ON',
                description: 'Hold your shelter until the shaking stops.',
                icon: Icons.pan_tool_alt,
              ),
              const SizedBox(height: 22),
              Container(
                padding: const EdgeInsets.all(15),
                decoration: BoxDecoration(
                  color: const Color(0xFF40070C),
                  borderRadius: BorderRadius.circular(14),
                  border: Border.all(color: Colors.white24),
                ),
                child: const Column(
                  children: [
                    Icon(
                      Icons.info_outline,
                      color: Colors.orangeAccent,
                      size: 28,
                    ),
                    SizedBox(height: 8),
                    Text(
                      'SIMULATED WARNING',
                      textAlign: TextAlign.center,
                      style: TextStyle(
                        color: Colors.orangeAccent,
                        fontWeight: FontWeight.bold,
                        letterSpacing: 1,
                      ),
                    ),
                    SizedBox(height: 6),
                    Text(
                      'Demo only. No live seismic sensor is connected. This is not an official earthquake warning.',
                      textAlign: TextAlign.center,
                      style: TextStyle(
                        color: Colors.white70,
                        fontSize: 12,
                        height: 1.5,
                      ),
                    ),
                  ],
                ),
              ),
              const SizedBox(height: 22),
              SizedBox(
                height: 54,
                child: ElevatedButton.icon(
                  onPressed: goBack,
                  icon: const Icon(Icons.arrow_back),
                  label: const Text(
                    'BACK TO MONITOR',
                    style: TextStyle(
                      fontWeight: FontWeight.bold,
                      letterSpacing: 0.7,
                    ),
                  ),
                  style: ElevatedButton.styleFrom(
                    backgroundColor: Colors.white,
                    foregroundColor: const Color(0xFF650B12),
                    shape: RoundedRectangleBorder(
                      borderRadius: BorderRadius.circular(13),
                    ),
                  ),
                ),
              ),
              const SizedBox(height: 12),
            ],
          ),
        ),
      ),
    );
  }
}

class SafetyStep extends StatelessWidget {
  final String number;
  final String title;
  final String description;
  final IconData icon;
  const SafetyStep({
    super.key,
    required this.number,
    required this.title,
    required this.description,
    required this.icon,
  });
  @override
  Widget build(BuildContext context) {
    return Container(
      padding: const EdgeInsets.all(15),
      decoration: BoxDecoration(
        color: Colors.white.withValues(alpha: 0.08),
        borderRadius: BorderRadius.circular(15),
        border: Border.all(color: Colors.white.withValues(alpha: 0.12)),
      ),
      child: Row(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Container(
            width: 44,
            height: 44,
            decoration: const BoxDecoration(
              color: Colors.white,
              shape: BoxShape.circle,
            ),
            child: Center(
              child: Text(
                number,
                style: const TextStyle(
                  color: Color(0xFF650B12),
                  fontWeight: FontWeight.w900,
                  fontSize: 20,
                ),
              ),
            ),
          ),
          const SizedBox(width: 14),
          Expanded(
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Row(
                  children: [
                    Icon(icon, color: Colors.white70, size: 19),
                    const SizedBox(width: 8),
                    Text(
                      title,
                      style: const TextStyle(
                        color: Colors.white,
                        fontWeight: FontWeight.w900,
                        letterSpacing: 1,
                      ),
                    ),
                  ],
                ),
                const SizedBox(height: 7),
                Text(
                  description,
                  style: const TextStyle(
                    color: Color(0xFFFFE8E8),
                    fontSize: 14,
                    height: 1.45,
                  ),
                ),
              ],
            ),
          ),
        ],
      ),
    );
  }
}
