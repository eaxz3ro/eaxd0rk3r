import json
import requests
import argparse
import sys

queries = [
    "site:{site} -www -shop -share -ir -mfa",
    "site:{site} ext:php inurl:?",
    "site:{site} inurl:api | site:*/rest | site:*/v1 | site:*/v2 | site:*/v3",
    "site:\"{site}\" ext:log | ext:txt | ext:conf | ext:cnf | ext:ini | ext:env | ext:sh | ext:bak | ext:backup | ext:swp | ext:old | ext:~ | ext:git | ext:svn | ext:htpasswd | ext:htaccess | ext:json",
    "inurl:conf | inurl:env | inurl:cgi | inurl:bin | inurl:etc | inurl:root | inurl:sql | inurl:backup | inurl:admin | inurl:php site:{site}",
    "inurl:\"error\" | intitle:\"exception\" | intitle:\"failure\" | intitle:\"server at\" | inurl:exception | \"database error\" | \"SQL syntax\" | \"undefined index\" | \"unhandled exception\" | \"stack trace\" site:{site}",
    "inurl:q= | inurl:s= | inurl:search= | inurl:query= | inurl:keyword= | inurl:lang= inurl:& site:{site}",
    "inurl:url= | inurl:return= | inurl:next= | inurl:redirect= | inurl:redir= | inurl:ret= | inurl:r2= | inurl:page= inurl:& inurl:http site:{site}",
    "inurl:id= | inurl:pid= | inurl:category= | inurl:cat= | inurl:action= | inurl:sid= | inurl:dir= inurl:& site:{site}",
    "inurl:http | inurl:url= | inurl:path= | inurl:dest= | inurl:html= | inurl:data= | inurl:domain=  | inurl:page= inurl:& site:{site}",
    "inurl:include | inurl:dir | inurl:detail= | inurl:file= | inurl:folder= | inurl:inc= | inurl:locate= | inurl:doc= | inurl:conf= inurl:& site:{site}",
    "inurl:cmd | inurl:exec= | inurl:query= | inurl:code= | inurl:do= | inurl:run= | inurl:read=  | inurl:ping= inurl:& site:{site}",
    "site:{site} \"choose file\"",
    "inurl:apidocs | inurl:api-docs | inurl:swagger | inurl:api-explorer site:\"{site}\"",
    "inurl:login | inurl:signin | intitle:login | intitle:signin | inurl:secure site:{site}",
    "inurl:test | inurl:env | inurl:dev | inurl:staging | inurl:sandbox | inurl:debug | inurl:temp | inurl:internal | inurl:demo site:{site}",
    "site:{site} ext:txt | ext:pdf | ext:xml | ext:xls | ext:xlsx | ext:ppt | ext:pptx | ext:doc | ext:docx intext:\"confidential\" | intext:\"Not for Public Release\" | intext:\"internal use only\" | intext:\"do not distribute\"",
    "inurl:email= | inurl:phone= | inurl:password= | inurl:secret= inurl:& site:{site}",
    "inurl:/content/usergenerated | inurl:/content/dam | inurl:/jcr:content | inurl:/libs/granite | inurl:/etc/clientlibs | inurl:/content/geometrixx | inurl:/bin/wcm | inurl:/crx/de site:{site}",
    "site:openbugbounty.org inurl:reports intext:\"{site}\"",
    "site:groups.google.com \"{site}\"",
    "site:pastebin.com \"{site}\"",
    "site:jsfiddle.net \"{site}\"",
    "site:codebeautify.org \"{site}\"",
    "site:codepen.io \"{site}\"",
    "site:s3.amazonaws.com \"{site}\"",
    "site:blob.core.windows.net \"{site}\"",
    "site:googleapis.com \"{site}\"",
    "site:drive.google.com \"{site}\"",
    "site:dev.azure.com \"{site}\"",
    "site:onedrive.live.com \"{site}\"",
    "site:digitaloceanspaces.com \"{site}\"",
    "site:sharepoint.com \"{site}\"",
    "site:s3-external-1.amazonaws.com \"{site}\"",
    "site:s3.dualstack.us-east-1.amazonaws.com \"{site}\"",
    "site:dropbox.com/s \"{site}\"",
    "site:box.com/s \"{site}\"",
    "site:docs.google.com inurl:\"/d/\" \"{site}\"",
    "site:jfrog.io \"{site}\"",
    "site:firebaseio.com \"{site}\""
]

