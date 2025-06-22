import os
import re
import yaml
from urllib.parse import urlparse

# --- Configuration ---
TEMPLATE_FILE = 'template.yaml'
SUBS_FILE = 'subscriptions.txt'
OUTPUT_DIR = 'output'
README_FILE = 'README.md'
# The user/repo name will be fetched from GitHub Actions environment variables
# For local testing, you can set it manually, e.g., 'YourUser/YourRepo'
GITHUB_REPO = os.environ.get('GITHUB_REPOSITORY')

def get_filename_from_url(url):
    """Extracts a clean filename from a URL."""
    path = urlparse(url).path
    filename = os.path.basename(path)
    # Remove file extension
    return os.path.splitext(filename)[0]

def update_readme(output_files):
    """Updates the README.md file with a list of generated config links."""
    if not GITHUB_REPO:
        print("Warning: GITHUB_REPOSITORY environment variable not set. Cannot generate public URLs.")
        print("Generated files:", output_files)
        return

    print(f"Updating README.md for repository: {GITHUB_REPO}")

    # Generate the markdown list of links
    links_md = f"## 🔗 لینک‌های کانفیگ (Raw)\n\n"
    links_md += "برای استفاده، لینک‌های زیر را مستقیما در کلش کپی کنید.\n\n"
    for filename in sorted(output_files):
        # The output file name already includes '.yaml'
        raw_url = f"https://raw.githubusercontent.com/{GITHUB_REPO}/main/{OUTPUT_DIR}/{filename}"
        # Use filename without extension as the link title
        title = os.path.splitext(filename)[0]
        links_md += f"* **{title}**: `{raw_url}`\n"

    # Read the existing README
    with open(README_FILE, 'r', encoding='utf-8') as f:
        readme_content = f.read()

    # Replace the content between the markers
    # Using regex to handle multi-line content between markers
    start_marker = ""
    end_marker = ""
    
    # Ensure markers exist in the README.md file
    if start_marker not in readme_content or end_marker not in readme_content:
        print(f"Error: Markers '{start_marker}' and '{end_marker}' not found in {README_FILE}.")
        print("Please add them to your README.md file.")
        return

    regex = re.compile(f"{re.escape(start_marker)}.*{re.escape(end_marker)}", re.DOTALL)
    new_readme_content = regex.sub(f"{start_marker}\n{links_md}\n{end_marker}", readme_content)

    # Write the updated content back to README.md
    with open(README_FILE, 'w', encoding='utf-8') as f:
        f.write(new_readme_content)
    print("README.md updated successfully.")


def main():
    """Main function to generate configs."""
    print("Starting config generation process...")
    
    # 1. Read the template
    try:
        with open(TEMPLATE_FILE, 'r', encoding='utf-8') as f:
            template_data = yaml.safe_load(f)
        print(f"Successfully loaded template file: {TEMPLATE_FILE}")
    except Exception as e:
        print(f"Error reading template file {TEMPLATE_FILE}: {e}")
        return

    # 2. Ensure output directory exists
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    # 3. Read subscription links
    try:
        with open(SUBS_FILE, 'r', encoding='utf-8') as f:
            subscriptions = [line.strip() for line in f if line.strip() and not line.startswith('#')]
        print(f"Found {len(subscriptions)} subscription(s) in {SUBS_FILE}")
    except FileNotFoundError:
        print(f"Error: Subscription file not found at {SUBS_FILE}")
        return
        
    generated_files = []

    # 4. Process each subscription
    for sub_line in subscriptions:
        custom_name = None
        if ',' in sub_line:
            url, custom_name = [part.strip() for part in sub_line.split(',', 1)]
        else:
            url = sub_line
        
        if not custom_name:
            # Auto-detect name from URL
            file_name_base = get_filename_from_url(url)
            if not file_name_base:
                print(f"Warning: Could not determine a filename for URL: {url}. Skipping.")
                continue
        else:
            file_name_base = custom_name
            
        output_filename = f"{file_name_base}.yaml"
        output_path = os.path.join(OUTPUT_DIR, output_filename)
        
        print(f"Processing: {url} -> {output_path}")

        # Create a copy of the template data to modify
        config_data = template_data.copy()
        
        # Modify the proxy-provider URL
        # Assumes the provider to be modified is named 'proxy'
        try:
            config_data['proxy-providers']['proxy']['url'] = url
        except KeyError:
            print("Error: The template file does not have 'proxy-providers' -> 'proxy' structure.")
            continue

        # Write the new config file
        with open(output_path, 'w', encoding='utf-8') as f:
            yaml.dump(config_data, f, allow_unicode=True, sort_keys=False)
            
        generated_files.append(output_filename)

    print(f"\nGenerated {len(generated_files)} config files in '{OUTPUT_DIR}' directory.")

    # 5. Update the README file
    if generated_files:
        update_readme(generated_files)

if __name__ == "__main__":
    main()
