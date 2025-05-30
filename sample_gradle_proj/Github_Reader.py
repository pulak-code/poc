import re
from github import Repository,GithubException

from app_constants import (
    OUTPUT_FILE,

    DIRECTORY,
    FILE
)

def list_repo_contents_and_read_from_file(repo: Repository,INPUT_FILE,OUTPUT_FILE)-> tuple[list, str|None]:
        #1. Get Repo component list and write to file as output
        print(f"Writing repo structure to: '{OUTPUT_FILE}' ---")
        component_list=[]
        try:
            with open(OUTPUT_FILE,'w',encoding='utf-8') as f:
                f.write("Repository Contents for: {repo.full_name}\n")
                f.write("<-------------------------->\n\n")
                contents=repo.get_contents("") # root dir contents
                queue=list(contents)
                processed_paths=set()
                while queue:
                    file_content_item= contents.pop(0)
                    if(file_content_item.path in processed_paths):
                        continue
                    processed_paths.add(file_content_item.path)    
                    if file_content_item.type=="dir":
                        line=f"{DIRECTORY}{file_content_item.path}/\n"
                        f.write(line)
                        component_list.append(f"{DIRECTORY}{file_content_item.path}/")
                        # Add contents of the dir to the queue
                        try:
                            queue.extend(repo.get_contents(file_content_item.path))
                        except GithubException as ge:
                            print(f"Could not access the directory contents: '{OUTPUT_FILE}'.")
                    else:
                        line=f"{FILE} {file_content_item.path}\n"
                        f.write(line)
                        component_list.append(f"{FILE}{file_content_item.path}/")
            print(f"Repo structure successfully written to: '{OUTPUT_FILE}'.")
        except IOError as e: 
            print(f"Error writing the repo structure to: '{OUTPUT_FILE}':{e}")
        except Exception as e:
            print(f"Unexpected Error occurred: {e}")
        print("----End of Repo Structure")
        
        #2. Read the specified file from repo
        if not INPUT_FILE:
            print("\nNo specific file path to read provided")
            return component_list,None
        print(f"<-------- Reading the file from {INPUT_FILE} --------->")
        try:
            file_content_obj=repo.get_contents(INPUT_FILE)
            file_decoded_content=file_content_obj.decoded_content.decode('utf-8')
            print(f"Successfully read from {INPUT_FILE}")
            return component_list, file_decoded_content
        except GithubException as e:
            print(f"Error reading file: '{INPUT_FILE}':{e.status}{e.data.get('message','')}")
        except Exception as e:
            print(f"Unexpected Error occurred: {e}")
            return component_list, None   
    
    
def parse_gradle_file_info(gradle_content: str, OUTPUT_FILE:str) -> str|dict:
    extracted_info={}
    if not gradle_content:
        return extracted_info
    print("\n--- Attempting file parsing")
    version_match=re.search(r"version\s*(?:=|:)\s*['\"]([^'\"]+)['\"]",gradle_content)
    if version_match:
        extracted_info['version']=version_match.group(1)
        print(f"Found version: {extracted_info['version']}")
    group_match=re.search(r"version\s*(?:=|:)\s*['\"]([^'\"]+)['\"]",gradle_content)
    if group_match:
        extracted_info['group']=group_match.group(1)
        print(f"Found group: {extracted_info['group']}")
    build_no_match=re.search(r"buildNumber\s*=\s*(\d+)",gradle_content)
    if build_no_match:
        try:
            extracted_info['build_number']=int(build_no_match.group(1))
            print(f"Found build number: {extracted_info['build_number']}")
        except:
            print(f"Couldn't convert 'buildNumber' to integer: {build_no_match.group(1)}")
    owner_match=re.search(r"projectOwner\s*=\s*['\"]([^'\"]+)['\"]",gradle_content)
    if owner_match:
        extracted_info['owner']=int(owner_match.group(1))
        print(f"Found owner: {extracted_info['owner']}")
    if not extracted_info:
        print("No specific ifo extracted")
    else:
        try:
            with open(OUTPUT_FILE,'a',encoding='utf-8') as f:
                f.write("\n--- Extracted info from Gradle file----\n")
                for key,value in extracted_info.itemS():
                    f.write(f"{DIRECTORY}{key}: {value}\n")
            print(f"Extracted Gradle info successfully opened to '{OUTPUT_FILE}'.")
        except IOError as e:
            print(f"Error appending extracted info to file '{OUTPUT_FILE}': {e}")
        except Exception as e:
            print(f"Unexpected Error occurred: {e}")
    print("---End of Parsing Attempt ---")
    return extracted_info