def get_sites_from_file(file_path):
    try:
        with open(file_path, "r") as f:
            return [line.strip() for line in f if line.strip()]
    except FileNotFoundError:
        print("\033[31m[ERROR] File not found. Please provide a valid file path.\033[0m")
        sys.exit(1)

def get_queries():
    print("\033[37mAvailable Google Dork queries:\033[0m")
    for i, query in enumerate(queries, start=1):
        print(f"\033[37m{i}.\033[0m {query}")
    selected = input("\033[37mEnter query numbers (comma-separated or range e.g., 1-5): \033[0m").strip()
    if '-' in selected:
        try:
            start, end = map(int, selected.split('-'))
            if 1 <= start <= end <= len(queries):
                return [queries[i - 1] for i in range(start, end + 1)]
            else:
                print("\033[31m[ERROR] Invalid range. Please try again.\033[0m")
                return get_queries()
        except ValueError:
            print("\033[31m[ERROR] Invalid range format. Please try again.\033[0m")
            return get_queries()
    else:
        try:
            indices = [int(i) - 1 for i in selected.split(",") if i.strip().isdigit()]
            if not all(0 <= i < len(queries) for i in indices):
                print("\033[31m[ERROR] Some indices are out of range. Please try again.\033[0m")
                return get_queries()
        except ValueError:
            print("\033[31m[ERROR] Invalid input. Please try again.\033[0m")
            return get_queries()
    return [queries[i] for i in indices]

def execute_dorks(sites, selected_queries, output_file=None):
    api_key = 'YOUR-API-KEY-HERE'
    search_engine_id = 'YOUR-CSE-ID-HERE'
    results_data = []
    for site in sites:
        print(f"\033[34mSITE: {site}\033[0m", end=" ")  
        for query in selected_queries:
            dork = query.format(site=site)
            print(f"\033[33mRunning query: {dork}\033[0m")  
            for start in range(1, 101, 10):
                url = "https://www.googleapis.com/customsearch/v1"
                params = {
                    "key": api_key,
                    "cx": search_engine_id,
                    "q": dork,
                    "start": start,
                }
                response = requests.get(url, params=params)
                if response.status_code == 200:
                    results = response.json().get("items", [])
                    if results:
                        print(f"\033[32mResults for query: {dork}\033[0m") 
                        for item in results:
                            result_entry = {
                                "query": dork,
                                "title": item["title"],
                                "link": item["link"],
                            }
                            results_data.append(result_entry)
                            print(f"- \033[32m{item['title']}\033[0m\n{item['link']}") 
                    else:
                        print("\033[31mNo results found.\033[0m")  
                        break
                elif response.status_code == 429:
                    print("\033[31m[ERROR] Quota has been reached for today. Exiting.\033[0m")
                    sys.exit(1)
                else:
                    print(f"\033[31m[ERROR] {response.status_code} - {response.text}\033[0m") 
                    break
    if output_file:
        with open(output_file, "w") as f:
            json.dump(results_data, f, indent=4)
        print(f"\033[32mResults saved to {output_file}\033[0m")  

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Google Dorker for Bug Bounty by eaxz3ro", usage="python3 eaxd0rk3r.py [-u URL] [-f FILE] [-o OUTPUT]")
    parser.add_argument("-u", "--url", help="Single URL.")
    parser.add_argument("-f", "--file", help="File containing multiple URLs.")
    parser.add_argument("-o", "--output", help="Output file to save results.")
    args = parser.parse_args()
    
    if not args.url and not args.file:
        print("\033[31m[ERROR] Supply -h or --help for usage information.\033[0m")
        sys.exit(1)
    sites = [args.url] if args.url else get_sites_from_file(args.file)
    selected_queries = get_queries()
    execute_dorks(sites, selected_queries, args.output) 
