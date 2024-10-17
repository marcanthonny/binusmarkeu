import streamlit as st
from web_crawler import news_search
from analyze_instagram import analyze_instagram_data
from instagram_sentiment import analyze_sentiments
from analyze_tiktok import analyze_tiktok_data
from facebook_sentiment import analyze_facebook_sentiments
from analyze_facebook import analyze_facebook_data
from twitter_sentiment import analyze_twitter_sentiments

st.set_page_config(layout="wide", page_title="Media Center")

st.title("Media Center")

st.markdown("<hr style='border: 1px solid #acb9bf;'>", unsafe_allow_html=True)

# Function to display the modular design


  # Line separator
 
    #st.markdown()

#topcoleft, topcolright = st.column_config

st.markdown(
    """
    <style>
        .centered-text {
            text-align: center;
        }
    </style>
    <div style="font-size: 18px; font-color: #f4f6f6">
    
    Dalam era informasi yang serba cepat seperti sekarang, keberadaan dashboard data analisis menjadi sangat penting dalam dunia politik. Dengan banyaknya data yang tersedia, mulai dari opini publik, tren media sosial, hingga hasil survei, politisi dan tim kampanye dapat dengan cepat dan akurat memahami dinamika yang terjadi di lapangan. Dashboard data analisis memungkinkan pengambilan keputusan yang lebih tepat dengan memvisualisasikan data kompleks secara sederhana dan mudah dipahami. Hal ini tidak hanya membantu dalam menyusun strategi yang efektif, tetapi juga dalam merespon perubahan sentimen publik dengan cepat dan efisien. Dalam konteks persaingan politik yang semakin ketat, kemampuan untuk mengolah dan menganalisis data secara real-time melalui dashboard yang intuitif dan komprehensif dapat menjadi kunci kesuksesan.
    </div>
    """,
    unsafe_allow_html=True
)    
st.markdown('')
st.markdown(
        """
        <div style="font-size: 28px; text-align: center;">
        Temukan wawasan berharga dengan fitur Analisis Sentimen untuk media sosial.
        </div>
        """,
        unsafe_allow_html=True
    )
#Sentiment Analysis
leftcolumn, middlecolumn, rightcolumn = st.columns([1, 1, 1])

with leftcolumn:
    sentiment_fig = analyze_sentiments()
    st.plotly_chart(sentiment_fig, use_container_width=True)

with middlecolumn:
    facebook_fig = analyze_facebook_sentiments()
    st.plotly_chart(facebook_fig, use_container_width=True)

with rightcolumn:
    twit_fig = analyze_twitter_sentiments()
    st.plotly_chart(twit_fig, use_container_width=True)

st.markdown(
        """
        <div style="font-size: 28px; text-align: center;">
        Perhatikan data anda dengan tampilan optimal dengan bagan interaktif dan data paling mutakhir oleh API kami.
        </div>
        """,
        unsafe_allow_html=True
    )

#Instagram Engagement
engagement_fig = analyze_instagram_data()
st.plotly_chart(engagement_fig, use_container_width=True)

#TikTok Engagement
tiktok_fig = analyze_tiktok_data()
st.plotly_chart(tiktok_fig, use_container_width=True)

#facebook engagement
facebook_engage = analyze_facebook_data()
st.plotly_chart(facebook_engage, use_container_width=True)

#Search Bar
searchbar, howmanyselect = st.columns([3,1])

with searchbar:
    query = st.text_input("Enter search term")

with howmanyselect:
    num_results = st.number_input("Number of results", min_value=1, max_value=10, value=5)

if query:
    st.write(f'Searching for "{query}"...')
    news_links = news_search(query, num_results)
    
    if news_links:
        st.write('### Found the following links:')
        for title, link, site, date in news_links:
            st.markdown(f"""
                <div style='border: 1px solid #ddd; padding: 10px; border-radius: 5px; margin-bottom: 10px;'>
                    <h4 style='margin: 0;'><a href='{link}' target='_blank'>{title}</a></h4>
                    <p style='margin: 5px 0;'>Source: <a href='{site}' target='_blank'>{site}</a></p>
                    <p style='margin: 5px 0;'>Date: {date}</p>
                </div>
                """, unsafe_allow_html=True)
    else:
        st.write('No results found.')


# Main app logic
st.markdown("<h1 style='text-align: center; color: #2196F3;'></h1>", unsafe_allow_html=True)
