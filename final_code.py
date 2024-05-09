from trsim_worldview import *
import time
import sdcardio
import board
import busio
import digitalio
import storage
import pwmio
from adafruit_motor import servo
import adafruit_bme680

# LED:
# When the PBF header is inserted and data is not streaming = LED blinks with interval of 5 seconds
# When the PBF header is removed and data is not streaming = One second ON, One second OFF
# When the PBF header is inserted and data is streaming = LED blinks with interval of 3 seconds
# When the PBF header is removed and data is streaming = LED ON, does not blink


# Use any pin that is not taken by SPI
SD_CS = board.D10

# Connect to the card and mount the filesystem.
spi = busio.SPI(board.SCK, board.MOSI, board.MISO)
sdcard = sdcardio.SDCard(spi, SD_CS)
vfs = storage.VfsFat(sdcard)
storage.mount(vfs, "/sd")

BME_avail = False
try:
    i2c = board.I2C()
    b = adafruit_bme680.Adafruit_BME680_I2C(i2c, debug=False)
    temperature_offset = -5
    b.sea_level_pressure = 1013.25
    BME_avail = True
except Exception as e:
    print(f"BME sensor initialization failed: {e}")

pwm = pwmio.PWMOut(board.D5, frequency=50)
servo = servo.Servo(pwm, min_pulse=750, max_pulse=2250)

def main():
    sim = Simulator()
    timestamp = 0
    servo_time = 0
    with open("/sd/WORLD27.txt", "a") as f:
        f.write(
            "Time, Latitude, Longitude, Altitude, Speed, Heading, Velocity Down, \
            Pressure, Temperature, BME Gas, BME Rel Hum, BME Temp, BME Pres, BME Alt\n"
        )
    while True:
        sim.update()

        if sim.new_data:
            current_status = sim.status
            sim.prev_status = current_status
            status_change_message = ""

            # Check if the status has changed
            if current_status != sim.prev_status:
                # Create the status change message
                if current_status == STATUS_INITIALIZING:
                    status_change_message = "Balloon is initializing\n"
                elif current_status == STATUS_LAUNCHING:
                    status_change_message = "Balloon is launching\n"
                elif current_status == STATUS_FLOATING:
                    status_change_message = "Balloon is floating\n"
                elif current_status == STATUS_TERMINATING:
                    status_change_message = "Balloon is terminating\n"
                # Update the previous status
                sim.prev_status = current_status
            if time.time() > (servo_time + 120):
                servo.angle = 0
                time.sleep(0.5)
                #servo.angle(180)
                servo.angle = 180
                time.sleep(0.5)
                #servo.angle(0)
                servo.angle = 0
                servo_time = time.time()

            if time.time() > (timestamp + 1):
                if BME_avail:
                    bme_g = b.gas
                    bme_rh = b.relative_humidity
                    bme_t = b.temperature + temperature_offset
                    bme_p = b.pressure
                    bme_a = b.altitude
                else:
                    bme_g = bme_rh = bme_t = bme_p = bme_a = ("N/A")

                # Write data to the SD card
                with open("/sd/WORLD27.txt", "a") as f:
                    if status_change_message:
                        f.write(status_change_message)
                    # In data_to_save make sure there is ONLY the data you want to save to the SD Card
                    data_to_save = "{},{},{},{},{},{},{},{},{},{},{},{},{},{}\n".format(
                        sim.time,
                        sim.latitude,
                        sim.longitude,
                        sim.altitude,
                        sim.speed,
                        sim.heading,
                        sim.velocity_down,
                        sim.pressure,
                        sim.temperature,
                        bme_g,
                        bme_rh,
                        bme_t,
                        bme_p,
                        bme_a,
                    )
                    f.write(data_to_save)
                    print("Saving to SD card:", data_to_save)
                timestamp = time.time()

if __name__ == "__main__":
    main()
