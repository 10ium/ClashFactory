import os
import re
import sys  # ماژول sys برای خروج از برنامه با پیام خطا اضافه شد
import yaml
import requests
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
    """
    Updates the README.md file with a list of generated config links.
    This version includes robust error handling to identify the exact problem.
    """
    if not GITHUB_REPO:
        # این خطا نباید رخ دهد چون در اکشن تعریف شده، اما برای اطمینان
        sys.exit("Critical Error: GITHUB_REPOSITORY environment variable is not set.")

    print(f"Updating README.md for repository: {GITHUB_REPO}")

    # 1. Build the new list of links as a markdown string
    links_md_content = "## 🔗 لینک‌های کانفیگ آماده (Raw)\n\n"
    links_md_content += "برای استفاده، لینک‌های زیر را مستقیما در کلش کپی کنید.\n\n"
    for filename in sorted(output_files):
        raw_url = f"https://raw.githubusercontent.com/{GITHUB_REPO}/main/{OUTPUT_DIR}/{filename}"
        title = os.path.splitext(filename)[0]
        links_md_content += f"* **{title}**: `{raw_url}`\n"

    # 2. Read the entire content of the README.md file
    try:
        with open(README_FILE, 'r', encoding='utf-8') as f:
            readme_content = f.read()
    except FileNotFoundError:
        # اگر فایل ریدمی پیدا نشود، با این پیام خطا خارج شو
        sys.exit(f"CRITICAL ERROR: The '{README_FILE}' file was not found in the repository root.")

    # 3. Define markers and check for their existence
    start_marker = "<!-- START_LINKS -->"
    end_marker = "<!-- END_LINKS -->"

    if start_marker not in readme_content or end_marker not in readme_content:
        # اگر نشانگرها پیدا نشوند، با این پیام خطا خارج شو
        sys.exit(
            f"CRITICAL ERROR: Markers '{start_marker}' and '{end_marker}' not found in {README_FILE}.\n"
            "Please ensure both markers exist in your README file."
        )

    # 4. Split content and reconstruct
    try:
        before_part = readme_content.split(start_marker)[0]
        after_part = readme_content.split(end_marker)[1]
    except IndexError:
        # اگر در جدا کردن محتوا مشکلی پیش بیاید
        sys.exit(
            "CRITICAL ERROR: Could not split README content. "
            "Please check if the start and end markers are correctly placed and not duplicated."
        )

    new_readme_content = (
        before_part +
        start_marker +
        "\n\n" +
        links_md_content +
        "\n" +
        end_marker +
        after_part
    )

    # 6. Write the new content back to the file
    with open(README_FILE, 'w', encoding='utf-8') as f:
        f.write(new_readme_content)

    print("README.md updated successfully.")


def main():
    print("Starting advanced config generation process...")
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
            # این نباید اتفاق بیافتد اما برای اطمینان
            continue
        config_data = yaml.safe_load(yaml.dump(template_data))
        raw_provider_url = f"https://raw.githubusercontent.com/{GITHUB_REPO}/main/{provider_path}"
        config_data['proxy-providers']['proxy']['url'] = raw_provider_url
        config_data['proxy-providers']['proxy']['path'] = f"./{provider_path}"
        output_filename = f"{file_name_base}.yaml"
        output_path = os.path.join(OUTPUT_DIR, output_filename)
        with open(output_path, 'w', encoding='utf-8') as f:
            yaml.dump(config_data, f, allow_unicode=True, sort_keys=False)
        generated_files.append(output_filename)
        print(f"  -> Generated final config: {output_path}\n")

    if generated_files:
        update_readme(generated_files)

if __name__ == "__main__":
    main()


