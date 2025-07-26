# Material-Testing-app

import streamlit as stimport pandas as pdimport numpy as npimport matplotlib.pyplot as pltfrom reportlab.lib import colorsfrom reportlab.lib.pagesizes import letterfrom reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, Imagefrom reportlab.lib.styles import getSampleStyleSheet, ParagraphStylefrom reportlab.lib.units import inchfrom reportlab.lib.enums import TA_CENTERfrom datetime import datetimeimport ioimport os
Page configuration
st.set_page_config(    page_title="MatTest Pro",    page_icon="🧱",    layout="wide",    initial_sidebar_state="expanded")
Custom CSS
st.markdown("""

    .main-header {
        font-size: 36px;
        color: #1e3d59;
        text-align: center;
        padding: 20px;
        background-color: #f5f5f5;
        border-radius: 10px;
        margin-bottom: 30px;
    }
    .section-header {
        font-size: 24px;
        color: #2e7d32;
        margin-top: 20px;
        margin-bottom: 10px;
    }
    .test-card {
        background-color: #f8f9fa;
        padding: 20px;
        border-radius: 10px;
        margin-bottom: 20px;
        border: 1px solid #dee2e6;
    }

""", unsafe_allow_html=True)
Initialize session state
if 'project_info' not in st.session_state:    st.session_state.project_info = {        'contractor': '',        'client': '',        'consultant': '',        'project_name': '',        'date': datetime.now().strftime("%Y-%m-%d")    }
Helper functions
def create_pdf_report(test_name, project_info, test_data, graphs):    """Generate PDF report with test results and graphs"""    buffer = io.BytesIO()    doc = SimpleDocTemplate(buffer, pagesize=letter)    story = []    styles = getSampleStyleSheet()
# Custom styles
title_style = ParagraphStyle(
    'CustomTitle',
    parent=styles['Heading1'],
    fontSize=24,
    textColor=colors.HexColor('#1e3d59'),
    alignment=TA_CENTER,
    spaceAfter=30
)

header_style = ParagraphStyle(
    'CustomHeader',
    parent=styles['Heading2'],
    fontSize=16,
    textColor=colors.HexColor('#2e7d32'),
    spaceAfter=12
)

# Title
story.append(Paragraph(f"MatTest Pro - {test_name} Report", title_style))
story.append(Spacer(1, 20))

# Project Information Table
project_data = [
    ['Project Information', ''],
    ['Contractor:', project_info['contractor']],
    ['Client:', project_info['client']],
    ['Consultant:', project_info['consultant']],
    ['Project Name:', project_info['project_name']],
    ['Test Date:', project_info['date']],
    ['Test Type:', test_name]
]

project_table = Table(project_data, colWidths=[2*inch, 4*inch])
project_table.setStyle(TableStyle([
    ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
    ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
    ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
    ('FONTSIZE', (0, 0), (-1, 0), 14),
    ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
    ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
    ('GRID', (0, 0), (-1, -1), 1, colors.black)
]))

story.append(project_table)
story.append(Spacer(1, 30))

# Test Results
story.append(Paragraph("Test Results", header_style))

# Convert test data to table format
test_table_data = []
for key, value in test_data.items():
    test_table_data.append([key, str(value)])

if test_table_data:
    results_table = Table(test_table_data, colWidths=[3*inch, 3*inch])
    results_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (0, -1), colors.lightgrey),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('LEFTPADDING', (0, 0), (-1, -1), 12),
        ('RIGHTPADDING', (0, 0), (-1, -1), 12),
    ]))
    story.append(results_table)

# Add graphs
if graphs:
    story.append(Spacer(1, 20))
    story.append(Paragraph("Test Graphs", header_style))
    for graph in graphs:
        img = Image(graph, width=6*inch, height=4*inch)
        story.append(img)
        story.append(Spacer(1, 20))

# Build PDF
doc.build(story)
buffer.seek(0)
return buffer

