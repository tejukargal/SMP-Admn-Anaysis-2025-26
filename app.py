import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime
import os

# Configure page
st.set_page_config(
    page_title="Student Admission Analytics",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS for professional and colorful UI
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');
    
    .main-header {
        font-family: 'Inter', sans-serif;
        font-size: 2.2rem;
        font-weight: 800;
        color: #ffffff;
        text-align: center;
        margin-bottom: 1.5rem;
        padding: 1rem;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 12px;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4);
    }
    
    .metric-card {
        background: linear-gradient(135deg, #ffffff 0%, #f8f9ff 100%);
        padding: 1rem;
        border-radius: 12px;
        border: 2px solid transparent;
        background-clip: padding-box;
        box-shadow: 0 4px 20px rgba(0,0,0,0.08);
        text-align: center;
        position: relative;
        overflow: hidden;
    }
    
    .metric-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 4px;
        background: linear-gradient(90deg, #ff6b6b, #4ecdc4, #45b7d1, #96ceb4);
    }
    
    .metric-value {
        font-family: 'Inter', sans-serif;
        font-size: 2.2rem;
        font-weight: 800;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }
    
    .metric-label {
        font-family: 'Inter', sans-serif;
        font-size: 0.9rem;
        font-weight: 600;
        color: #6c757d;
        margin-top: 0.3rem;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    .stButton > button {
        font-family: 'Inter', sans-serif;
        width: 100%;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 8px;
        padding: 0.6rem 1.2rem;
        font-weight: 700;
        font-size: 0.95rem;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        transition: all 0.3s ease;
    }
    
    .stButton > button:hover {
        background: linear-gradient(135deg, #5a67d8 0%, #6b46c1 100%);
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(102, 126, 234, 0.4);
    }
    
    .report-section {
        background: linear-gradient(135deg, #ffffff 0%, #f8faff 100%);
        padding: 1.5rem;
        border-radius: 12px;
        margin: 0.8rem 0;
        border: 1px solid #e2e8f0;
        box-shadow: 0 4px 15px rgba(0,0,0,0.05);
    }
    
    .stDataFrame {
        font-family: 'Inter', sans-serif;
        font-weight: 500;
    }
    
    .stDataFrame th {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
    }
    
    .stTabs [data-baseweb="tab"] {
        font-family: 'Inter', sans-serif;
        font-weight: 700;
        background: linear-gradient(135deg, #f1f3f4 0%, #e8eaf6 100%);
        border-radius: 8px;
        color: #667eea;
        padding: 0.5rem 1rem;
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
    }
    
    .stSubheader {
        font-family: 'Inter', sans-serif;
        font-weight: 700;
        color: #2d3748;
        border-bottom: 3px solid;
        border-image: linear-gradient(90deg, #667eea, #764ba2) 1;
        padding-bottom: 0.5rem;
    }
    
    .stMultiSelect > div > div {
        font-family: 'Inter', sans-serif;
        font-weight: 600;
    }
    
    h1, h2, h3, h4, h5, h6 {
        font-family: 'Inter', sans-serif;
        font-weight: 700;
    }
    
    .metric-students { 
        background: linear-gradient(135deg, #ff6b6b 0%, #ee5a52 100%); 
        color: white; 
    }
    .metric-courses { 
        background: linear-gradient(135deg, #4ecdc4 0%, #44a08d 100%); 
        color: white; 
    }
    .metric-years { 
        background: linear-gradient(135deg, #45b7d1 0%, #096dd9 100%); 
        color: white; 
    }
</style>
""", unsafe_allow_html=True)

@st.cache_data
def load_data():
    """Load and process the student data from Excel file"""
    try:
        # Look for Excel files in the current directory
        excel_files = [f for f in os.listdir('.') if f.endswith(('.xlsx', '.xls'))]
        
        if not excel_files:
            st.error("No Excel file found in the project folder. Please add your student data Excel file.")
            return None
            
        # Use the first Excel file found
        file_path = excel_files[0]
        
        # Read Excel file
        df = pd.read_excel(file_path)
        
        # Clean column names (remove extra spaces)
        df.columns = df.columns.str.strip()
        
        # Standardize column names based on the image
        column_mapping = {
            'Sl No': 'sl_no',
            'Student Name': 'student_name',
            'Father Name': 'father_name',
            'Year': 'year',
            'Course': 'course',
            'Reg No': 'reg_no',
            'Cat': 'category',
            'Adm Type': 'admission_type',
            'Adm Cat': 'admission_category',
            'Date': 'date',
            'Rpt': 'report',
            'Admn Year': 'admission_year',
            'In/Out': 'status',
            'Remarks': 'remarks'
        }
        
        # Rename columns if they exist
        for old_name, new_name in column_mapping.items():
            if old_name in df.columns:
                df = df.rename(columns={old_name: new_name})
        
        # Convert date column to datetime and format
        if 'date' in df.columns:
            df['date'] = pd.to_datetime(df['date'], errors='coerce')
            df['date_formatted'] = df['date'].dt.strftime('%d-%b-%y')
        
        # Filter only admitted students ('In' status) and exclude Due Fee students
        if 'status' in df.columns:
            df = df[df['status'].str.upper() == 'IN']
        
        # Exclude students with "Due Fee" in remarks (only count paid students)
        if 'remarks' in df.columns:
            df = df[~df['remarks'].str.contains('Due Fee', case=False, na=False)]
        
        # Clean and standardize data
        for col in ['year', 'course', 'admission_year']:
            if col in df.columns:
                df[col] = df[col].astype(str).str.strip()
        
        return df
        
    except Exception as e:
        st.error(f"Error loading data: {str(e)}")
        return None

def create_year_course_stats(df):
    """Create year and course-wise statistics with subtotals and grand total"""
    if df is None or df.empty:
        return None
    
    # Group by year and course
    stats = df.groupby(['year', 'course']).agg({
        'student_name': 'count'
    }).reset_index()
    
    stats.columns = ['Year', 'Course', 'Total Students']
    
    # Add subtotals for each year
    subtotals = []
    years = stats['Year'].unique()
    
    for year in years:
        year_data = stats[stats['Year'] == year]
        subtotal = year_data['Total Students'].sum()
        subtotals.append({
            'Year': f"{year} - Subtotal", 
            'Course': '', 
            'Total Students': subtotal
        })
    
    # Add grand total
    grand_total = stats['Total Students'].sum()
    subtotals.append({
        'Year': 'GRAND TOTAL', 
        'Course': '', 
        'Total Students': grand_total
    })
    
    # Combine stats with subtotals
    final_stats = []
    for year in years:
        year_data = stats[stats['Year'] == year].to_dict('records')
        final_stats.extend(year_data)
        final_stats.append(next(s for s in subtotals if s['Year'] == f"{year} - Subtotal"))
    
    final_stats.append(subtotals[-1])  # Grand total
    
    return pd.DataFrame(final_stats), stats

def create_datewise_stats(df):
    """Create date-wise admission statistics with totals"""
    if df is None or df.empty or 'date' not in df.columns:
        return None
    
    # Group by date and course
    date_stats = df.groupby(['date_formatted', 'course']).size().reset_index()
    date_stats.columns = ['Date', 'Course', 'Admissions']
    
    # Add subtotals for each date
    subtotals = []
    dates = date_stats['Date'].unique()
    
    for date in dates:
        date_data = date_stats[date_stats['Date'] == date]
        subtotal = date_data['Admissions'].sum()
        subtotals.append({
            'Date': f"{date} - Subtotal", 
            'Course': '', 
            'Admissions': subtotal
        })
    
    # Add grand total
    grand_total = date_stats['Admissions'].sum()
    subtotals.append({
        'Date': 'GRAND TOTAL', 
        'Course': '', 
        'Admissions': grand_total
    })
    
    # Combine stats with subtotals
    final_stats = []
    for date in dates:
        date_data = date_stats[date_stats['Date'] == date].to_dict('records')
        final_stats.extend(date_data)
        final_stats.append(next(s for s in subtotals if s['Date'] == f"{date} - Subtotal"))
    
    final_stats.append(subtotals[-1])  # Grand total
    
    return pd.DataFrame(final_stats)

def create_course_student_list(df, selected_years=None, selected_courses=None):
    """Create filtered student list by course with serial numbers and totals"""
    if df is None or df.empty:
        return None
    
    filtered_df = df.copy()
    
    # Apply filters
    if selected_years and len(selected_years) > 0:
        filtered_df = filtered_df[filtered_df['year'].isin(selected_years)]
    
    if selected_courses and len(selected_courses) > 0:
        filtered_df = filtered_df[filtered_df['course'].isin(selected_courses)]
    
    # Select relevant columns for display
    display_columns = ['student_name', 'father_name', 'year', 'course', 
                      'admission_year', 'category', 'date_formatted']
    
    available_columns = [col for col in display_columns if col in filtered_df.columns]
    student_list = filtered_df[available_columns].copy()
    
    # Add serial number column
    if not student_list.empty:
        student_list.insert(0, 'Sl No', range(1, len(student_list) + 1))
        student_list['Sl No'] = student_list['Sl No'].apply(lambda x: f"{x:02d}")
    
    # Rename columns for display
    column_names = {
        'student_name': 'Student Name',
        'father_name': 'Father Name',
        'year': 'Year',
        'course': 'Course',
        'admission_year': 'Admission Year',
        'category': 'Category',
        'date_formatted': 'Date'
    }
    
    student_list = student_list.rename(columns=column_names)
    
    # Add total count row
    if not student_list.empty:
        total_count = len(student_list)
        total_row = pd.DataFrame([{
            'Sl No': '',
            'Student Name': f'TOTAL STUDENTS: {total_count}',
            'Father Name': '',
            'Year': '',
            'Course': '',
            'Admission Year': '',
            'Category': '',
            'Date': ''
        }])
        student_list = pd.concat([student_list, total_row], ignore_index=True)
    
    return student_list

def main():
    # Header
    st.markdown('<div class="main-header">🎓 Student Admission Analytics</div>', 
                unsafe_allow_html=True)
    
    # Load data
    df = load_data()
    
    if df is None:
        st.stop()
    
    # Navigation tabs
    tab1, tab2, tab3 = st.tabs(["📈 Year & Course Statistics", "📅 Date-wise Admissions", "👥 Student List"])
    
    with tab1:
        st.markdown('<div class="report-section">', unsafe_allow_html=True)
        
        final_stats, stats = create_year_course_stats(df)
        
        if final_stats is not None:
            # Summary metrics with different colors
            col1, col2, col3 = st.columns(3)
            
            with col1:
                total_students = stats['Total Students'].sum()
                st.markdown(f"""
                <div class="metric-card metric-students">
                    <div class="metric-value" style="color: white;">{total_students}</div>
                    <div class="metric-label" style="color: #ffe6e6;">Total Students</div>
                </div>
                """, unsafe_allow_html=True)
            
            with col2:
                total_courses = df['course'].nunique()
                st.markdown(f"""
                <div class="metric-card metric-courses">
                    <div class="metric-value" style="color: white;">{total_courses}</div>
                    <div class="metric-label" style="color: #e6fffe;">Total Courses</div>
                </div>
                """, unsafe_allow_html=True)
            
            with col3:
                total_years = df['year'].nunique()
                st.markdown(f"""
                <div class="metric-card metric-years">
                    <div class="metric-value" style="color: white;">{total_years}</div>
                    <div class="metric-label" style="color: #e6f7ff;">Academic Years</div>
                </div>
                """, unsafe_allow_html=True)
            
            # Statistics table
            st.subheader("📋 Statistics Table")
            
            # Style the dataframe for better presentation
            def style_dataframe(df):
                def highlight_totals(row):
                    if 'Subtotal' in str(row['Year']) or 'GRAND TOTAL' in str(row['Year']):
                        return ['background-color: #f1f3f4; font-weight: bold; color: #2d3748'] * len(row)
                    return [''] * len(row)
                return df.style.apply(highlight_totals, axis=1)
            
            styled_df = style_dataframe(final_stats)
            st.dataframe(styled_df, use_container_width=True, hide_index=True)
            
            # Bar chart visualization
            st.subheader("📊 Course-wise Distribution")
            fig_bar = px.bar(stats, x='Course', y='Total Students', color='Year',
                           title="Student Distribution by Course and Year",
                           color_discrete_sequence=['#667eea', '#764ba2', '#ff6b6b', '#4ecdc4', '#45b7d1', '#96ceb4'])
            fig_bar.update_layout(
                showlegend=True, 
                height=400,
                title_font_family="Inter",
                title_font_size=18,
                title_font_color="#2d3748",
                font_family="Inter",
                font_color="#2d3748"
            )
            st.plotly_chart(fig_bar, use_container_width=True)
        
        st.markdown("</div>", unsafe_allow_html=True)
    
    with tab2:
        st.markdown('<div class="report-section">', unsafe_allow_html=True)
        
        date_stats = create_datewise_stats(df)
        
        if date_stats is not None:
            st.subheader("📋 Date-wise Admission Table")
            
            # Style the dataframe for better presentation
            def style_date_dataframe(df):
                def highlight_totals(row):
                    if 'Subtotal' in str(row['Date']) or 'GRAND TOTAL' in str(row['Date']):
                        return ['background-color: #f1f3f4; font-weight: bold; color: #2d3748'] * len(row)
                    return [''] * len(row)
                return df.style.apply(highlight_totals, axis=1)
            
            styled_date_df = style_date_dataframe(date_stats)
            st.dataframe(styled_date_df, use_container_width=True, hide_index=True)
            
            # Filter out total rows for chart
            chart_data = date_stats[
                (~date_stats['Date'].str.contains('Subtotal', na=False)) & 
                (~date_stats['Date'].str.contains('GRAND TOTAL', na=False))
            ]
            
            if not chart_data.empty:
                st.subheader("📊 Daily Admission Trends")
                fig_line = px.bar(chart_data, x='Date', y='Admissions', 
                                color='Course', title="Daily Admissions by Course",
                                color_discrete_sequence=['#667eea', '#764ba2', '#ff6b6b', '#4ecdc4', '#45b7d1', '#96ceb4'])
                fig_line.update_layout(
                    xaxis_tickangle=-45, 
                    height=400,
                    title_font_family="Inter",
                    title_font_size=18,
                    title_font_color="#2d3748",
                    font_family="Inter",
                    font_color="#2d3748"
                )
                st.plotly_chart(fig_line, use_container_width=True)
        
        st.markdown("</div>", unsafe_allow_html=True)
    
    with tab3:
        st.markdown('<div class="report-section">', unsafe_allow_html=True)
        
        # Filter controls
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("🎓 Year Filter")
            available_years = sorted(df['year'].unique())
            selected_years = st.multiselect("Select Years:", available_years, default=available_years)
        
        with col2:
            st.subheader("📚 Course Filter")
            available_courses = sorted(df['course'].unique())
            selected_courses = st.multiselect("Select Courses:", available_courses, default=available_courses)
        
        # Generate filtered list
        if st.button("🔍 Generate List", type="primary"):
            student_list = create_course_student_list(df, selected_years, selected_courses)
            
            if student_list is not None and not student_list.empty:
                st.subheader("📋 Student List")
                
                # Style the student list dataframe
                def style_student_dataframe(df):
                    def highlight_total(row):
                        if 'TOTAL STUDENTS:' in str(row['Student Name']):
                            return ['background-color: #667eea; font-weight: bold; color: white'] * len(row)
                        return [''] * len(row)
                    return df.style.apply(highlight_total, axis=1)
                
                styled_student_df = style_student_dataframe(student_list)
                st.dataframe(styled_student_df, use_container_width=True, hide_index=True)
                
                # Download button
                csv = student_list.to_csv(index=False)
                st.download_button(
                    label="📥 Download CSV",
                    data=csv,
                    file_name=f"students_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                    mime="text/csv"
                )
            else:
                st.warning("No students found with the selected filters.")
        
        st.markdown("</div>", unsafe_allow_html=True)

if __name__ == "__main__":
    main()