import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load Netflix dataset
df = pd.read_csv('netflix_titles.csv', encoding='ISO-8859-1')
df = df.iloc[:, :12]
df['date_added'] = pd.to_datetime(df['date_added'], errors='coerce').dt.date
df['released_year'] = pd.to_datetime(df['date_added'], errors='coerce').dt.year

# Extract numeric duration from the 'duration' column
df['duration_minutes'] = df['duration'].str.extract('(\d+)').astype(float)

# Function to display the head of the dataframe
def show_head():
    st.write("### First 5 Rows of the Dataset")
    st.write(df.head())

# Function to display dataset info
def show_info():
    st.write("### Dataset Info")
    info_df = pd.DataFrame({
        'Column': df.columns,
        'Non-Null Count': df.notnull().sum(),
        'Dtype': df.dtypes
    })
    st.dataframe(info_df)

# Function to replace missing values and display the result
def fill_missing_values():
    st.write("### Replacing Missing Values")
    df['director'] = df['director'].fillna(df['director'].mode()[0])
    df['cast'] = df['cast'].fillna(df['cast'].mode()[0])
    df['country'] = df['country'].fillna(df['country'].mode()[0])
    df['date_added'] = df['date_added'].fillna(df['date_added'].mode()[0])
    df['rating'] = df['rating'].fillna(df['rating'].mode()[0])
    df['duration'] = df['duration'].fillna(df['duration'].mode()[0])
    st.write("Missing Values After Filling:")
    st.write(df.isnull().sum())

# Function to filter by age range
def filter_by_age():
    st.write("##### Filter by Age Range")
    age_ranges = {
        'All Ages': None,
        'Kids': ['TV-Y', 'TV-Y7', 'G', 'TV-G'],
        'Teens': ['PG', 'PG-13', 'TV-PG'],
        'Adults': ['R', 'TV-MA', 'NC-17']
    }
    selected_range = st.selectbox('Select Age Range', list(age_ranges.keys()))
    if selected_range != 'All Ages':
        filtered_df = df[df['rating'].isin(age_ranges[selected_range])]
        st.write(f"##### Movies/Shows for {selected_range}")
        st.write(filtered_df[['title', 'rating', 'type', 'duration']])
    else:
        st.write("##### All Movies/Shows")
        st.write(df[['title', 'rating', 'type', 'duration']])

# Function to filter by country
def filter_by_country():
    st.write("##### Filter by Country")
    
    # Fetch unique country values
    unique_countries = df['country'].dropna().unique()
    
    # Dropdown for selecting a country
    selected_country = st.selectbox('Select Country', sorted(unique_countries))
    
    # Check if a country is selected
    if selected_country:
        filtered_df = df[df['country'] == selected_country]
        st.write(f"##### Movies/Shows from {selected_country}")
        st.write(filtered_df[['title', 'country', 'type', 'rating', 'duration']])

# Function to filter by year range
def filter_by_year():
    st.write("### Filter by Year Range")
    
    # Get the range of years available in the dataset
    min_year = int(df['released_year'].min())
    max_year = int(df['released_year'].max())
    
    # Create a slider to select a range of years
    start_year, end_year = st.slider(
        'Select Year Range', 
        min_value=min_year, 
        max_value=max_year, 
        value=(min_year, max_year), 
        step=1
    )
    
    # Filter the dataset based on the selected year range
    filtered_df = df[(df['released_year'] >= start_year) & (df['released_year'] <= end_year)]
    st.write(f"### Movies/Shows from {start_year} to {end_year}")
    st.write(filtered_df[['title', 'date_added', 'type', 'rating', 'duration']])

# Function to filter by duration range
def filter_by_duration():
    st.write("### Filter by Duration Range (in minutes)")
    
    # Get the range of durations available in the dataset
    min_duration = int(df['duration_minutes'].min())
    max_duration = int(df['duration_minutes'].max())
    
    # Create a slider to select a range of durations
    min_duration, max_duration = st.slider(
        'Select Duration Range', 
        min_value=min_duration, 
        max_value=max_duration, 
        value=(min_duration, max_duration), 
        step=1
    )
    
    # Filter the dataset based on the selected duration range
    filtered_df = df[(df['duration_minutes'] >= min_duration) & (df['duration_minutes'] <= max_duration)]
    st.write(f"### Movies/Shows with Duration from {min_duration} to {max_duration} minutes")
    st.write(filtered_df[['title', 'duration', 'type', 'rating']])