def plot_to_buffer(fig):    """Convert matplotlib figure to buffer for PDF"""    buf = io.BytesIO()    fig.savefig(buf, format='png', dpi=300, bbox_inches='tight')    buf.seek(0)    return buf
Main App
st.markdown('🧱 MatTest Pro – Material Testing App', unsafe_allow_html=True)st.write("Enter test data to perform soil or concrete tests and generate PDF reports compliant with ASTM standards.")
Sidebar for project information
with st.sidebar:    st.header("📋 Project Information")    st.session_state.project_info['contractor'] = st.text_input("Contractor Name", st.session_state.project_info['contractor'])    st.session_state.project_info['client'] = st.text_input("Client Name", st.session_state.project_info['client'])    st.session_state.project_info['consultant'] = st.text_input("Consultant Name", st.session_state.project_info['consultant'])    st.session_state.project_info['project_name'] = st.text_input("Project Name", st.session_state.project_info['project_name'])    st.session_state.project_info['date'] = st.date_input("Test Date", datetime.now()).strftime("%Y-%m-%d")
Test Category Selection
test_category = st.selectbox("Select Test Category", ["Soil Tests", "Concrete Tests"])
if test_category == "Soil Tests":    st.markdown('Soil Testing Section', unsafe_allow_html=True)    soil_test = st.selectbox(        "Select Soil Test",        ["Atterberg Limits", "Compaction Test (Proctor)", "California Bearing Ratio (CBR)"]    )
if soil_test == "Atterberg Limits":
    st.markdown('<div class="test-card">', unsafe_allow_html=True)
    st.subheader("Atterberg Limits Test (ASTM D4318)")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("**Liquid Limit Test**")
        ll_data = []
        num_ll_points = st.number_input("Number of test points", min_value=3, max_value=6, value=3)
        
        for i in range(num_ll_points):
            st.write(f"Test Point {i+1}")
            cols = st.columns(3)
            blows = cols[0].number_input(f"Blows", min_value=10, max_value=50, key=f"ll_blows_{i}")
            moisture = cols[1].number_input(f"Moisture Content (%)", min_value=0.0, max_value=100.0, key=f"ll_moisture_{i}")
            if blows > 0 and moisture >= 0:
                ll_data.append({'Blows': blows, 'Moisture': moisture})
    
    with col2:
        st.write("**Plastic Limit Test**")
        pl_moisture = st.number_input("Plastic Limit Moisture Content (%)", min_value=0.0, max_value=100.0)
    
    if st.button("Calculate Atterberg Limits"):
        if len(ll_data) >= 3:
            # Calculate LL using flow curve
            df_ll = pd.DataFrame(ll_data)
            
            # Log transform for linear regression (ASTM D4318)
            log_blows = np.log10(df_ll['Blows'])
            coeffs = np.polyfit(log_blows, df_ll['Moisture'], 1)
            
            # LL at 25 blows
            ll_25 = coeffs[0] * np.log10(25) + coeffs[1]
            
            # Use single PL value
            pl = pl_moisture if pl_moisture > 0 else 0
            
            # Calculate PI
            pi = ll_25 - pl if pl > 0 and ll_25 >= pl else 0
            
            # Validation
            if pl > ll_25:
                st.error("Plastic Limit cannot be greater than Liquid Limit.")
            else:
                # Display results
                st.success("Test Results:")
                col1, col2, col3 = st.columns(3)
                col1.metric("Liquid Limit (LL)", f"{ll_25:.1f}%")
                col2.metric("Plastic Limit (PL)", f"{pl:.1f}%")
                col3.metric("Plasticity Index (PI)", f"{pi:.1f}%")
                
                # Plot flow curve
                fig, ax = plt.subplots(figsize=(10, 6))
                ax.semilogx(df_ll['Blows'], df_ll['Moisture'], 'bo-', markersize=8, label='Test Data')
                
                # Plot regression line
                x_range = np.logspace(np.log10(10), np.log10(50), 100)
                y_range = coeffs[0] * np.log10(x_range) + coeffs[1]
                ax.semilogx(x_range, y_range, 'r--', label='Best Fit Line')
                ax.axvline(x=25, color='g', linestyle=':', label='25 Blows')
                ax.axhline(y=ll_25, color='g', linestyle=':', alpha=0.5)
                
                ax.set_xlabel('Number of Blows (log scale)')
                ax.set_ylabel('Moisture Content (%)')
                ax.set_title('Liquid Limit Flow Curve (ASTM D4318)')
                ax.grid(True, which="both", ls="-", alpha=0.3)
                ax.legend()
                
                st.pyplot(fig)
                
                # Generate PDF Report
                test_data = {
                    'Liquid Limit (LL)': f"{ll_25:.1f}%",
                    'Plastic Limit (PL)': f"{pl:.1f}%",
                    'Plasticity Index (PI)': f"{pi:.1f}%",
                    'Test Standard': 'ASTM D4318'
                }
                
                graphs = [plot_to_buffer(fig)]
                pdf_buffer = create_pdf_report("Atterberg Limits", st.session_state.project_info, test_data, graphs)
                
                st.download_button(
                    label="📄 Download PDF Report",
                    data=pdf_buffer,
                    file_name=f"Atterberg_Limits_Report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf",
                    mime="application/pdf"
                )
    
    st.markdown('</div>', unsafe_allow_html=True)

