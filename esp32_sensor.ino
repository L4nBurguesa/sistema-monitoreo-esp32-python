#include <Arduino.h>

// --- Configuración de Pines ---
// Se utiliza el GPIO 34, que es un pin de solo entrada (ADC1_CH6)
const int POT_PIN = 34; 

// --- Variables para el control de tiempo ---
unsigned long last_time = 0;
const int interval = 100; // Lectura periódica cada 100 ms

void setup() {
  // Configuración de la velocidad del puerto serial (UART)
  Serial.begin(115200);
  
  // Configuración de la resolución del ADC (12 bits: 0 a 4095)
  analogReadResolution(12);
  
  // Mensaje inicial (opcional, para depuración)
  // Serial.println("Iniciando sistema de monitoreo...");
}

void loop() {
  // Uso de millis() para ejecución no bloqueante cada 100 ms
  if (millis() - last_time >= interval) {
    last_time = millis();

    // 1. Leer el valor crudo del ADC
    int adc_value = analogRead(POT_PIN);

    // 2. Calcular el voltaje correspondiente
    // Referencia: 3.3V y resolución de 4095 (12 bits)
    float voltage = (adc_value * 3.3) / 4095.0;

    // 3. Enviar datos por puerto serial con el formato: tiempo_ms,adc,voltaje
    // Ejemplo esperado: 1250,1843,1.49
    Serial.print(last_time);
    Serial.print(",");
    Serial.print(adc_value);
    Serial.print(",");
    Serial.println(voltage, 2); // 2 decimales para el voltaje
  }
}
