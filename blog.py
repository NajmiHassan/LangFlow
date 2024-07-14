import streamlit as st
import requests
from bs4 import BeautifulSoup
import openai

# Initialize OpenAI API key (replace '<YOUR_API_KEY>' with your actual API key)
api_key = '724b5711ab0e45db83b975ecc63bd7fa'
base_url = "https://api.aimlapi.com"

def fetch_content_from_urls(urls):
    contents = []
    for url in urls:
        url = url.strip()
        try:
            response = requests.get(url)
            response.raise_for_status()
            soup = BeautifulSoup(response.content, 'html.parser')
            contents.append(soup.get_text())
        except requests.exceptions.RequestException as e:
            st.error(f"Failed to fetch {url}: {e}")
    return contents

def generate_blog_with_gpt35(references, instructions):
    # Combine references and instructions into a single prompt
    prompt = f"References:\n\n{references}\n\nInstructions:\n\n{instructions}\n\nGenerate a blog post based on the above references and instructions:"
    
    # Call OpenAI's GPT-3.5 Turbo to generate blog content
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "system",
                "content": "You are an AI assistant who helps generate blog posts based on given references and instructions.",
            },
            {
                "role": "user",
                "content": prompt
            },
        ],
    )
    
    # Extract the generated text
    blog_content = response['choices'][0]['message']['content'].strip()
    return blog_content

st.title("Blog Writing Chatbot")
st.markdown("Hey there, wordsmith! 📝🌟 Ready to create some magic with your blog posts? Let our chatbot guide you through crafting engaging content effortlessly. Let's get started! 💪💡")
st.markdown("You will get toyr blog here after entering urls and hit generate blog button")
# Sidebar for inputs
st.sidebar.header("WordSmith")
urls_input = st.sidebar.text_area("Enter URLs (comma-separated)")
references_input = st.sidebar.text_area("Enter Additional References")
instructions_input = st.sidebar.text_area("Enter Instructions")

if st.sidebar.button("Generate Blog"):
    urls = [url.strip() for url in urls_input.split(',')]
    url_contents = fetch_content_from_urls(urls)
    references = "\n".join(url_contents) + "\n" + references_input

    blog_content = generate_blog_with_gpt35(references, instructions_input)

    st.markdown("### Generated Blog")
    st.write(blog_content)