elif soil_test == "Compaction Test (Proctor)":
    st.markdown('<div class="test-card">', unsafe_allow_html=True)
    st.subheader("Compaction Test (ASTM D698/D1557)")
    
    test_type = st.radio("Select Test Type", ["Standard Proctor (ASTM D698)", "Modified Proctor (ASTM D1557)"])
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("**Test Data Input**")
        num_points = st.number_input("Number of test points", min_value=4, max_value=8, value=5)
        
        compaction_data = []
        for i in range(num_points):
            st.write(f"Point {i+1}")
            cols = st.columns(2)
            moisture = cols[0].number_input(f"Moisture %", min_value=0.0, max_value=50.0, key=f"comp_moisture_{i}")
            density = cols[1].number_input(f"Dry Density (g/cm³)", min_value=1.0, max_value=2.5, key=f"comp_density_{i}", step=0.01)
            if moisture > 0 and density > 0:
                compaction_data.append({'Moisture': moisture, 'Density': density})
    
    with col2:
        st.write("**Additional Parameters**")
        specific_gravity = st.number_input("Specific Gravity (Gs)", min_value=2.4, max_value=3.0, value=2.65)
    
    if st.button("Calculate Compaction Results"):
        if len(compaction_data) >= 4:
            df_comp = pd.DataFrame(compaction_data)
            
            # Fit polynomial for smooth curve (ASTM D698/D1557)
            coeffs = np.polyfit(df_comp['Moisture'], df_comp['Density'], 2)
            poly = np.poly1d(coeffs)
            
            # Find theoretical maximum from polynomial
            moisture_range = np.linspace(df_comp['Moisture'].min(), df_comp['Moisture'].max(), 100)
            density_curve = poly(moisture_range)
            
            theoretical_max_idx = np.argmax(density_curve)
            theoretical_max_density = density_curve[theoretical_max_idx]
            theoretical_opt_moisture = moisture_range[theoretical_max_idx]
            
            # Display results
            st.success("Test Results:")
            col1, col2 = st.columns(2)
            col1.metric("Maximum Dry Density", f"{theoretical_max_density:.2f} g/cm³")
            col2.metric("Optimum Moisture Content", f"{theoretical_opt_moisture:.1f}%")
            
            # Plot compaction curve
            fig, ax = plt.subplots(figsize=(10, 6))
            
            # Plot test points
            ax.plot(df_comp['Moisture'], df_comp['Density'], 'bo', markersize=10, label='Test Data')
            
            # Plot fitted curve
            ax.plot(moisture_range, density_curve, 'r-', linewidth=2, label='Fitted Curve')
            
            # Mark maximum point
            ax.plot(theoretical_opt_moisture, theoretical_max_density, 'g*', markersize=15, label='Maximum Density')
            
            # Add Zero Air Voids curve (ρ_w = 1 g/cm³)
            zav_moisture = np.linspace(5, 30, 100)
            zav_density = (specific_gravity * 1.0) / (1 + (zav_moisture/100) * specific_gravity)
            ax.plot(zav_moisture, zav_density, 'k--', alpha=0.5, label='Zero Air Voids')
            
            ax.set_xlabel('Moisture Content (%)')
            ax.set_ylabel('Dry Density (g/cm³)')
            ax.set_title(f'{test_type} - Moisture-Density Relationship')
            ax.grid(True, alpha=0.3)
            ax.legend()
            
            st.pyplot(fig)
            
            # Generate PDF Report
            test_data = {
                'Test Type': test_type,
                'Maximum Dry Density': f"{theoretical_max_density:.2f} g/cm³",
                'Optimum Moisture Content': f"{theoretical_opt_moisture:.1f}%",
                'Specific Gravity': f"{specific_gravity:.2f}",
                'Test Standard': 'ASTM D698' if 'Standard' in test_type else 'ASTM D1557'
            }
            
            graphs = [plot_to_buffer(fig)]
            pdf_buffer = create_pdf_report("Compaction Test", st.session_state.project_info, test_data, graphs)
            
            st.download_button(
                label="📄 Download PDF Report",
                data=pdf_buffer,
                file_name=f"Compaction_Test_Report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf",
                mime="application/pdf"
            )
    
    st.markdown('</div>', unsafe_allow_html=True)

