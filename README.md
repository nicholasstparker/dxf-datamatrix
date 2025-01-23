<img src="/images/sample-barcode-engraved.JPG" width="480" alt="sample engraved barcode">

## Setup
1. Clone this repo
2. Open "settings.ini" and change any desired settings. See [here](#settings). for settings explanations. Be sure to save changes.
3. Run "generate_serials.bat"
4. Done!

## Settings
### Serial
**BaseSerial**: Your base serial number without the incrementor. Be sure to include a "-" or any trailing character you desire.

**StartingSerial**: Serial number to start from. Defaults to 1.

**EndingSerial**: Serial number to end at. Defaults to 10.

**NumberOfZeroes**: Number of zeroes in serial number. 3 would be 001, 002, 003... 4 would be 0001, 0002...

### Scaling
**TargetSize**: The rough desire of the rectangular size. Default is 25, which ends up being ~23 in ezcad 2. This is a conveinance setting and not really needed as DXF are innately scalable.

### Hatching - Hatching is a sort of "fill" for dxf files, where they might appear solid when zoomed out but are actually made of closely grouped horizontal lines.
**EnableHatching**: Self-explanatory

**HatchSpacing**: Distance between lines. Default is .2. I find this to be a good balance. Too small a number will increase processing time and can slow down any program importing the dxf.

### Output
**RelativeOutputPath**: Path relative to running directory to place serials. Defaults to serials. Do not include leading or trailing slashes.
