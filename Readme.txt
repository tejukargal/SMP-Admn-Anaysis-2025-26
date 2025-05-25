# Student Admission Data Analytics Dashboard

A modern, responsive Streamlit application for analyzing student admission data with interactive filtering and visualization capabilities.

## Features

- **Year & Course Statistics**: Comprehensive statistics showing student distribution across years and courses
- **Date-wise Analysis**: Track daily admission trends with interactive date filtering  
- **Student List with Filters**: Interactive filtering by year and course with export functionality
- **Responsive Design**: Works seamlessly on desktop and mobile devices
- **Modern UI**: Clean, professional interface with interactive visualizations

## Setup Instructions

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Prepare Your Data
- Place your Excel file (.xlsx or .xls) in the same folder as `app.py`
- Ensure your Excel file has columns matching the format:
  - Student Name, Father Name, Year, Course, Date, In/Out, Remarks, etc.

### 3. Run the Application
```bash
streamlit run app.py
```

### 4. Access the Dashboard
- Open your browser and go to `http://localhost:8501`
- The dashboard will automatically load and display your data

## Data Requirements

Your Excel file should contain these columns:
- **Student Name**: Full name of the student
- **Year**: Academic year (e.g., "1st Yr", "2nd Yr")
- **Course**: Course code or name (e.g., "CS", "ME", "EC")
- **Date**: Admission date
- **In/Out**: Status ("In" for admitted students)
- **Remarks**: Payment status (e.g., "Due Fee" for pending payments)

## Usage

### Default View
- The application opens with Year & Course Statistics displayed by default
- View total students, courses, academic years, and due fee statistics

### Navigation
Use the sidebar to switch between different reports:

1. **📈 Year & Course Statistics**
   - Overview metrics and detailed statistics
   - Interactive bar charts and pie charts
   - Breakdown by year and course

2. **📅 Date-wise Admissions**  
   - Daily admission trends
   - Date range filtering
   - Course-wise admission patterns

3. **👥 Student List with Filters**
   - Checkbox filters for Year and Course
   - Detailed student information
   - CSV export functionality

### Filtering
- Use checkboxes to select specific years and courses
- Click "Generate Filtered List" to apply filters
- Download filtered results as CSV files

## Technical Features

- **Data Processing**: Automatically filters only admitted students (In status)
- **Fee Tracking**: Identifies students with due fees from remarks
- **Interactive Charts**: Plotly-powered visualizations
- **Export Options**: Download filtered data as CSV
- **Responsive Design**: Mobile-friendly interface
- **Error Handling**: Graceful handling of data issues

## Support

For issues or questions:
1. Ensure your Excel file is in the correct format
2. Check that all required columns are present
3. Verify the file is in the same directory as the application

## File Structure
```
project/
│
├── app.py                 # Main application
├── requirements.txt       # Dependencies
├── README.md             # This file
└── your_data.xlsx        # Your student data Excel file
```