elif soil_test == "California Bearing Ratio (CBR)":
    st.markdown('<div class="test-card">', unsafe_allow_html=True)
    st.subheader("California Bearing Ratio Test (ASTM D1883)")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("**Test Setup**")
        test_condition = st.selectbox("Test Condition", ["Soaked", "Unsoaked"])
        compaction_effort = st.selectbox("Compaction Effort", ["10 Blows", "25 Blows", "56 Blows"])
        
        st.write("**Penetration Test Data**")
        penetration_values = [0.0, 0.025, 0.050, 0.075, 0.100, 0.125, 0.150, 0.175, 0.200, 0.300, 0.400, 0.500]
        load_data = []
        
        for pen in penetration_values:
            load = st.number_input(f"Load at {pen:.3f} inch (lbs)", min_value=0.0, max_value=5000.0, 
                                 key=f"cbr_load_{pen}", step=10.0)
            if load > 0:
                load_data.append({'Penetration': pen, 'Load': load})
    
    with col2:
        st.write("**Sample Information**")
        initial_moisture = st.number_input("Initial Moisture Content (%)", min_value=0.0, max_value=50.0)
        final_moisture = st.number_input("Final Moisture Content (%)", min_value=0.0, max_value=50.0)
        dry_density = st.number_input("Dry Density (g/cm³)", min_value=1.0, max_value=2.5)
        
        if test_condition == "Soaked":
            swell_reading = st.number_input("Swell Reading (%)", min_value=0.0, max_value=10.0, step=0.1)
    
    if st.button("Calculate CBR"):
        if len(load_data) >= 5:
            df_cbr = pd.DataFrame(load_data)
            
            # Calculate stress (psi) = Load (lbs) / Area (3 sq.in.) per ASTM D1883
            df_cbr['Stress'] = df_cbr['Load'] / 3.0
            
            # Standard stress values at 0.1" and 0.2" (ASTM D1883)
            standard_stress_01 = 1000  # psi
            standard_stress_02 = 1500  # psi
            
            # Interpolate to find stress at 0.1" and 0.2"
            stress_01 = np.interp(0.1, df_cbr['Penetration'], df_cbr['Stress'])
            stress_02 = np.interp(0.2, df_cbr['Penetration'], df_cbr['Stress'])
            
            # Calculate CBR values
            cbr_01 = (stress_01 / standard_stress_01) * 100
            cbr_02 = (stress_02 / standard_stress_02) * 100
            
            # Design CBR (typically the value at 0.1")
            design_cbr = cbr_01
            
            # Display results
            st.success("Test Results:")
            col1, col2, col3 = st.columns(3)
            col1.metric("CBR at 0.1 inch", f"{cbr_01:.1f}%")
            col2.metric("CBR at 0.2 inch", f"{cbr_02:.1f}%")
            col3.metric("Design CBR", f"{design_cbr:.1f}%")
            
            # Plot load-penetration curve
            fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))
            
            # Load vs Penetration
            ax1.plot(df_cbr['Penetration'], df_cbr['Load'], 'bo-', markersize=8, linewidth=2)
            ax1.axvline(x=0.1, color='r', linestyle='--', alpha=0.5, label='0.1 inch')
            ax1.axvline(x=0.2, color='g', linestyle='--', alpha=0.5, label='0.2 inch')
            ax1.set_xlabel('Penetration (inches)')
            ax1.set_ylabel('Load (lbs)')
            ax1.set_title('Load vs Penetration Curve (ASTM D1883)')
            ax1.grid(True, alpha=0.3)
            ax1.legend()
            
            # Stress vs Penetration
            ax2.plot(df_cbr['Penetration'], df_cbr['Stress'], 'ro-', markersize=8, linewidth=2)
            ax2.axvline(x=0.1, color='r', linestyle='--', alpha=0.5)
            ax2.axvline(x=0.2, color='g', linestyle='--', alpha=0.5)
            ax2.axhline(y=stress_01, color='r', linestyle=':', alpha=0.5)
            ax2.axhline(y=stress_02, color='g', linestyle=':', alpha=0.5)
            ax2.set_xlabel('Penetration (inches)')
            ax2.set_ylabel('Stress (psi)')
            ax2.set_title('Stress vs Penetration Curve (ASTM D1883)')
            ax2.grid(True, alpha=0.3)
            
            plt.tight_layout()
            st.pyplot(fig)
            
            # Generate PDF Report
            test_data = {
                'Test Condition': test_condition,
                'Compaction Effort': compaction_effort,
                'Initial Moisture Content': f"{initial_moisture:.1f}%",
                'Final Moisture Content': f"{final_moisture:.1f}%",
                'Dry Density': f"{dry_density:.2f} g/cm³",
                'CBR at 0.1 inch': f"{cbr_01:.1f}%",
                'CBR at 0.2 inch': f"{cbr_02:.1f}%",
                'Design CBR': f"{design_cbr:.1f}%",
                'Test Standard': 'ASTM D1883'
            }
            
            if test_condition == "Soaked":
                test_data['Swell'] = f"{swell_reading:.1f}%"
            
            graphs = [plot_to_buffer(fig)]
            pdf_buffer = create_pdf_report("California Bearing Ratio", st.session_state.project_info, test_data, graphs)
            
            st.download_button(
                label="📄 Download PDF Report",
                data=pdf_buffer,
                file_name=f"CBR_Test_Report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf",
                mime="application/pdf"
            )
    
    st.markdown('</div>', unsafe_allow_html=True)

