import streamlit as st
import time

def main():
    st.title("Bulk Link Opener")
    
    # Add warning about pop-ups at the top
    st.warning("""
    ⚠️ Important: Most browsers limit how many tabs can be opened automatically.
    If not all links open:
    1. Look for a pop-up blocker icon in your address bar
    2. Click it and select 'Always allow pop-ups from this site'
    3. Click 'Open All Links' again
    """)
    
    # Text area for links
    st.write("Paste your links below (one per line)")
    links_text = st.text_area("Links", height=200)
    
    # Add option for delay
    delay_ms = st.slider("Delay between opening links (milliseconds)", 
                        min_value=100, 
                        max_value=1000, 
                        value=200,
                        help="Increase this if your browser is blocking tabs from opening")
    
    if st.button("Open All Links"):
        links = [link.strip() for link in links_text.split('\n') if link.strip()]
        
        if links:
            # Create container for status updates
            status_container = st.empty()
            
            # Create hidden links and add auto-click JavaScript
            for i, link in enumerate(links):
                if not link.startswith(('http://', 'https://')):
                    link = 'http://' + link
                
                # Create a hidden link with a unique ID
                st.markdown(f'<a id="link{i}" href="{link}" target="_blank" style="display:none">{link}</a>', 
                          unsafe_allow_html=True)
            
            # Add JavaScript with better handling and feedback
            js = f"""
            <script>
                function openLinks() {{
                    let links = document.querySelectorAll('a[id^="link"]');
                    let totalLinks = links.length;
                    let openedLinks = 0;
                    
                    links.forEach((link, index) => {{
                        setTimeout(() => {{
                            try {{
                                let opened = window.open(link.href, '_blank');
                                if (opened) {{
                                    openedLinks++;
                                    // Update progress (if we could communicate back to Streamlit)
                                }}
                            }} catch (e) {{
                                console.error('Failed to open:', link.href);
                            }}
                        }}, index * {delay_ms});
                    }});
                }}
                
                // Execute after a brief delay to ensure all links are rendered
                setTimeout(openLinks, 1000);
            </script>
            """
            st.components.v1.html(js, height=0)
            
            # Show links that should be opening
            st.write("### Links being processed:")
            for i, link in enumerate(links, 1):
                st.write(f"{i}. [{link}]({link})")
            
            st.info(f"""
            Attempting to open {len(links)} links...
            
            If some links don't open:
            1. Check your browser's address bar for a pop-up blocker icon
            2. Try increasing the delay using the slider above
            3. As a fallback, you can manually Ctrl/Cmd+Click the links above
            """)
        
        else:
            st.warning("Please paste some links first!")

if __name__ == "__main__":
    main()
