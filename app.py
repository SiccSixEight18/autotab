import streamlit as st
import time

def main():
    st.title("Bulk Link Opener")
    st.write("Paste your links below (one per line)")
    
    # Text area for links
    links_text = st.text_area("Links", height=200)
    
    if st.button("Open All Links"):
        # Split the text into individual links
        links = [link.strip() for link in links_text.split('\n') if link.strip()]
        
        if links:
            # Create hidden links and add auto-click JavaScript
            for i, link in enumerate(links):
                if not link.startswith(('http://', 'https://')):
                    link = 'http://' + link
                
                # Create a hidden link with a unique ID
                st.markdown(f'<a id="link{i}" href="{link}" target="_blank" style="display:none">{link}</a>', unsafe_allow_html=True)
            
            # Add JavaScript to auto-click all links
            js = """
            <script>
                function openLinks() {
                    let links = document.querySelectorAll('a[id^="link"]');
                    links.forEach(link => {
                        setTimeout(() => {
                            link.click();
                        }, 100);  // Small delay between clicks to help browser handle them
                    });
                }
                // Execute after a brief delay to ensure all links are rendered
                setTimeout(openLinks, 500);
            </script>
            """
            st.components.v1.html(js, height=0)
            
            st.success(f"Opening {len(links)} links...")
            
        else:
            st.warning("Please paste some links first!")

    st.info("""
    ⚠️ Note: You may need to allow pop-ups in your browser for this to work.
    If links don't open automatically, check your browser's pop-up settings.
    """)

if __name__ == "__main__":
    main()