elif test_category == "Concrete Tests":    st.markdown('Concrete Testing Section', unsafe_allow_html=True)    concrete_test = st.selectbox(        "Select Concrete Test",        ["Slump Test", "Compressive Strength (Cube/Cylinder)", "Water-Cement Ratio", "Fineness Modulus", "Unit Weight Test"]    )
if concrete_test == "Slump Test":
    st.markdown('<div class="test-card">', unsafe_allow_html=True)
    st.subheader("Slump Test (ASTM C143)")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("**Test Parameters**")
        slump = st.number_input("Measured Slump (cm)", min_value=0.0, max_value=30.0, step=0.1)
        slump_type = st.selectbox("Slump Type Observed", ["True", "Shear", "Collapse"])
    
    with col2:
        st.write("**Acceptance Criteria**")
        min_slump = st.number_input("Minimum Acceptable Slump (cm)", min_value=0.0, max_value=30.0, value=5.0)
        max_slump = st.number_input("Maximum Acceptable Slump (cm)", min_value=0.0, max_value=30.0, value=12.5)
    
    if st.button("Calculate Slump Test Results"):
        # Validation
        if max_slump < min_slump:
            st.error("Maximum slump cannot be less than minimum slump.")
        elif slump_type in ["Shear", "Collapse"]:
            st.warning(f"Slump type '{slump_type}' indicates potential issues with mix consistency.")
        else:
            # Check acceptability
            is_acceptable = min_slump <= slump <= max_slump
            status = "Pass" if is_acceptable else "Fail"
            
            # Display results
            st.success("Test Results:")
            col1, col2, col3 = st.columns(3)
            col1.metric("Measured Slump", f"{slump:.1f} cm")
            col2.metric("Slump Type", slump_type)
            col3.metric("Status", status)
            
            # Generate PDF Report
            test_data = {
                'Measured Slump': f"{slump:.1f} cm",
                'Slump Type': slump_type,
                'Minimum Acceptable Slump': f"{min_slump:.1f} cm",
                'Maximum Acceptable Slump': f"{max_slump:.1f} cm",
                'Status': status,
                'Test Standard': 'ASTM C143'
            }
            
            graphs = []
            pdf_buffer = create_pdf_report("Slump Test", st.session_state.project_info, test_data, graphs)
            
            st.download_button(
                label="📄 Download PDF Report",
                data=pdf_buffer,
                file_name=f"Slump_Test_Report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf",
                mime="application/pdf"
            )
    
    st.markdown('</div>', unsafe_allow_html=True)

