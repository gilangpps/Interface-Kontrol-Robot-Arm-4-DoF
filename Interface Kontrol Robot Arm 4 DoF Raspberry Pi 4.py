import RPi.GPIO as GPIO
import tkinter as tk
from tkinter import ttk

# Konfigurasi GPIO
GPIO.setmode(GPIO.BCM)

# Pin GPIO untuk servo
servo_pins = [17, 27, 22, 23]  # Ganti dengan pin GPIO yang sesuai
servos = {}

# Inisialisasi servo motor
for pin in servo_pins:
    GPIO.setup(pin, GPIO.OUT)
    servos[pin] = GPIO.PWM(pin, 50)  # 50 Hz untuk servo
    servos[pin].start(7.5)  # Posisi netral (90 derajat)

def set_servo_angle(servo, angle):
    # Hitung duty cycle dari sudut (0-180)
    duty_cycle = 2.5 + (angle / 180.0) * 10
    servos[servo].ChangeDutyCycle(duty_cycle)

def on_slider_change(servo_index, value):
    # Ambil pin GPIO berdasarkan indeks servo
    servo_pin = servo_pins[servo_index]
    angle = int(float(value))
    set_servo_angle(servo_pin, angle)

# Antarmuka GUI menggunakan Tkinter
root = tk.Tk()
root.title("Kontrol Robot Arm 4 DoF")

# Buat slider untuk masing-masing servo
for i in range(len(servo_pins)):
    frame = ttk.Frame(root)
    frame.pack(padx=10, pady=10)
    
    label = ttk.Label(frame, text=f"Servo {i + 1}")
    label.pack(side=tk.LEFT)
    
    slider = ttk.Scale(
        frame, from_=0, to=180, orient=tk.HORIZONTAL,
        command=lambda value, servo_index=i: on_slider_change(servo_index, value)
    )
    slider.set(90)  # Atur slider agar dimulai dari tengah (90 derajat)
    slider.pack(side=tk.LEFT, fill=tk.X, expand=True)

root.mainloop()

# Bersihkan GPIO saat program selesai
for pin in servo_pins:
    servos[pin].stop()
GPIO.cleanup()
