import streamlit as st
import webbrowser
import time

def main():
    st.title("Bulk Link Opener")
    st.write("Paste your links below (one per line)")
    
    # Text area for links
    links_text = st.text_area("Links", height=200)
    
    # Delay slider to prevent browser from blocking popups
    delay = st.slider("Delay between opening links (seconds)", 0.0, 2.0, 0.5)
    
    if st.button("Open Links"):
        # Split the text into individual links
        links = [link.strip() for link in links_text.split('\n') if link.strip()]
        
        if links:
            st.write(f"Opening {len(links)} links...")
            progress_bar = st.progress(0)
            
            for i, link in enumerate(links):
                # Add http:// if no protocol specified
                if not link.startswith(('http://', 'https://')):
                    link = 'http://' + link
                
                webbrowser.open(link, new=2)  # new=2 opens in new tab
                progress = (i + 1) / len(links)
                progress_bar.progress(progress)
                time.sleep(delay)
                
            st.success("All links opened!")
        else:
            st.warning("Please paste some links first!")

if __name__ == "__main__":
    main()