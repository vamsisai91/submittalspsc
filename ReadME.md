# Petticoat Schmitt Submittals Extraction

This Streamlit app allows users to upload a PDF file, input specific details, and extract section numbers and submittals from a technical specifications. The app generates Excel and Word documents with the extracted information.

## Features

- Upload PDF files for processing
- Extract section numbers and submittals from specified pages
- Generate and download Excel and Word documents with the extracted information
- Display company logo and tagline
- Include a footer with copyright information

## Requirements

- Python 3.7 or higher
- Streamlit
- PyMuPDF
- OpenPyXL
- python-docx

## Installation

1. Clone the repository to your local machine:

    ```sh
    git clone https://github.com/vamsisai91/submittalspsc
    cd submittalpsc
    ```

2. Create a virtual environment:

    ```sh
    python -m venv myenv
    ```

3. Activate the virtual environment:

    - On Windows:

        ```sh
        myenv\Scripts\activate
        ```

    - On macOS and Linux:

        ```sh
        source myenv/bin/activate
        ```

4. Install the required packages:

    ```sh
    pip install -r requirements.txt
    ```

## Running the App

1. Save the company logo image as `logo.png` in the project root directory.

2. Run the Streamlit app:

    ```sh
    streamlit run app.py
    ```

3. Open your web browser and navigate to `http://localhost:8501` to access the app.

## Project Structure

pdf-section-number-extraction/
├── submittalswebpage.py
├── logo.png
├── requirements.txt
└── README.md

- `submittalswebpage.py`: The main Streamlit application file.
- `logo.png`: The company logo image file.
- `requirements.txt`: A list of Python dependencies.
- `README.md`: This file.

## How to Use

1. Open the app in your web browser.
2. Upload a PDF file.
3. Enter the project name, starting page, ending page, and the submittals master section number.
4. Click "Extract Section Numbers" to extract section numbers from the specified pages.
5. Review the extracted section numbers.
6. Click "Confirm and Extract Documents" to generate Excel and Word documents.
7. Download the generated documents using the provided download buttons.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more details.

## Contact

For any questions or feedback, please contact Vamsi Sai Kalsapudi, Consultant @ Petticoat Schmitt (vkalasapudi@petticoatschmitt.com).

## Acknowledgments

- [Streamlit](https://www.streamlit.io/)
- [PyMuPDF](https://pymupdf.readthedocs.io/)
- [OpenPyXL](https://openpyxl.readthedocs.io/)
- [python-docx](https://python-docx.readthedocs.io/)