elif concrete_test == "Compressive Strength (Cube/Cylinder)":
    st.markdown('<div class="test-card">', unsafe_allow_html=True)
    st.subheader("Compressive Strength Test (ASTM C39)")
    
    specimen_type = st.radio("Specimen Type", ["Cube", "Cylinder"])
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("**Specimen Dimensions**")
        if specimen_type == "Cube":
            side = st.number_input("Cube Side Length (mm)", min_value=100.0, max_value=200.0, value=150.0)
            area = side ** 2  # mm²
        else:
            diameter = st.number_input("Cylinder Diameter (mm)", min_value=100.0, max_value=200.0, value=150.0)
            height = st.number_input("Cylinder Height (mm)", min_value=200.0, max_value=400.0, value=300.0)
            area = np.pi * (diameter / 2) ** 2  # mm²
    
    with col2:
        st.write("**Test Data Input**")
        num_specimens = st.number_input("Number of Specimens", min_value=1, max_value=5, value=3)
        
        strength_data = []
        for i in range(num_specimens):
            st.write(f"Specimen {i+1}")
            cols = st.columns(3)
            age = cols[0].number_input(f"Age (days)", min_value=1, max_value=90, value=28, key=f"strength_age_{i}")
            load = cols[1].number_input(f"Failure Load (kN)", min_value=0.0, max_value=5000.0, key=f"strength_load_{i}")
            if age > 0 and load > 0:
                strength = (load * 1000) / area * 0.001  # Convert kN to N, divide by mm², convert to MPa
                strength_data.append({'Age': age, 'Load': load, 'Strength': strength})
    
    if st.button("Calculate Compressive Strength"):
        if strength_data:
            df_strength = pd.DataFrame(strength_data)
            avg_strength = df_strength['Strength'].mean()
            
            # Display results
            st.success("Test Results:")
            col1, col2 = st.columns(2)
            col1.metric("Average Compressive Strength", f"{avg_strength:.1f} MPa")
            col2.metric("Number of Specimens", len(df_strength))
            
            # Plot strength vs age
            fig, ax = plt.subplots(figsize=(10, 6))
            ax.plot(df_strength['Age'], df_strength['Strength'], 'bo-', markersize=8, label='Test Data')
            ax.axhline(y=avg_strength, color='r', linestyle='--', label=f'Average Strength: {avg_strength:.1f} MPa')
            
            ax.set_xlabel('Age (days)')
            ax.set_ylabel('Compressive Strength (MPa)')
            ax.set_title(f'Compressive Strength vs Age (ASTM C39 - {specimen_type})')
            ax.grid(True, alpha=0.3)
            ax.legend()
            
            st.pyplot(fig)
            
            # Generate PDF Report
            test_data = {
                'Specimen Type': specimen_type,
                'Average Compressive Strength': f"{avg_strength:.1f} MPa",
                'Number of Specimens': len(df_strength),
                'Test Standard': 'ASTM C39'
            }
            if specimen_type == "Cube":
                test_data['Cube Side Length'] = f"{side:.1f} mm"
            else:
                test_data['Cylinder Diameter'] = f"{diameter:.1f} mm"
                test_data['Cylinder Height'] = f"{height:.1f} mm"
            
            graphs = [plot_to_buffer(fig)]
            pdf_buffer = create_pdf_report("Compressive Strength", st.session_state.project_info, test_data, graphs)
            
            st.download_button(
                label="📄 Download PDF Report",
                data=pdf_buffer,
                file_name=f"Compressive_Strength_Report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf",
                mime="application/pdf"
            )
    
    st.markdown('</div>', unsafe_allow_html=True)

