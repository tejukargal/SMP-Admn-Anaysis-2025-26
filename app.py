import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import os
import glob
from io import BytesIO

# Page configuration
st.set_page_config(
    page_title="SMP Admission Analysis 2025-26",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS for modern UI
st.markdown("""
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;700;800&display=swap" rel="stylesheet">
<style>
    * {
        font-family: 'Inter', sans-serif !important;
    }
    
    .main-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 15px;
        margin-bottom: 2rem;
        text-align: center;
        color: white;
        font-weight: 800;
        font-size: 2.5rem;
        box-shadow: 0 10px 30px rgba(0,0,0,0.2);
    }
    
    .metric-card {
        padding: 1.5rem;
        border-radius: 15px;
        text-align: center;
        color: white;
        font-weight: 800;
        margin: 0.5rem;
        box-shadow: 0 8px 25px rgba(0,0,0,0.15);
        transition: transform 0.3s ease;
    }
    
    .metric-card:hover {
        transform: translateY(-5px);
    }
    
    .metric-card-red {
        background: linear-gradient(135deg, #ff6b6b 0%, #ee5a52 100%);
    }
    
    .metric-card-teal {
        background: linear-gradient(135deg, #4ecdc4 0%, #44a08d 100%);
    }
    
    .metric-card-blue {
        background: linear-gradient(135deg, #45b7d1 0%, #096dd9 100%);
    }
    
    .course-box {
        padding: 1.5rem;
        border-radius: 12px;
        text-align: center;
        color: white;
        font-weight: 800;
        margin: 0.3rem;
        box-shadow: 0 6px 20px rgba(0,0,0,0.1);
        min-height: 100px;
        display: flex;
        flex-direction: column;
        justify-content: center;
    }
    
    .course-ce { background: linear-gradient(135deg, #ff9a9e 0%, #fad0c4 100%); }
    .course-me { background: linear-gradient(135deg, #a8edea 0%, #fed6e3 100%); }
    .course-ee { background: linear-gradient(135deg, #ffecd2 0%, #fcb69f 100%); }
    .course-cs { background: linear-gradient(135deg, #a8caba 0%, #5d4e75 100%); }
    .course-ec { background: linear-gradient(135deg, #d299c2 0%, #fef9d7 100%); }
    
    .section-separator {
        font-size: 1.8rem;
        font-weight: 800;
        margin: 2rem 0 1rem 0;
        color: #2c3e50;
    }
    
    .styled-table {
        font-size: 1.3rem;
        font-weight: 700;
    }
    
    .table-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        font-weight: 800;
        font-size: 1.4rem;
    }
    
    .subtotal-row {
        background: linear-gradient(135deg, #ffeaa7 0%, #fab1a0 100%);
        font-weight: 800;
        font-size: 1.4rem;
    }
    
    .grand-total-row {
        background: linear-gradient(135deg, #a29bfe 0%, #6c5ce7 100%);
        color: white;
        font-weight: 800;
        font-size: 1.5rem;
    }
    
    .filter-container {
        background: #f8f9fa;
        padding: 1.5rem;
        border-radius: 12px;
        margin-bottom: 1rem;
        border: 2px solid #e9ecef;
    }
    
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 8px;
        padding: 0.5rem 1.5rem;
        font-weight: 700;
        transition: all 0.3s ease;
        font-size: 0.8rem;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 5px 15px rgba(0,0,0,0.2);
    }
    
    /* Reset button styling */
    div[data-testid="column"]:nth-child(2) .stButton > button {
        background: linear-gradient(135deg, #ff6b6b 0%, #ee5a52 100%);
        color: white;
    }
    
    div[data-testid="column"]:nth-child(2) .stButton > button:hover {
        background: linear-gradient(135deg, #ff5252 0%, #d32f2f 100%);
        transform: translateY(-2px);
        box-shadow: 0 5px 15px rgba(255, 107, 107, 0.4);
    }
    
    .filter-section {
        background: #e9ecef;
        padding: 1rem;
        border-radius: 8px;
        margin: 0.5rem;
        border: 1px solid #dee2e6;
    }
    
    .filter-title {
        font-weight: 700;
        font-size: 1rem;
        color: #495057;
        margin-bottom: 0.5rem;
    }
    
    .stCheckbox > label {
        font-weight: 600;
        font-size: 0.85rem;
        color: #2c3e50;
    }
    
    .stCheckbox > div {
        background: transparent;
        padding: 0.2rem;
        border-radius: 4px;
        margin: 0.1rem;
        transition: all 0.3s ease;
    }
    
    .stCheckbox > div[data-checked="true"] {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border: 2px solid #5a67d8;
        color: white;
    }
    
    .stCheckbox > div[data-checked="false"] {
        background: #f8f9fa;
        border: 2px solid #dee2e6;
        color: #495057;
    }
    
    .stCheckbox input[type="checkbox"]:checked + div {
        background: linear-gradient(135deg, #48bb78 0%, #38a169 100%) !important;
        border: 2px solid #38a169 !important;
        box-shadow: 0 2px 8px rgba(56, 161, 105, 0.3) !important;
    }
    
    .stCheckbox input[type="checkbox"]:not(:checked) + div {
        background: #f8f9fa !important;
        border: 2px solid #dee2e6 !important;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1) !important;
    }
    
    .stCheckbox label span {
        transition: color 0.3s ease;
    }
    
    .stCheckbox input[type="checkbox"]:checked + div label span {
        color: white !important;
        font-weight: 700 !important;
    }
    
    .stSelectbox > div > div {
        border-radius: 8px;
        border: 2px solid #e9ecef;
    }
    
    .stTabs [data-baseweb="tab-list"] {
        gap: 2px;
    }
    
    .stTabs [data-baseweb="tab"] {
        height: 50px;
        padding: 0px 20px;
        background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
        border-radius: 10px 10px 0 0;
        color: #495057;
        font-weight: 700;
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
    }
</style>
""", unsafe_allow_html=True)

@st.cache_data
def load_data():
    """Load and preprocess CSV data"""
    try:
        # Look for CSV files in the current directory
        csv_files = glob.glob("*.csv")
        
        if not csv_files:
            st.error("No CSV files found in the project directory!")
            return None
            
        # Load the first CSV file found
        file_path = csv_files[0]
        
        # Try different encodings for CSV reading
        encodings = ['utf-8', 'latin-1', 'cp1252', 'iso-8859-1']
        df = None
        
        for encoding in encodings:
            try:
                df = pd.read_csv(file_path, encoding=encoding)
                break
            except UnicodeDecodeError:
                continue
        
        if df is None:
            st.error(f"Could not read CSV file with any supported encoding. Please ensure the file is properly formatted.")
            return None
        
        # Standardize column names
        df.columns = df.columns.str.strip()
        
        # Filter data: only "In" status students, exclude "Due Fee" in remarks
        df_filtered = df[
            (df['In/Out'].str.strip().str.upper() == 'IN') &
            (~df['Remarks'].str.contains('Due Fee', na=False, case=False))
        ].copy()
        
        # Convert date to dd-mmm-yy format
        if 'Date' in df_filtered.columns:
            df_filtered['Date'] = pd.to_datetime(df_filtered['Date'], errors='coerce')
            df_filtered['Formatted_Date'] = df_filtered['Date'].dt.strftime('%d-%b-%y')
        
        return df_filtered
        
    except Exception as e:
        st.error(f"Error loading data: {str(e)}")
        return None

def create_metric_cards(df):
    """Create summary metric cards"""
    total_students = len(df)
    total_courses = df['Course'].nunique() if 'Course' in df.columns else 0
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown(f"""
        <div class="metric-card metric-card-red">
            <h2>{total_students}</h2>
            <h4>Total Students</h4>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="metric-card metric-card-teal">
            <h2>{total_courses}</h2>
            <h4>Total Courses</h4>
        </div>
        """, unsafe_allow_html=True)

def create_course_strength_boxes(df):
    """Create course-wise student strength boxes"""
    if 'Course' not in df.columns:
        return
        
    course_counts = df['Course'].value_counts().sort_index()
    courses = list(course_counts.index)
    
    # Divide courses into rows if more than 5
    if len(courses) <= 5:
        cols = st.columns(len(courses))
        for i, (course, count) in enumerate(course_counts.items()):
            course_class = f"course-{course.lower()}" if course.lower() in ['ce', 'me', 'ee', 'cs', 'ec'] else 'course-cs'
            with cols[i]:
                st.markdown(f"""
                <div class="course-box {course_class}">
                    <h2>{course}</h2>
                    <h4>{count} Students</h4>
                </div>
                """, unsafe_allow_html=True)
    else:
        # Split into multiple rows
        mid = len(courses) // 2 + len(courses) % 2
        row1_courses = courses[:mid]
        row2_courses = courses[mid:]
        
        cols1 = st.columns(len(row1_courses))
        for i, course in enumerate(row1_courses):
            count = course_counts[course]
            course_class = f"course-{course.lower()}" if course.lower() in ['ce', 'me', 'ee', 'cs', 'ec'] else 'course-cs'
            with cols1[i]:
                st.markdown(f"""
                <div class="course-box {course_class}">
                    <h2>{course}</h2>
                    <h4>{count} Students</h4>
                </div>
                """, unsafe_allow_html=True)
        
        cols2 = st.columns(len(row2_courses))
        for i, course in enumerate(row2_courses):
            count = course_counts[course]
            course_class = f"course-{course.lower()}" if course.lower() in ['ce', 'me', 'ee', 'cs', 'ec'] else 'course-cs'
            with cols2[i]:
                st.markdown(f"""
                <div class="course-box {course_class}">
                    <h2>{course}</h2>
                    <h4>{count} Students</h4>
                </div>
                """, unsafe_allow_html=True)

def create_year_course_stats_table(df):
    """Create year-course statistics table with styling"""
    if 'Year' not in df.columns or 'Course' not in df.columns:
        return
        
    # Create pivot table
    stats_table = df.groupby(['Year', 'Course']).size().reset_index(name='Total Students')
    
    # Create a formatted table for display
    display_data = []
    
    for year in sorted(df['Year'].unique()):
        year_data = stats_table[stats_table['Year'] == year]
        
        for _, row in year_data.iterrows():
            display_data.append({
                'Year': row['Year'],
                'Course': row['Course'],
                'Total Students': row['Total Students']
            })
        
        # Add subtotal row
        year_total = year_data['Total Students'].sum()
        display_data.append({
            'Year': f'**{year} - Subtotal**',
            'Course': '**All Courses**',
            'Total Students': f'**{year_total}**'
        })
    
    # Add grand total
    grand_total = df.shape[0]
    display_data.append({
        'Year': '**GRAND TOTAL**',
        'Course': '**ALL YEARS**',
        'Total Students': f'**{grand_total}**'
    })
    
    display_df = pd.DataFrame(display_data)
    
    st.markdown('<div class="section-separator">📊 Year & Course Statistics</div>', unsafe_allow_html=True)
    st.dataframe(
        display_df,
        use_container_width=True,
        hide_index=True,
        column_config={
            "Year": st.column_config.TextColumn("Year", width="medium"),
            "Course": st.column_config.TextColumn("Course", width="medium"),
            "Total Students": st.column_config.TextColumn("Total Students", width="medium")
        }
    )

def create_course_chart(df):
    """Create course-wise bar chart"""
    if 'Course' not in df.columns:
        return
        
    course_year_stats = df.groupby(['Course', 'Year']).size().reset_index(name='Students')
    
    fig = px.bar(
        course_year_stats,
        x='Course',
        y='Students',
        color='Year',
        title='Course-wise Student Distribution by Academic Year',
        text='Students',
        color_discrete_sequence=px.colors.qualitative.Set3
    )
    
    fig.update_layout(
        font_family="Inter",
        font_size=14,
        title_font_size=18,
        title_font_family="Inter",
        title_font_color="#2c3e50",
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        height=500
    )
    
    fig.update_traces(texttemplate='%{text}', textposition='outside')
    fig.update_xaxes(title_font_size=16, tickfont_size=14)
    fig.update_yaxes(title_font_size=16, tickfont_size=14)
    
    st.plotly_chart(fig, use_container_width=True)

def create_datewise_stats(df):
    """Create date-wise admission statistics"""
    if 'Formatted_Date' not in df.columns or 'Course' not in df.columns:
        return
        
    # Group by date and course
    date_stats = df.groupby(['Formatted_Date', 'Course']).size().reset_index(name='Admissions')
    
    # Create display table with subtotals
    display_data = []
    
    for date in sorted(df['Formatted_Date'].unique(), key=lambda x: pd.to_datetime(x, format='%d-%b-%y')):
        date_data = date_stats[date_stats['Formatted_Date'] == date]
        
        for _, row in date_data.iterrows():
            display_data.append({
                'Date': row['Formatted_Date'],
                'Course': row['Course'],
                'Admissions': row['Admissions']
            })
        
        # Add subtotal
        date_total = date_data['Admissions'].sum()
        display_data.append({
            'Date': f'**{date} - Subtotal**',
            'Course': '**All Courses**',
            'Admissions': f'**{date_total}**'
        })
    
    # Add grand total
    grand_total = df.shape[0]
    display_data.append({
        'Date': '**GRAND TOTAL**',
        'Course': '**ALL DATES**',
        'Admissions': f'**{grand_total}**'
    })
    
    display_df = pd.DataFrame(display_data)
    
    st.markdown('<div class="section-separator">📅 Date-wise Admission Statistics</div>', unsafe_allow_html=True)
    st.dataframe(
        display_df,
        use_container_width=True,
        hide_index=True,
        column_config={
            "Date": st.column_config.TextColumn("Date", width="medium"),
            "Course": st.column_config.TextColumn("Course", width="medium"),
            "Admissions": st.column_config.TextColumn("Admissions", width="medium")
        }
    )
    
    # Create chart
    chart_data = df.groupby(['Formatted_Date', 'Course']).size().reset_index(name='Admissions')
    
    fig = px.bar(
        chart_data,
        x='Formatted_Date',
        y='Admissions',
        color='Course',
        title='Daily Admission Trends by Course',
        text='Admissions',
        color_discrete_sequence=px.colors.qualitative.Set2
    )
    
    fig.update_layout(
        font_family="Inter",
        font_size=14,
        title_font_size=18,
        title_font_family="Inter",
        title_font_color="#2c3e50",
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        height=500,
        xaxis_tickangle=-45
    )
    
    fig.update_traces(texttemplate='%{text}', textposition='outside')
    fig.update_xaxes(title_font_size=16, tickfont_size=14)
    fig.update_yaxes(title_font_size=16, tickfont_size=14)
    
    st.plotly_chart(fig, use_container_width=True)

def create_student_list_tab(df):
    """Create filtered student list with export functionality"""
    st.markdown('<div class="section-separator">👥 Student List with Filters</div>', unsafe_allow_html=True)
    
    # Create two columns for Year and Course filters
    filter_col1, filter_col2 = st.columns(2)
    
    # Year filter section
    with filter_col1:
        st.markdown('<div class="filter-section">', unsafe_allow_html=True)
        st.markdown('<div class="filter-title">Year</div>', unsafe_allow_html=True)
        
        available_years = sorted(df['Year'].unique()) if 'Year' in df.columns else []
        
        # Initialize session state for years (default: unchecked)
        if 'selected_years' not in st.session_state:
            st.session_state.selected_years = []
        
        # Check if all years are selected for "All" checkbox state
        all_years_selected = len(st.session_state.selected_years) == len(available_years) and set(st.session_state.selected_years) == set(available_years)
        
        # All checkbox for years with toggle logic
        if st.checkbox("All", value=all_years_selected, key="all_years"):
            # If "All" is checked, select all years
            st.session_state.selected_years = available_years.copy()
        else:
            # If "All" is unchecked, clear all years
            if all_years_selected:  # Only clear if it was previously all selected
                st.session_state.selected_years = []
        
        # Individual year checkboxes in rows
        year_rows = [available_years[i:i+3] for i in range(0, len(available_years), 3)]
        for row in year_rows:
            year_cols = st.columns(len(row))
            for i, year in enumerate(row):
                with year_cols[i]:
                    is_checked = year in st.session_state.selected_years
                    # Individual checkbox change
                    if st.checkbox(year, value=is_checked, key=f"year_{year}"):
                        if year not in st.session_state.selected_years:
                            st.session_state.selected_years.append(year)
                    else:
                        if year in st.session_state.selected_years:
                            st.session_state.selected_years.remove(year)
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Course filter section
    with filter_col2:
        st.markdown('<div class="filter-section">', unsafe_allow_html=True)
        st.markdown('<div class="filter-title">Course</div>', unsafe_allow_html=True)
        
        available_courses = sorted(df['Course'].unique()) if 'Course' in df.columns else []
        
        # Initialize session state for courses (default: unchecked)
        if 'selected_courses' not in st.session_state:
            st.session_state.selected_courses = []
        
        # Check if all courses are selected for "All" checkbox state
        all_courses_selected = len(st.session_state.selected_courses) == len(available_courses) and set(st.session_state.selected_courses) == set(available_courses)
        
        # All checkbox for courses with toggle logic
        if st.checkbox("All", value=all_courses_selected, key="all_courses"):
            # If "All" is checked, select all courses
            st.session_state.selected_courses = available_courses.copy()
        else:
            # If "All" is unchecked, clear all courses
            if all_courses_selected:  # Only clear if it was previously all selected
                st.session_state.selected_courses = []
        
        # Individual course checkboxes in rows
        course_rows = [available_courses[i:i+3] for i in range(0, len(available_courses), 3)]
        for row in course_rows:
            course_cols = st.columns(len(row))
            for i, course in enumerate(row):
                with course_cols[i]:
                    is_checked = course in st.session_state.selected_courses
                    # Individual checkbox change
                    if st.checkbox(course, value=is_checked, key=f"course_{course}"):
                        if course not in st.session_state.selected_courses:
                            st.session_state.selected_courses.append(course)
                    else:
                        if course in st.session_state.selected_courses:
                            st.session_state.selected_courses.remove(course)
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Reset and Generate buttons
    col1, col2, col3, col4, col5 = st.columns([2, 1, 1, 1, 2])
    
    with col2:
        if st.button("🔄 Reset", use_container_width=True):
            st.session_state.selected_years = []
            st.session_state.selected_courses = []
            st.rerun()
    
    with col4:
        generate_list = st.button("📋 Generate List", use_container_width=True)
    
    st.markdown("---")
    
    # Display data only when Generate List button is clicked
    if generate_list:
        if st.session_state.selected_years and st.session_state.selected_courses:
            filtered_df = df[
                (df['Year'].isin(st.session_state.selected_years)) &
                (df['Course'].isin(st.session_state.selected_courses))
            ].copy()
            
            if not filtered_df.empty:
                # Add serial number (remove existing Sl No column if present)
                filtered_df.reset_index(drop=True, inplace=True)
                if 'Sl No' in filtered_df.columns:
                    filtered_df.drop('Sl No', axis=1, inplace=True)
                filtered_df.insert(0, 'Sl No', range(1, len(filtered_df) + 1))
                filtered_df['Sl No'] = filtered_df['Sl No'].apply(lambda x: f"{x:02d}")
                
                # Select and reorder columns for display
                display_columns = ['Sl No', 'Student Name', 'Father Name', 'Year', 'Course']
                
                # Add additional columns if they exist
                optional_columns = ['Admn Year', 'Cat', 'Formatted_Date']
                for col in optional_columns:
                    if col in filtered_df.columns:
                        if col == 'Formatted_Date':
                            display_columns.append('Date')
                            filtered_df['Date'] = filtered_df['Formatted_Date']
                        else:
                            display_columns.append(col)
                
                # Filter to available columns
                available_display_columns = [col for col in display_columns if col in filtered_df.columns]
                student_list = filtered_df[available_display_columns]
                
                # Add total count row
                total_row = pd.DataFrame([['**TOTAL**'] + [''] * (len(available_display_columns) - 2) + [f'**{len(student_list)} Students**']], 
                                       columns=available_display_columns)
                display_list = pd.concat([student_list, total_row], ignore_index=True)
                
                st.dataframe(
                    display_list,
                    use_container_width=True,
                    hide_index=True,
                    height=400
                )
                
                # Download button
                csv_buffer = BytesIO()
                student_list.to_csv(csv_buffer, index=False)
                csv_buffer.seek(0)
                
                st.download_button(
                    label="📥 Download CSV",
                    data=csv_buffer.getvalue(),
                    file_name=f"student_list_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                    mime="text/csv",
                    use_container_width=False
                )
                
            else:
                st.warning("No students found with the selected filters.")
        else:
            st.error("Please select at least one year and one course before generating the list.")

def main():
    """Main application function"""
    # Header
    st.markdown("""
    <div class="main-header">
        SMP Admission Analysis 2025-26
    </div>
    """, unsafe_allow_html=True)
    
    # Load data
    df = load_data()
    
    if df is None or df.empty:
        st.error("No valid data found. Please ensure your CSV file is in the project directory and contains the required columns.")
        return
    
    # Create tabs
    tab1, tab2, tab3 = st.tabs(["📈 Year & Course Statistics", "📅 Date-wise Admissions", "👥 Student List"])
    
    with tab1:
        # Summary metrics
        create_metric_cards(df)
        
        st.markdown('<div style="margin: 2rem 0;"></div>', unsafe_allow_html=True)
        
        # Course strength boxes
        st.markdown('<div class="section-separator">🎯 Course-wise Student Strength</div>', unsafe_allow_html=True)
        create_course_strength_boxes(df)
        
        st.markdown('<div style="margin: 2rem 0;"></div>', unsafe_allow_html=True)
        
        # Statistics table
        create_year_course_stats_table(df)
        
        st.markdown('<div style="margin: 2rem 0;"></div>', unsafe_allow_html=True)
        
        # Bar chart
        st.markdown('<div class="section-separator">📊 Course Distribution Chart</div>', unsafe_allow_html=True)
        create_course_chart(df)
    
    with tab2:
        create_datewise_stats(df)
    
    with tab3:
        create_student_list_tab(df)

if __name__ == "__main__":
    main()
