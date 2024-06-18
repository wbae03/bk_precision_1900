import argparse
import time

from bk1902b import BK1902B


def main():
    # Parse the command line arguments
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "port", help="Path to the serial port (e.g. /dev/ttyUSB1 or COM3)"
    )
    args = parser.parse_args()

    with BK1902B(args.port) as psu:
        print("Resetting output")
        psu.disable_output()
        #psu.set_output_off()
        psu.set_current(0.1)
        psu.set_voltage(1)
        time.sleep(10)
        #psu.set_output_on()
        psu.enable_output()

        for voltage in range(1, 701, 1): # last element in range not counted!!!
            voltage = voltage / 100
            psu.set_voltage(1.1 + voltage)
            time.sleep(0.6)
            output = psu.get_display()
            mode = "CV" if output[2] else "CC"
            print(
                f"Voltage set to {round(1.1 + voltage,2)}V."
                + f"Measured: {output[0]}V @ {output[1]}A {mode}"
            )
        psu.disable_output()
        #psu.set_output_off()


if __name__ == "__main__":
    main()
