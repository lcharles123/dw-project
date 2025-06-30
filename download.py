import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import config

def download_file(url, download_dir):
    """Download a file from a URL and save it to the specified directory"""
    if not os.path.exists(download_dir):
        os.makedirs(download_dir)
    
    local_filename = os.path.join(download_dir, url.split('/')[-1])
    
    with requests.get(url, stream=True) as r:
        r.raise_for_status()
        with open(local_filename, 'wb') as f:
            for chunk in r.iter_content(chunk_size=8192): 
                f.write(chunk)
    return local_filename

def find_and_download_links(url, pattern='.csv', target='_blank'):
    """Find links matching pattern and target attribute, then download them"""
    try:
        # Get the webpage content
        response = requests.get(url)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, 'html.parser')
        base_url = response.url  # Get final URL after redirects
        
        found_links = []
        
        # Find all links that match our criteria
        for link in soup.find_all('a', class_="resource-url-analytics", href=True):
            href = link['href']
            link_target = link.get('target', '')
            
            # Check if link matches our pattern and target
            if href.lower().endswith(pattern.lower()) and link_target == target:
                # Make absolute URL if it's relative
                absolute_url = urljoin(base_url, href)
                found_links.append(absolute_url)
                
                # Download the file
                try:
                    saved_path = download_file(absolute_url, DOWNLOAD_DIR)
                    print(f"Downloaded: {absolute_url} -> {saved_path}")
                except Exception as e:
                    print(f"Failed to download {absolute_url}: {e}")
        
        return found_links
    
    except Exception as e:
        print(f"Error processing {url}: {e}")
        return []


if __name__ == "__main__":
    target_url = config.CSV_REPO_URL 
    file_extension = ".csv"
    DOWNLOAD_DIR = config.DOWNLOAD_DIR
    print(f"Searching {target_url} for {file_extension} files...")
    found_files = find_and_download_links(target_url, pattern=file_extension)
    
    print("\nFound files:")
    for i, file_url in enumerate(found_files, 1):
        print(f"{i}. {file_url}")