elif concrete_test == "Water-Cement Ratio":
    st.markdown('<div class="test-card">', unsafe_allow_html=True)
    st.subheader("Water-Cement Ratio Calculation")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("**Mix Parameters**")
        water_weight = st.number_input("Weight of Water (kg)", min_value=0.0, max_value=1000.0)
        cement_weight = st.number_input("Weight of Cement (kg)", min_value=0.0, max_value=1000.0)
    
    with col2:
        st.write("**Validation Range**")
        min_wc = st.number_input("Minimum Acceptable W/C Ratio", min_value=0.0, max_value=1.0, value=0.3)
        max_wc = st.number_input("Maximum Acceptable W/C Ratio", min_value=0.0, max_value=1.0, value=0.7)
    
    if st.button("Calculate Water-Cement Ratio"):
        if cement_weight > 0:
            wc_ratio = water_weight / cement_weight
            is_acceptable = min_wc <= wc_ratio <= max_wc
            status = "Pass" if is_acceptable else "Fail"
            
            # Display results
            st.success("Test Results:")
            col1, col2, col3 = st.columns(3)
            col1.metric("Water-Cement Ratio", f"{wc_ratio:.2f}")
            col2.metric("Water Weight", f"{water_weight:.1f} kg")
            col3.metric("Status", status)
            
            # Generate PDF Report
            test_data = {
                'Water-Cement Ratio': f"{wc_ratio:.2f}",
                'Water Weight': f"{water_weight:.1f} kg",
                'Cement Weight': f"{cement_weight:.1f} kg",
                'Minimum Acceptable W/C': f"{min_wc:.2f}",
                'Maximum Acceptable W/C': f"{max_wc:.2f}",
                'Status': status
            }
            
            graphs = []
            pdf_buffer = create_pdf_report("Water-Cement Ratio", st.session_state.project_info, test_data, graphs)
            
            st.download_button(
                label="📄 Download PDF Report",
                data=pdf_buffer,
                file_name=f"Water_Cement_Ratio_Report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf",
                mime="application/pdf"
            )
        else:
            st.error("Cement weight must be greater than zero.")
    
    st.markdown('</div>', unsafe_allow_html=True)

