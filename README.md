# Unity Package Unpacker

Unity Package Unpacker is a command-line tool for extracting the contents of **'.unitypackage'** files. It supports extracting both asset files and metadata files.

## Features

- Easily extract the contents of .unitypackage files
- Option to extract or ignore associated .meta files
- Compatible with **Windows**, **macOS**, and **Linux** operating systems

## Prerequisites

- Python 3.6 or later

## Installation

Clone this Git repository and navigate to the project directory:

```bash
git clone https://github.com/yourusername/unity-package-unpacker.git
cd unity-package-unpacker
```

## Usage
Use the **'unity_unpacker.py'** script to extract the contents of a **'.unitypackage file'**. The basic syntax is as follows:

```bash
python unity_unpacker.py [--nometa] input_file output_path
```

- **--nometa**: (optional) If this flag is provided, the .meta files will not be extracted.
- **input_file**: The path to the .unitypackage file you want to extract.
- **output_path**: The path to the directory where you want to extract the package contents.

## Example
To extract the contents of an **'example.unitypackage'** file into an **'output'** folder:

```bash
python unity_unpacker.py example.unitypackage output
```

To extract the contents without the **'.meta'** files:

```bash
python unity_unpacker.py --nometa example.unitypackage output
```

## License
This project is licensed under the **MIT** License.