# Function to choose filter type (Age, Country, Year, Duration)
def filter():
    st.write("### Filter Movies/Shows")
    filter_options = ['Select Filter', 'By Age Range', 'By Country', 'By Year', 'By Duration']
    selected_filter = st.selectbox('Select Filter Type', filter_options)
    
    if selected_filter == 'By Age Range':
        filter_by_age()
    elif selected_filter == 'By Country':
        filter_by_country()
    elif selected_filter == 'By Year':
        filter_by_year()
    elif selected_filter == 'By Duration':
        filter_by_duration()

# Extract numeric duration from the 'duration' column
df['duration_minutes'] = df['duration'].str.extract('(\d+)').astype(float)


# Function to display Bar Plot
def bar_plot():
    st.write("### Bar Plot: Count of Movies vs TV Shows")
    fig, ax = plt.subplots()
    df['type'].value_counts().plot(kind='bar', ax=ax, color=['#FF6347', '#4682B4'])
    ax.set_title('Count of Movies vs TV Shows')
    ax.set_xlabel('Type')
    ax.set_ylabel('Count')
    st.pyplot(fig)

# Function to display Histogram
def histogram_plot():
    st.write("### Histogram: Distribution of Movie/Show Durations")
    fig, ax = plt.subplots()
    sns.histplot(df['duration_minutes'].dropna(), bins=20, kde=True, color='purple', ax=ax)
    ax.set_title('Distribution of Durations')
    ax.set_xlabel('Duration (minutes)')
    st.pyplot(fig)

# Function to display Heatmap
def heatmap_plot():
    st.write("### Heatmap: Correlation Matrix")
    fig, ax = plt.subplots()
    numerical_cols = df.select_dtypes(include=['float64', 'int64'])
    sns.heatmap(numerical_cols.corr(), annot=True, cmap='coolwarm', ax=ax)
    ax.set_title('Correlation Heatmap')
    st.pyplot(fig)

# Function to display Pie Chart
def pie_chart():
    st.write("### Pie Chart: Top 5 Content Ratings")
    fig, ax = plt.subplots()
    df['rating'].value_counts().head(5).plot(kind='pie', autopct='%1.1f%%', startangle=90, colors=sns.color_palette('pastel'), ax=ax)
    ax.set_ylabel('')
    ax.set_title('Top 5 Content Ratings')
    st.pyplot(fig)










# Streamlit UI Layout
# st.title("StreamSmart: Netflix Insights")
st.markdown("""
<h1 style='text-align: center;'>
    <span style='color: red;'><b><i>Stream</i></b></span>
    <span style='color: black;'><b><i>Smart:</i></b></span>
    <span style='color: red;'><b><i>Netflix</i></b></span>
    <span style='color: black;'><b><i>Insights</i></b></span>
</h1>
""", unsafe_allow_html=True)


if st.button('Show Head of Dataset'):
    show_head()

if st.button('Show Dataset Info'):
    show_info()

if st.button('Replace Missing Values'):
    fill_missing_values()

filter()  # Show filter options (age, country, year, or duration)


st.write("### Select a Plot to Display")
plot_options = ['Select a Plot', 'Bar Plot: Movies vs TV Shows', 'Histogram: Duration Distribution', 'Heatmap: Correlation Matrix', 'Pie Chart: Content Ratings']
selected_plot = st.selectbox('Choose a Plot', plot_options)

if selected_plot == 'Bar Plot: Movies vs TV Shows':
    bar_plot()
elif selected_plot == 'Histogram: Duration Distribution':
    histogram_plot()
elif selected_plot == 'Heatmap: Correlation Matrix':
    heatmap_plot()
elif selected_plot == 'Pie Chart: Content Ratings':
    pie_chart()