elif concrete_test == "Fineness Modulus":
    st.markdown('<div class="test-card">', unsafe_allow_html=True)
    st.subheader("Fineness Modulus Test (ASTM C136)")
    
    st.write("**Sieve Analysis Data**")
    sieve_sizes = [4.75, 2.36, 1.18, 0.6, 0.3, 0.15, 0.075]  # mm
    fm_data = []
    
    for size in sieve_sizes:
        retained = st.number_input(f"Weight Retained on {size} mm Sieve (g)", min_value=0.0, key=f"fm_retained_{size}")
        if retained >= 0:
            fm_data.append({'Sieve Size': size, 'Retained': retained})
    
    if st.button("Calculate Fineness Modulus"):
        df_fm = pd.DataFrame(fm_data)
        total_retained = df_fm['Retained'].sum()
        
        if total_retained > 0:
            # Calculate cumulative % retained
            df_fm['Cumulative Retained'] = df_fm['Retained'].cumsum()
            df_fm['Cumulative % Retained'] = (df_fm['Cumulative Retained'] / total_retained) * 100
            
            # Fineness Modulus = Sum(Cumulative % Retained) / 100
            fm = df_fm['Cumulative % Retained'].sum() / 100
            
            # Display results
            st.success("Test Results:")
            col1, col2 = st.columns(2)
            col1.metric("Fineness Modulus", f"{fm:.2f}")
            col2.metric("Total Weight Retained", f"{total_retained:.1f} g")
            
            # Plot gradation curve
            fig, ax = plt.subplots(figsize=(10, 6))
            ax.semilogx(df_fm['Sieve Size'], df_fm['Cumulative % Retained'], 'bo-', markersize=8, label='Gradation')
            
            ax.set_xlabel('Sieve Size (mm, log scale)')
            ax.set_ylabel('Cumulative % Retained')
            ax.set_title('Sieve Analysis - Fineness Modulus (ASTM C136)')
            ax.grid(True, which="both", ls="-", alpha=0.3)
            ax.legend()
            ax.invert_xaxis()  # Larger sieves on left
            
            st.pyplot(fig)
            
            # Generate PDF Report
            test_data = {
                'Fineness Modulus': f"{fm:.2f}",
                'Total Weight Retained': f"{total_retained:.1f} g",
                'Test Standard': 'ASTM C136'
            }
            
            graphs = [plot_to_buffer(fig)]
            pdf_buffer = create_pdf_report("Fineness Modulus", st.session_state.project_info, test_data, graphs)
            
            st.download_button(
                label="📄 Download PDF Report",
                data=pdf_buffer,
                file_name=f"Fineness_Modulus_Report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf",
                mime="application/pdf"
            )
        else:
            st.error("Total weight retained must be greater than zero.")
    
    st.markdown('</div>', unsafe_allow_html=True)

elif concrete_test == "Unit Weight Test":
    st.markdown('<div class="test-card">', unsafe_allow_html=True)
    st.subheader("Unit Weight Test (ASTM C138)")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("**Test Parameters**")
        volume = st.number_input("Container Volume (m³)", min_value=0.001, max_value=0.1, value=0.01, step=0.001)
        weight_empty = st.number_input("Empty Container Weight (kg)", min_value=0.0, max_value=100.0)
        weight_filled = st.number_input("Filled Container Weight (kg)", min_value=0.0, max_value=200.0)
    
    with col2:
        st.write("**Validation Range**")
        min_density = st.number_input("Minimum Acceptable Density (kg/m³)", min_value=1000.0, max_value=3000.0, value=2200.0)
        max_density = st.number_input("Maximum Acceptable Density (kg/m³)", min_value=1000.0, max_value=3000.0, value=2500.0)
    
    if st.button("Calculate Unit Weight"):
        if volume > 0 and weight_filled >= weight_empty:
            unit_weight = (weight_filled - weight_empty) / volume  # kg/m³
            is_acceptable = min_density <= unit_weight <= max_density
            status = "Pass" if is_acceptable else "Fail"
            
            # Display results
            st.success("Test Results:")
            col1, col2, col3 = st.columns(3)
            col1.metric("Unit Weight", f"{unit_weight:.1f} kg/m³")
            col2.metric("Container Volume", f"{volume:.3f} m³")
            col3.metric("Status", status)
            
            # Generate PDF Report
            test_data = {
                'Unit Weight': f"{unit_weight:.1f} kg/m³",
                'Container Volume': f"{volume:.3f} m³",
                'Empty Container Weight': f"{weight_empty:.1f} kg",
                'Filled Container Weight': f"{weight_filled:.1f} kg",
                'Minimum Acceptable Density': f"{min_density:.1f} kg/m³",
                'Maximum Acceptable Density': f"{max_density:.1f} kg/m³",
                'Status': status,
                'Test Standard': 'ASTM C138'
            }
            
            graphs = []
            pdf_buffer = create_pdf_report("Unit Weight Test", st.session_state.project_info, test_data, graphs)
            
            st.download_button(
                label="📄 Download PDF Report",
                data=pdf_buffer,
                file_name=f"Unit_Weight_Test_Report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf",
                mime="application/pdf"
            )
        else:
            st.error("Invalid inputs: Ensure volume is positive and filled weight is at least equal to empty weight.")
    
    st.markdown('</div>', unsafe_allow_html=True)

Cleanup temporary files
if os.path.exists("temp_plot.png"):    os.remove("temp_plot.png")
