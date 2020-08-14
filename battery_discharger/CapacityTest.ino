
struct Battery {
  String identifier;
  int on_pin;
  int v_in;
  double current; // in Amps
  
  unsigned long start_time = millis();
  unsigned long total_time = 0;
  double capacity = -1.0;
  bool finished = false;
  bool no_current_voltage = false;
  double v_cutoff = -1.0;

  Battery(String id, int on, int v, double curr): identifier(id), on_pin(on), v_in(v), current(curr) {}
};

Battery bat1 = {"A", 2, A3, 0.81};
Battery bat2 = {"B", 3, A4, 0.82};

void setup() {
  Serial.begin(9600);
  
  pinMode(bat1.on_pin, OUTPUT);
  pinMode(bat2.on_pin, OUTPUT);
  

  digitalWrite(bat1.on_pin, HIGH);
  digitalWrite(bat2.on_pin, HIGH);
}

void loop() {
//  digitalWrite(bat1.on_pin, LOW);
//  digitalWrite(bat2.on_pin, LOW);
  checkBattery(&bat1);
  checkBattery(&bat2);
  delay(3000);
}

void checkBattery(Battery *bat) {
  Serial.println();
  Serial.print(bat->identifier);
  Serial.print(" <----> ");
  Serial.println(bat->current);
  double voltage = 0.0;

  if (bat->finished) {
    complete(bat);
    return;
  }
  
  if (bat->no_current_voltage) {
    digitalWrite(bat->on_pin, LOW);
    delay(100);
    bat->start_time += 100;
    voltage = analogRead(bat->v_in) * 5.0 / 1023.0;
    digitalWrite(bat->on_pin, HIGH);
    delay(1000);
    Serial.print("No current voltage reading: ");
    Serial.println(voltage);
  }
  else {
    voltage = analogRead(bat->v_in) * 5.0 / 1023.0;
    Serial.print("Normal voltage reading: ");
    Serial.println(voltage);
  }

  if (voltage <= 3.0) {
    bat->no_current_voltage = true;
  }

  if (voltage < 2.5) {
    bat->total_time = millis() - bat->start_time;
    bat->capacity = bat->total_time / 1000.0 / 3600.0 * bat->current;
    bat->finished = true;
    bat->v_cutoff = voltage;
    digitalWrite(bat->on_pin, LOW);
  }
}



void complete(Battery *bat) {
  digitalWrite(bat->on_pin, LOW);
    Serial.print("TOTAL TIME: ");
    Serial.print(bat->total_time);
    Serial.print(" VOLTAGE CUTOFF: ");
    Serial.println(bat->v_cutoff);
    Serial.print("CAPACITY: ");
    Serial.println(bat->capacity, 4);
}
