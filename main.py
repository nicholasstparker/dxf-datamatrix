import configparser
import ezdxf
from ezdxf import units
from pylibdmtx.pylibdmtx import encode
from PIL import Image
from ezdxf.math import Matrix44
from loguru import logger
import os

if __name__ == "__main__":
    # setup loguru
    logger.remove()
    logger.add(lambda msg: print(msg, end=""), format="{message}", colorize=True)

    # read settings
    config = configparser.ConfigParser()
    config.read("settings.ini")
    # serial settings
    base_serial = config.get("Serial", "BaseSerial")
    starting_serial = config.getint("Serial", "StartingSerial")
    ending_serial = config.getint("Serial", "EndingSerial")
    number_of_zeroes = config.getint("Serial", "NumberOfZeroes")
    # scaling settings
    target_size = config.getfloat("Scaling", "TargetSize")
    # hatching settings
    hatching_enabled = config.getboolean("Hatching", "EnableHatching")
    hatch_spacing = config.getfloat("Hatching", "HatchSpacing")
    # output settings
    relative_output_directory = config.get("Output", "RelativeOutputPath")

    # create directory for output files
    os.makedirs(relative_output_directory, exist_ok=True)

    # black color tuple
    black = (0, 0, 0)

    # internal vars for progress tracking
    _serials_done = 0
    _number_of_serials = ending_serial + 1 - starting_serial

    for i in range(starting_serial, ending_serial + 1):
        serial = base_serial + str(i).zfill(number_of_zeroes)
        data = serial.encode("utf-8")
        encoded = encode(data)
        img = Image.frombytes('RGB', (encoded.width, encoded.height), encoded.pixels)

        doc = ezdxf.new("R12")
        msp = doc.modelspace()

        for row in range(0, encoded.height, 5):
            for col in range(0, encoded.width, 5):
                pixel = img.getpixel((col, row))
                if pixel == black:
                    transformed_row = encoded.height - row
                    msp.add_line((col, transformed_row), (col + 5, transformed_row))
                    msp.add_line((col + 5, transformed_row), (col + 5, transformed_row - 5))
                    msp.add_line((col + 5, transformed_row - 5), (col, transformed_row - 5))
                    msp.add_line((col, transformed_row - 5), (col, transformed_row))

                    if hatching_enabled:
                        y = transformed_row - hatch_spacing
                        while y > transformed_row - 5:
                            msp.add_line((col, y), (col + 5, y))
                            y -= hatch_spacing

        scale_factor = target_size / encoded.width
        scaling_matrix = Matrix44.scale(scale_factor, scale_factor, scale_factor)
        for entity in msp:
            entity.transform(scaling_matrix)

        doc.saveas(f"{relative_output_directory}/{serial}.dxf")
        _serials_done += 1
        percent_done = round(_serials_done / _number_of_serials * 100, 2)
        logger.info(f"\033[32m{percent_done}%\033[0m - Proccessed {relative_output_directory}/{serial}.dxf")

    logger.success(f"\033[35mDone!\033[0m")

    a = input('Press enter to exit..')
    if a:
        exit(0)
