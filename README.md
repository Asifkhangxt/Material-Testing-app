MatTest Pro

MatTest Pro is a Streamlit-based web app for soil and concrete material testing, adhering to ASTM standards. It calculates results, generates graphs, and produces PDF reports, with a clean UI and deployment on Hugging Face Spaces.
Features
•	Soil Tests:
o	Atterberg Limits (ASTM D4318): Computes LL, PL, PI, with flow curve.
o	Compaction Test (ASTM D698/D1557): Finds max dry density, optimum moisture, with Zero Air Voids curve.
o	CBR (ASTM D1883): Calculates CBR at 0.1"/0.2", with load/stress vs. penetration curves.
•	Concrete Tests:
o	Slump Test (ASTM C143): Measures workability (cm), checks acceptance.
o	Compressive Strength (ASTM C39): Computes strength (MPa), with strength vs. age plot.
o	Water-Cement Ratio: Validates w/c ratio (0.3–0.7).
o	Fineness Modulus (ASTM C136): Calculates FM, with gradation curve.
o	Unit Weight Test (ASTM C138): Determines density (kg/m³), checks acceptability.
•	PDF Reports: Includes project info, results, standards, and graphs via reportlab.
•	UI: Custom CSS, sidebar for project details, responsive layout.
•	Deployment: Optimized for local and cloud use (Hugging Face Spaces).
Prerequisites
•	Python: 3.10+
•	Dependencies: requirements.txt (Streamlit, Pandas, NumPy, Matplotlib, ReportLab)
Installation
1.	Clone repo:
cd mattest-pro
2.	Create virtual environment (optional):
3.	python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
4.	Install dependencies:
pip install -r requirements.txt
5.	Run app:
streamlit run app.py
Open http://localhost:8501.
File Structure
mattest-pro/
├── app.py           # Streamlit app
├── requirements.txt # Dependencies
├── README.md        # Documentation
└── Dockerfile       # For Hugging Face Spaces
•	app.py: Handles UI, calculations, and PDF generation.
•	requirements.txt: Lists streamlit==1.38.0, pandas==2.2.2, numpy==1.26.4, matplotlib==3.9.2, reportlab==4.2.2.
•	Dockerfile: Configures container for deployment.
Usage
1.	Access: Run locally or via Hugging Face Spaces URL.
2.	Project Details: Enter contractor, client, consultant, project name, test date (default: July 26, 2025) in sidebar.
3.	Select Test: Choose Soil or Concrete Tests from dropdown.
4.	Perform Tests:
o	Soil Tests:
	Atterberg Limits: Input 3–6 LL points (blows, moisture %), single PL. Click to calculate LL, PL, PI, and plot.
	Compaction Test: Select D698/D1557, input 4–8 points (moisture %, dry density), specific gravity (default: 2.65). Click for results and curve.
	CBR: Select soaked/unsoaked, blows (10/25/56), input 12 loads (0.0–0.5"), moisture, density, swell (if soaked). Click for CBR and curves.
o	Concrete Tests:
	Slump Test: Input slump (cm), type, min/max. Click for results.
	Compressive Strength: Select cube/cylinder, input 1–5 specimens (age, load kN). Click for strength (MPa) and plot.
	Water-Cement Ratio: Input water, cement weights, min/max. Click for w/c and pass/fail.
	Fineness Modulus: Input 7 sieve weights (4.75–0.075 mm). Click for FM and curve.
	Unit Weight Test: Input volume, empty/filled weights, min/max density. Click for density and pass/fail.
5.	Results: View metrics, graphs, and download PDF reports with project info, results, standards, and graphs.
ASTM Compliance
•	Soil Tests:
o	Atterberg Limits: LL via log-transformed regression, PI = LL - PL.
o	Compaction: Quadratic fit for max density (1.0–2.5 g/cm³), Zero Air Voids curve.
o	CBR: Stress = load / 3 in², CBR at 0.1"/0.2" via interpolation.
•	Concrete Tests:
o	Slump: Workability, acceptability check.
o	Compressive Strength: Strength = load (N) / area (mm²) * 0.001.
o	Fineness Modulus: FM = Σ(Cumulative % Retained) / 100.
o	Unit Weight: Density = (filled - empty) / volume.
o	Water-Cement Ratio: Validates w/c (0.3–0.7).
Note: Simplified calculations (e.g., no oversize correction for Compaction). Refer to ASTM for precision.
Hugging Face Deployment
1.	Create a Streamlit Space on Hugging Face.
2.	Upload app.py, requirements.txt, Dockerfile:
3.	FROM python:3.10-slim
4.	WORKDIR /app
5.	COPY requirements.txt .
6.	RUN pip install -r requirements.txt
7.	COPY . .
8.	EXPOSE 8501
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
9.	Commit and access via provided URL.
10.	Check build logs for errors.
Contributing
1.	Fork and clone repo.
2.	Create branch: git checkout -b feature/your-feature.
3.	Add features, update README.md, test thoroughly.
4.	Submit PR with clear description.
Extending the App
•	Add asphalt tests (e.g., ASTM D6927).
•	Use plotly for interactive graphs.
•	Generate LaTeX reports with pdflatex.
•	Add ASTM corrections (e.g., D4718 for Compaction).
•	Integrate SQLite for data storage.
Troubleshooting
•	Dependencies: Verify requirements.txt installation.
•	Graphs: Check Matplotlib, clear temp_plot.png.
•	PDFs: Ensure reportlab and valid inputs.
•	Deployment: Review Hugging Face logs, verify Dockerfile.
License
MIT License. See LICENSE.
Contact
Open GitHub issues or email [asifkhan.gxt@gmail.com].

