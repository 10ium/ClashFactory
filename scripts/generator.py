import os
import sys
import yaml
import requests
import copy  # برای کپی عمیق و مطمئن
from urllib.parse import urlparse, quote_plus

# --- Configuration ---
TEMPLATE_FILE = 'template.yaml'
SUBS_FILE = 'subscriptions.txt'
FORMAT_FILE = 'format.txt'
OUTPUT_DIR = 'output'
PROVIDERS_DIR = 'providers'
README_FILE = 'README.md'
GITHUB_REPO = os.environ.get('GITHUB_REPOSITORY')


def get_filename_from_url(url):
    path = urlparse(url).path
    filename = os.path.basename(path)
    return os.path.splitext(filename)[0]


def update_readme(output_files):
    """Updates the README.md file with a list of generated config links."""
    if not GITHUB_REPO:
        sys.exit("Critical Error: GITHUB_REPOSITORY environment variable is not set.")

    print(f"Updating README.md for repository: {GITHUB_REPO}")

    links_md_content = "## 🔗 لینک‌های کانفیگ آماده (Raw)\n\n"
    links_md_content += "برای استفاده، لینک‌های زیر را مستقیما در کلش کپی کنید.\n\n"
    for filename in sorted(output_files):
        raw_url = f"https://raw.githubusercontent.com/{GITHUB_REPO}/main/{OUTPUT_DIR}/{filename}"
        title = os.path.splitext(filename)[0]
        links_md_content += f"* **{title}**: `{raw_url}`\n"

    try:
        with open(README_FILE, 'r', encoding='utf-8') as f:
            readme_content = f.read()
    except FileNotFoundError:
        sys.exit(f"CRITICAL ERROR: The '{README_FILE}' file was not found in the repository root.")

    start_marker = "<!-- START_LINKS -->"
    end_marker = "<!-- END_LINKS -->"

    if start_marker not in readme_content or end_marker not in readme_content:
        sys.exit(f"CRITICAL ERROR: Markers '{start_marker}' and '{end_marker}' not found in {README_FILE}.")

    try:
        before_part = readme_content.split(start_marker)[0]
        after_part = readme_content.split(end_marker)[1]
    except IndexError:
        sys.exit("CRITICAL ERROR: Could not split README content. Check marker placement.")

    new_readme_content = (
        before_part + start_marker + "\n\n" +
        links_md_content + "\n" + end_marker + after_part
    )

    with open(README_FILE, 'w', encoding='utf-8') as f:
        f.write(new_readme_content)

    print("README.md updated successfully.")


def main():
    print("Starting advanced config generation process with corrected YAML format...")
    try:
        with open(TEMPLATE_FILE, 'r', encoding='utf-8') as f:
            template_data = yaml.safe_load(f)
        with open(FORMAT_FILE, 'r', encoding='utf-8') as f:
            format_string = f.read().strip()
        if "[URL]" not in format_string:
            print(f"Warning: Placeholder [URL] not found in {FORMAT_FILE}. Using original URLs directly.")
            format_string = "[URL]"
    except FileNotFoundError as e:
        sys.exit(f"CRITICAL ERROR: A required file is missing: {e.filename}")
    except Exception as e:
        sys.exit(f"CRITICAL ERROR: Could not read template or format file: {e}")

    os.makedirs(OUTPUT_DIR, exist_ok=True)
    os.makedirs(PROVIDERS_DIR, exist_ok=True)

    try:
        with open(SUBS_FILE, 'r', encoding='utf-8') as f:
            subscriptions = [line.strip() for line in f if line.strip() and not line.startswith('#')]
    except FileNotFoundError:
        sys.exit(f"CRITICAL ERROR: Subscription file '{SUBS_FILE}' not found.")
        
    generated_files = []

    for sub_line in subscriptions:
        custom_name = None
        if ',' in sub_line:
            original_url, custom_name = [part.strip() for part in sub_line.split(',', 1)]
        else:
            original_url = sub_line
        
        file_name_base = custom_name if custom_name else get_filename_from_url(original_url)
        if not file_name_base:
            print(f"Warning: Could not determine a filename for URL: {original_url}. Skipping.")
            continue
        
        wrapped_url = format_string.replace("[URL]", quote_plus(original_url))
        
        print(f"Processing: {original_url}")
        print(f"  -> Wrapped URL: {wrapped_url}")
        
        provider_filename = f"{file_name_base}.txt"
        provider_path = os.path.join(PROVIDERS_DIR, provider_filename)
        try:
            response = requests.get(wrapped_url, timeout=30)
            response.raise_for_status()
            with open(provider_path, 'w', encoding='utf-8') as f:
                f.write(response.text)
            print(f"  -> Successfully saved content to {provider_path}")
        except requests.RequestException as e:
            print(f"  -> Error downloading from wrapped URL: {e}. Skipping.")
            continue

        if not GITHUB_REPO:
            continue
        
        # استفاده از copy.deepcopy برای ساخت یک کپی کامل و امن از تمپلیت
        config_data = copy.deepcopy(template_data)
        
        raw_provider_url = f"https://raw.githubusercontent.com/{GITHUB_REPO}/main/{provider_path}"
        config_data['proxy-providers']['proxy']['url'] = raw_provider_url
        config_data['proxy-providers']['proxy']['path'] = f"./{provider_path}"
        
        output_filename = f"{file_name_base}.yaml"
        output_path = os.path.join(OUTPUT_DIR, output_filename)
        
        with open(output_path, 'w', encoding='utf-8') as f:
            # --- این بخش کلیدی و اصلاح شده است ---
            # sort_keys=False: ترتیب کلیدها را حفظ می‌کند
            # default_flow_style=False: فرمت بلاک با تورفتگی را اعمال می‌کند
            yaml.dump(
                config_data, 
                f, 
                allow_unicode=True, 
                sort_keys=False, 
                default_flow_style=False
            )
            
        generated_files.append(output_filename)
        print(f"  -> Generated final config with correct format: {output_path}\n")

    if generated_files:
        update_readme(generated_files)

if __name__ == "__main__":
    main()


